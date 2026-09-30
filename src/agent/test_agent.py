from src.agent.graph import build_graph


graph = build_graph()


queries = [
    #"What is your refund policy?",
   # "Tell me about customer CUS_1001",
   # "What is the status of transaction TXN_5001?",
  #  "What is the status of ticket TKT_7001?",
    "I was charged twice for my subscription. Can I get a refund?"
]


for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)
    print("=" * 80)

    result = graph.invoke({
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    })

    print("\nFINAL RESPONSE:")
    print(result["messages"][-1].content)

    print("\nMESSAGE TRACE:")

    for i, message in enumerate(
        result["messages"],
        start=1
    ):

        print(f"\n--- Message {i} ---")

        print(
            "Type:",
            type(message).__name__
        )

        print(
            "Content:",
            message.content
        )

        if getattr(message, "tool_calls", None):

            print(
                "Tool Calls:",
                message.tool_calls
            )