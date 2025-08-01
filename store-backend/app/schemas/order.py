from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    customer_email: EmailStr
    product_name: str
    amount_total: int

class OrderResponse(BaseModel):
    id: int
    customer_email: str
    stripe_checkout_session_id: str
    status: str
    created_at: datetime
    product_name: str
    amount_total: int

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    product_name: Optional[str] = None
    amount_total: Optional[int] = None
