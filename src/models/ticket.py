from datetime import datetime
from pydantic import BaseModel, Field


class Ticket(BaseModel):
    ticket_id: str
    customer_id: str
    subscription_id: str
    issue_type: str
    description: str
    transaction_ids: list[str] = Field(default_factory=list)
    status: str
    priority: str
    created_at: datetime
    resolution: str | None = None