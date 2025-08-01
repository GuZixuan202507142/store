from pydantic import BaseModel, EmailStr

class CheckoutSessionCreate(BaseModel):
    email: EmailStr
    price_id: str
