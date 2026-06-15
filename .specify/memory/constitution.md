<!--
  SYNC IMPACT REPORT
  Version change: (template) → 1.0.0
  Modified principles: 6 placeholders filled with named principles
    - [PRINCIPLE_1_NAME] → I. Tech Stack Immutability
    - [PRINCIPLE_2_NAME] → II. Agent Architecture Integrity
    - [PRINCIPLE_3_NAME] → III. Project Structure Compliance
    - [PRINCIPLE_4_NAME] → IV. Coding Standards (Python & TypeScript)
    - [PRINCIPLE_5_NAME] → V. Security & Configuration Isolation
    - [PRINCIPLE_6_NAME] → VI. API & Communication Protocol
  Added sections:
    - Error Handling & Observability (filled from [SECTION_2_NAME])
    - Development Workflow (filled from [SECTION_3_NAME])
    - Governance fully populated (was placeholder)
  Removed sections: N/A
  Templates requiring updates:
    - plan-template.md: ✅ No changes needed (Constitution Check section is placeholder-based)
    - spec-template.md: ✅ No changes needed
    - tasks-template.md: ✅ No changes needed
    - adr-template.md: ✅ No changes needed
    - checklist-template.md: ✅ No changes needed
    - agent-file-template.md: ✅ No changes needed
  Follow-up TODOs: None -- 2026-06-11
-->

# Multi-Agent Research System Constitution

## Core Principles

### I. Tech Stack Immutability

The following technologies are FIXED and MUST NOT be changed without a MAJOR
constitution amendment:

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, Python 3.11+
- **Agent Framework**: OpenAI Agents SDK
- **LLM Provider**: Groq API (model: llama-3.3-70b-versatile)
- **Web Search**: Tavily API
- **Package Manager (Frontend)**: pnpm
- **Package Manager (Backend)**: uv
- **Communication**: REST + SSE (Server-Sent Events)

**Rationale**: The stack was chosen for compatibility, performance, and
maintainability across the full pipeline. Changing any component risks breaking
the integrated agent architecture and MUST be evaluated holistically.

### II. Agent Architecture Integrity

The system MUST implement exactly 5 agents with strict boundary rules:

1. **Orchestrator Agent** — routes user queries to sub-agents, combines results.
   MUST NEVER be exposed to the frontend.
2. **Web Search Agent** — searches the web using Tavily API.
3. **Research Agent** — performs deep multi-query research, compares sources.
4. **Analyzer Agent** — processes data, finds patterns and insights.
5. **Reporter Agent** — generates the final structured report.

Frontend shows ONLY agents 2–5 with live status updates via SSE.

**Rules**:
- The Orchestrator MUST NOT have a publicly routable endpoint.
- Each agent MUST have a single responsibility only.
- No agent may call another agent directly; all inter-agent routing goes through
  the Orchestrator.
- No synchronous blocking calls allowed in any agent.

**Rationale**: Clear separation of concerns prevents spaghetti architecture,
enables independent testing, and allows parallel development of each agent.

### III. Project Structure Compliance

All source code MUST follow the prescribed folder structure:

```
project-root/
├── backend/
│   ├── agents/         # Agent files
│   ├── routers/        # FastAPI route files
│   ├── models/         # Pydantic models
│   ├── tools/          # Agent tools (search, etc.)
│   ├── services/       # Business logic
│   ├── main.py
│   └── pyproject.toml
├── frontend/
│   ├── app/            # Next.js 15 App Router
│   ├── components/     # Reusable components
│   ├── lib/            # Utilities, API calls
│   ├── hooks/          # Custom React hooks
│   ├── types/          # TypeScript types
│   └── package.json
```

**Rationale**: Consistent structure reduces cognitive load, enables automated
tooling, and ensures every developer knows exactly where to find or place code.

### IV. Coding Standards (Python & TypeScript)

**Python (Backend)**:
- Type hints are MANDATORY on every function signature.
- All I/O and agent calls MUST use `async/await`. No blocking code permitted.
- Pydantic models MUST be used for all request/response data.
- Every function MUST have a docstring describing purpose, parameters, and
  return value.
