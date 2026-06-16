---
description: "Task list for Orchestrator Agent feature implementation"
---

# Tasks: Orchestrator Agent

**Input**: Design documents from `/specs/001-orchestrator/`
**Prerequisites**: plan.md, spec.md

**Tests**: Not requested in spec — no test tasks generated.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency configuration, and directory structure

- [X] T001 Create `backend/` directory structure with `agents/`, `models/`, `routers/` subdirectories and `__init__.py` files
- [X] T002 Create `backend/pyproject.toml` with dependencies: openai-agents, fastapi==0.115.0, uvicorn==0.30.0, python-dotenv==1.0.0, pydantic==2.7.0, httpx==0.27.0
- [X] T003 [P] Create `backend/.env.example` with `GROQ_API_KEY=` and `TAVILY_API_KEY=` placeholders
- [X] T004 Create `backend/.env` from `.env.example` for local development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared entities and types that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Pydantic models in `backend/models/research.py`: `ResearchRequest` (user_query, session_id), `AgentResult` (agent_name, status, data, error), `StatusUpdate` (agent, status, detail), `FinalReport` (structured report output)
- [X] T006 [P] Create `backend/models/__init__.py` exporting all model classes

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Orchestrator Runs Full Research Pipeline (Priority: P1) 🎯 MVP

**Goal**: Orchestrator accepts a research query, coordinates 4 sub-agents in sequence (Web Search → Research → Analyzer → Reporter), and returns a final structured report.

**Independent Test**: Call `Orchestrator.run(user_query="test", session_id="sess1")` and verify it invokes all 4 mock agents in order and returns a `FinalReport`.

- [X] T007 [US1] Create `backend/agents/orchestrator.py` with `Orchestrator` class that accepts `user_query` and `session_id`, with stub sub-agent calls (Web Search → Research → Analyzer → Reporter) and `run()` async method returning `FinalReport`
- [X] T008 [US1] Configure Groq API client in `backend/agents/orchestrator.py` with base URL `https://api.groq.com/openai/v1` and model `llama-3.3-70b-versatile` using OpenAI Agents SDK
- [X] T009 [US1] Implement mock/placeholder sub-agents in `backend/agents/orchestrator.py` that accept input and return dummy `AgentResult` data for testing
- [X] T010 [US1] Create `backend/routers/__init__.py` and `backend/routers/research.py` with FastAPI router and POST `/api/v1/research` endpoint that calls `Orchestrator.run()` and returns `FinalReport`
- [X] T011 [US1] Create `backend/main.py` with FastAPI app, CORS middleware, and router registration for `/api/v1/research`

**Checkpoint**: User Story 1 fully functional — POST `/api/v1/research` returns a structured report

---

## Phase 4: User Story 2 — Orchestrator Streams Agent Status Updates (Priority: P1)

**Goal**: During pipeline execution, the Orchestrator emits real-time SSE events indicating which agent is currently running, so the frontend can display live status.

**Independent Test**: Subscribe to the SSE stream and verify 8 events per run (start + complete for each of 4 agents) in correct order.

- [X] T012 [P] [US2] Add async event emission to `Orchestrator.run()` in `backend/agents/orchestrator.py` — emit `StatusUpdate` events (`{"agent": "...", "status": "running"}` and `{"agent": "...", "status": "completed"}`) before and after each sub-agent call via an asyncio.Queue or callback
- [X] T013 [US2] Add GET `/api/v1/research/stream/{session_id}` SSE streaming endpoint in `backend/routers/research.py` that subscribes to orchestrator events and yields SSE-formatted `StatusUpdate` messages

**Checkpoint**: User Stories 1 AND 2 both work — POST returns report, SSE streams status updates

---

## Phase 5: User Story 3 — Orchestrator Handles Sub-Agent Failure Gracefully (Priority: P2)

**Goal**: If any sub-agent fails, the Orchestrator captures the error, logs it, streams an error event, and continues with partial results.

**Independent Test**: Make a sub-agent throw an exception; verify Orchestrator returns partial results with error detail instead of crashing.

- [X] T014 [US3] Wrap each sub-agent call in `Orchestrator.run()` in `backend/agents/orchestrator.py` with try/except — on failure emit `{"agent": "...", "status": "error", "detail": "..."}` SSE event, log the error, and continue pipeline with available data
- [X] T015 [US3] Add structured logging with timestamps for every agent start, completion, and failure in `backend/agents/orchestrator.py`

**Checkpoint**: User Stories 1–3 functional — pipeline recovers from individual agent failures

---

## Phase 6: User Story 4 — Orchestrator Rejects Invalid Input (Priority: P3)

**Goal**: Orchestrator validates the incoming query before starting the pipeline, rejecting empty or over-length queries with a structured error.

**Independent Test**: Call `run()` with empty string or 1000+ char string; verify immediate error response without any API calls.

- [X] T016 [US4] Add input validation to `Orchestrator.run()` in `backend/agents/orchestrator.py`: reject empty `user_query` with `{"detail": "user_query must not be empty", "code": "INVALID_INPUT"}` and queries over 1000 chars with `{"detail": "user_query exceeds maximum length of 1000", "code": "INVALID_INPUT"}`

**Checkpoint**: All 4 user stories complete — invalid queries rejected before any sub-agent work

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T017 [P] Add `backend/.gitignore` for Python virtual environments, `.env`, `__pycache__`
- [ ] T018 Run mypy type checking on all `backend/` code — ensure no `Any` types per SC-005
- [ ] T019 Create `backend/README.md` with setup instructions and API docs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational — MVP entry point
- **User Story 2 (Phase 4)**: Depends on US1 (needs orchestrator running) — streaming builds on core pipeline
- **User Story 3 (Phase 5)**: Depends on US1 (modifies orchestrator.run()) — can be done after or alongside US2
- **User Story 4 (Phase 6)**: Depends on US1 (adds validation to orchestrator.run()) — can be done independently after US1
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — No dependencies on other stories
- **US2 (P1)**: Depends on US1 — adds SSE to orchestrator and streaming endpoint
- **US3 (P2)**: Depends on US1 — adds error wrapping to orchestrator pipeline
- **US4 (P3)**: Depends on US1 — adds input validation to orchestrator entry point

### Within Each User Story

- Models before services
- Core implementation before endpoints
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- US3 and US4 can be worked on in parallel after US1 is done (they modify different aspects of orchestrator.py)
- US2 depends on US1, so it's sequential

---

## Parallel Example: User Story 1

```bash
# Task: Create Pydantic models in backend/models/research.py
# Task: Create backend/models/__init__.py
```

## Parallel Example: User Story 3 & 4 (after US1 complete)

```bash
# Task: Add error handling to orchestrator.py (US3)
# Task: Add input validation to orchestrator.py (US4)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (core pipeline + POST endpoint)
4. **STOP and VALIDATE**: Test POST `/api/v1/research` returns structured report
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → POST endpoint works → Deploy/Demo (MVP!)
3. Add US2 → SSE streaming works → Deploy/Demo
4. Add US3 → Error recovery works → Deploy/Demo
5. Add US4 → Input validation works → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 + US2 (core pipeline + SSE)
   - Developer B: US3 (error handling — can integrate after US1)
   - Developer C: US4 (validation — can integrate after US1)
3. Stories integrate after US1 is stable

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US2 adds SSE to the same `orchestrator.py` as US1 — sequential execution required
- US3 and US4 modify `orchestrator.py` independently — can parallelize after US1
- No sub-agents (Web Search, Research, Analyzer, Reporter) — placeholder/mock only per plan
- Commit after each phase or logical group
