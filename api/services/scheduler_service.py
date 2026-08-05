"""APScheduler service for scheduled reports."""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from api.core.database import SessionLocal, SQLiteSessionLocal
from api.models.models import Report
from api.services.report_service import trigger_report

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def init_scheduler():
    """Initialize and start the scheduler."""
    scheduler.start()
    load_scheduled_reports()
    logger.info("Scheduler started and reports loaded")


def load_scheduled_reports():
    """Load all active scheduled reports into the scheduler."""
    db = SessionLocal()
    try:
        reports = db.query(Report).filter(Report.status == "active", Report.schedule.isnot(None)).all()
        for report in reports:
            add_report_job(report)
    finally:
        db.close()


def add_report_job(report: Report):
    """Add a report to the scheduler."""
    if not report.schedule:
        return
    
    job_id = f"report_{report.id}"
    
    # Remove existing job if present
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    try:
        trigger = CronTrigger.from_crontab(report.schedule)
        scheduler.add_job(
            execute_scheduled_report,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            args=[report.id]
        )
        logger.info(f"Scheduled report {report.id} with cron: {report.schedule}")
    except Exception as e:
        logger.error(f"Failed to schedule report {report.id}: {e}")


def remove_report_job(report_id: int):
    """Remove a report from the scheduler."""
    job_id = f"report_{report_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)


def execute_scheduled_report(report_id: int):
    """Execute a scheduled report."""
    db = SessionLocal()
    sqlite_db = SQLiteSessionLocal()
    try:
        trigger_report(db, sqlite_db, report_id, user_id=None, triggered_by="scheduled")
    except Exception as e:
        logger.error(f"Scheduled report {report_id} failed: {e}")
    finally:
        db.close()
        sqlite_db.close()


def shutdown_scheduler():
    """Shutdown the scheduler."""
    scheduler.shutdown()
