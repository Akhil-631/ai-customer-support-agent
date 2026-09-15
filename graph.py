from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from llm_client import call_llm
from prompts import (
    RESPONSE_GENERATION_PROMPT,
    CONVERSATIONAL_RESPONSE_PROMPT
)
from rag_pipeline import ask_rag
from typing import TypedDict
from models import ToolResult

from state import AgentState
from agent import (
    classify_intent,
    validate_request
)

from tools import (
    get_order_status,
    get_delivery_status,
    get_refund_status,
    cancel_order,
    escalate_to_human
)

class GraphContext(TypedDict):

    rag_index: object
    rag_chunks: list

def classify_node(state: AgentState):

    # Reset turn-specific state

    state.tool_result = None
    state.final_response = None
    state.next_action = None
    state.human_decision = None
    state.human_review_required = False

    # Resume a pending parameter collection

    if state.pending_parameter == "order_id":

        state.order_id = state.user_query.strip()

        return state

    # Normal intent classification

    result = classify_intent(state.user_query)

    state.intent = result.get("intent")
    new_order_id = result.get("order_id")
    if new_order_id:
        state.order_id = new_order_id
    state.confidence = result.get("confidence", 0.0)
    state.requires_human = result.get("requires_human", False)

    return state

def validate_node(state: AgentState):

    result = {
        "intent": state.intent,
        "order_id": state.order_id,
    }

    validation = validate_request(result)

    if validation["valid"]:

        state.next_action = "continue"
        state.pending_parameter = None

        if state.intent == "cancel_order":

            state.human_review_required = True

    else:
        state.next_action = "request_information"
        state.pending_parameter = "order_id"
        state.tool_result = {
            "success": False,
            "message": validation["message"],
            "error": "VALIDATION_ERROR"
        }

    return state

def route_after_validation(state: AgentState):

    if state.next_action == "request_information":
        return "request_information"

    if state.human_review_required:
        return "human_review"

    return "continue"

def request_information_node(state: AgentState):

    return state

def continue_node(state: AgentState):

    return state

def execute_tool_node(state: AgentState):

    intent = state.intent
    order_id = state.order_id

    try:

        if intent == "order_status":

            tool_result = get_order_status(order_id)

        elif intent == "delivery_status":
            
            tool_result = get_delivery_status(order_id)

        elif intent == "refund_status":
            
            tool_result = get_refund_status(order_id)

        elif intent == "cancel_order":

            tool_result = cancel_order(order_id)

        elif intent == "human_support":

            tool_result = escalate_to_human(
                order_id,
                state.user_query
            )
        else:

            tool_result = ToolResult(
                success= False,
                message= "Unable to determine the appropriate action.",
                error= "UNKNOWN_INTENT"
            )

    except Exception:

        tool_result = ToolResult(
            success=False,
            message="An unexpected error occured while processing the request.",
            error="TOOL_EXECUTION_ERROR"
        )

    state.tool_result = tool_result.model_dump()

    return state

def route_after_tool(state: AgentState):

    if state.tool_result is None:
        return "error"

    if state.tool_result.get("success"):
        return "success"

    return "error"

def tool_success_node(state: AgentState):

    state.next_action = "complete"

    return state

def tool_error_node(state: AgentState):

    state.next_action = "handle_error"

    return state

def route_tool_error(state: AgentState):

    if state.tool_result is None:
        return "handle_error"

    error = state.tool_result.get("error")

    if error in {
        "ORDER_NOT_FOUND",
        "REFUND_NOT_FOUND"
    }:
        return "user_message"

    if error in {
        "ORDER_NOT_CANCELLABLE",
        "ORDER_ALREADY_CANCELLED",
        "MIXED_FULFILLMENT_STATE"
    }:
        return "business_rule" 

    return "escalate"

def user_message_node(state: AgentState):

    state.next_action = "inform_user"

    return state

def business_rule_node(state: AgentState):

    state.next_action = "explain_business_rule"

    return state

def escalate_error_node(state: AgentState):

    state.next_action = "escalate_error"

    return state

def human_review_node(state: AgentState):

    state.human_review_required = True

    decision = interrupt({
        "message": "Human review is required.",
        "user_query": state.user_query,
        "intent": state.intent,
        "order_id": state.order_id,
    })

    state.human_decision = decision
    state.human_review_required = False

    return state

def route_after_human_review(state: AgentState):

    if state.human_decision == "approve":
        return "approve"

    if state.human_decision == "reject":
        return "reject"

    if state.human_decision == "escalate":
        return "escalate"

    return "escalate"
    
def route_after_classification(state: AgentState):

    if state.intent == "general_query":
        return "rag"

    if state.intent == "conversational":
        return "conversational"

    if state.requires_human and state.intent != "human_support":
        return "human_review"

    return "validate"

def generate_response_node(state: AgentState):

    tool_result = state.tool_result

    user_message = f"""
Customer Query: {state.user_query}

Intent: {state.intent}

Tool Result: {tool_result}
"""

    response = call_llm(
        RESPONSE_GENERATION_PROMPT,
        user_message
    )

    state.final_response = response

    return state

