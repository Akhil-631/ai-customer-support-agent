from llm_client import call_llm
from prompts import INTENT_CLASSIFICATION_PROMPT

from tools import (
    cancel_order,
    get_delivery_status,
    get_refund_status,
    get_order_status,
    escalate_to_human
)

import json


# -------------------------------
# Intent Classification
# -------------------------------

def classify_intent(user_query):

    prompt = INTENT_CLASSIFICATION_PROMPT + user_query

    response = call_llm(
        system_message="You are a strict intent classifier. Return ONLY valid JSON.",
        user_message=prompt
    )

    print("\nRAW LLM RESPONSE")
    print(response)
    print("-" * 50)

    try:
        return json.loads(response)

    except Exception:

        return {
            "intent": "general_query",
            "order_id": None,
            "confidence": 0.0,
            "requires_human": False
        }


# -------------------------------
# Routing
# -------------------------------

def route_intent(result, user_query):

    intent = result["intent"]

    order_id = result.get("order_id")

    confidence = result.get("confidence", 0)

    requires_human = result.get("requires_human", False)

    # Low confidence
    if confidence < 0.50:

        return (
            "I'm not completely confident about your request."
            " Could you please rephrase it?"
        )

    # Human approval

    if requires_human:

        return escalate_to_human(
            order_id,
            user_query
        )

    # Routing

    if intent == "order_status":

        return get_order_status(order_id)

    elif intent == "delivery_status":

        return get_delivery_status(order_id)

    elif intent == "refund_status":

        return get_refund_status(order_id)

    elif intent == "cancel_order":

        return cancel_order(order_id)

    elif intent == "human_support":

        return escalate_to_human(
            order_id,
            user_query
        )

    else:

        return (
            "Sorry, I couldn't understand your request."
        )