from embedding_model import generate_embeddings
from vector_store import search_vector_store
from reranker import rerank_results


def retrieve_context(
    query,
    index,
    chunks,
    top_k=5,
    rerank_top_k=3
):
    """
    Retrieve relevant knowledge-base chunks
    for a user query.
    """

    query_embedding = generate_embeddings(
        [query]
    )

    results = search_vector_store(
        index,
        chunks,
        query_embedding,
        top_k=top_k
    )

    if not results:
        return []

    unique_results = []
    seen_content = set()

    for result in results:

        content = result["content"]

        if content in seen_content:
            continue

        seen_content.add(content)

        unique_results.append(result)

    reranked_results = rerank_results(
        query,
        unique_results,
        top_k=rerank_top_k
    )

    return reranked_results
