from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    customer_email: EmailStr
    amount: int
    currency: str = "usd"

class OrderResponse(BaseModel):
    id: int
    customer_email: str
    amount: int
    currency: str
    status: str
    stripe_payment_intent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
