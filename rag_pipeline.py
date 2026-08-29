from retriever import retrieve_context
from context_builder import build_context
from generation import generate_grounded_response


def ask_rag(
    query,
    index,
    stored_chunks,
    top_k=5,
    rerank_top_k=3
):
    """
    Complete end-to-end RAG pipeline.

    Query
    → Retrieval
    → Reranking
    → Context Building
    → Grounded Generation
    """

    results = retrieve_context(
        query,
        index,
        stored_chunks,
        top_k=top_k,
        rerank_top_k=rerank_top_k
    )

    context = build_context(
        results
    )

    response = generate_grounded_response(
        query,
        context
    )

    return {
        "response": response,
        "results": results,
        "context": context
    }