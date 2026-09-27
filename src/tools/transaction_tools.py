from src.database.repositories import TransactionRepository


transaction_repository = TransactionRepository()


def get_transaction(transaction_id: str):

    transaction = (
        transaction_repository
        .get_transaction(transaction_id)
    )

    if transaction is None:
        return {
            "found": False,
            "message": "Transaction not found."
        }

    return {
        "found": True,
        "transaction": transaction.model_dump()
    }


def get_customer_transactions(customer_id: str):

    transactions = (
        transaction_repository
        .get_customer_transactions(customer_id)
    )

    return {
        "count": len(transactions),
        "transactions": [
            transaction.model_dump()
            for transaction in transactions
        ]
    }