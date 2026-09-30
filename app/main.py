from typing import Any

from fastapi import FastAPI

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agent.graph import build_graph

from app.schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="Enterprise Customer Support Agent",
    description=(
        "LLM-driven Agentic RAG customer support API "
        "using LangGraph."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# GRAPH
# ---------------------------------------------------------------------------

graph = build_graph()


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def extract_text(content: Any) -> str:
    """
    Convert LangChain/Gemini message content into plain text.

    Gemini may return either:

        "some text"

    or:

        [
            {"type": "text", "text": "some text"}
        ]

    This helper normalizes both formats.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):

                if item.get("type") == "text":
                    text = item.get("text")

                    if text:
                        text_parts.append(str(text))

        return "\n".join(text_parts)

    return str(content)


def get_interrupt_question(result: dict) -> str:
    """
    Extract the question from a LangGraph interrupt.
    """

    interrupt_data = result["__interrupt__"][0]

    value = interrupt_data.value

    if isinstance(value, dict):
        return value.get(
            "question",
            "Additional information is required.",
        )

    return str(value)


# ---------------------------------------------------------------------------
# HEALTH
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "customer-support-agent",
    }


# ---------------------------------------------------------------------------
# CHAT
# ---------------------------------------------------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.session_id,
        },
        "recursion_limit": 25,
    }

    try:

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=request.message
                    )
                ]
            },
            config=config,
        )

        # ---------------------------------------------------------
        # HUMAN INPUT REQUIRED
        # ---------------------------------------------------------

        if "__interrupt__" in result:

            return ChatResponse(
                status="input_required",
                session_id=request.session_id,
                question=get_interrupt_question(result),
            )

        # ---------------------------------------------------------
        # FINAL RESPONSE
        # ---------------------------------------------------------

        final_message = result["messages"][-1]

        response_text = extract_text(
            final_message.content
        )

        return ChatResponse(
            status="completed",
            session_id=request.session_id,
            response=response_text,
        )

    except Exception as exc:

        return ChatResponse(
            status="error",
            session_id=request.session_id,
            error=str(exc),
        )


# ---------------------------------------------------------------------------
# RESUME CHAT
# ---------------------------------------------------------------------------

@app.post(
    "/chat/resume",
    response_model=ChatResponse,
)
def resume_chat(request: ChatRequest):

    config = {
        "configurable": {
            "thread_id": request.session_id,
        },
        "recursion_limit": 25,
    }

    try:

        result = graph.invoke(
            Command(
                resume=request.message
            ),
            config=config,
        )

        # ---------------------------------------------------------
        # ANOTHER HUMAN INPUT REQUIRED
        # ---------------------------------------------------------

        if "__interrupt__" in result:

            return ChatResponse(
                status="input_required",
                session_id=request.session_id,
                question=get_interrupt_question(result),
            )

        # ---------------------------------------------------------
        # FINAL RESPONSE
        # ---------------------------------------------------------

        final_message = result["messages"][-1]

        response_text = extract_text(
            final_message.content
        )

        return ChatResponse(
            status="completed",
            session_id=request.session_id,
            response=response_text,
        )

    except Exception as exc:

        return ChatResponse(
            status="error",
            session_id=request.session_id,
            error=str(exc),
        )