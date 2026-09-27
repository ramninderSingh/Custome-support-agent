from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base"
    ):

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5
    ):

        if not documents:
            return []

        pairs = [
            (
                query,
                document["text"]
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = []

        for document, score in zip(
            documents,
            scores
        ):

            result = document.copy()

            result["reranker_score"] = float(
                score
            )

            ranked.append(result)

        ranked.sort(
            key=lambda x: x["reranker_score"],
            reverse=True
        )

        return ranked[:top_k]