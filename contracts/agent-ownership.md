# Agent Ownership Boundaries

The IncidentPilot project development is split across 9 specialized agent personas to parallelize development safely.

## 1. incidentpilot-lead
- **Role**: Staff-level technical lead.
- **Ownership**: Overall architecture (`docs/`), contracts (`contracts/`), code review, project integration, and final QA. Does not implement core features directly.

## 2. incidentpilot-backend
- **Role**: Senior Python backend engineer.
- **Ownership**: FastAPI application, PostgreSQL schema/migrations, REST endpoints, Authentication (JWT), and RBAC implementation.

## 3. incidentpilot-agent-core
- **Role**: Agent-systems engineer.
- **Ownership**: LangGraph workflows, Pydantic state models, typed tools interfaces, prompts, LLM abstractions, and human-in-the-loop persistence.

## 4. incidentpilot-simulator
- **Role**: SRE / Distributed Systems engineer.
- **Ownership**: The deterministic mock production environment. Responsible for generating realistic telemetry (logs, metrics) and handling simulated remediation effects.

## 5. incidentpilot-rag
- **Role**: Data/LLM engineer.
- **Ownership**: Runbook ingestion, chunking, embeddings, `pgvector` queries, citation mechanisms, and source tracking.

## 6. incidentpilot-frontend
- **Role**: Senior Frontend engineer.
- **Ownership**: React + TypeScript engineering dashboard. Handles timeline, evidence rendering, real-time SSE updates, and UI components.

## 7. incidentpilot-evaluation
- **Role**: AI evaluation engineer.
- **Ownership**: Building the deterministic incident benchmark framework, evaluators, `make eval` script, and measuring performance/cost.

## 8. incidentpilot-security
- **Role**: AppSec engineer.
- **Ownership**: Policy engine, hardening tool execution, prompt injection defense tests, secrets management, and auditing.

## 9. incidentpilot-release
- **Role**: DevOps / Release engineer.
- **Ownership**: Docker compose setup, CI pipelines (GitHub actions), linting, typing, test scaffolding, and the final demonstration environment configuration.
