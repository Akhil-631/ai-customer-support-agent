from llm_client import call_llm
from prompts import GROUNDED_GENERATION_PROMPT


def generate_grounded_response(
    query,
    context
):
    """
    Generate an answer using only retrieved context.
    """

    prompt = GROUNDED_GENERATION_PROMPT.format(
        context=context,
        query=query
    )

    response = call_llm(
        prompt,
        ""
    )

    return response