def rag_node(state: AgentState, runtime):

    rag_index = runtime.context["rag_index"]
    rag_chunks = runtime.context["rag_chunks"]

    result = ask_rag(
        state.user_query,
        rag_index,
        rag_chunks
    )

    state.final_response = result["response"]

    return state

def human_approved_node(state: AgentState):

    state.next_action = "human_approved"

    return state

def human_rejected_node(state: AgentState):

    state.tool_result = {
        "success": False,
        "message": "The cancellation request was rejected by human support.",
        "error": "CANCELLATION_REJECTED"
    }

    state.next_action = "human_rejected"

    return state

def human_escalated_node(state: AgentState):

    try:

        tool_result = escalate_to_human(
            state.order_id,
            state.user_query
        )

    except Exception:

        tool_result = ToolResult(
            success=False,
            message="An unexpected error occurred while escalating the request.",
            error="TOOL_EXECUTION_ERROR"
        )

    state.tool_result = tool_result.model_dump()

    state.next_action = "human_escalated"

    return state

def execute_approved_cancel_node(state: AgentState):

    try:

        tool_result = cancel_order(
            state.order_id
        )

    except Exception:

        tool_result = ToolResult(
            success=False,
            message="An unexpected error occurred while cancelling the order.",
            error="TOOL_EXECUTION_ERROR"
        )

    state.tool_result = tool_result.model_dump()

    return state

def conversational_node(state: AgentState):

    response = call_llm(
        CONVERSATIONAL_RESPONSE_PROMPT,
        state.user_query
    )

    state.final_response = response

    return state

graph_builder = StateGraph(AgentState)

graph_builder.add_node(
    "classify_intent",
    classify_node
)

graph_builder.add_node(
    "conversational",
    conversational_node
)

graph_builder.add_node(
    "validate_request",
    validate_node
)

graph_builder.add_node(
    "request_information",
    request_information_node
)

graph_builder.add_node(
    "continue",
    continue_node
)

graph_builder.add_node(
    "execute_tool",
    execute_tool_node
)

graph_builder.add_node(
    "tool_success",
    tool_success_node
)

graph_builder.add_node(
    "tool_error",
    tool_error_node
)

graph_builder.add_node(
    "user_message",
    user_message_node
)

graph_builder.add_node(
    "business_rule",
    business_rule_node
)

graph_builder.add_node(
    "escalate_error",
    escalate_error_node
)

graph_builder.add_node(
    "human_review",
    human_review_node
)

graph_builder.add_node(
    "human_approved",
    human_approved_node
)

graph_builder.add_node(
    "execute_approved_cancel",
    execute_approved_cancel_node
)

graph_builder.add_node(
    "human_rejected",
    human_rejected_node
)

graph_builder.add_node(
    "human_escalated",
    human_escalated_node
)

graph_builder.add_node(
    "generate_response",
    generate_response_node
)

graph_builder.add_node(
    "rag",
    rag_node
)

graph_builder.add_edge(
    START,
    "classify_intent"
)

graph_builder.add_conditional_edges(
    "classify_intent",
    route_after_classification,
    {
        "validate": "validate_request",
        "human_review": "human_review",
        "rag": "rag",
        "conversational": "conversational"
    }
)

graph_builder.add_conditional_edges(
    "human_review",
    route_after_human_review,
    {
        "approve": "human_approved",
        "reject": "human_rejected",
        "escalate": "human_escalated"
    }
)

graph_builder.add_edge(
    "human_approved",
    "execute_approved_cancel"
)

graph_builder.add_edge(
    "execute_approved_cancel",
    "generate_response"
)

graph_builder.add_edge(
    "human_rejected",
    "generate_response"
)

graph_builder.add_edge(
    "human_escalated",
    "generate_response"
)

graph_builder.add_conditional_edges(
    "validate_request",
    route_after_validation,
    {
        "request_information": "request_information",
        "human_review": "human_review",
        "continue": "continue"
    }   
)

graph_builder.add_edge(
    "request_information",
    "generate_response"
)

graph_builder.add_edge(
    "continue",
    "execute_tool"
)

graph_builder.add_conditional_edges(
    "execute_tool",
    route_after_tool,
    {
        "success": "tool_success",
        "error": "tool_error"
    }
)

graph_builder.add_edge(
    "tool_success",
    "generate_response"
)

graph_builder.add_conditional_edges(
    "tool_error",
    route_tool_error,
    {
        "user_message": "user_message",
        "business_rule": "business_rule",
        "escalate": "escalate_error"
    }
)

graph_builder.add_edge(
    "user_message",
    "generate_response"
)

graph_builder.add_edge(
    "business_rule",
    "generate_response"
)

graph_builder.add_edge(
    "escalate_error",
    "generate_response"
)

graph_builder.add_edge(
    "generate_response",
    END
)

graph_builder.add_edge(
    "rag",
    END
)

graph_builder.add_edge(
    "conversational",
    END
)

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory
)

