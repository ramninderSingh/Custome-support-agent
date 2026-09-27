from sentence_transformers import SentenceTransformer

class EmbeddingModel:

    def __init__(
            self,
            model_name = "BAAI/bge-small-en-v1.5"
    ):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, normalize_embeddings = True, show_progress_bar=True)
        return embeddings.tolist()
    
    def encode_query(self, query: str) -> list[float]:
        embedding = self.model.encode(query, normalize_embeddings=True)
        return embedding.tolist()

    # normalizing embeddings to use cosine sim