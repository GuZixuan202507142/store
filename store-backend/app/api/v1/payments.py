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

@router.get("/inventory")
async def get_inventory_count(db: AsyncSession = Depends(get_session)):
    """

    Returns the number of items in the inventory.
    """
    count = await payment_service.get_inventory_count(db)
    return {"inventory_count": count}

@router.post("/add-inventory")
async def add_inventory_item(
    request: Request,
    db: AsyncSession = Depends(get_session)
):
    """
    Adds a new item to the inventory.
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")

    try:
        await payment_service.add_inventory_item(username=username, password=password, db=db)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
