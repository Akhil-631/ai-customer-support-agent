from knowledge_loader import load_documents
from chunker import chunk_documents
from embedding_model import generate_embeddings
from vector_store import build_vector_store


def initialize_rag():

    documents = load_documents()

    stored_chunks = chunk_documents(
        documents
    )

    texts = [
        chunk["content"]
        for chunk in stored_chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    index, stored_chunks = build_vector_store(
        stored_chunks,
        embeddings
    )

    return index, stored_chunks