from src.tools.subscription_tools import get_customer_subscription
import re
from src.agent.nodes.utils import extract_customer_id

def subscription_node(state):

    query = state["user_query"]

    customer_id = (state.get("customer_id") or extract_customer_id(query))

    print("[SUBSCRIPTION] Looking up subscription")

    if not customer_id:
        return {
            "subscription_data": None,

            "tool_result": [{
                "source": "subscription",
                "found": False,
                "error": "customer_id_required"
            }]
        }

    result = get_customer_subscription(customer_id)

    return {
        "subscription_data": result.get(
            "subscription"
        ),

        "tool_result": [{
            "source": "subscription",
            **result
        }]
    }


  