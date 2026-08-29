def build_context(results):
    """
    Convert retrieved chunks into a clean
    context string for the LLM.
    """

    if not results:
        return ""

    context_parts = []

    for result in results:

        source = result["metadata"]["source"]
        content = result["content"]

        context_parts.append(
            f"[Source: {source}]\n"
            f"{content}"
        )

    return "\n\n".join(context_parts)