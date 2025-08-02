from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services import payment_service
from app.db.session import get_session

router = APIRouter()

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
