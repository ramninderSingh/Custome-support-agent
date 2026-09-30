from langgraph.prebuilt import ToolNode

from src.agent.tools import (
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base,
    ask_human
)


tools = [
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base,
    ask_human
]


tool_node = ToolNode(tools)