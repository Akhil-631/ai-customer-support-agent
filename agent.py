from llm_client import call_llm
from prompts import INTENT_CLASSIFICATION_PROMPT, INTENT_CORRECTION_PROMPT
import re
from models import ToolResult

from tools import (
    cancel_order,
    get_delivery_status,
    get_refund_status,
    get_order_status,
    escalate_to_human
)

import json

from pydantic import BaseModel, Field
from enum import Enum

# -------------------------------
# Allowed Intents
# -------------------------------

class Intent(str, Enum):

    ORDER_STATUS = "order_status"
    DELIVERY_STATUS = "delivery_status"
    REFUND_STATUS = "refund_status"
    CANCEL_ORDER = "cancel_order"
    HUMAN_SUPPORT = "human_support"
    GENERAL_QUERY = "general_query"
    CONVERSATIONAL = "conversational"

# -------------------------------
# LLM Response Schema
# -------------------------------

class IntentResult(BaseModel):

    model_config = {
        "extra": "forbid" 
    }

    intent: Intent

    order_id: str | None = None

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    requires_human: bool

# -------------------------------
# Intent Classification
# -------------------------------

def classify_intent(user_query):

    prompt = INTENT_CLASSIFICATION_PROMPT + user_query

    try:

        response = call_llm(
            system_message="You are a strict intent classifier. Return ONLY valid JSON.",
            user_message=prompt
        )

    except Exception as e:

        print("\nLLM API ERROR")
        print(e)
        print("-" * 50)

        return {
            "intent": "general_query",
            "order_id": None,
            "confidence": 0.0,
            "requires_human": True,
            "llm_failed": True
        }
    # Empty LLM response
    if not response or not response.strip():

        print("\nLLM EMPTY RESPONSE")
        print("-" * 50)

        return {
            "intent": "general_query",
            "order_id": None,
            "confidence": 0.0,
            "requires_human": True,
            "llm_failed": False
        }

    print("\nRAW LLM RESPONSE")
    print(response)
    print("-" * 50)

# First Validation attempt

    try:

        parsed_response = json.loads(response)

        validated_response = IntentResult.model_validate(
            parsed_response
        )

        result = validated_response.model_dump(mode="json")

        # Enforce application-level confidence policy
        if result["confidence"] < 0.70:
            result["requires_human"] = True

        result["llm_failed"] = False

        return result

    except Exception as e:

        print("\nLLM RESPONSE VALIDATION ERROR")
        print(e)
        print("-" * 50)

# Output connection Retry

    retry_prompt = INTENT_CORRECTION_PROMPT + user_query

    try:

        retry_response = call_llm(
            system_message=(
                "You are a strict intent classifier."
                "Return ONLY valid JSON matching the required schema."
            ),
            user_message=retry_prompt
        )

        print("\nLLM CORRECTION RETRY RESPONSE")
        print(retry_response)
        print("-" * 50)

        retry_parsed = json.loads(retry_response)

        retry_validated = IntentResult.model_validate(retry_parsed)

        result = retry_validated.model_dump(mode="json")

        result["llm_failed"] = False

        return result

    except Exception as e:

        print("\nLLM CORRECTION RETRY FAILED")
        print(e)
        print("-" * 50)

        return {
            "intent": "general_query",
            "order_id": None,
            "confidence": 0.0,
            "requires_human": True,
            "llm_failed": False
        }


# -------------------------------
# Input / Parameter Validation
# -------------------------------

def validate_request(result):

    intent = result.get("intent")
    order_id = result.get("order_id")

    # Intents that require an Order ID
    order_id_required_intents = {
        "order_status",
        "delivery_status",
        "refund_status",
        "cancel_order"
    }

    # Order ID is required
    if intent in order_id_required_intents:

        if not order_id:

            return {
                "valid": False,
                "message": (
                    "Please provide your Order ID "
                    "so I can help you with this request."
                )
            }

        # Basic Order ID format validation
        order_id_pattern = r"^[A-Z]{2}-\d{4}-\d+$"

        if not re.match(order_id_pattern, order_id.strip()):
            return {
                "valid": False,
                "message": (
                    "The Order ID format doesn't appear to be valid."
                    " Please provide a valid Order ID."
                )
            }

    return {
        "valid": True,
        "message": None
    }

# -------------------------------
# Routing
# -------------------------------

def route_intent(result, user_query):

    intent = result["intent"]

    order_id = result.get("order_id")

    confidence = result.get("confidence", 0)

    requires_human = result.get("requires_human", False)

    llm_failed = result.get("llm_failed", False)

    # LLM service failure
    if llm_failed:

        return (
            "I'm currently unable to process your request because "
            "the AI service is temporarily unavailable. "
            "Please try again shortly or contact human support."
        )

    # Validate required information
    validation = validate_request(result)

    if not validation["valid"]:
        return ToolResult(
            success=False,
            message=validation["message"],
            error="MISSING_REQUIRED_PARAMETER"
        )

    # Low confidence
    if confidence < 0.50:

        return ToolResult(
            success=False,
            message=(
                "I'm not completely confident about your request. "
                "Could you please rephrase it?"
            ),
            error="LOW_CONFIDENCE"
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

        return ToolResult(
            success=False,
            message="Sorry, I couldn't understand your request.",
            error="UNKNOWN_INTENT"
        )