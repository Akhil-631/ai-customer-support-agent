# 🤖 AI Customer Support Assistant

An enterprise-oriented AI Customer Support Assistant built with **Python, LangGraph, FastAPI, React, PostgreSQL, RAG, and Large Language Models (LLMs)**.

The system combines LLM-powered intent classification, controlled business tool execution, retrieval-augmented generation, persistent database operations, and human-in-the-loop workflows into a modular customer support architecture.

The project evolved from a simpler V1 Streamlit application into a multi-layer V2 architecture designed around **agent orchestration, backend APIs, a customer-facing interface, and a company operations portal**.

---

## 🚀 Key Features

### 🧠 AI Agent

- LLM-powered intent classification
- Structured intent extraction using Pydantic
- Confidence-based routing
- Request validation
- Order ID extraction and validation
- Conversational request handling

### 🛠️ Business Tool Execution

- Order status lookup
- Delivery status lookup
- Refund status lookup
- Order cancellation
- Human support escalation
- Controlled tool execution through the agent workflow

### 🔎 Retrieval-Augmented Generation

- Knowledge-base ingestion
- Text chunking
- Sentence Transformer embeddings
- FAISS vector similarity search
- Context retrieval for general customer questions
- RAG responses generated using retrieved knowledge

### 🔄 LangGraph Agent Orchestration

The agent workflow is implemented using **LangGraph**.

It supports:

- Conditional routing
- Tool execution
- Error handling
- Human-in-the-loop interrupts
- Approval / rejection / escalation branches
- Final response generation

### 👨‍💼 Human-in-the-Loop

High-impact or ambiguous requests can be paused for human review.

The system provides:

- Persistent human review requests
- Company-side review queue
- Approve
- Reject
- Escalate
- Backend state persistence
- Customer-side status updates

### 🗄️ PostgreSQL

The backend uses PostgreSQL for persistent application data including:

- Orders
- Refunds
- Support tickets
- Human review requests

Database access is isolated through a repository layer.

### 🌐 Full-Stack Application

The V2 application contains:

- **FastAPI backend**
- **React/Vite customer interface**
- **Company operations portal**
- **Assistant UI**
- **PostgreSQL persistence**

---

# 🏗️ System Architecture

```
                         ┌──────────────────────────┐
                         │      React Frontend      │
                         │                          │
                         │  Customer Portal         │
                         │  Company Portal          │
                         └────────────┬─────────────┘
                                      │
                                      │ HTTP / JSON
                                      ▼
                         ┌──────────────────────────┐
                         │       FastAPI API        │
                         │                          │
                         │  /chat                   │
                         │  /human-review           │
                         │  /human-reviews          │
                         │  /conversation/{id}      │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      LangGraph Agent     │
                         │                          │
                         │  Intent Classification   │
                         │  Request Validation      │
                         │  Conditional Routing     │
                         │  Tool Execution          │
                         │  Human Review             │
                         │  Response Generation     │
                         └───────┬──────────┬───────┘
                                 │          │
                    ┌────────────┘          └──────────────┐
                    ▼                                      ▼
          ┌──────────────────┐                    ┌──────────────────┐
          │   Business Tools │                    │       RAG        │
          │                  │                    │                  │
          │ Order Status     │                    │ Knowledge Base   │
          │ Delivery Status  │                    │ Embeddings       │
          │ Refund Status    │                    │ FAISS Search     │
          │ Cancel Order     │                    │ Context Retrieval│
          │ Human Support    │                    └──────────────────┘
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Repository Layer │
          │                  │
          │ SQLAlchemy       │
          │ Database Queries │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │   PostgreSQL     │
          │                  │
          │ Orders           │
          │ Refunds          │
          │ Support Tickets  │
          │ Human Reviews    │
          └──────────────────┘
```

---

# 🔄 LangGraph Workflow

The core agent workflow is implemented as a stateful LangGraph.

```
START
  │
  ▼
classify_intent
  │
  ├── conversational ───────────────► conversation ──► END
  │
  ├── general_query ────────────────► RAG ──────────► END
  │
  ├── requires_human ───────────────► human_review
  │
  └── business request
          │
          ▼
    validate_request
          │
          ├── request_information ─► generate_response
          │
          ├── human_review ─────────► human_review
          │
          └── continue
                │
                ▼
          execute_tool
                │
                ├── success ───────► tool_success
                │
                └── error ─────────► error handling
                                         │
                                         ▼
                                  generate_response
                                         │
                                         ▼
                                        END
```

### Human Review Branch

```text
human_review
     │
     ├── approve ──► human_approved ──► execute_approved_cancel
     │                                      │
     │                                      ▼
     │                              generate_response
     │
     ├── reject ───► human_rejected ──► generate_response
     │
     └── escalate ► human_escalated ─► generate_response
```

The actual graph can also be visualized locally using:

