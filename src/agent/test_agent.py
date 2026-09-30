import uuid

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agent.graph import build_graph


def run_test(query: str):
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    graph = build_graph()

    # Each test gets its own conversation/thread.
    config = {
        "configurable": {
            "thread_id": f"test-{uuid.uuid4()}",
        },
        "recursion_limit": 25,
    }

    # Initial user message
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=query)
            ]
        },
        config=config,
    )

    # ---------------------------------------------------------
    # HUMAN-IN-THE-LOOP
    # ---------------------------------------------------------

    while "__interrupt__" in result:

        interrupt_data = result["__interrupt__"][0]

        question = interrupt_data.value.get(
            "question",
            "The agent needs additional information."
        )

        print("\n" + "-" * 80)
        print("AGENT NEEDS YOUR INPUT")
        print("-" * 80)

        print(f"\nAgent: {question}")

        human_answer = input("\nYou: ")

        # Resume the SAME graph/thread.
        result = graph.invoke(
            Command(
                resume=human_answer
            ),
            config=config,
        )

    # ---------------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------------

    print("\n" + "-" * 80)
    print("FINAL RESPONSE")
    print("-" * 80)

    final_message = result["messages"][-1]

    print(final_message.content)

    # ---------------------------------------------------------
    # MESSAGE TRACE
    # ---------------------------------------------------------

    print("\n" + "-" * 80)
    print("MESSAGE TRACE")
    print("-" * 80)

    for i, message in enumerate(result["messages"]):

        print(
            f"\n[{i}] "
            f"{type(message).__name__}"
        )

        if getattr(message, "content", None):
            print(f"Content: {message.content}")

        if getattr(message, "tool_calls", None):

            print("Tool calls:")

            for tool_call in message.tool_calls:

                print(
                    f"  - {tool_call['name']}"
                    f"({tool_call['args']})"
                )


if __name__ == "__main__":

    queries = [

        # Simple RAG
     #   "What is your refund policy?",

        # Customer lookup
      #  "Show me my subscription information for customer CUST_1001.",

        # Multi-step investigation
        (
            "I was charged twice for my subscription. "
            "Check what happened and tell me whether I may be "
            "eligible for a refund."
        ),

        # Multi-step investigation + action
      #  (
      #      "I was charged twice for my subscription. "
      #      "Investigate it and create a support ticket for me if needed."
      #  ),
    ]

    for query in queries:

        try:
            run_test(query)

        except Exception as exc:

            print("\nERROR:")
            print(exc)