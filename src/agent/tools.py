from src.tools.customer_tools import get_customer
from src.tools.subscription_tools import (
    get_customer_subscription
)
from src.tools.transaction_tools import (
    get_transaction,
    get_customer_transactions
)
from src.tools.ticket_tools import (
    get_ticket,
    get_customer_tickets
)

from src.rag.pipeline import RAGPipeline


rag_pipeline = RAGPipeline()


def customer_lookup(customer_id: str):
    """
    Look up a customer by customer ID.
    """

    return get_customer(customer_id)


def subscription_lookup(customer_id: str):
    """
    Look up the subscription belonging to a customer.
    """

    return get_customer_subscription(
        customer_id
    )


def transaction_lookup(
    customer_id: str
):
    """
    Look up all transactions belonging
    to a customer.
    """

    return get_customer_transactions(
        customer_id
    )


def transaction_lookup_by_id(
    transaction_id: str
):
    """
    Look up a specific transaction.
    """

    return get_transaction(
        transaction_id
    )


def ticket_lookup(
    customer_id: str
):
    """
    Look up all tickets belonging
    to a customer.
    """

    return get_customer_tickets(
        customer_id
    )


def ticket_lookup_by_id(
    ticket_id: str
):
    """
    Look up a specific support ticket.
    """

    return get_ticket(
        ticket_id
    )


def search_knowledge_base(
    query: str
):
    """
    Search enterprise support policies.
    """

    results = rag_pipeline.search(
        query=query,
        retrieval_k=10,
        rerank_k=5
    )

    return results

def ask_human(question: str):
    """
    Ask the human user for additional information when
    the agent cannot continue without clarification.

    This tool does not actually retrieve data.
    It signals that the agent needs input from the user.
    """

    return {
        "requires_human_input": True,
        "question": question
    }