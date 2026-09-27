from src.rag.pipeline import RAGPipeline


def main():

    rag = RAGPipeline()

    query = (
        "I was charged twice for my subscription. "
        "Can I get a refund?"
    )

    results = rag.search(
        query=query,
        retrieval_k=10,
        rerank_k=5
    )

    print("\n")
    print("=" * 80)
    print("QUERY")
    print("=" * 80)

    print(query)

    print("\n")
    print("=" * 80)
    print("RERANKED RESULTS")
    print("=" * 80)

    for i, result in enumerate(results):

        print(f"\nRESULT {i + 1}")

        print(
            f"Reranker score: "
            f"{result['reranker_score']:.4f}"
        )

        print(
            f"Vector score: "
            f"{result['score']:.4f}"
        )

        print(
            f"Source: "
            f"{result['metadata']['source']}"
        )

        print(
            f"Section: "
            f"{result['metadata']['section']}"
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()