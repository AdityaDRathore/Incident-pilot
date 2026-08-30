# Installing the IncidentPilot Antigravity team

This bundle contains workspace-scoped Antigravity custom agents, a workspace rule, and workflows.

## Expected repository layout

Copy `.agents/` into the root of your IncidentPilot Git repository:

```text
your-repo/
├── .agents/
│   ├── agents/
│   ├── rules/
│   └── workflows/
├── docs/
│   └── master-spec.md
└── ...
```

Antigravity automatically discovers workspace agents under `.agents/agents/` and workspace rules under `.agents/rules/`.

## Recommended order

1. Copy `.agents/` into repo root.
2. Save the master build specification as `docs/master-spec.md`.
3. Open/reload the repository in Antigravity.
4. Open the Agent Manager / Customizations and confirm the agents appear.
5. Run `/workflow-01-bootstrap`.
6. Review architecture and contracts.
7. Run `/workflow-02-build-core`.
8. Run `/workflow-03-integrate`.
9. Run `/workflow-04-security`.
10. Run `/workflow-05-frontend`.
11. Run `/workflow-06-evaluate`.
12. Run `/workflow-07-release`.
13. Run `/workflow-08-portfolio`.

Do not run all workflows blindly. Review each milestone before moving to the next.

## Agent naming

Custom agents:
- incidentpilot-lead
- incidentpilot-backend
- incidentpilot-agent-core
- incidentpilot-simulator
- incidentpilot-rag
- incidentpilot-security
- incidentpilot-frontend
- incidentpilot-evaluation
- incidentpilot-release

## Important

The YAML `tools` lists deliberately use only tool names shown in the current Antigravity subagent documentation. Misspelled tool names can cause a subagent to hang.

The lead agent is the only custom agent configured with `mainAgent: true`. All implementation specialists are subagents.

Use sandboxed command execution. Let Antigravity surface permission requests when an operation needs user approval.
