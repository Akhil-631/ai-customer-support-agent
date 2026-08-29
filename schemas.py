from pydantic import BaseModel, Field

class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        description="Customer Support Message"
    )

    conversation_id: str = Field(
        min_length=1,
        description="Conversation Identifier"
    )

class HumanReviewRequest(BaseModel):

    conversation_id: str = Field(
        min_length=1,
        description="Conversation Identifier"
    )

    decision: str = Field(
        min_length=1,
        description="Human Review Decision"
    )

class ChatResponse(BaseModel):

    response: str

    intent: str | None = None

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    requires_human: bool

    order_id: str | None = None

    human_review_required: bool = False

    human_review_data: dict | None = None