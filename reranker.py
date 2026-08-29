from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


reranker = CrossEncoder(
    MODEL_NAME
)


def rerank_results(
    query,
    results,
    top_k=3
):
    """
    Rerank retrieved documents using a cross-encoder.
    """

    if not results:
        return []

    pairs = [
        (query, result["content"])
        for result in results
    ]

    scores = reranker.predict(
        pairs
    )

    reranked_results = []

    for result, score in zip(
        results,
        scores
    ):

        result_copy = result.copy()

        result_copy["rerank_score"] = float(
            score
        )

        reranked_results.append(
            result_copy
        )

    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_results[:top_k]