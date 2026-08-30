# Database Contracts

PostgreSQL is the primary data store, using `pgvector` for runbooks.

## Relational Tables
- **`users`**: id, email, role, created_at
- **`incidents`**: id, title, description, severity, service, environment, status, start_time, end_time, created_by
- **`agent_runs`**: id, incident_id, status, current_phase, retry_count, budget_used, created_at, updated_at
- **`agent_state`**: id, run_id, state_json, checkpoint_id (used by LangGraph persistence)
- **`evidence`**: id, run_id, source, type, content, relevance, tool_used, timestamp
- **`hypotheses`**: id, run_id, description, confidence, status, created_at
- **`tool_calls`**: id, run_id, tool_name, arguments, status, result, error, latency_ms, start_time, end_time
- **`approvals`**: id, run_id, action_type, target, status, approved_by, created_at
- **`audit_logs`**: id, user_id, action, resource, timestamp

## Vector Tables
- **`documents`**: id, title, source_url, type
- **`document_chunks`**: id, document_id, content, embedding (VECTOR), metadata_json
