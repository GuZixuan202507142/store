import base64
import logging
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SENDER_EMAIL = settings.EMAIL_SENDER

def get_gmail_service():
    """Initializes and returns the Gmail API service using OAuth 2.0 credentials."""
    try:
        creds = Credentials.from_authorized_user_info(
            info={
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "refresh_token": settings.GMAIL_REFRESH_TOKEN,
            },
            scopes=SCOPES
        )
        service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail service initialized successfully")
        return service
    except RefreshError as e:
        logger.error(f"Gmail credentials refresh failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to create Gmail service: {e}")
        return None

async def send_purchase_confirmation(to_email: str, order_id: int):
    """Sends a purchase confirmation email."""
    service = get_gmail_service()
    if not service:
        logger.error("Gmail service not available. Skipping email.")
        raise Exception("Email service unavailable")

    # Validate email format
    if not to_email or "@" not in to_email:
        logger.error(f"Invalid email address: {to_email}")
        raise ValueError("Invalid email address")

    subject = "Your GitHub Copilot Purchase Confirmation"
    body = f"""
    <p>Hello,</p>
    <p>Thank you for your purchase from our store!</p>
    <p>Your Order ID is: <strong>{order_id}</strong>.</p>
    <p>We have received your payment for the GitHub Copilot Education Edition account. You will receive another email shortly with your account details and setup instructions.</p>
    <p>Thank you for your business!</p>
    <p>Best regards,<br>The GitHub Copilot Store Team</p>
    """
    
    try:
        message = MIMEText(body, 'html')
        message['to'] = to_email
        message['from'] = SENDER_EMAIL
        message['subject'] = subject
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {
            'raw': encoded_message
        }

        send_message = (service.users().messages().send(userId='me', body=create_message).execute())
        logger.info(f"Message Id: {send_message['id']} sent to {to_email}")
        return send_message['id']
        
    except Exception as e:
        logger.error(f"An error occurred while sending email to {to_email}: {e}")
        raise Exception(f"Failed to send email: {str(e)}")
