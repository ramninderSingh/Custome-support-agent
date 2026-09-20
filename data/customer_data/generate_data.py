from __future__ import annotations

import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any


# ============================================================
# Configuration
# ============================================================

SEED = 42
NUM_CUSTOMERS = 20

OUTPUT_DIR = Path("data")

random.seed(SEED)

REFERENCE_DATE = datetime(2026, 9, 20, 12, 0, 0)

PLANS = {
    "basic": {
        "monthly_price": 799,
    },
    "pro": {
        "monthly_price": 1999,
    },
    "enterprise": {
        "monthly_price": 7999,
    },
}

PAYMENT_METHODS = ["card", "upi", "net_banking"]

FIRST_NAMES = [
    "Aarav",
    "Vivaan",
    "Aditya",
    "Arjun",
    "Kabir",
    "Rohan",
    "Rahul",
    "Karan",
    "Ananya",
    "Priya",
    "Isha",
    "Meera",
    "Neha",
    "Diya",
    "Aditi",
    "Simran",
    "Kavya",
    "Sneha",
    "Nisha",
    "Pooja",
]

LAST_NAMES = [
    "Sharma",
    "Mehta",
    "Verma",
    "Singh",
    "Patel",
    "Kumar",
    "Malhotra",
    "Gupta",
    "Kapoor",
    "Bhatia",
]


# ============================================================
# Utility Functions
# ============================================================

