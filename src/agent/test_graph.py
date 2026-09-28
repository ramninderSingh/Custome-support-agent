from src.agent.graph import build_graph


graph = build_graph()


query = "Tell me about subscription of customer CUS_1001"


result = graph.invoke({
    "user_query": query
})

print("\n" + "=" * 70)
print("FINAL STATE")
print("=" * 70)

print("\nQuery:")
print(query)

print("\nRoute:")
print(result.get("route"))

print("\nCustomer Data:")
print(result.get("customer_data"))

print("\nSubscription Data:")
print(result.get("subscription_data"))

print("\nTransaction Data:")
print(result.get("transaction_data"))

print("\nTicket Data:")
print(result.get("ticket_data"))

print("\nRAG Context:")

for i, document in enumerate(
    result.get("rag_context", []),
    start=1
):
    print(f"\n--- Document {i} ---")

    print(
        "Source:",
        document["metadata"].get("source")
    )

    print(
        "Section:",
        document["metadata"].get("section")
    )

    print(
        "Vector Score:",
        document.get("score")
    )

    print(
        "Reranker Score:",
        document.get("reranker_score")
    )

    print(
        "Text:",
        document["text"]
    )

print("\nTool Results:")
print(result.get("tool_result"))