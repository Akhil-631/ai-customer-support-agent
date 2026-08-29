def chunk_documents(
    documents,
    chunk_size=150,
    overlap=30
):

    chunks = []

    step = chunk_size - overlap

    for document in documents:

        words = document["content"].split()

        for start in range(
            0,
            len(words),
            step
        ):

            chunk_words = words[
                start:start + chunk_size
            ]

            if not chunk_words:
                continue

            chunk_text = " ".join(
                chunk_words
            )

            chunks.append(
                {
                    "content": chunk_text,
                    "metadata": document["metadata"].copy()
                }
            )

    return chunks