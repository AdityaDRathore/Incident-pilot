# Build Plan

## Phase 1: Architecture & Contracts (Current)
- Generate architecture, ADRs, and build plan.
- Define explicit contracts (State, Tools, DB, Events, APIs) for independent agents.
- **Exit**: Contracts are reviewed and finalized.

## Phase 2: Simulation & RAG Foundation (`incidentpilot-simulator`, `incidentpilot-rag`)
- **Simulator**: Implement the mock production environment, scenarios (DB pool, bad deployment, etc.), and deterministic telemetry (logs, metrics).
- **RAG**: Implement document chunking, embeddings, and pgvector storage.
- **Exit**: We can query mock metrics and retrieve mock runbook chunks.

## Phase 3: Backend API & Database (`incidentpilot-backend`)
- **Database**: PostgreSQL schema migrations (users, incidents, audit logs, state).
- **API**: FastAPI scaffolding, Auth/RBAC, CRUD endpoints for incidents.
- **Exit**: REST API works, database is responsive.

## Phase 4: Agent Core (`incidentpilot-agent-core`)
- **Graph**: Implement LangGraph workflow nodes (Plan, Investigate, Hypothesize, Remediate).
- **State**: Pydantic state tracking.
- **Tools**: Connect to simulator and RAG tools with strict schemas.
- **Exit**: Agent can execute an investigation end-to-end via script.

## Phase 5: Security & Safety (`incidentpilot-security`)
- **Policy Engine**: Implement risk assessment and role-based permissions.
- **Hardening**: Test for prompt injection, ensure safe failure modes.
- **Exit**: System reliably blocks dangerous unapproved actions.

## Phase 6: Human-in-the-Loop & Execution Persistence
- **Pause/Resume**: Implement LangGraph persistence.
- **API Integration**: Connect API approval endpoints to graph resumption.
- **Exit**: An incident can be paused, await HTTP approval, and resume.

## Phase 7: Frontend Dashboard (`incidentpilot-frontend`)
- **UI**: Build React dashboard, incident timeline, evidence viewer, and evaluation page.
- **Real-time**: Hook up SSE/WebSockets for live agent traces.
- **Exit**: Full user experience is visible.

## Phase 8: Evaluation Framework (`incidentpilot-evaluation`)
- **Benchmarks**: 50 deterministic incident tasks.
- **Evaluators**: Measure success, cost, hallucination rate, and injection resistance.
- **Exit**: CI can run `make eval` and output a full evaluation report.

## Phase 9: Final Polish & Release (`incidentpilot-release`, `incidentpilot-lead`)
- **Docker**: Finalize `docker-compose.yml`.
- **Docs**: README, case study, demo script.
- **QA**: End-to-end testing and portfolio-ready validation.
- **Exit**: Project is ready for demonstration.
