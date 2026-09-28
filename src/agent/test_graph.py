from src.agent.graph import build_graph


def main():

    graph = build_graph()

    queries = [
        "What is your refund policy?",
        "I was charged twice for my subscription.",
        "What is my current subscription plan?",
        "What is the status of ticket TKT_7001?",
        "Why did my payment fail?",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("QUERY:", query)

        result = graph.invoke({
            "user_query": query
        })

        print("\nROUTE:")
        print(result["route"].model_dump())


if __name__ == "__main__":
    main()