import smtplib
from email.message import EmailMessage

from app.core.config import settings


def _send_email(to_email: str, subject: str, body: str) -> None:
    smtp_host = settings.smtp_host
    smtp_port = settings.smtp_port
    smtp_username = settings.smtp_username
    smtp_password = settings.smtp_password
    email_from = settings.email_from or smtp_username

    if not all([smtp_host, smtp_port, smtp_username, smtp_password, email_from]):
        raise RuntimeError("SMTP settings are missing in .env")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_subscription_email(user_email: str, invoice: dict) -> None:
    body = f"""Hello,

Your subscription has been activated successfully.

Invoice ID: {invoice.get('invoice_id')}
Plan: {invoice.get('plan')}
Amount: {invoice.get('amount')} {invoice.get('currency')}
Date: {invoice.get('date')}

Thank you,
PM Team
"""
    _send_email(user_email, "Your Project Subscription Invoice", body)


def send_payment_failed_email(user_email: str, reason: str = "Payment could not be completed") -> None:
    body = f"""Hello,

We could not complete your payment for the Pro subscription.

Reason: {reason}

Your account has not been upgraded.

Please try again later.

Thank you,
PM Team
"""
    _send_email(user_email, "Your Project Payment Failed", body)


def send_subscription_cancelled_email(user_email: str) -> None:
    body = """Hello,

Your Pro subscription has been cancelled successfully.

Your account has now been downgraded to the Free plan.

Thank you,
PM Team
"""
    _send_email(user_email, "Your Project Subscription Cancelled", body)

