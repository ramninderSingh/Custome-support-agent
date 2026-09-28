from src.tools.customer_tools import get_customer
import re
from src.agent.nodes.utils import extract_customer_id


def customer_node(state):

    query = state["user_query"]

    customer_id = (state.get("customer_id") or extract_customer_id(query))
    print("[CUSTOMER] Looking up customer")

    if not customer_id:
        return {
            "customer_data": None,

            "tool_result": [{
                "source": "customer",
                "found": False,
                "error": "customer_id_required"
            }]
        }

    result = get_customer(customer_id=customer_id)

    return {
        "customer_id":customer_id,
        "customer_data": result.get("customer"),
        "tool_result": [{
            "source": "customer",
            **result
        }
        ]

    }

    
    