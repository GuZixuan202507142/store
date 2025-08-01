import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.config import settings

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
        return service
    except Exception as e:
        print(f"Failed to create Gmail service: {e}")
        return None

async def send_purchase_confirmation(to_email: str, order_id: int):
    """Sends a purchase confirmation email."""
    service = get_gmail_service()
    if not service:
        print("Gmail service not available. Skipping email.")
        return

    subject = "Your GitHub Copilot Purchase Confirmation"
    body = f"""
    <p>Hello,</p>
    <p>Thank you for your purchase from our store!</p>
    <p>Your Order ID is: <strong>{order_id}</strong>.</p>
    <p>We have received your payment for the GitHub Copilot Education Edition account. You will receive another email shortly with your account details and setup instructions.</p>
    <p>Thank you for your business!</p>
    """
    
    message = MIMEText(body, 'html')
    message['to'] = to_email
    message['from'] = SENDER_EMAIL
    message['subject'] = subject
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
        'raw': encoded_message
    }

    try:
        send_message = (service.users().messages().send(userId='me', body=create_message).execute())
        print(f"Message Id: {send_message['id']} sent to {to_email}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
