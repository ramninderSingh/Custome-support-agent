from src.tools.transaction_tools import get_customer_transactions,get_transaction
import re
from src.agent.nodes.utils import extract_customer_id,extract_transaction_id

def transaction_node(state):
    query = state["user_query"]

    print("[TRANSACTION] Looking up transactions")

    transaction_id = extract_transaction_id(query)

    if transaction_id:

        result = get_transaction(transaction_id)

        transactions = []

        if result.get("found"):
            transactions.append(result["transaction"])

        return {
            "transaction_data": transactions,

            "tool_result": [{
                "source": "transaction",
                **result
            }]
        }

    customer_id = (state.get("customer_id") or extract_customer_id(query))

    if not customer_id:

        return {
            "transaction_data": [],

            "tool_result": [{
                "source": "transaction",
                "found": False,
                "error": "customer_id_required"
            }]
        }

    result = get_customer_transactions(customer_id)

    return {
        "transaction_data": result.get(
            "transactions",
            []
        ),

        "tool_result": [{
            "source": "transaction",
            **result
        }]
    }
   


