from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
async def get_orders():
    """Get all orders"""
    pass

@router.post("/orders")
async def create_order():
    """Create a new order"""
    pass

@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    """Get a specific order"""
    pass
