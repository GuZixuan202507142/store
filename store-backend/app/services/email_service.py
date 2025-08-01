import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.sender_email = settings.EMAIL_SENDER
        self._gmail_service = None
        
    def _get_gmail_service(self):
        """Get Gmail API service with OAuth2 credentials"""
        if self._gmail_service is None:
            # Create credentials from individual components
            creds = Credentials(
                token=None,
                refresh_token=settings.GMAIL_REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=settings.GMAIL_CLIENT_ID,
                client_secret=settings.GMAIL_CLIENT_SECRET,
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )
            
            # Refresh the token if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            self._gmail_service = build('gmail', 'v1', credentials=creds)
        
        return self._gmail_service
        
    async def send_order_confirmation(self, customer_email: str, order_id: int):
        """Send order confirmation email to customer"""
        try:
            subject = f"Order Confirmation - #{order_id}"
            body = f"""
            Thank you for your order!
            
            Order ID: {order_id}
            
            We will process your order shortly and send you updates.
            
            Best regards,
            Store Team
            """
            
            await self._send_email(customer_email, subject, body)
            logger.info(f"Order confirmation email sent to {customer_email}")
            
        except Exception as e:
            logger.error(f"Failed to send email to {customer_email}: {str(e)}")
            
    async def _send_email(self, to_email: str, subject: str, body: str):
        """Internal method to send email using Gmail API"""
        try:
            service = self._get_gmail_service()
            
            # Create message
            message = MIMEMultipart()
            message['to'] = to_email
            message['from'] = self.sender_email
            message['subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            send_message = {'raw': raw_message}
            result = service.users().messages().send(userId='me', body=send_message).execute()
            
            logger.info(f"Email sent successfully. Message ID: {result['id']}")
            
        except Exception as e:
            logger.error(f"Failed to send email via Gmail API: {str(e)}")
            raise
