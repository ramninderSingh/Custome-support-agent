import re

from src.tools.ticket_tools import (
    get_ticket,
    get_customer_tickets
)

from src.agent.nodes.utils import extract_transaction_id,extract_customer_id,extract_ticket_id

def ticket_node(state):

    query = state["user_query"]

    print("[TICKET] Looking up tickets")

    # --------------------------------------------------
    # Specific ticket
    # --------------------------------------------------

    ticket_id = extract_ticket_id(query)

    if ticket_id:

        result = get_ticket(
            ticket_id
        )

        tickets = []

        if result.get("found"):
            tickets.append(
                result["ticket"]
            )

        return {
            "ticket_data": tickets,

            "tool_result": [{
                "source": "ticket",
                **result
            }]
        }

    # --------------------------------------------------
    # Customer tickets
    # --------------------------------------------------

    customer_id = (state.get("customer_id") or extract_customer_id(query))

    if not customer_id:
        return {
            "ticket_data": [],

            "tool_result": [{
                "source": "ticket",
                "found": False,
                "error": "customer_id_required"
            }]
        }

    result = get_customer_tickets(customer_id)

    return {
        "ticket_data": result.get(
            "tickets",
            []
        ),

        "tool_result": [{
            "source": "ticket",
            **result
        }]
    }