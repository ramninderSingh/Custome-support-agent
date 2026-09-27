from datetime import datetime

from src.database.repositories import TicketRepository
from src.models.ticket import Ticket


ticket_repository = TicketRepository()


def get_ticket(ticket_id: str):

    ticket = ticket_repository.get_ticket(ticket_id)

    if ticket is None:
        return {
            "found": False,
            "message": f"Ticket {ticket_id} not found."
        }

    return {
        "found": True,
        "ticket": ticket.model_dump()
    }


def get_customer_tickets(customer_id: str):

    tickets = ticket_repository.get_customer_tickets(
        customer_id
    )

    return {
        "count": len(tickets),
        "tickets": [
            ticket.model_dump()
            for ticket in tickets
        ]
    }


def create_ticket(
    customer_id: str,
    subscription_id: str,
    issue_type: str,
    description: str,
    priority: str = "medium",
    transaction_ids: list[str] | None = None
):

    ticket = Ticket(
        ticket_id=_generate_ticket_id(),
        customer_id=customer_id,
        subscription_id=subscription_id,
        issue_type=issue_type,
        description=description,
        transaction_ids=transaction_ids or [],
        status="open",
        priority=priority,
        created_at=datetime.now(),
        resolution=None
    )

    ticket_repository.create_ticket(ticket)

    return {
        "success": True,
        "ticket": ticket.model_dump()
    }


def _generate_ticket_id():

    tickets = ticket_repository.store.read()

    numbers = [
        int(ticket["ticket_id"].split("_")[1])
        for ticket in tickets
        if ticket["ticket_id"].startswith("TKT_")
    ]

    next_number = max(numbers, default=7000) + 1

    return f"TKT_{next_number}"