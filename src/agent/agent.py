import os
import json

from dotenv import load_dotenv
from google import genai

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

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL = "gemini-3.5-flash-lite"


TOOLS = [
    customer_lookup,
    subscription_lookup,
    transaction_lookup,
    transaction_lookup_by_id,
    ticket_lookup,
    ticket_lookup_by_id,
    search_knowledge_base,
    ask_human
]


SYSTEM_PROMPT = """
You are an enterprise customer support agent.

You have access to tools for:

- customer information
- subscriptions
- transactions
- support tickets
- enterprise support policies

Use tools whenever additional information is required.

You may call multiple tools.

You may call tools multiple times.

Do not invent customer-specific information.

Use the knowledge base for company policies.

Use database tools for customer-specific information.

If required information is missing and you cannot
determine it from the available context, use the
ask_human tool.

Examples of when to ask the human:

- A customer ID is required but not available.
- A transaction ID is required but not available.
- The user has not provided enough information to
  identify which transaction they mean.
- An action requires confirmation from the customer.
- The request is ambiguous and guessing could lead
  to an incorrect action.

Do not ask the human for information that can already
be obtained using one of your tools.

When asking the human, ask one clear and concise
question.

Do not invent customer-specific information.

Continue investigating after receiving the human's answer.

When you have enough information, provide the final answer.

Do not expose internal tool names or system architecture.
"""


def run_agent(user_query: str):

    chat = client.chats.create(
        model=MODEL,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "tools": TOOLS
        }
    )

    response = chat.send_message(
        user_query
    )

    while True:

        # ------------------------------------------------
        # Check whether Gemini wants to call a tool
        # ------------------------------------------------

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:
                function_calls.append(
                    part.function_call
                )

        # ------------------------------------------------
        # No tool calls = final answer
        # ------------------------------------------------

        if not function_calls:

            return response.text

        # ------------------------------------------------
        # Execute tools
        # ------------------------------------------------

        tool_results = []

        for call in function_calls:

            tool_name = call.name
            tool_args = dict(
                call.args
            )

            print(
                f"\n[TOOL CALL] {tool_name}"
            )

            print(
                "[ARGS]",
                tool_args
            )

            # Map tool name → Python function

            tool_map = {
                "customer_lookup":
                    customer_lookup,

                "subscription_lookup":
                    subscription_lookup,

                "transaction_lookup":
                    transaction_lookup,

                "transaction_lookup_by_id":
                    transaction_lookup_by_id,

                "ticket_lookup":
                    ticket_lookup,

                "ticket_lookup_by_id":
                    ticket_lookup_by_id,

                "search_knowledge_base":
                    search_knowledge_base,

                "ask_human":
                    ask_human   
            }

            tool = tool_map[tool_name]

            result = tool(
                **tool_args
            )

            print(
                "[TOOL RESULT]",
                result
            )

            tool_results.append(
                {
                    "function_response": {
                        "name": tool_name,
                        "response": result
                    }
                }
            )

        # ------------------------------------------------
        # Send tool results back to Gemini
        # ------------------------------------------------

        response = chat.send_message(
            tool_results
        )