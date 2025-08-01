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

async def send_account_credentials(to_email: str, account_email: str, account_password: str, order_id: int):
    """发送GitHub Copilot账号密码"""
    service = get_gmail_service()
    if not service:
        logger.error("Gmail service not available. Skipping email.")
        raise Exception("Email service unavailable")

    # Validate email format
    if not to_email or "@" not in to_email:
        logger.error(f"Invalid email address: {to_email}")
        raise ValueError("Invalid email address")

    subject = "🎉 Your GitHub Copilot Account Details"
    body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #24292e;">🚀 Your GitHub Copilot Account is Ready!</h2>
        
        <p>Hello,</p>
        
        <p>Congratulations! Your GitHub Copilot Education Edition purchase has been processed successfully.</p>
        
        <div style="background-color: #f6f8fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #0366d6; margin-top: 0;">📋 Account Details</h3>
            <p><strong>Order ID:</strong> #{order_id}</p>
            <p><strong>Account Email:</strong> <code style="background: #e1e4e8; padding: 2px 4px; border-radius: 3px;">{account_email}</code></p>
            <p><strong>Password:</strong> <code style="background: #e1e4e8; padding: 2px 4px; border-radius: 3px;">{account_password}</code></p>
        </div>
        
        <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
            <h4 style="margin-top: 0; color: #856404;">🔒 Important Security Information</h4>
            <ul style="margin-bottom: 0; color: #856404;">
                <li>Please change your password after first login</li>
                <li>Keep your credentials secure and don't share them</li>
                <li>This account is valid for 1 year from today</li>
            </ul>
        </div>
        
        <h3 style="color: #0366d6;">🚀 How to Get Started</h3>
        <ol>
            <li>Go to <a href="https://github.com/login" style="color: #0366d6;">GitHub.com</a></li>
            <li>Log in using the credentials above</li>
            <li>Visit <a href="https://github.com/features/copilot" style="color: #0366d6;">GitHub Copilot</a> to start using your AI pair programmer</li>
            <li>Install the GitHub Copilot extension in your favorite IDE</li>
        </ol>
        
        <div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
            <p style="margin: 0; color: #155724;"><strong>💡 Pro Tip:</strong> Make sure to install the GitHub Copilot extension in VS Code, JetBrains IDEs, or other supported editors to get the full AI coding experience!</p>
        </div>
        
        <hr style="border: none; border-top: 1px solid #e1e4e8; margin: 30px 0;">
        
        <p>If you have any questions or need support, please don't hesitate to contact us.</p>
        
        <p>Happy coding with GitHub Copilot! 🤖</p>
        
        <p>Best regards,<br>
        <strong>The GitHub Copilot Store Team</strong></p>
    </div>
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
        logger.info(f"Account credentials sent to {to_email}, Message Id: {send_message['id']}")
        return send_message['id']
        
    except Exception as e:
        logger.error(f"Failed to send account credentials to {to_email}: {e}")
        raise Exception(f"Failed to send account credentials: {str(e)}")
