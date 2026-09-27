from src.database.repositories import SubscriptionRepository


subscription_repository = SubscriptionRepository()


def get_customer_subscription(customer_id: str):

    subscription = (
        subscription_repository
        .get_customer_subscription(customer_id)
    )

    if subscription is None:
        return {
            "found": False,
            "message": "No subscription found."
        }

    return {
        "found": True,
        "subscription": subscription.model_dump()
    }