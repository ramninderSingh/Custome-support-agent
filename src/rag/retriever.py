from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 10
    ):

        query_embedding = (
            self.embedding_model
            .encode_query(query)
        )

        results = self.vector_store.search(
            query_vector=query_embedding,
            limit=top_k
        )

        return [
            {
                "text": result.payload["text"],
                "metadata": {
                    key: value
                    for key, value in result.payload.items()
                    if key != "text"
                },
                "score": result.score
            }
            for result in results
        ]