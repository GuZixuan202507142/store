from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from app.models.order import Order
from app.schemas.order import OrderResponse
from app.db.session import get_session

router = APIRouter()

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_session)):
    """Get all orders"""
    try:
        statement = select(Order)
        result = await db.exec(statement)
        orders = result.all()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_session)):
    """Get a specific order"""
    try:
        statement = select(Order).where(Order.id == order_id)
        result = await db.exec(statement)
        order = result.first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/email/{email}", response_model=List[OrderResponse])
async def get_orders_by_email(email: str, db: AsyncSession = Depends(get_session)):
    """Get orders by customer email"""
    try:
        statement = select(Order).where(Order.customer_email == email)
        result = await db.exec(statement)
        orders = result.all()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
