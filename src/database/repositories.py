from pathlib import Path

from src.database.json_store import JSONStore
from src.models.customer import Customer
from src.models.subscription import Subscription
from src.models.transaction import Transaction
from src.models.ticket import Ticket


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "customer_data"


class CustomerRepository:

    def __init__(self):
        self.store = JSONStore(
            DATA_DIR / "customers.json"
        )

    def get_customer(self, customer_id: str) -> Customer | None:

        customers = self.store.read()

        for customer in customers:
            if customer["customer_id"] == customer_id:
                return Customer(**customer)

        return None

    def get_all(self) -> list[Customer]:

        return [
            Customer(**customer)
            for customer in self.store.read()
        ]


class SubscriptionRepository:

    def __init__(self):
        self.store = JSONStore(
            DATA_DIR / "subscriptions.json"
        )

    def get_subscription(
        self,
        subscription_id: str
    ) -> Subscription | None:

        subscriptions = self.store.read()

        for subscription in subscriptions:

            if subscription["subscription_id"] == subscription_id:
                return Subscription(**subscription)

        return None

    def get_customer_subscription(
        self,
        customer_id: str
    ) -> Subscription | None:

        subscriptions = self.store.read()

        for subscription in subscriptions:

            if subscription["customer_id"] == customer_id:
                return Subscription(**subscription)

        return None


class TransactionRepository:

    def __init__(self):
        self.store = JSONStore(
            DATA_DIR / "transactions.json"
        )

    def get_transaction(
        self,
        transaction_id: str
    ) -> Transaction | None:

        transactions = self.store.read()

        for transaction in transactions:

            if transaction["transaction_id"] == transaction_id:
                return Transaction(**transaction)

        return None

    def get_customer_transactions(
        self,
        customer_id: str
    ) -> list[Transaction]:

        return [
            Transaction(**transaction)
            for transaction in self.store.read()
            if transaction["customer_id"] == customer_id
        ]


class TicketRepository:

    def __init__(self):
        self.store = JSONStore(
            DATA_DIR / "tickets.json"
        )

    def get_ticket(
        self,
        ticket_id: str
    ) -> Ticket | None:

        tickets = self.store.read()

        for ticket in tickets:

            if ticket["ticket_id"] == ticket_id:
                return Ticket(**ticket)

        return None

    def get_customer_tickets(
        self,
        customer_id: str
    ) -> list[Ticket]:

        return [
            Ticket(**ticket)
            for ticket in self.store.read()
            if ticket["customer_id"] == customer_id
        ]

    def create_ticket(self, ticket: Ticket) -> Ticket:

        tickets = self.store.read()

        tickets.append(ticket.model_dump(mode="json"))

        self.store.write(tickets)

        return ticket

    def update_ticket(self, updated_ticket: Ticket) -> Ticket:

        tickets = self.store.read()

        for i, ticket in enumerate(tickets):

            if ticket["ticket_id"] == updated_ticket.ticket_id:

                tickets[i] = updated_ticket.model_dump(mode="json")

                self.store.write(tickets)

                return updated_ticket

        raise ValueError(
            f"Ticket {updated_ticket.ticket_id} not found"
        )