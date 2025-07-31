from pydantic import BaseModel
from typing import Optional

class PaymentCreate(BaseModel):
    amount: int
    currency: str = "usd"
    customer_email: str

class PaymentResponse(BaseModel):
    id: str
    amount: int
    currency: str
    status: str
    client_secret: Optional[str] = None

class StripeWebhookEvent(BaseModel):
    id: str
    type: str
    data: dict
