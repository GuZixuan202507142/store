from fastapi import APIRouter

router = APIRouter()

@router.post("/payments")
async def create_payment():
    """Create a new payment"""
    pass

@router.get("/payments/{payment_id}")
async def get_payment(payment_id: int):
    """Get payment status"""
    pass

@router.post("/webhooks/stripe")
async def stripe_webhook():
    """Handle Stripe webhook events"""
    pass
