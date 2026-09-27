from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    customer_id: str
    name: str
    email: EmailStr
    account_status: str
    subscription_id: str