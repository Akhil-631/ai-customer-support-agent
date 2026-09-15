from fastapi import FastAPI
from langgraph.types import Command
from fastapi.middleware.cors import CORSMiddleware

from graph import graph
from state import AgentState
from rag_setup import initialize_rag

from schemas import (
    ChatRequest,
    ChatResponse,
    HumanReviewRequest
)

app = FastAPI(
    title="Enterprise AI Customer Support Agent",
    description="AI Customer Support Agent API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG resources

index, stored_chunks = initialize_rag()

# Chat Endpoint

@app.post(
    "/chat",
    response_model=ChatResponse
)

def chat(request: ChatRequest):

    state = AgentState(
        user_query=request.message
    )

    config = {
        "configurable": {
            "thread_id": request.conversation_id
        }
    }

    result = graph.invoke(
        state,
        config,
        context={
            "rag_index": index,
            "rag_chunks": stored_chunks
        }
    )

    print("\n============ GRAPH RESULT ============")
    print(result)
    print("======================================\n")

# Check whether graph is waiting for human review

    snapshot = graph.get_state(config)

    if snapshot.next:

        print("\n============ GRAPH INTERRUPTED ============")
        print(snapshot.next)
        print("======================================\n")

        interrupts = snapshot.tasks[0].interrupts

        human_review_data = None

        if interrupts:

            human_review_data = interrupts[0].value

        return ChatResponse(
            response="Human review is required for this request.",
            intent=result.get("intent"),
            confidence=result.get("confidence", 0.0),
            requires_human=True,
            order_id=result.get("order_id"),
            human_review_required=True,
            human_review_data=human_review_data
        )

    return ChatResponse(
        response=result.get(
            "final_response",
            "I was unable to generate a response"
        ),
        intent=result.get("intent"),
        confidence=result.get("confidence", 0.0),
        requires_human=result.get("requires_human", False),
        order_id=result.get("order_id"),
        human_review_required=False,
        human_review_data=None
    )

@app.post(
    "/human-review",
    response_model=ChatResponse
)
def human_review(request: HumanReviewRequest):

    decision = request.decision.strip().lower()

    if decision not in {
        "approve",
        "reject",
        "escalate"
    }:

        return ChatResponse(
            response=(
                "Invalid human review decision. "
                "Please choose approve, reject, or escalate."
            ),
            requires_human=True,
            human_review_required=True
        )

    config = {
        "configurable": {
            "thread_id": request.conversation_id
        }
    }

    result = graph.invoke(
        Command(resume=decision),
        config,
        context={
            "rag_index": index,
            "rag_chunks": stored_chunks
        }
    )

    print("\n============ HUMAN REVIEW RESULT ============")
    print(result)
    print("=============================================\n")

    snapshot = graph.get_state(config)

    if snapshot.next:

        interrupts = snapshot.tasks[0].interrupts

        human_review_data = None

        if interrupts:
            human_review_data = interrupts[0].value

        return ChatResponse(
            response="Human review is still required.",
            intent=result.get("intent"),
            confidence=result.get("confidence", 0.0),
            requires_human=True,
            order_id=result.get("order_id"),
            human_review_required=True,
            human_review_data=human_review_data
        )

    return ChatResponse(
        response=result.get(
            "final_response",
            "I was unable to generate a response"
        ),
        intent=result.get("intent"),
        confidence=result.get("confidence", 0.0),
        requires_human=result.get("requires_human", False),
        order_id=result.get("order_id"),
        human_review_required=False,
        human_review_data=None
    )