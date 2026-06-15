# Feature Specification: Orchestrator Agent

**Feature Branch**: `001-orchestrator`
**Created**: 2026-06-11
**Status**: Draft
**Input**: User description of the Orchestrator Agent as the backend entry point for research queries

## User Scenarios & Testing

### User Story 1 - Orchestrator Runs Full Research Pipeline (Priority: P1)

A user submits a research query via the FastAPI router. The Orchestrator receives the query, coordinates all 4 sub-agents in sequence, and returns the final structured report.

**Why this priority**: This is the core function — without it there is no research system.

**Independent Test**: Can be tested by simulating a user query through the internal API (bypassing the router). The orchestrator should invoke Web Search → Research → Analyzer → Reporter and return a complete report.

**Acceptance Scenarios**:

1. **Given** a valid `user_query` and `session_id`, **When** the Orchestrator `run()` is called, **Then** it returns a structured report with status updates for each agent.
2. **Given** the Orchestrator has completed the pipeline, **When** the Reporter Agent finishes, **Then** the final output contains a complete structured report.

---

### User Story 2 - Orchestrator Streams Agent Status Updates (Priority: P1)

During execution, the Orchestrator emits real-time status updates indicating which agent is currently running (Web Search, Research, Analyzer, Reporter).

**Why this priority**: The frontend must display live status to the user; without streaming the experience is degraded.

**Independent Test**: Can be tested by subscribing to the SSE stream emitted by the Orchestrator and verifying that each agent's start/complete event is received in order.

**Acceptance Scenarios**:

1. **Given** an Orchestrator run is in progress, **When** each sub-agent starts, **Then** an SSE event `{"agent": "web_search", "status": "running"}` is emitted.
2. **Given** a sub-agent completes, **When** it finishes, **Then** an SSE event `{"agent": "web_search", "status": "completed"}` is emitted.

---

### User Story 3 - Orchestrator Handles Sub-Agent Failure Gracefully (Priority: P2)

If any sub-agent fails (e.g., API timeout, invalid response), the Orchestrator captures the error, logs it, streams an error event, and continues with partial results where possible.

**Why this priority**: Robustness matters for production use; a single agent failure should not crash the entire research session.

**Independent Test**: Can be tested by making a sub-agent throw an exception and verifying the Orchestrator returns partial results with an error detail.

**Acceptance Scenarios**:

1. **Given** the Web Search Agent fails with a timeout, **When** the Orchestrator catches the exception, **Then** it streams `{"agent": "web_search", "status": "error", "detail": "..."}` and proceeds to Research Agent with empty search results.
2. **Given** a sub-agent returns invalid data, **When** validation fails, **Then** the error is logged and the pipeline continues with available data.

---

### User Story 4 - Orchestrator Rejects Invalid Input (Priority: P3)

The Orchestrator validates the incoming query before starting the pipeline. Empty or malformed queries are rejected immediately with a structured error.

**Why this priority**: Defensive input handling prevents wasted API calls and confusing downstream errors.

**Independent Test**: Can be tested by calling `run()` with an empty string and expecting an immediate error response.

**Acceptance Scenarios**:

1. **Given** an empty `user_query`, **When** the Orchestrator validates input, **Then** it returns `{"detail": "user_query must not be empty", "code": "INVALID_INPUT"}`.
2. **Given** a `user_query` exceeding 1000 characters, **When** validated, **Then** it returns `{"detail": "user_query exceeds maximum length of 1000", "code": "INVALID_INPUT"}`.

### Edge Cases

- What happens when all sub-agents fail? Orchestrator returns an error report with details from each failure.
- How does the system handle a session_id that already has an active run? Orchestrator queues or rejects duplicate session_id (policy TBD).
- What if the Groq API is unreachable? All sub-agent calls fail; Orchestrator reports infrastructure error.
- What if an agent takes longer than the configured timeout? Orchestrator cancels the agent and proceeds with available results.

## Requirements

### Functional Requirements

- **FR-001**: Orchestrator MUST accept `user_query: str` and `session_id: str` as input.
- **FR-002**: Orchestrator MUST execute sub-agents in the fixed order: Web Search → Research → Analyzer → Reporter.
- **FR-003**: Orchestrator MUST pass the output of each sub-agent as input to the next sub-agent in the chain.
- **FR-004**: Orchestrator MUST emit SSE status events for each agent lifecycle (running, completed, error).
- **FR-005**: Orchestrator MUST wrap every sub-agent call in try/except and handle failures gracefully.
- **FR-006**: Orchestrator MUST return the Reporter Agent's structured report as the final output.
- **FR-007**: Orchestrator MUST validate `user_query` is non-empty and within length limits before starting the pipeline.
- **FR-008**: Orchestrator MUST use the OpenAI Agents SDK handoff pattern to invoke sub-agents.
- **FR-009**: Orchestrator MUST run all agent calls asynchronously.
- **FR-010**: Orchestrator MUST NOT expose any public HTTP endpoint — called only internally from the FastAPI router.
- **FR-011**: Orchestrator MUST use the Groq API (base URL: `https://api.groq.com/openai/v1`, model: `llama-3.3-70b-versatile`) as the LLM provider.
- **FR-012**: Orchestrator MUST log every agent start, completion, and failure with timestamps.

### Key Entities

- **ResearchRequest**: Input to the Orchestrator containing `user_query` and `session_id`.
- **AgentResult**: Output from each sub-agent containing `agent_name`, `status`, `data` (varies by agent), and optional `error`.
- **StatusUpdate**: SSE event emitted for each agent containing `agent`, `status`, and optional `detail`.
- **FinalReport**: Structured report output from the Reporter Agent, returned as the final Orchestrator output.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Orchestrator completes a full 4-agent pipeline for any valid query in under 60 seconds (dependent on sub-agent performance).
- **SC-002**: Orchestrator correctly streams exactly 8 status events per successful run (start + complete for each of 4 agents).
- **SC-003**: Orchestrator handles all sub-agent failure scenarios without crashing — error response always returned.
- **SC-004**: Orchestrator rejects 100% of empty or over-length queries with a structured error before any API calls.
- **SC-005**: All Orchestrator code passes strict mypy type checking with no `Any` types.
