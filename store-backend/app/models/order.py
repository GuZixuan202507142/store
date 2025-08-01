from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_email: str = Field(index=True)
    stripe_checkout_session_id: str = Field(unique=True)
    status: str = Field(default="pending") # e.g., pending, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product_name: str
    amount_total: int # in cents
