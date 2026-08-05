import logging
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Optional, List, Dict, Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import pytz

from database.core.storage.base_pool import DatabasePool
from database.core.storage.pool_factory import create_pool  # fallback if not provided

logger = logging.getLogger(__name__)

# Global scheduler instance
_scheduler = None
_db_pool = None  # will be set on initialization

def get_scheduler() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is None:
        jobstores = {'default': MemoryJobStore()}
        executors = {'default': ThreadPoolExecutor(max_workers=5)}
        job_defaults = {
            'coalesce': True,
            'max_instances': 3,
            'misfire_grace_time': 60
        }
        _scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
            timezone=pytz.UTC
        )
        _scheduler.add_listener(_job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    return _scheduler

def _job_listener(event):
    if event.exception:
        logger.error(f"Job {event.job_id} failed: {event.exception}")
    else:
        logger.info(f"Job {event.job_id} executed successfully")

def schedule_report(report_id: int, schedule_str: str) -> bool:
    scheduler = get_scheduler()
    job_id = f"report_{report_id}"

    # Remove existing job if any
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    try:
        # Build the trigger
        if schedule_str.startswith("interval:"):
            parts = schedule_str.split(":")
            if len(parts) != 2:
                raise ValueError("Invalid interval format")
            key_value = parts[1].split("=")
            if len(key_value) != 2:
                raise ValueError("Invalid interval format")
            key, value = key_value[0].strip(), int(key_value[1].strip())
            trigger = IntervalTrigger(**{key: value}, timezone=pytz.UTC)
        else:
            # Assume cron expression
            trigger = CronTrigger.from_crontab(schedule_str, timezone=pytz.UTC)

        # Add the job
        scheduler.add_job(
            func=execute_scheduled_report,
            trigger=trigger,
            id=job_id,
            args=[report_id],
            replace_existing=True
        )

        # Retrieve the job to get next_run_time
        job = scheduler.get_job(job_id)
        if job and hasattr(job, 'next_run_time') and job.next_run_time:
            next_run = job.next_run_time.isoformat()
            # Update next_run in database using the global pool
            if _db_pool:
                _db_pool.execute_query(
                    "UPDATE reports SET next_run = %s WHERE id = %s",
                    (next_run, report_id)
                )
        else:
            logger.warning(f"Could not determine next_run_time for report {report_id}")

        logger.info(f"Scheduled report {report_id} with schedule '{schedule_str}'")
        return True
    except Exception as e:
        logger.error(f"Failed to schedule report {report_id}: {e}")
        return False

def unschedule_report(report_id: int) -> bool:
    scheduler = get_scheduler()
    job_id = f"report_{report_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"Unscheduled report {report_id}")
        if _db_pool:
            _db_pool.execute_query(
                "UPDATE reports SET next_run = NULL WHERE id = %s",
                (report_id,)
            )
        return True
    return False

def execute_scheduled_report(report_id: int):
    """Execute a scheduled report using the global database pool."""
    from database.core.reporting.service import ReportService
    try:
        logger.info(f"Executing scheduled report {report_id}")
        # Use the global pool; if not set, fallback to creating one (not ideal)
        pool = _db_pool or create_pool()
        result = ReportService.execute_report(report_id, pool, parameters={})  # <-- fixed signature
        scheduler = get_scheduler()
        job = scheduler.get_job(f"report_{report_id}")
        next_run = job.next_run_time.isoformat() if job and hasattr(job, 'next_run_time') and job.next_run_time else None

        if pool:
            pool.execute_query(
                """
                UPDATE reports
                SET last_run = %s, next_run = %s
                WHERE id = %s
                """,
                (datetime.utcnow().isoformat(), next_run, report_id)
            )
        _deliver_report(report_id, result, pool)
        logger.info(f"Scheduled report {report_id} completed: {result.get('result_size', 0)} rows")
    except Exception as e:
        logger.exception(f"Error executing scheduled report {report_id}: {e}")

def _deliver_report(report_id: int, result: Dict[str, Any], db_pool: DatabasePool):
    from database.core.reporting.service import ReportService
    from database.core.reporting.exports import export_excel, export_pdf

    report = ReportService.get_report(report_id, db_pool)
    if not report:
        return
    recipients = report.get("recipients", [])
    if not recipients:
        logger.info(f"No recipients for report {report_id}, skipping delivery")
        return

    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    from_email = os.environ.get("SMTP_FROM", smtp_user)

    if not all([smtp_host, smtp_user, smtp_pass]):
        logger.warning("SMTP not configured, skipping email delivery")
        return

    export_format = report.get("export_format", "json")
    subject = f"Report: {report['name']} (ID {report_id})"
    body = f"Please find attached the report '{report['name']}' executed at {datetime.utcnow().isoformat()}."

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # The output is already in the result; we need to fetch it again or use the result.
    # For simplicity, we'll re-export from the result data.
    # But result may not contain raw data; we can re-run export.
    # We'll assume result contains "output" with the file content (bytes/string)
    output = result.get("output")
    if output is None:
        logger.error(f"No output data for report {report_id}")
        return

    if export_format == "excel":
        filename = f"report_{report_id}.xlsx"
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_bytes = output if isinstance(output, bytes) else output  # already bytes from export_excel
    elif export_format == "pdf":
        filename = f"report_{report_id}.pdf"
        mimetype = "application/pdf"
        file_bytes = output if isinstance(output, bytes) else output
    else:
        # JSON: output is a string
        filename = f"report_{report_id}.json"
        mimetype = "application/json"
        file_bytes = output.encode('utf-8') if isinstance(output, str) else output

    part = MIMEApplication(file_bytes, Name=filename)
    part['Content-Disposition'] = f'attachment; filename="{filename}"'
    msg.attach(part)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        logger.info(f"Email sent to {recipients} for report {report_id}")
    except Exception as e:
        logger.error(f"Failed to send email for report {report_id}: {e}")

def initialize_scheduler(db_pool: DatabasePool):
    """Initialize the scheduler with a database pool."""
    global _db_pool
    _db_pool = db_pool
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")

    # Load active reports with schedule
    rows = db_pool.fetch_all(
        "SELECT id, schedule FROM reports WHERE status = 'active' AND schedule IS NOT NULL AND schedule != ''"
    )
    for row in rows:
        report_id = row["id"]
        schedule_str = row["schedule"]
        try:
            schedule_report(report_id, schedule_str)
        except Exception as e:
            logger.error(f"Error loading scheduled report {report_id}: {e}")

def shutdown_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=True)
        logger.info("Scheduler shut down")
