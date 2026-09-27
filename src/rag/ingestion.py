from pathlib import Path

from src.rag.chunker import MarkdownChunker
from src.rag.embeddings import EmbeddingModel
from src.rag.vector_store import VectorStore


POLICY_DIR = Path("data/policies")


def ingest_policies():

    chunker = MarkdownChunker()

    embedding_model = EmbeddingModel()

    vector_store = VectorStore()

    all_chunks = []


    for file_path in POLICY_DIR.glob("*.md"):

        print(
            f"Processing {file_path.name}"
        )

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = chunker.chunk_document(
            text=text,
            source=file_path.name
        )

        all_chunks.extend(chunks)

    print(
        f"Created {len(all_chunks)} chunks"
    )

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = embedding_model.encode(
        texts
    )

    vector_store.add_documents(
        documents=all_chunks,
        embeddings=embeddings
    )

    for i, chunk in enumerate(all_chunks):
        print("\n" + "=" * 80)
        print(f"CHUNK {i + 1}")
        print("=" * 80)

        print("Source:", chunk["metadata"]["source"])
        print("Section:", chunk["metadata"]["section"])
        print("Text:")
        print(chunk["text"])

    print("Ingestion completed.")


if __name__ == "__main__":
    ingest_policies()


