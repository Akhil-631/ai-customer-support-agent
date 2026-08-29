from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


model = SentenceTransformer(
    MODEL_NAME
)


def generate_embeddings(texts):

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)

    embeddings = embeddings / norms

    return embeddings