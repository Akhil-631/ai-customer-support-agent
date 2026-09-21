from fastapi import FastAPI
from langgraph.types import Command
from fastapi.middleware.cors import CORSMiddleware

from graph import graph
from state import AgentState
from rag_setup import initialize_rag
from database.repository import (
    create_human_review,
    get_pending_human_reviews,
    update_human_review_by_conversation
)

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

        # Persist human review request
            if human_review_data:

                review_id = create_human_review(
                    conversation_id=request.conversation_id,
                    order_id=result.get("order_id"),
                    request_type=human_review_data.get(
                        "request_type",
                        "Human Support"
                    ),
                    issue=human_review_data.get(
                        "issue",
                        request.message
                    )
                )

                print(
                    f"Human review request created: {review_id}"
                )

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

@app.get("/human-reviews")
def get_human_reviews():

    reviews = get_pending_human_reviews()

    return {
        "reviews": reviews
    }

@app.get("/conversation/{conversation_id}")
def get_conversation_state(conversation_id: str):

    config = {
        "configurable": {
            "thread_id": conversation_id
        }
    }

    snapshot = graph.get_state(config)

    values = snapshot.values

    return {
        "requires_human": values.get(
            "requires_human",
            False
        ),
        "human_review_required": values.get(
            "human_review_required",
            False
        ),
        "human_decision": values.get(
            "human_decision"
        ),
        "final_response": values.get(
            "final_response"
        ),
        "next_action": values.get(
            "next_action"
        )
    }

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

    review_status = {
        "approve": "Approved",
        "reject": "Rejected",
        "escalate": "Escalated"
    }[decision]

    updated_reviews = update_human_review_by_conversation(
        request.conversation_id,
        review_status
    )

    print(
        f"Human review status updated: "
        f"{review_status} ({updated_reviews} record(s))"
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

