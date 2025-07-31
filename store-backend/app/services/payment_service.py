import stripe
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_API_KEY

class PaymentService:
    def __init__(self):
        self.stripe = stripe
        
    async def create_payment_intent(
        self, 
        amount: int, 
        currency: str = "usd",
        customer_email: Optional[str] = None
    ) -> stripe.PaymentIntent:
        """Create a Stripe PaymentIntent"""
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata={
                    "customer_email": customer_email or ""
                }
            )
            logger.info(f"Payment intent created: {payment_intent.id}")
            return payment_intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise
            
    async def confirm_payment(self, payment_intent_id: str) -> stripe.PaymentIntent:
        """Confirm a payment intent"""
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent
            
        except stripe.error.StripeError as e:
            logger.error(f"Error confirming payment: {str(e)}")
            raise
            
    def verify_webhook_signature(self, payload: bytes, sig_header: str) -> dict:
        """Verify Stripe webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
            
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            raise
