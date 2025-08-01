from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.payment import CheckoutSessionCreate
from app.services import payment_service
from app.db.session import get_session

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session(
    checkout_data: CheckoutSessionCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Creates a Stripe Checkout Session and returns the URL.
    """
    try:
        session_url = await payment_service.create_stripe_checkout_session(
            email=checkout_data.email,
            price_id=checkout_data.price_id
        )
        return {"url": session_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    Handles incoming webhooks from Stripe.
    """
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        await payment_service.handle_stripe_webhook(
            payload=payload,
            sig_header=sig_header,
            db=db
        )
        return {"status": "success"}
    except ValueError as e: # Invalid payload
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))