def save_json(filename: str, data: list[dict[str, Any]]) -> None:
    """Save a list of dictionaries as formatted JSON."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / filename

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Created {path}")


def format_datetime(dt: datetime) -> str:
    """Return ISO formatted datetime without microseconds."""

    return dt.replace(microsecond=0).isoformat()


def random_datetime(days_back: int = 30) -> datetime:
    """Generate a random datetime within the last N days."""

    seconds_back = random.randint(0, days_back * 24 * 60 * 60)

    return REFERENCE_DATE - timedelta(seconds=seconds_back)


def random_date(days_back: int = 30) -> str:
    """Generate a random date."""

    return random_datetime(days_back).date().isoformat()


# ============================================================
# Customer Generation
# ============================================================

def generate_customers() -> list[dict[str, Any]]:
    """Generate customer records."""

    customers = []

    for i in range(NUM_CUSTOMERS):

        customer_id = f"CUS_{1001 + i}"

        first_name = FIRST_NAMES[i]
        last_name = random.choice(LAST_NAMES)

        name = f"{first_name} {last_name}"

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{1001 + i}"
            f"@example.com"
        )

        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "account_status": "active",
        }

        customers.append(customer)

    return customers


# ============================================================
# Subscription Generation
# ============================================================

def generate_subscriptions(
    customers: list[dict[str, Any]]
) -> list[dict[str, Any]]:

    subscriptions = []

    for i, customer in enumerate(customers):

        subscription_id = f"SUB_{2001 + i}"

        plan = random.choice(list(PLANS.keys()))

        price = PLANS[plan]["monthly_price"]

        # Some accounts will have different states
        if i == 19:
            status = "cancelled"
        elif i == 18:
            status = "past_due"
        else:
            status = "active"

        start_date = (
            REFERENCE_DATE.date()
            - timedelta(days=random.randint(60, 300))
        )

        renewal_date = start_date + timedelta(days=30)

        # Move renewal date forward until it is in the future.
        while renewal_date <= REFERENCE_DATE.date():
            renewal_date += timedelta(days=30)

        subscription = {
            "subscription_id": subscription_id,
            "customer_id": customer["customer_id"],
            "plan": plan,
            "monthly_price": price,
            "currency": "INR",
            "start_date": start_date.isoformat(),
            "renewal_date": renewal_date.isoformat(),
            "status": status,
        }

        subscriptions.append(subscription)

        # Keep the relationship in the customer record.
        customer["subscription_id"] = subscription_id

    return subscriptions


# ============================================================
# Transaction Helpers
# ============================================================

def create_transaction(
    transaction_id: str,
    customer_id: str,
    subscription_id: str,
    amount: int,
    status: str,
    description: str,
    timestamp: datetime | None = None,
    payment_method: str | None = None,
) -> dict[str, Any]:

    if timestamp is None:
        timestamp = random_datetime(30)

    if payment_method is None:
        payment_method = random.choice(PAYMENT_METHODS)

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "subscription_id": subscription_id,
        "amount": amount,
        "currency": "INR",
        "timestamp": format_datetime(timestamp),
        "status": status,
        "payment_method": payment_method,
        "description": description,
    }


# ============================================================
# Transaction Generation
# ============================================================

def generate_transactions(
    customers: list[dict[str, Any]],
    subscriptions: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    transactions = []

    subscription_by_customer = {
        subscription["customer_id"]: subscription
        for subscription in subscriptions
    }

    transaction_counter = 5001

    for index, customer in enumerate(customers):

        customer_id = customer["customer_id"]

        subscription = subscription_by_customer[customer_id]

        subscription_id = subscription["subscription_id"]

        amount = subscription["monthly_price"]

        # ----------------------------------------------------
        # Scenario 1: Duplicate payment
        # Customers 1 and 2
        # ----------------------------------------------------

        if index in {0, 1}:

            base_time = random_datetime(15)

            txn_1 = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status="successful",
                description="Monthly subscription renewal",
                timestamp=base_time,
            )

            transaction_counter += 1

            txn_2 = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status="successful",
                description="Duplicate subscription charge",
                timestamp=base_time + timedelta(minutes=2),
                payment_method=txn_1["payment_method"],
            )

            transaction_counter += 1

            transactions.extend([txn_1, txn_2])

        # ----------------------------------------------------
        # Scenario 2: Refund requested / already refunded
        # Customers 3 and 4
        # ----------------------------------------------------

        elif index in {2, 3}:

            txn_status = "refunded" if index == 3 else "successful"

            txn = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status=txn_status,
                description="Monthly subscription payment",
            )

            transaction_counter += 1

            transactions.append(txn)

        # ----------------------------------------------------
        # Scenario 3: Failed payment
        # Customers 5 and 6
        # ----------------------------------------------------

        elif index in {4, 5}:

            txn = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status="failed",
                description="Subscription payment attempt",
            )

            transaction_counter += 1

            transactions.append(txn)

        # ----------------------------------------------------
        # Scenario 4: Pending payment
        # Customer 7
        # ----------------------------------------------------

        elif index == 6:

            txn = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status="pending",
                description="Subscription payment processing",
            )

            transaction_counter += 1

            transactions.append(txn)

        # ----------------------------------------------------
        # Scenario 5: Large enterprise payment
        # Customer 8
        # ----------------------------------------------------

        elif index == 7:

            # Enterprise customer gets an additional large payment
            # useful for testing refund approval workflows.

            txn = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=max(amount, 25000),
                status="successful",
                description="Enterprise subscription payment",
            )

            transaction_counter += 1

            transactions.append(txn)

        # ----------------------------------------------------
        # Scenario 6: Multiple failed attempts
        # Customers 9 and 10
        # ----------------------------------------------------

        elif index in {8, 9}:

            for attempt in range(2):

                txn = create_transaction(
                    transaction_id=f"TXN_{transaction_counter}",
                    customer_id=customer_id,
                    subscription_id=subscription_id,
                    amount=amount,
                    status="failed",
                    description=(
                        f"Subscription payment attempt "
                        f"{attempt + 1}"
                    ),
                )

                transaction_counter += 1

                transactions.append(txn)

        # ----------------------------------------------------
        # Scenario 7: Normal successful account
        # Remaining customers
        # ----------------------------------------------------

        else:

            txn = create_transaction(
                transaction_id=f"TXN_{transaction_counter}",
                customer_id=customer_id,
                subscription_id=subscription_id,
                amount=amount,
                status="successful",
                description="Monthly subscription payment",
            )

            transaction_counter += 1

            transactions.append(txn)

            # Some customers get historical transactions too
            if index % 2 == 0:

                old_txn = create_transaction(
                    transaction_id=f"TXN_{transaction_counter}",
                    customer_id=customer_id,
                    subscription_id=subscription_id,
                    amount=amount,
                    status="successful",
                    description="Previous monthly subscription payment",
                    timestamp=REFERENCE_DATE - timedelta(days=45),
                )

                transaction_counter += 1

                transactions.append(old_txn)

    return transactions


# ============================================================
# Ticket Generation
# ============================================================

def generate_tickets(
    customers: list[dict[str, Any]],
    transactions: list[dict[str, Any]],
    subscriptions: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    tickets = []

    ticket_counter = 7001

    transactions_by_customer: dict[str, list[dict[str, Any]]] = {}

    for transaction in transactions:

        customer_id = transaction["customer_id"]

        transactions_by_customer.setdefault(
            customer_id,
            []
        ).append(transaction)

    subscription_by_customer = {
        subscription["customer_id"]: subscription
        for subscription in subscriptions
    }

    for index, customer in enumerate(customers):

        customer_id = customer["customer_id"]

        customer_transactions = transactions_by_customer.get(
            customer_id,
            []
        )

        subscription = subscription_by_customer[customer_id]

        # ----------------------------------------------------
        # Duplicate payment ticket
        # ----------------------------------------------------

        if index in {0, 1}:

            successful_transactions = [
                txn
                for txn in customer_transactions
                if txn["status"] == "successful"
            ]

            transaction_ids = [
                txn["transaction_id"]
                for txn in successful_transactions
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "duplicate_payment",
                "description": (
                    "Customer reported being charged twice "
                    "for the same subscription."
                ),
                "transaction_ids": transaction_ids,
                "status": "open",
                "priority": "high",
                "created_at": format_datetime(random_datetime(7)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Refund request
        # ----------------------------------------------------

        elif index == 2:

            transaction = customer_transactions[0]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "refund_request",
                "description": (
                    "Customer requested a refund "
                    "for a recent subscription payment."
                ),
                "transaction_ids": [
                    transaction["transaction_id"]
                ],
                "status": "open",
                "priority": "medium",
                "created_at": format_datetime(random_datetime(5)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Already refunded
        # ----------------------------------------------------

        elif index == 3:

            refunded_transactions = [
                txn["transaction_id"]
                for txn in customer_transactions
                if txn["status"] == "refunded"
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "refund_status",
                "description": (
                    "Customer asked about the status "
                    "of a previously requested refund."
                ),
                "transaction_ids": refunded_transactions,
                "status": "resolved",
                "priority": "low",
                "created_at": format_datetime(random_datetime(15)),
                "resolution": "Refund already processed.",
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Failed payment
        # ----------------------------------------------------

        elif index in {4, 5}:

            failed_transactions = [
                txn["transaction_id"]
                for txn in customer_transactions
                if txn["status"] == "failed"
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "payment_failure",
                "description": (
                    "Customer reported that their "
                    "subscription payment failed."
                ),
                "transaction_ids": failed_transactions,
                "status": "open",
                "priority": "high",
                "created_at": format_datetime(random_datetime(3)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Pending payment
        # ----------------------------------------------------

        elif index == 6:

            pending_transactions = [
                txn["transaction_id"]
                for txn in customer_transactions
                if txn["status"] == "pending"
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "payment_pending",
                "description": (
                    "Customer wants to know why "
                    "their payment is still pending."
                ),
                "transaction_ids": pending_transactions,
                "status": "open",
                "priority": "medium",
                "created_at": format_datetime(random_datetime(2)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Large refund
        # ----------------------------------------------------

        elif index == 7:

            large_transactions = [
                txn["transaction_id"]
                for txn in customer_transactions
                if txn["amount"] >= 20000
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "large_refund_request",
                "description": (
                    "Customer requested a refund for "
                    "a large enterprise transaction."
                ),
                "transaction_ids": large_transactions,
                "status": "open",
                "priority": "high",
                "created_at": format_datetime(random_datetime(4)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Multiple failed payments
        # ----------------------------------------------------

        elif index in {8, 9}:

            failed_transactions = [
                txn["transaction_id"]
                for txn in customer_transactions
                if txn["status"] == "failed"
            ]

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "repeated_payment_failure",
                "description": (
                    "Customer has experienced multiple "
                    "failed payment attempts."
                ),
                "transaction_ids": failed_transactions,
                "status": "open",
                "priority": "high",
                "created_at": format_datetime(random_datetime(4)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Cancellation ticket
        # ----------------------------------------------------

        elif index in {10, 11, 12}:

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "subscription_cancellation",
                "description": (
                    "Customer requested cancellation "
                    "of their subscription."
                ),
                "transaction_ids": [],
                "status": "open",
                "priority": "medium",
                "created_at": format_datetime(random_datetime(5)),
                "resolution": None,
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Normal billing question
        # ----------------------------------------------------

        elif index in {13, 14, 15}:

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "billing_question",
                "description": (
                    "Customer requested clarification "
                    "about their monthly billing."
                ),
                "transaction_ids": [],
                "status": "resolved",
                "priority": "low",
                "created_at": format_datetime(random_datetime(10)),
                "resolution": (
                    "Billing information was explained "
                    "to the customer."
                ),
            }

            ticket_counter += 1

            tickets.append(ticket)

        # ----------------------------------------------------
        # Invoice request
        # ----------------------------------------------------

        else:

            ticket = {
                "ticket_id": f"TKT_{ticket_counter}",
                "customer_id": customer_id,
                "subscription_id": subscription["subscription_id"],
                "issue_type": "invoice_request",
                "description": (
                    "Customer requested a copy of "
                    "their latest invoice."
                ),
                "transaction_ids": [],
                "status": "resolved",
                "priority": "low",
                "created_at": format_datetime(random_datetime(10)),
                "resolution": "Invoice provided to customer.",
            }

            ticket_counter += 1

            tickets.append(ticket)

    return tickets


# ============================================================
# Consistency Validation
# ============================================================

def validate_data(
    customers: list[dict[str, Any]],
    subscriptions: list[dict[str, Any]],
    transactions: list[dict[str, Any]],
    tickets: list[dict[str, Any]],
) -> None:
    """
    Validate all foreign-key relationships and uniqueness constraints.
    """

    # --------------------------------------------------------
    # Customer IDs
    # --------------------------------------------------------

    customer_ids = {
        customer["customer_id"]
        for customer in customers
    }

    assert len(customer_ids) == len(customers), (
        "Duplicate customer IDs found."
    )

    assert len(customers) == NUM_CUSTOMERS, (
        f"Expected {NUM_CUSTOMERS} customers, "
        f"got {len(customers)}."
    )

    # --------------------------------------------------------
    # Subscription IDs
    # --------------------------------------------------------

    subscription_ids = {
        subscription["subscription_id"]
        for subscription in subscriptions
    }

    assert len(subscription_ids) == len(subscriptions), (
        "Duplicate subscription IDs found."
    )

    # Every customer has exactly one subscription.
    subscription_customer_ids = [
        subscription["customer_id"]
        for subscription in subscriptions
    ]

    assert set(subscription_customer_ids) == customer_ids, (
        "Every customer must have exactly one subscription."
    )

    assert len(subscription_customer_ids) == len(
        set(subscription_customer_ids)
    ), (
        "A customer has more than one subscription."
    )

    # --------------------------------------------------------
    # Customer → Subscription consistency
    # --------------------------------------------------------

    subscription_by_id = {
        subscription["subscription_id"]: subscription
        for subscription in subscriptions
    }

    for customer in customers:

        subscription_id = customer["subscription_id"]

        assert subscription_id in subscription_by_id, (
            f"Customer {customer['customer_id']} references "
            f"missing subscription {subscription_id}"
        )

        subscription = subscription_by_id[subscription_id]

        assert subscription["customer_id"] == customer["customer_id"], (
            f"Customer/subscription mismatch for "
            f"{customer['customer_id']}"
        )

    # --------------------------------------------------------
    # Transaction consistency
    # --------------------------------------------------------

    transaction_ids = {
        transaction["transaction_id"]
        for transaction in transactions
    }

    assert len(transaction_ids) == len(transactions), (
        "Duplicate transaction IDs found."
    )

    for transaction in transactions:

        customer_id = transaction["customer_id"]
        subscription_id = transaction["subscription_id"]

        assert customer_id in customer_ids, (
            f"Transaction references missing customer "
            f"{customer_id}"
        )

        assert subscription_id in subscription_ids, (
            f"Transaction references missing subscription "
            f"{subscription_id}"
        )

        subscription = subscription_by_id[subscription_id]

        assert subscription["customer_id"] == customer_id, (
            f"Transaction {transaction['transaction_id']} has "
            f"inconsistent customer/subscription relationship."
        )

    # --------------------------------------------------------
    # Ticket consistency
    # --------------------------------------------------------

    ticket_ids = {
        ticket["ticket_id"]
        for ticket in tickets
    }

    assert len(ticket_ids) == len(tickets), (
        "Duplicate ticket IDs found."
    )

    for ticket in tickets:

        customer_id = ticket["customer_id"]
        subscription_id = ticket["subscription_id"]

        assert customer_id in customer_ids, (
            f"Ticket references missing customer {customer_id}"
        )

        assert subscription_id in subscription_ids, (
            f"Ticket references missing subscription "
            f"{subscription_id}"
        )

        subscription = subscription_by_id[subscription_id]

        assert subscription["customer_id"] == customer_id, (
            f"Ticket {ticket['ticket_id']} has inconsistent "
            f"customer/subscription relationship."
        )

        # Every transaction mentioned in a ticket must exist.
        for transaction_id in ticket["transaction_ids"]:

            assert transaction_id in transaction_ids, (
                f"Ticket {ticket['ticket_id']} references "
                f"missing transaction {transaction_id}"
            )

    print("\nAll consistency checks passed.")


# ============================================================
# Main
# ============================================================

def main():

    print("Generating CloudDesk customer-support dataset...\n")

    # 1. Generate customers
    customers = generate_customers()

    # 2. Generate subscriptions
    subscriptions = generate_subscriptions(customers)

    # 3. Generate transactions
    transactions = generate_transactions(
        customers,
        subscriptions,
    )

    # 4. Generate tickets
    tickets = generate_tickets(
        customers,
        transactions,
        subscriptions,
    )

    # 5. Validate everything before writing
    validate_data(
        customers,
        subscriptions,
        transactions,
        tickets,
    )

    # 6. Save JSON files
    save_json("customers.json", customers)
    save_json("subscriptions.json", subscriptions)
    save_json("transactions.json", transactions)
    save_json("tickets.json", tickets)

    # 7. Summary
    print("\nDataset summary")
    print("----------------")
    print(f"Customers      : {len(customers)}")
    print(f"Subscriptions  : {len(subscriptions)}")
    print(f"Transactions   : {len(transactions)}")
    print(f"Tickets        : {len(tickets)}")
    print(f"Output folder  : {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()