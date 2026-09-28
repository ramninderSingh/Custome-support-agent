from typing import Annotated, TypedDict
import operator

from src.router.schema import QueryRoute
from src.models.customer import Customer
from src.models.subscription import Subscription
from src.models.transaction import Transaction
from src.models.ticket import Ticket


class AgentState(TypedDict, total=False):

    # User input
    user_query: str
    customer_id: str | None

    # Router
    route: QueryRoute

    # Database results
    customer_data: Customer | None
    subscription_data: Subscription | None
    transaction_data: list[Transaction]
    ticket_data: list[Ticket]

    # RAG
    rag_context: list[dict]

    # Results from all retrieval nodes
    tool_result: Annotated[
        list[dict],
        operator.add
    ]

    # Future actions
    action: dict | None

    # Final answer
    response: str | None