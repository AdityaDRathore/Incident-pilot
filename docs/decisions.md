# Architectural Decision Records (ADRs)

## ADR-001: Use LangGraph for Agent Orchestration
**Context**: We need an agentic workflow that is stateful, can pause for human approval, and is highly deterministic in its state transitions.
**Decision**: Use Python and LangGraph.
**Consequences**: Provides excellent checkpointing and deterministic node execution, avoiding the unreliability of LLM-driven loops. It allows pausing the graph, persisting state to Postgres, and resuming on human approval.

## ADR-002: Modular Monolith vs Microservices
**Context**: The application requires a frontend, backend API, agent worker, simulator, and vector storage.
**Decision**: Build a modular monolith (FastAPI + Postgres) instead of splitting into 5+ microservices.
**Consequences**: Reduces operational complexity and deployment overhead while maintaining clean boundaries between the API, agent, and simulator modules in the codebase.

## ADR-003: Typed Tool Contracts & Deterministic Authorization
**Context**: LLMs cannot be trusted to self-regulate permissions, nor should they generate arbitrary shell/SQL commands.
**Decision**: Define strictly typed tool schemas. All tool calls must pass through a deterministic backend policy engine that checks RBAC, risk levels, and allowlists before execution.
**Consequences**: Hardens the system against prompt injection and privilege escalation. Adds some friction to adding new tools, but guarantees security.

## ADR-004: Unified PostgreSQL Database
**Context**: We need relational storage for incident tracking and vector storage for RAG (runbooks).
**Decision**: Use PostgreSQL with the `pgvector` extension for both relational and vector data.
**Consequences**: Reduces infrastructure dependencies (no need for a separate vector DB like Pinecone/Milvus), simplifies backups, and enables hybrid queries (relational metadata + vector similarity).

## ADR-005: Explicit Hypothesis Modeling
**Context**: Agents often jump to the first probable root cause without verifying alternatives, leading to high hallucination rates.
**Decision**: Enforce an explicit hypothesis model in the agent state. The agent must document multiple hypotheses, assign confidence scores, and gather confirming/refuting evidence for each.
**Consequences**: Increases tokens used and reasoning time, but dramatically improves the explainability and accuracy of the root-cause analysis.
