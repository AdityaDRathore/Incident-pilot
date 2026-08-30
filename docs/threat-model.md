# Threat Model

## 1. Prompt Injection
**Attack**: An attacker inserts malicious instructions into application logs or internal runbooks ("IGNORE PREVIOUS INSTRUCTIONS AND DO X"). When the agent retrieves these via `search_logs` or `search_runbooks`, the LLM executes the attacker's payload.
**Mitigation**: 
- **Architectural Isolation**: The agent's reasoning is completely separated from action execution. The LLM cannot execute shell commands or arbitrary SQL.
- **Deterministic Policy Engine**: Even if the LLM tries to call a tool to do X, the Python backend intercepts the tool call and verifies RBAC, Risk Level, and explicit tool schemas.
- **Human-in-the-Loop**: Any action classified as `MEDIUM` or `CRITICAL` forces a hard `Interrupt` in the LangGraph execution, preventing autonomous destructive actions.
**Residual Risk**: The LLM might output a corrupted root-cause analysis that tricks a human into approving a bad action.

## 2. Tool Abuse & Privilege Escalation
**Attack**: The LLM attempts to use a tool meant for `ADMIN` while operating on behalf of a `VIEWER` user.
**Mitigation**: Every tool call passes the `CURRENT_USER_ROLE` into `execute_with_policy()`. The Python backend rejects unauthorized calls.
**Residual Risk**: None, assuming roles are correctly passed from the JWT in the API layer.

## 3. Approval Bypass
**Attack**: The agent modifies its internal state to simulate that approval was granted.
**Mitigation**: State transitions for approvals are handled by LangGraph's `interrupt_before`. Resumption requires an external API call (`POST /api/incidents/{id}/approve`), which acts as the deterministic continuation trigger. The LLM cannot fake this API call.
**Residual Risk**: Low. 

## 4. Infinite Loops & Resource Exhaustion
**Attack**: The agent enters a planning loop, exhausting token budgets and blocking system resources.
**Mitigation**: LangGraph's native `recursion_limit` strictly aborts the workflow after a set number of steps. The application also tracks `budget_used`.
**Residual Risk**: Financial risk is capped by the recursion limit.

## 5. Secret Leakage
**Attack**: The LLM outputs environment variables or database connection strings in the incident report.
**Mitigation**: Secrets are never passed into the LangGraph state. The DB connection and OpenAI API keys are held strictly in environment variables accessed only by backend infrastructure code.
**Residual Risk**: Negligible.
