from src.database.repositories import CustomerRepository


customer_repository = CustomerRepository()


def get_customer(customer_id: str):

    """
    Retrieve customer account information.

    Args:
        customer_id: Unique customer identifier.

    Returns:
        Customer information if found.
        ;
    """

    customer = customer_repository.get_customer(customer_id)

    if customer is None:
        return {
            "found": False,
            "message": f"Customer {customer_id} not found."
        }

    return {
        "found": True,
        "customer": customer.model_dump()
    }