- Environment variables MUST be loaded ONLY from `.env` via `python-dotenv`.
- Every agent call MUST be wrapped in `try`/`except` with structured error
  responses.

**TypeScript (Frontend)**:
- `strict` mode MUST be enabled in `tsconfig.json`.
- The `any` type is FORBIDDEN. Use `unknown` with type guards.
- Every component MUST have typed props (via `interface` or `type` alias).
- API calls MUST go exclusively through `lib/api.ts`.
- No inline styles — Tailwind CSS classes only.

**Rationale**: Type safety and consistent style prevent entire categories of
bugs and make the codebase self-documenting.

### V. Security & Configuration Isolation

- No hardcoded API keys, secrets, or tokens in source code.
- All secrets MUST reside in `.env` files in the project root.
- `.env` MUST be listed in `.gitignore` and MUST NEVER be committed.
- Backend reads env vars through `python-dotenv` only (loaded at startup).
- Frontend uses `NEXT_PUBLIC_*` prefix for client-safe variables; all other
  secrets stay server-side only.
- Both `.env` and `.env.example` MUST document every required variable with a
  description.

**Rationale**: Preventing secret exposure is the highest-priority security
requirement. Environment-based configuration also enables different deployments
without code changes.

### VI. API & Communication Protocol

- Backend runs on port `8000`.
- Frontend runs on port `3000`.
- CORS MUST be configured to allow only `localhost:3000`.
- All agent responses MUST stream via Server-Sent Events (SSE).
- All endpoints MUST follow REST conventions (resource nouns, HTTP verbs,
  standard status codes).
- API prefix: `/api/v1`.
- Orchestrator is NEVER directly callable from the frontend.

**Rationale**: A consistent API surface simplifies frontend integration,
enables independent development, and allows standard tooling (OpenAPI, client
generators).

## Error Handling & Observability

- Every agent call MUST be wrapped in `try`/`except` that returns a structured
  error response to the caller.
- SSE event stream MUST include error events (`event: error`) with structured
  JSON payloads containing `detail` and `code` fields.
- The Orchestrator MUST handle sub-agent failures gracefully — partial results
  SHOULD be returned rather than failing the entire request.
- All API error responses MUST follow a consistent shape:
  ```json
  { "detail": "Human-readable message", "code": "ERROR_CODE" }
  ```
- Structured logging MUST be used throughout the backend (stdout is acceptable
  for development).

**Rationale**: Users receive meaningful feedback when things go wrong, and
developers can diagnose issues without tracing through opaque failures.

## Development Workflow

- Frontend and backend are developed independently with separate dev servers
  (`pnpm dev` on `:3000`, `uv run uvicorn` on `:8000`).
- Backend changes MUST be tested with `pytest` before frontend integration.
- Frontend changes MUST pass `tsc --noEmit` (type checking) before commit.
- All new features MUST start with a specification in `.specify/`.
- Every feature plan MUST include a "Constitution Check" section verifying
  alignment with all six principles.
- No feature may bypass a principle without a documented exception in the
  feature plan, reviewed and approved during planning.

**Rationale**: Structured workflow prevents regressions, ensures consistency,
and makes the development process predictable for all contributors.

## Governance

This constitution is the supreme authority for all project decisions. All other
practices, guidelines, and conventions are subordinate.

### Amendment Procedure
1. A proposal MUST be documented, including rationale and impact analysis.
2. The proposal MUST undergo team review.
3. If approved, a migration plan MUST accompany the change.
4. The constitution MUST be updated and version-bumped atomically with the
   change.

### Versioning Policy
- **MAJOR** (1.x.x): Backward-incompatible principle removal or redefinition.
- **MINOR** (x.1.x): New principle or materially expanded guidance.
- **PATCH** (x.x.1): Clarifications, wording, typo fixes, non-semantic
  refinements.

### Compliance Review
- Every feature plan MUST include a "Constitution Check" section.
- An annual review of all principles MUST be conducted for continued relevance.
- Constitution violations MUST be documented and justified in the feature plan.

**Version**: 1.0.0 | **Ratified**: 2026-06-11 | **Last Amended**: 2026-06-11
