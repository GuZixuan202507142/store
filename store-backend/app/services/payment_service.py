import stripe
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.core.config import settings
from app.models.order import Order
from . import email_service

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Stripe with API key
if settings.STRIPE_API_KEY:
    stripe.api_key = settings.STRIPE_API_KEY
    logger.info(f"Stripe API key initialized with key ending in: {settings.STRIPE_API_KEY[-4:]}")
else:
    logger.error("STRIPE_API_KEY not found in environment variables")
    raise ValueError("STRIPE_API_KEY not configured")

async def create_stripe_checkout_session(email: str, price_id: str) -> str:
    """
    Creates a Stripe Checkout session.
    """
    try:
        # Correct Stripe API usage
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{settings.FRONTEND_URL}?payment_success=true",
            cancel_url=f"{settings.FRONTEND_URL}?payment_cancelled=true",
            customer_email=email,
        )
        logger.info(f"Created checkout session {checkout_session.id} for {email}")
        return checkout_session.url
    except Exception as e:
        logger.error(f"Stripe error creating checkout session: {type(e).__name__}: {str(e)}")
        raise Exception(f"Payment processing error: {str(e)}")

async def handle_stripe_webhook(payload: bytes, sig_header: str, db: AsyncSession):
    """
    Handles Stripe webhook events, specifically for completed checkouts.
    """
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.info(f"Received webhook event: {event['type']}")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        raise ValueError("Invalid signature") from e

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        
        if not customer_email:
            logger.error(f"Customer email not found in webhook event for session {session.id}")
            raise ValueError("Customer email not found in webhook event.")

        try:
            # Check if order already exists
            statement = select(Order).where(Order.stripe_checkout_session_id == session.id)
            result = await db.exec(statement)
            existing_order = result.first()
            
            if existing_order:
                logger.info(f"Order for session {session.id} already exists. Skipping.")
                return

            # Get product name from line items if available
            product_name = "GitHub Copilot Education Edition"
            if session.get('line_items') and session['line_items']['data']:
                product_name = session['line_items']['data'][0].get('description', product_name)

            # Create a new order in the database
            new_order = Order(
                customer_email=customer_email,
                stripe_checkout_session_id=session.id,
                status='completed',
                product_name=product_name,
                amount_total=session.get('amount_total', 0)
            )
            db.add(new_order)
            await db.commit()
            await db.refresh(new_order)
            
            logger.info(f"Created order {new_order.id} for customer {customer_email}")

            # Send a confirmation email
            try:
                await email_service.send_purchase_confirmation(
                    to_email=customer_email,
                    order_id=new_order.id
                )
                logger.info(f"Sent confirmation email to {customer_email}")
            except Exception as email_error:
                logger.error(f"Failed to send confirmation email: {str(email_error)}")
                # Don't raise here - the order was created successfully
                
        except Exception as db_error:
            logger.error(f"Database error processing webhook: {str(db_error)}")
            await db.rollback()
            raise

    else:
        logger.info(f"Unhandled event type {event['type']}")
        print(f"Unhandled event type {event['type']}")
