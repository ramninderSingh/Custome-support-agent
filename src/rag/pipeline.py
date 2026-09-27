from src.rag.retriever import Retriever
from src.rag.reranker import Reranker


class RAGPipeline:

    def __init__(self):

        self.retriever = Retriever()

        self.reranker = Reranker()

    def search(
        self,
        query: str,
        retrieval_k: int = 10,
        rerank_k: int = 5
    ):

        retrieved_documents = (
            self.retriever.retrieve(
                query=query,
                top_k=retrieval_k
            )
        )

        reranked_documents = (
            self.reranker.rerank(
                query=query,
                documents=retrieved_documents,
                top_k=rerank_k
            )
        )

        return reranked_documents