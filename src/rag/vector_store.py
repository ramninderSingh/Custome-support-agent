from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


class VectorStore:

    def __init__(
        self,
        path: str = "data/vector_db",
        collection_name: str = "support_policies",
        vector_size: int = 384
    ):

        self.client = QdrantClient(
            path=path
        )

        self.collection_name = collection_name

        collections = (
            self.client
            .get_collections()
            .collections
        )

        existing = {
            collection.name
            for collection in collections
        }

        if collection_name not in existing:

            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def add_documents(
        self,
        documents: list[dict],
        embeddings: list[list[float]]
    ):

        points = []

        for index, (document, embedding) in enumerate(
            zip(documents, embeddings)
        ):

            points.append(
                PointStruct(
                    id=index,
                    vector=embedding,
                    payload={
                        "text": document["text"],
                        **document["metadata"]
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 10
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )

        return results.points