```bash
python visualize_graph.py
```

This generates an interactive browser-based LangGraph visualization from the actual graph definition.

---

# 🔎 RAG Architecture

General customer questions are routed to the RAG pipeline instead of business tools.

```
Customer Question
       │
       ▼
Intent Classification
       │
       ▼
   General Query
       │
       ▼
Knowledge Base
       │
       ▼
Text Chunking
       │
       ▼
Sentence Transformer
Embeddings
       │
       ▼
FAISS
Vector Similarity Search
       │
       ▼
Relevant Context
       │
       ▼
LLM
       │
       ▼
Customer Response
```

The current implementation uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- FAISS vector search

---

# 👨‍💼 Human-in-the-Loop Workflow

Certain requests should not be executed automatically.

For example, a cancellation request can be routed to human review when the workflow determines that human intervention is required.

```
Customer Request
       │
       ▼
AI Agent
       │
       ▼
Human Review Required
       │
       ▼
Persistent Review Request
       │
       ▼
Company Review Queue
       │
       ├── Approve
       │
       ├── Reject
       │
       └── Escalate
       │
       ▼
LangGraph Resumes
       │
       ▼
Final Customer Response
```

Human review requests are persisted in PostgreSQL so the company portal can retrieve pending requests independently of the customer interface.

---

# 🌐 Application Interfaces

## Customer Portal

The customer-facing application provides:

- Conversational interaction with the AI assistant
- Order-related requests
- Delivery queries
- Refund queries
- Cancellation requests
- General knowledge-base questions
- Human review status updates

## Company Portal

The company-facing workspace provides:

- Human Review Queue
- Pending review requests
- Request details
- Approve action
- Reject action
- Escalate action

Other company workspace areas are intentionally presented as future integration points rather than simulated live systems.

---

# 🔌 Backend API

The FastAPI backend currently exposes the following core endpoints:

| Endpoint | Purpose |
|---|---|
| `POST /chat` | Process a customer request |
| `POST /human-review` | Submit a human review decision |
| `GET /human-reviews` | Retrieve pending human review requests |
| `GET /conversation/{conversation_id}` | Retrieve conversation workflow state |

The backend maintains a conversation-specific LangGraph state using a unique conversation ID.

---

# 🗄️ Database Architecture

Database operations are separated from the AI agent through a repository layer.

```text
LangGraph Agent
      │
      ▼
Business Tools
      │
      ▼
Repository Layer
      │
      ▼
SQLAlchemy
      │
      ▼
PostgreSQL
```

### Current database entities

- `orders`
- `refunds`
- `support_tickets`
- `human_review_requests`

The AI agent does not directly manipulate the database.

Business operations are performed through controlled tools, which call repository functions.

---

# 📂 Project Structure

```text
ai-customer-support-agent/
│
├── agent.py
├── graph.py
├── state.py
├── tools.py
├── api.py
├── llm_client.py
├── prompts.py
├── rag.py
├── visualize_graph.py
│
├── database/
│   └── repository.py
│
├── knowledge_base/
│   └── ...
│
├── data/
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── company/
│   │   └── runtime/
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
│   └── ...
│
├── integrations/
│   └── ...
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Language | Python, JavaScript |
| LLM | Groq API / OpenAI-compatible SDK |
| Agent Framework | LangGraph |
| AI Validation | Pydantic |
| RAG | Sentence Transformers, FAISS |
| Backend | FastAPI |
| Frontend | React, Vite |
| Assistant UI | Assistant UI |
| Database | PostgreSQL |
| Database Access | SQLAlchemy |
| Database Driver | psycopg2 |
| Vector Search | FAISS |
| Embeddings | `all-MiniLM-L6-v2` |
| API Communication | REST / JSON |

---

# 💬 Example Queries

### 📦 Order Status

```text
What is the status of order CA-2017-152156?
```

### 🚚 Delivery Status

```text
Where is my order CA-2017-152156?
```

### 💰 Refund Status

```text
What is the refund status of order CA-2017-152156?
```

### ❌ Cancel Order

```text
Cancel my order CA-2017-152156
```

Depending on the workflow state, the cancellation request may be executed automatically or routed to human review.

### 👨‍💼 Human Support

```text
My payment was deducted twice.
```

### 🔎 Knowledge Base

```text
What is your return policy?
```

---

# 🧠 Agent Decision-Making

The system separates **reasoning from execution**.

The LLM is responsible for understanding the user's request and producing a structured intent.

The agent then validates the request before deciding what should happen next.

```text
User Request
     │
     ▼
LLM Classification
     │
     ▼
Structured Intent
     │
     ▼
Validation
     │
     ├── Missing information
     │        │
     │        ▼
     │   Ask customer
     │
     ├── General question
     │        │
     │        ▼
     │       RAG
     │
     ├── Human required
     │        │
     │        ▼
     │   Human Review
     │
     └── Valid business request
              │
              ▼
         Business Tool
