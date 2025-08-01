import stripe
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.core.config import settings
from app.models.order import Order
from . import email_service

stripe.api_key = settings.STRIPE_API_KEY

async def create_stripe_checkout_session(email: str, price_id: str) -> str:
    """
    Creates a Stripe Checkout session.
    """
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
    return checkout_session.url

async def handle_stripe_webhook(payload: bytes, sig_header: str, db: AsyncSession):
    """
    Handles Stripe webhook events, specifically for completed checkouts.
    """
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError as e:
        raise ValueError("Invalid signature") from e

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        
        if not customer_email:
            raise ValueError("Customer email not found in webhook event.")

        # Check if order already exists
        statement = select(Order).where(Order.stripe_checkout_session_id == session.id)
        result = await db.exec(statement)
        if result.first():
            print(f"Order for session {session.id} already exists. Skipping.")
            return

        # Create a new order in the database
        new_order = Order(
            customer_email=customer_email,
            stripe_checkout_session_id=session.id,
            status='completed',
            product_name="GitHub Copilot Education Edition", # Or get from line_items
            amount_total=session.get('amount_total', 0)
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        # Send a confirmation email
        await email_service.send_purchase_confirmation(
            to_email=customer_email,
            order_id=new_order.id
        )

    else:
        print(f"Unhandled event type {event['type']}")
