from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    subscription_id: str
    amount: float
    currency: str
    timestamp: datetime
    status: str
    payment_method: str
    description: str