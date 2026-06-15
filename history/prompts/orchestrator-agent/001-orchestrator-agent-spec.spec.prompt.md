---
id: 001
title: orchestrator-agent-spec
stage: spec
date: 2026-06-11
surface: agent
model: deepseek-v4-flash-free
feature: orchestrator-agent
branch: main
user: developer
command: generate orchestrator agent spec
labels: [spec, orchestrator, agent-architecture]
links:
  spec: specs/orchestrator-agent.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-orchestrator/spec.md (created, was mistakenly at specs/orchestrator-agent.md — corrected)
  - history/prompts/orchestrator-agent/001-orchestrator-agent-spec.spec.prompt.md
tests: []
---

## Prompt

```text
generate a spec at specs/orchestrator-agent.md for the Orchestrator Agent.## What is Orchestrator Agent- It is the main entry point for all research queries in the backend- It receives user query from FastAPI router- It decides which sub-agents to call and in what order- It combines all sub-agent results into a single final output- It is NEVER directly exposed to frontend — only called internally## Inputs- user_query: str — the research question from user- session_id: str — unique id for this research session## What it does step by step1. Receives user query2. Plans which agents to run: Web Search → Research → Analyzer → Reporter3. Runs Web Search Agent first — gets raw search results4. Passes results to Research Agent — gets deep research5. Passes to Analyzer Agent — gets insights and patterns6. Passes to Reporter Agent — gets final report7. Streams each agent status update back to FastAPI via SSE8. Returns final combined result## Outputs- Streams status updates: which agent is running right now- Final output: structured report from Reporter Agent## Agent Flow (FIXED order)Web Search Agent → Research Agent → Analyzer Agent → Reporter Agent## Tech Details- Uses OpenAI Agents SDK- Groq API as LLM (llama-3.3-70b-versatile)- Base URL: https://api.groq.com/openai/v1- Async execution- Handoffs to sub-agents using OpenAI Agents SDK handoff pattern## File location- Spec file: specs/orchestrator-agent.md- Future implementation will be at: backend/agents/orchestrator.pyWrite this as a clean structured spec file in markdown. This spec will be used to create plan and tasks later.
```

## Response snapshot

Created the Orchestrator Agent spec at `specs/orchestrator-agent.md`. The spec follows the spec-template.md structure with 4 user stories (prioritized P1–P3), edge cases, 12 functional requirements, key entities (ResearchRequest, AgentResult, StatusUpdate, FinalReport), and 5 measurable success criteria. The spec covers core pipeline execution, SSE streaming, graceful error handling, and input validation.

## Outcome

- ✅ Impact: Created initial Orchestrator Agent specification covering all described requirements
- 🧪 Tests: N/A (spec document)
- 📁 Files: specs/orchestrator-agent.md (created), history/prompts/orchestrator-agent/001-orchestrator-agent-spec.spec.prompt.md (created)
- 🔁 Next prompts: Plan generation for Orchestrator Agent, tasks breakdown
- 🧠 Reflection: Spec covers all user-provided details. User stories are independently testable. Added edge cases and validation requirements not explicitly requested but necessary for robustness.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): spec-template
- Next experiment (smallest change to try): N/A
