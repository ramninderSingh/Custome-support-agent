from src.rag.pipeline import RAGPipeline

rag_pipeline = RAGPipeline()

def rag_node(state):

    query = state["user_query"]
    print("[RAG] Running knowledge retrieval")

    results = rag_pipeline.search(
        query=query,
        retrieval_k=10,
        rerank_k=5
    )

    rag_context = []

    for result in results:
        rag_context.append({
            "text": result["text"],
            "metadata": result["metadata"],
            "score": result.get("score"),
            "reranker_score": result.get("reranker_score")
        })
    
    return {
        "rag_context": rag_context
    }
