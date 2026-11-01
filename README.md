# Enterprise Customer Support Agent

An AI-powered customer support agent built with **LangGraph**, **Gemini**, and **Agentic RAG**. It can answer policy-related questions, retrieve customer information, investigate transactions and tickets, and create support tickets using tools.

This project is a work in progress. Some integrations and evaluation capabilities are planned.

## Features

- **Agentic workflow:** Uses LangGraph to manage the conversation and tool-calling flow.
- **Policy-based RAG:** Retrieves relevant information from support policy documents.
- **Vector search and reranking:** Uses Qdrant for vector storage, BGE embeddings for retrieval, and a cross-encoder reranker to refine results.
- **Customer data lookup:** Retrieves customer, subscription, transaction, and ticket information from the current JSON-based data store.
- **Ticket creation:** Allows the agent to create support tickets through a tool.
- **Human-in-the-loop:** Pauses the workflow when information or confirmation is needed and resumes after the user responds.
- **API and chat UI:** Exposes the agent through FastAPI and provides a Streamlit chat interface.

## Tech Stack

- **Language:** Python
- **Agent orchestration:** LangGraph, LangChain
- **LLM:** Google Gemini (Gemini 3.5 Flash Lite)
- **RAG:** Sentence Transformers, BAAI/bge-small-en-v1.5
- **Reranking:** BAAI/bge-reranker-base
- **Vector database:** Qdrant (local persistent storage)
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Data validation:** Pydantic

## Project Structure

```text
.
├── app/
│   ├── main.py                 # FastAPI application
│   ├── schemas.py              # Request and response schemas
│   └── streamlit_app.py        # Streamlit chat interface
├── data/
│   ├── customer_data/          # Sample customer and business records
│   ├── policies/               # Support policy documents
│   └── vector_db/              # Local Qdrant storage
├── src/
│   ├── agent/                  # LangGraph agent, state, tools and nodes
│   ├── database/               # JSON data store and repositories
│   ├── models/                 # Pydantic data models
│   ├── rag/                    # Chunking, ingestion, retrieval and reranking
│   └── tools/                  # Customer, subscription, ticket and transaction tools
├── requirements.txt
└── README.md
```

## How It Works

1. The user sends a query through the Streamlit interface.
2. The FastAPI backend passes the message to the LangGraph workflow.
3. The agent decides whether it needs policy information, customer data, transaction details, or ticket information.
4. It calls the relevant tools and can use multiple tools to investigate a request.
5. For policy questions, the RAG pipeline retrieves relevant document chunks from Qdrant and reranks them.
6. If required information is missing, the workflow pauses and asks the user for clarification.
7. The agent uses the available information to provide a response or perform a supported action, such as creating a support ticket.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ramninderSingh/Custome-support-agent.git
cd Custome-support-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\\Scripts\\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Keep your API key private. Do not commit the `.env` file to the repository.

### 5. Ingest the support policies

Run the ingestion script to chunk the policy documents, generate embeddings, and store them in the local Qdrant database:

```bash
python -m src.rag.ingestion
```

Run ingestion again whenever the policy documents need to be added or refreshed.

## Running the Application

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

In a second terminal, start the Streamlit interface:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit interface connects to the API at `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks whether the API is running |
| POST | `/chat` | Sends a message to the agent |
| POST | `/chat/resume` | Resumes a conversation after human input |

A conversation uses a `session_id` to maintain its LangGraph state.

## Future Integrations

The project is actively being developed. Planned improvements include:

- [ ] **SQL Server integration:** Replace the current JSON-based customer data storage with Microsoft SQL Server. Add database connectivity and repository support for customer, subscription, transaction, and ticket records.
- [ ] **Evaluation pipeline:** Build a repeatable evaluation pipeline for the RAG and agent workflows. Include retrieval metrics such as Recall@K, Precision@K and MRR, alongside answer quality, faithfulness, tool-selection accuracy, and end-to-end task success.
- [ ] **Improved observability:** Add structured logging and tracing for agent steps, tool calls, retrieval results, and failures.
- [ ] **Expanded integrations:** Connect additional enterprise systems and support workflows as needed.

## Current Status

This is an ongoing project. The core agent workflow, policy retrieval pipeline, sample data tools, FastAPI endpoints, and Streamlit interface are present. The project is still evolving, and the planned integrations above are not yet implemented.
