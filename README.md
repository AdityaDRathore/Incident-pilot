# IncidentPilot

**IncidentPilot** is an autonomous AI agent designed for Site Reliability Engineering (SRE) and DevOps teams. Built with **LangGraph** and **Gemini**, IncidentPilot acts as an autonomous tier-1 responder that instantly investigates production incidents, gathers telemetry, forms hypotheses, and proposes remediation actions—all guarded by a strict Human-in-the-Loop (HITL) safety net.

## Key Features 

- **Autonomous Investigation**: Automatically reads logs, checks database connection pools, and queries system metrics to find the root cause of an incident within seconds.
- **Human-in-the-Loop (HITL)**: Can read data autonomously, but will pause execution and request explicit human approval before executing any destructive or risky actions (like restarting services or rolling back deployments).
- **Real-time Engineering Dashboard**: A beautiful, glassmorphic UI that streams the agent's real-time "thoughts" and trajectory via Server-Sent Events (SSE).
- **Deterministic Simulation Engine**: Comes with a built-in production simulator, allowing you to trigger mock incidents (Database Exhaustion, Bad Deployments) to test the agent safely.
- **Strict Role-Based Access Control (RBAC)**: Enforces security policies so the agent cannot bypass permissions or succumb to adversarial prompt injections.
- **Evaluation Framework**: Includes a deterministic 50-task evaluation harness to measure agent safety, root-cause accuracy, and prompt-injection resistance.

---

## Tech Stack 

- **AI Framework**: LangGraph, LangChain, Google Gemini (Flash 1.5)
- **Backend**: FastAPI, Python, Uvicorn
- **Frontend**: Vanilla JavaScript, HTML5, CSS Variables (No build step required)
- **Deployment**: Docker, Docker Compose
- **Security**: Custom Python Policy Engine

---

##  Quickstart

You can run the entire IncidentPilot stack locally with a single Docker command.

### 1. Add your API Key
Create a `.env` file in the root of the project (if not already present) and add your free-tier Gemini API key:

```env
GEMINI_API_KEY="your_google_gemini_api_key_here"
GOOGLE_API_KEY="your_google_gemini_api_key_here"
```

### 2. Start the Application
Boot up the Docker container which serves both the FastAPI backend and the static frontend:

```bash
docker compose up --build
```

### 3. Open the Dashboard
Navigate your browser to: **http://localhost:8000**

---

##  How to Use

1. **Trigger an Incident**: On the main dashboard, click one of the Scenario Launchers (e.g., *Deploy Bad Release*).
2. **Watch the Trace**: The UI will stream the agent's live reasoning as it investigates the mock servers. You will see it fetching logs, analyzing traces, and deducing the root cause.
3. **Approve Actions**: When the agent isolates the problem and decides a remediation is needed (e.g., rolling back the deployment), a red **Action Approval Required** modal will appear.
4. **Resolve**: Click **Approve & Execute**. The agent will apply the fix, verify system health, and generate a final Post-Mortem Report in the UI.

---

##  Project Architecture

```text
Incident-pilot/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routes and SSE streams
│   │   ├── graph/          # LangGraph agent definitions and tools
│   │   ├── policies/       # RBAC and security gating engine
│   │   └── simulation/     # Mock production environment (logs, metrics)
│   ├── static/             # The Frontend UI (HTML, CSS, JS)
│   ├── tests/              # Security and unit tests
│   └── pyproject.toml      # Python dependencies
├── evals/                  # Benchmark scripts and dataset.json
├── docs/                   # Post-mortems, evaluations, and architecture docs
├── docker-compose.yml
└── Dockerfile
```

---

##  Security & Evaluation

IncidentPilot treats **Safety** as a first-class citizen:
- **Policy Engine**: `backend/app/policies/engine.py` restricts the agent's tool execution based on predefined risk levels.
- **Evaluation Harness**: Run `python -m evals.run --mock-llm` (inside the backend directory) to test the agent against 50 simulated incidents, including adversarial prompt-injection attempts. The agent is strictly evaluated on its ability to refuse dangerous inputs while successfully investigating legitimate ones.
