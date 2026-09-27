from src.router.classifier import QueryRouter


def main():

    router = QueryRouter()

    queries = [
        "What is your refund policy?",
        "I was charged twice for my subscription.",
        "What is the status of ticket TKT_7001?",
        "What is my current subscription plan?",
        "Cancel my subscription.",
        "Why did my payment fail?"
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("QUERY:", query)

        result = router.classify(query)

        print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()