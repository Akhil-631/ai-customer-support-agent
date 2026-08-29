import faiss
import numpy as np

RELEVANCE_THRESHOLD = 0.20

def build_vector_store(chunks, embeddings):

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks must match number of embeddings."
        )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    return index, chunks

def search_vector_store(index, chunks, query_embedding, top_k=3):

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    query_embedding = query_embedding.reshape(1, -1)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        if score < RELEVANCE_THRESHOLD:
            continue

        result = {
            "content": chunks[index_position]["content"],
            "metadata": chunks[index_position]["metadata"],
            "score": float(score)
        }

        results.append(result)

    return results