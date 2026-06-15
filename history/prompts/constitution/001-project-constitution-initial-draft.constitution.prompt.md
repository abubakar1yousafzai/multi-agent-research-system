---
id: 001
title: project-constitution-initial-draft
stage: constitution
date: 2026-06-11
surface: agent
model: deepseek-v4-flash-free
feature: none
branch: main
user: developer
command: constitution update
labels: [constitution, governance, principles]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-project-constitution-initial-draft.constitution.prompt.md
tests: []
---

## Prompt

```text
You are an expert software generate a constitution for my project with the following details:

## Project Identity
- Name: Multi-Agent Research System
- Purpose: A web-based AI research assistant that searches the web, performs deep research, analyzes data, and generates reports
- Users: Researchers, students, professionals who need quick deep research

## Tech Stack (FIXED — never change these)
- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python 3.11+
- Agent Framework: OpenAI Agents SDK
- LLM Provider: Groq API (model: llama-3.3-70b-versatile)
- Web Search: Tavily API
- Package Manager Frontend: pnpm
- Package Manager Backend: uv
- Communication: REST + SSE (Server-Sent Events) for streaming

## Agent Architecture (FIXED)
There are exactly 5 agents:
1. Orchestrator Agent - routes user query to sub-agents, combines results. NEVER exposed to frontend.
2. Web Search Agent - searches web using Tavily API
3. Research Agent - performs deep multi-query research, compares sources
4. Analyzer Agent - processes data, finds patterns and insights
5. Reporter Agent - generates final structured report

Frontend shows only agents 2, 3, 4, 5 with live status updates.

## Project Folder Structure (FIXED)
project-root/
├── backend/
│   ├── agents/         # all agent files here
│   ├── routers/        # FastAPI route files
│   ├── models/         # Pydantic models
│   ├── tools/          # agent tools (search, etc)
│   ├── services/       # business logic
│   ├── main.py
│   └── pyproject.toml
├── frontend/
│   ├── app/            # Next.js 15 App Router
│   ├── components/     # reusable components
│   ├── lib/            # utilities, api calls
│   ├── hooks/          # custom React hooks
│   ├── types/          # TypeScript types
│   └── package.json

## Python Coding Standards
- Type hints are MANDATORY on every function
- Use async/await everywhere - no blocking code
- Pydantic models for all request/response data
- Every function must have a docstring
- Environment variables ONLY from .env file via python-dotenv
- Error handling with try/except on every agent call

## TypeScript Coding Standards
- Strict mode ON always
- `any` type is FORBIDDEN
- Every component must have typed props
- API calls only through lib/api.ts
- No inline styles - Tailwind classes only

## API Rules
- Backend runs on port 8000
- Frontend runs on port 3000
- CORS must be configured for localhost:3000
- All agent responses stream via SSE
- All endpoints follow REST conventions
- API prefix: /api/v1

## Absolute Rules (NEVER break these)
- No hardcoded API keys anywhere
- No synchronous blocking calls in agents
- Orchestrator is never directly called from frontend
- Each agent has single responsibility only
- No `any` type in TypeScript
- All secrets in .env files only

Write this as a clean, well-structured constitution with proper markdown formatting. This file will be referenced by all future specs, plans and tasks in this project.
```

## Response snapshot

Filled the constitution template with 6 named principles derived from the user's fixed requirements:
- I. Tech Stack Immutability
- II. Agent Architecture Integrity
- III. Project Structure Compliance
- IV. Coding Standards (Python & TypeScript)
- V. Security & Configuration Isolation
- VI. API & Communication Protocol

Added fully populated sections for Error Handling & Observability, Development Workflow, and Governance. Version set to 1.0.0 (initial draft), ratified 2026-06-11. Sync Impact Report prepended as HTML comment. No template changes required for plan-template.md, spec-template.md, or tasks-template.md.

## Outcome

- ✅ Impact: Created first version of project constitution with all placeholders replaced
- 🧪 Tests: N/A (constitution document)
- 📁 Files: .specify/memory/constitution.md (created), history/prompts/constitution/001-project-constitution-initial-draft.constitution.prompt.md (created)
- 🔁 Next prompts: Feature specifications, plan creation, ADR documentation
- 🧠 Reflection: All user-provided constraints mapped directly to constitution principles. Template structure was well-suited for this project.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): constitution-template
- Next experiment (smallest change to try): N/A
