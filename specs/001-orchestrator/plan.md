# Orchestrator Agent Implementation Plan

## Overview
This plan breaks down exactly what files to create, what dependencies to install, and what the folder structure will look like for the Orchestrator Agent.

---

## Files to Create

| # | File Path | Purpose |
|---|-----------|---------|
| 1 | `backend/agents/orchestrator.py` | Main Orchestrator Agent class with handoff logic to sub-agents and async execution |
| 2 | `backend/agents/__init__.py` | Empty init file for agents module |
| 3 | `backend/models/research.py` | Pydantic models for request/response: ResearchQuery (user_query, session_id), AgentStatus (agent_name, status, message), ResearchResult (final output) |
| 4 | `backend/routers/research.py` | FastAPI router with POST `/api/v1/research` endpoint and SSE streaming endpoint GET `/api/v1/research/stream/{session_id}` |
| 5 | `backend/main.py` | FastAPI app setup with CORS configuration and router registration |
| 6 | `backend/pyproject.toml` | All Python dependencies with versions |
| 7 | `backend/.env.example` | Environment variable template: GROQ_API_KEY=, TAVILY_API_KEY= |

---

## Dependencies to Install (backend)

| Package | Version |
|---------|---------|
| openai-agents | latest |
| fastapi | 0.115.0 |
| uvicorn | 0.30.0 |
| python-dotenv | 1.0.0 |
| pydantic | 2.7.0 |
| httpx | 0.27.0 |

---

## Folder Structure After Implementation

```
backend/
├── agents/
│   ├── __init__.py
│   └── orchestrator.py
├── models/
│   ├── __init__.py
│   └── research.py
├── routers/
│   ├── __init__.py
│   └── research.py
├── main.py
├── pyproject.toml
└── .env.example
```

---

## Dependencies Between Files

- `orchestrator.py` depends on → `models/research.py`
- `routers/research.py` depends on → `orchestrator.py`, `models/research.py`
- `main.py` depends on → `routers/research.py`

---

## What is NOT in This Plan

- No sub-agents (Web Search, Research, Analyzer, Reporter) — they come later
- No frontend — separate plan
- Sub-agents will be placeholder/mock for now so orchestrator can be tested

---

## Next Steps

This plan will be used to create tasks in the next step.