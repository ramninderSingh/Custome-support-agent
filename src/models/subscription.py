from pydantic import BaseModel
from datetime import date


class Subscription(BaseModel):
    subscription_id: str
    customer_id: str
    plan: str
    monthly_price: float
    currency: str
    start_date: date
    renewal_date: date
    status: str