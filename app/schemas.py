from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Message from the user",
    )

    session_id: str = Field(
        ...,
        min_length=1,
        description="Unique conversation/session ID",
    )


class ChatResponse(BaseModel):
    status: Literal[
        "completed",
        "input_required",
        "error",
    ]

    session_id: str

    response: str | None = None

    question: str | None = None

    error: str | None = None

    metadata: dict[str, Any] | None = None