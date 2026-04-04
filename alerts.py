"""
SeniorShield - Alert Service
Sends email and SMS alerts to trusted contacts when suspicious activity is detected.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from twilio.rest import Client as TwilioClient

from config import load_config

logger = logging.getLogger(__name__)


class AlertService:
    """Handles sending alerts to trusted contacts."""

    def __init__(self):
        self._config = None

    def _load_config(self):
        self._config = load_config()

    def send_alert(self, event):
        """Send alert via all configured channels."""
        self._load_config()
        contact = self._config["trusted_contact"]
        settings = self._config["alert_settings"]

        alert_message = self._format_alert_message(event)

        if settings.get("email_enabled"):
            self._send_email(contact, alert_message)

        if settings.get("sms_enabled"):
            self._send_sms(contact, alert_message)

    def _format_alert_message(self, event):
        """Format event into a readable alert message."""
        timestamp = datetime.fromisoformat(event["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
        severity_emoji = {
            "low": "⚠️",
            "medium": "⚠️️",
            "high": "🚨"
        }.get(event["severity"], "⚠️")

        message = f"""
{severity_emoji} SeniorShield Alert

Mika's computer detected suspicious activity.

What happened: {event["description"]}
Time: {timestamp}
Severity: {event["severity"].upper()}

Please check in with them to make sure they're okay.

- SeniorShield
"""
        return message.strip()

    def _send_email(self, contact, message):
        """Send alert via email."""
        settings = self._config["alert_settings"]

        try:
            msg = MIMEMultipart()
            msg['From'] = settings.get("from_email", "seniorshield@example.com")
            msg['To'] = contact["email"]
            msg['Subject'] = "⚠️ SeniorShield Alert - Action Needed"

            msg.attach(MIMEText(message, 'plain'))

            # Note: For production, use proper SMTP with TLS
            # This is a placeholder that works with Gmail App Passwords
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            # You'll need to configure actual SMTP credentials
            # For now, log what would be sent
            logger.info(f"EMAIL ALERT would be sent to {contact['email']}: {message[:100]}...")

            # Uncomment and configure for real email:
            # with smtplib.SMTP(smtp_server, smtp_port) as server:
            #     server.starttls()
            #     server.login(settings["smtp_username"], settings["smtp_password"])
            #     server.send_message(msg)

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    def _send_sms(self, contact, message):
        """Send alert via Twilio SMS."""
        settings = self._config["alert_settings"]

        try:
            twilio_sid = settings.get("twilio_sid")
            twilio_token = settings.get("twilio_token")
            twilio_from = settings.get("twilio_from")

            if not all([twilio_sid, twilio_token, twilio_from]):
                logger.warning("Twilio not configured, skipping SMS")
                return

            client = TwilioClient(twilio_sid, twilio_token)
            client.messages.create(
                body=message[:1600],  # Twilio limit
                from_=twilio_from,
                to=contact["phone"]
            )

            logger.info(f"SMS alert sent to {contact['phone']}")

        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")


# Singleton instance
_alert_service = None


def get_alert_service():
    global _alert_service
    if _alert_service is None:
        _alert_service = AlertService()
    return _alert_service
