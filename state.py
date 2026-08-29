from typing import Any, Optional
from pydantic import BaseModel


class AgentState(BaseModel):

    user_query: str = ""

    intent: Optional[str] = None

    order_id: Optional[str] = None

    pending_parameter: Optional[str] = None

    confidence: float = 0.0

    requires_human: bool = False

    tool_result: Optional[Any] = None

    next_action: Optional[str] = None

    human_review_required: bool = False

    human_decision: Optional[str] = None

    final_response: Optional[str] = None

    rag_response: Optional[str] = None