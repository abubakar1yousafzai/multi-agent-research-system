---
id: 007
title: orchestrator-phase6-us4
stage: green
date: 2026-06-15
surface: cli
model: deepseek-v4-flash-free
feature: orchestrator
branch: 001-orchestrator
user: abubakar
command: /sp.implement (Phase 6 only)
labels: [green, orchestrator, us4, validation]
links:
  spec: specs/001-orchestrator/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - backend/agents/orchestrator.py
  - backend/routers/research.py
  - specs/001-orchestrator/tasks.md
tests:
  - N/A
---

## Prompt

```
only implement phase 6
```

## Response snapshot

Implemented Phase 6 — User Story 4 (Orchestrator Rejects Invalid Input):

- T016: Added `InvalidInputError` exception class in `backend/agents/orchestrator.py`; `run()` now validates `user_query` is non-empty (with strip) and ≤ 1000 chars before any pipeline work, raising `InvalidInputError` with structured `detail` and `code="INVALID_INPUT"`
- Updated POST `/api/v1/research` in `routers/research.py` to catch `InvalidInputError` and return 422 with `{"detail": "...", "code": "INVALID_INPUT"}`

T016 marked [X] in tasks.md.

## Outcome

- ✅ Impact: US4 input validation complete — empty/over-length queries rejected before any sub-agent calls with structured 422 error response
- 🧪 Tests: N/A
- 📁 Files: 2 modified, 1 updated
- 🔁 Next prompts: Phase 7 (polish — .gitignore, type checking, README)
- 🧠 Reflection: `ResearchRequest` model already has Pydantic `min_length`/`max_length` validation, but T016 adds defense-in-depth at the orchestrator layer as specified

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
