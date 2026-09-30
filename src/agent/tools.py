from typing import Any

from langchain_core.tools import tool
from langgraph.types import interrupt

from src.tools.customer_tools import get_customer
from src.tools.subscription_tools import get_customer_subscription
from src.tools.transaction_tools import (
    get_transaction,
    get_customer_transactions,
)
from src.tools.ticket_tools import (
    get_ticket,
    get_customer_tickets,
    create_ticket,
)

from src.rag.pipeline import RAGPipeline


# ---------------------------------------------------------------------------
# RAG
# ---------------------------------------------------------------------------

rag_pipeline = RAGPipeline()


# ---------------------------------------------------------------------------
# INFORMATION TOOLS
# ---------------------------------------------------------------------------

@tool
def customer_lookup(customer_id: str) -> dict[str, Any]:
    """
    Look up a customer using their customer ID.

    Use this when customer-specific information is required.
    Do not guess customer information.
    """
    return get_customer(customer_id)


@tool
def subscription_lookup(customer_id: str) -> dict[str, Any]:
    """
    Look up the subscription belonging to a customer.

    Use this when subscription status, plan, renewal date,
    price, or other subscription information is required.
    """
    return get_customer_subscription(customer_id)


@tool
def transaction_lookup(customer_id: str) -> dict[str, Any]:
    """
    Retrieve all transactions belonging to a customer.

    Use this when investigating billing history, duplicate
    charges, failed payments, refunds, or transaction history.
    """
    return get_customer_transactions(customer_id)


@tool
def transaction_lookup_by_id(transaction_id: str) -> dict[str, Any]:
    """
    Look up a specific transaction using its transaction ID.

    Use this when a particular transaction needs to be inspected.
    """
    return get_transaction(transaction_id)


@tool
def ticket_lookup(customer_id: str) -> dict[str, Any]:
    """
    Retrieve all support tickets belonging to a customer.

    Use this when investigating the customer's support history.
    """
    return get_customer_tickets(customer_id)


@tool
def ticket_lookup_by_id(ticket_id: str) -> dict[str, Any]:
    """
    Look up a specific support ticket using its ticket ID.
    """
    return get_ticket(ticket_id)


@tool
def search_knowledge_base(query: str) -> dict[str, Any]:
    """
    Search the enterprise knowledge base for policies and procedures.

    Use this for questions involving company policies such as:
    refunds, billing, cancellation, payment failures, eligibility,
    and other support policies.

    Customer-specific facts must be obtained from customer/database
    tools rather than from the knowledge base.
    """
    try:
        results = rag_pipeline.search(
            query=query,
            retrieval_k=10,
            rerank_k=5,
        )

        return {
            "success": True,
            "query": query,
            "results": results,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "query": query,
        }


# ---------------------------------------------------------------------------
# ACTION TOOLS
# ---------------------------------------------------------------------------

@tool
def create_support_ticket(
    customer_id: str,
    subscription_id: str,
    issue_type: str,
    description: str,
    priority: str = "medium",
    transaction_ids: list[str] | None = None,
) -> dict[str, Any]:
    """
    Create a new support ticket for a customer.

    This is an ACTION tool. Use it only when the user actually
    wants a support ticket created or when the workflow requires
    escalation through a support ticket.

    Required information:
    - customer_id
    - subscription_id
    - issue_type
    - description

    transaction_ids should contain relevant transaction IDs when
    the ticket concerns billing or payment issues.
    """
    try:
        result = create_ticket(
            customer_id=customer_id,
            subscription_id=subscription_id,
            issue_type=issue_type,
            description=description,
            priority=priority,
            transaction_ids=transaction_ids or [],
        )

        return {
            "success": True,
            "action": "create_support_ticket",
            "result": result,
        }

    except Exception as exc:
        return {
            "success": False,
            "action": "create_support_ticket",
            "error": str(exc),
        }


# ---------------------------------------------------------------------------
# HUMAN-IN-THE-LOOP
# ---------------------------------------------------------------------------

@tool
def ask_human(question: str) -> dict[str, Any]:
    """
    Ask the human user for additional information or clarification.

    Use this when the agent cannot safely continue without information
    that is not available from the existing tools.

    Examples:
    - Missing customer ID
    - Ambiguous transaction
    - User confirmation is required before an irreversible action
    - A policy explicitly requires human approval
    """
    answer = interrupt(
        {
            "type": "human_input",
            "question": question,
        }
    )

    return {
        "success": True,
        "human_input": answer,
    }


# ---------------------------------------------------------------------------
# TOOL REGISTRY
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    # Information
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base,

    # Actions
    create_support_ticket,

    # Human interaction
    ask_human,
]