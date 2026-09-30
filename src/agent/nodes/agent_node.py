from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.tools import (
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base
)


tools = [
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base
]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are an enterprise customer support agent.

You have access to tools that provide:

- customer information
- subscription information
- transaction information
- support ticket information
- enterprise support policies

Use tools whenever the user's question requires
information that you do not already have.

You may call multiple tools.

You may call the same or different tools multiple
times if necessary.

Do not invent customer-specific information.

Use the knowledge base for company policies.

Use database tools for customer-specific information.

Continue investigating until you have enough
reliable information to answer the user.

When you have enough information, provide the
final answer instead of calling another tool.

Do not expose internal tool names or system
architecture to the customer.
"""


def agent_node(state):

    messages = state["messages"]

    response = llm_with_tools.invoke(
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            *messages
        ]
    )

    return {
        "messages": [response]
    }