```

This prevents the LLM from directly performing database operations.

---

# 🏛️ Design Principles

### Separation of Responsibilities

The system separates:

- LLM reasoning
- Agent orchestration
- Business logic
- Database access
- API communication
- Frontend presentation

### Controlled Tool Execution

The AI agent does not directly modify application data.

Business operations are exposed through controlled tools.

### Repository Pattern

Database operations are isolated inside the repository layer.

This keeps database implementation separate from agent and business logic.

### Stateful Agent Workflow

LangGraph maintains the workflow state across multi-step interactions, including interrupted human-review workflows.

### Human Oversight

Requests that require human intervention can pause the agent workflow instead of being executed automatically.

### Real Backend State

The human review queue is backed by PostgreSQL rather than static frontend demo data.

---

# 🧪 Validation & Testing

The V2 workflow was tested across the following scenarios:

- Conversational requests
- General RAG questions
- Missing order IDs
- Valid order status requests
- Delivery status requests
- Refund status requests
- Invalid order IDs
- Cancellation requiring human review
- Human approval
- Human rejection
- Human escalation
- Empty review queue
- Live review queue
- Portal navigation
- Conversation isolation
- Browser refresh
- Backend restart

The human-review workflow was also tested end-to-end across:

```
Customer
   ↓
FastAPI
   ↓
LangGraph interrupt
   ↓
PostgreSQL review request
   ↓
Company Portal
   ↓
Human decision
   ↓
LangGraph resume
   ↓
Customer response
```

---

# 🔐 Configuration

Create a `.env` file based on `.env.example`.

Example:

```
GROQ_API_KEY=your_api_key

DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enterprise_ai_agent
```

Do not commit `.env` or API credentials to the repository.

---

# 🚀 Getting Started

## 1. Clone the repository

```
git clone <your-github-repository-url>
cd ai-customer-support-agent
```

## 2. Create a Python virtual environment

```
python -m venv .venv
```

Activate it on Windows:

```
.venv\Scripts\Activate.ps1
```

## 3. Install Python dependencies

```
pip install -r requirements.txt
```

## 4. Configure PostgreSQL

Create the required PostgreSQL database and configure the connection values in `.env`.

The application expects the required database tables to be available.

## 5. Configure environment variables

Create `.env` from `.env.example` and add your API/database configuration.

## 6. Start the FastAPI backend

```
uvicorn api:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

## 7. Start the React frontend

Open another terminal:

```
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```
http://localhost:5173
```

## 8. Open the application

Customer portal:

```
http://localhost:5173
```

Company portal:

```
http://localhost:5173/company
```

---

# 🖼️ Application Screenshots

## Customer Portal

![Customer Portal](screenshots/Customer%20Portal.png)

## Customer Support Response

![Customer Support Response](screenshots/Customer%20Support%20Response.png)

## RAG Response

![RAG Response](screenshots/RAG%20Response.png)

## Human Review Pending

![Human Review Pending](screenshots/Human%20Review%20Pending.png)

## Company Human Review Queue

![Company Human Review Queue](screenshots/Company%20Human%20Review%20queue.png)

## LangGraph Visualization

![LangGraph Visualization](screenshots/LangGraph%20Visualisation.png)

---

# 🔭 Future Integration Opportunities

The current V2 architecture intentionally leaves several areas as integration boundaries rather than simulating them.

Potential future integrations include:

- Existing CRM systems
- Contact-center platforms
- Real-time human-agent conversations
- Authentication and role-based access control
- Production observability and logging
- Cloud deployment
- Automated test suites
- Additional business tools
- External enterprise systems
- API/MCP-based enterprise integrations

The architecture is designed so that the AI assistant can eventually connect to existing enterprise customer-support infrastructure instead of replacing the entire CRM/contact-center system.

---

# 📈 Project Evolution

## V1

The initial version demonstrated:

- LLM intent classification
- Tool calling
- PostgreSQL integration
- Streamlit interface
- Human support escalation

## V2

The project was expanded into a more complete agent architecture with:

- LangGraph orchestration
- Stateful workflows
- RAG
- FAISS vector search
- FastAPI backend
- React frontend
- Company operations portal
- Persistent human-review workflow
- PostgreSQL-backed review queue
- Human-in-the-loop interrupts
- Conversation state management

The goal of V2 was not simply to add more UI features, but to demonstrate how an AI customer-support system can be structured as a modular backend agent rather than a single LLM-powered application.

---

# 👨‍💻 Author

**Akhil Marada**

B.Tech — Mechanical Engineering

This project was developed as a portfolio project to explore and demonstrate:

- AI Agent Architecture
- LangGraph
- RAG
- LLM-based decision making
- Tool calling
- Human-in-the-loop workflows
- FastAPI
- React
- PostgreSQL
- Enterprise-oriented AI system design
