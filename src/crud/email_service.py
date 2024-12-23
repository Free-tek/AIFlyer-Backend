import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from src.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SENDER_EMAIL

    def send_email(self, recipient: str, subject: str, html_content: str):
        """Synchronous send email using SMTP with SSL"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient

            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Create SSL context
            context = ssl.create_default_context()

            # Connect using SSL (not TLS)
            with smtplib.SMTP_SSL(self.smtp_server, int(self.smtp_port), context=context) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(message)

            print(f"Email sent successfully to {recipient}")
            return True

        except Exception as e:
            print(f"Failed to send email to {recipient}: {str(e)}")
            return False

    def send_payment_failed_notification(
        self, 
        recipient: str, 
        user_name: str,
        plan_tier: str,
        failure_reason: str
    ):
        """Send payment failure notification"""
        subject = "Important: Your Payment Failed"
        html_content = f"""
        <html>
            <body>
                <h2>Payment Failed Notice</h2>
                <p>Dear {user_name or "Valued Customer"},</p>
                <p>We were unable to process your payment for the {plan_tier} plan. As a result, your account has been reverted to the free plan with no access to create AI generated files.</p>
                <p>Please update your payment information to restore access to the {plan_tier} plan.</p>
                
                <p><strong>Reason for failure:</strong> {failure_reason}</p>
                
                <p>To restore your {plan_tier} plan access:</p>
                <ol>
                    <li>Log in to your account</li>
                    <li>Update your payment information</li>
                    <li>Resubscribe to your desired plan</li>
                </ol>
                
                <p>If you need assistance, please contact our support team.</p>
                
                <p>Best regards,<br>AIFlyer Team</p>
            </body>
        </html>
        """
        return self.send_email(recipient, subject, html_content)

    