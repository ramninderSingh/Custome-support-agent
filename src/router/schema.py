from typing import Literal
from pydantic import BaseModel, Field


class QueryRoute(BaseModel):
    intent: str

    route: Literal[
        "knowledge",
        "customer",
        "transaction",
        "ticket",
        "multi_source",
        "unknown"
    ]

    requires_knowledge: bool = False
    requires_customer_lookup: bool = False
    requires_subscription_lookup: bool = False
    requires_transaction_lookup: bool = False
    requires_ticket_lookup: bool = False
    requires_action: bool = False

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )