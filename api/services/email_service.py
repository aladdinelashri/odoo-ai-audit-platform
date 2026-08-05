"""Email delivery service with tenacity retry logic."""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from api.core.config import settings

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True
)
def _send_email_smtp(
    to_addresses: List[str],
    subject: str,
    body: str,
    attachment_data: Optional[bytes] = None,
    attachment_filename: Optional[str] = None,
    attachment_mimetype: Optional[str] = None
) -> None:
    """Send email via SMTP with tenacity retries."""
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_user
    msg["To"] = ", ".join(to_addresses)
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    if attachment_data and attachment_filename:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_data)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_filename}"
        )
        msg.attach(part)
    
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_tls:
            server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
    
    logger.info(f"Email sent successfully to {to_addresses}")


def deliver_report_email(
    recipients: List[str],
    report_name: str,
    execution_id: int,
    attachment_data: Optional[bytes] = None,
    attachment_filename: Optional[str] = None,
    attachment_mimetype: Optional[str] = None
) -> dict:
    """Deliver report via email to recipients."""
    if not recipients:
        return {"success": False, "error": "No recipients configured"}
    
    subject = f"Report: {report_name} (Execution #{execution_id})"
    body = f"""Your scheduled report "{report_name}" has been executed successfully.

Execution ID: {execution_id}
Status: Completed

Please find the attached report output.
"""
    
    try:
        _send_email_smtp(
            to_addresses=recipients,
            subject=subject,
            body=body,
            attachment_data=attachment_data,
            attachment_filename=attachment_filename,
            attachment_mimetype=attachment_mimetype
        )
        return {"success": True, "error": None}
    except Exception as e:
        logger.error(f"Failed to deliver email after retries: {str(e)}")
        return {"success": False, "error": str(e)}
