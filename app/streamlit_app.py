import uuid

import requests
import streamlit as st


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Enterprise Support Agent",
    page_icon="🤖",
    layout="centered",
)


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{uuid.uuid4()}"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

st.title("Enterprise Support Agent")
st.caption(
    "AI-powered customer support using Agentic RAG"
)


# ---------------------------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------------------------
# API CALL
# ---------------------------------------------------------------------------

def call_chat_api(message: str):

    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": message,
            "session_id": st.session_state.session_id,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def call_resume_api(message: str):

    response = requests.post(
        f"{API_URL}/chat/resume",
        json={
            "message": message,
            "session_id": st.session_state.session_id,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------------------------

if prompt := st.chat_input("How can I help you?"):

    # Show user message immediately
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------------------------------------------------
    # If waiting for human input, resume the existing graph
    # ---------------------------------------------------------

    if st.session_state.get("waiting_for_input", False):

        try:

            result = call_resume_api(prompt)

        except Exception as exc:

            error_message = f"API error: {exc}"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )

            with st.chat_message("assistant"):
                st.error(error_message)

            st.stop()

    # ---------------------------------------------------------
    # Normal message
    # ---------------------------------------------------------

    else:

        try:

            result = call_chat_api(prompt)

        except Exception as exc:

            error_message = f"API error: {exc}"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )

            with st.chat_message("assistant"):
                st.error(error_message)

            st.stop()

    # -----------------------------------------------------------------------
    # HANDLE RESPONSE
    # -----------------------------------------------------------------------

    status = result.get("status")

    # ---------------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------------

    if status == "completed":

        st.session_state.waiting_for_input = False

        answer = result.get(
            "response",
            "I was unable to generate a response.",
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    # ---------------------------------------------------------
    # HUMAN INPUT REQUIRED
    # ---------------------------------------------------------

    elif status == "input_required":

        st.session_state.waiting_for_input = True

        question = result.get(
            "question",
            "I need some additional information.",
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": question,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(question)

    # ---------------------------------------------------------
    # ERROR
    # ---------------------------------------------------------

    else:

        st.session_state.waiting_for_input = False

        error_message = result.get(
            "error",
            "Something went wrong.",
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )

        with st.chat_message("assistant"):
            st.error(error_message)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------

with st.sidebar:

    st.subheader("Session")

    st.code(
        st.session_state.session_id,
        language="text",
    )

    if st.button("New conversation"):

        st.session_state.session_id = (
            f"streamlit-{uuid.uuid4()}"
        )

        st.session_state.messages = []

        st.session_state.waiting_for_input = False

        st.rerun()