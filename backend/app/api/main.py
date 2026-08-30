import os
import sys
import uuid
import asyncio
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from typing import Dict, Any

# Ensure we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.simulation.simulator import initialize_incident, get_simulator
from app.graph.workflow import app as workflow_app
from app.tools.definitions import ALL_TOOLS
from langchain_core.messages import HumanMessage, AIMessage

# A global dictionary to hold running incidents for demo purposes
INCIDENTS = {}

app = FastAPI(title="IncidentPilot API", version="0.1.0")

class SimulateRequest(BaseModel):
    scenario: str

@app.post("/api/incidents/simulate")
async def simulate_incident(req: SimulateRequest):
    incident_id = str(uuid.uuid4())
    initialize_incident(incident_id, req.scenario)
    INCIDENTS[incident_id] = {
        "status": "investigating",
        "scenario": req.scenario,
        "logs": [],
        "agent_state": None,
        "approval_required": False
    }
    return {"id": incident_id, "status": "investigating"}

@app.post("/api/incidents/{incident_id}/approve")
async def approve_incident(incident_id: str):
    if incident_id not in INCIDENTS:
        raise HTTPException(status_code=404)
    INCIDENTS[incident_id]["approval_required"] = False
    return {"status": "approved"}

async def incident_event_generator(incident_id: str, request: Request):
    """Generates SSE events for the incident trace and simulator telemetry."""
    if incident_id not in INCIDENTS:
        yield {"data": json.dumps({"error": "Not found"})}
        return

    sim = get_simulator(incident_id)
    state = INCIDENTS[incident_id]
    
    # Send initial telemetry
    yield {"event": "telemetry", "data": json.dumps({"metrics": sim.metrics, "services": sim.services})}
    
    # We will simulate the graph progression here based on the integration_tests.py logic
    # but asynchronously yielding events to the frontend.
    
    messages = []
    
    # Step 1: Start
    await asyncio.sleep(1)
    yield {"event": "trace", "data": json.dumps({"message": "Starting investigation..."})}
    
    # Step 2: Search Logs
    await asyncio.sleep(1.5)
    yield {"event": "trace", "data": json.dumps({"message": "I will search logs for anomalies.", "tool": "search_logs"})}
    await asyncio.sleep(1.5)
    
    # Fake log results based on scenario
    log_results = "Anomalies found in logs."
    if state["scenario"] == "bad-deployment":
        log_results = "NullPointerException in checkout.discount.calculate"
        action_msg = "Logs show a failure. I will rollback the deployment."
        tool_name = "rollback_deployment"
        tool_args = {"service": "checkout-api", "to_version": "v2.8.0"}
    elif state["scenario"] == "redis-outage":
        log_results = "Connection refused to redis:6379"
        action_msg = "Redis connection refused. I will restart redis."
        tool_name = "restart_service"
        tool_args = {"service": "redis"}
    else:
        log_results = "Timeout acquiring DB connection from pool"
        action_msg = "Pool exhausted. I will restart the service."
        tool_name = "restart_service"
        tool_args = {"service": "checkout-api"}

    yield {"event": "trace", "data": json.dumps({"message": f"Log search results: {log_results}"})}
    
    # Step 3: Propose Action
    await asyncio.sleep(2)
    yield {"event": "trace", "data": json.dumps({"message": action_msg, "tool": tool_name})}
    
    # Step 4: Pause for approval
    state["approval_required"] = True
    yield {"event": "approval", "data": json.dumps({"tool": tool_name, "args": tool_args})}
    
    # Wait for approval via the endpoint
    while state["approval_required"]:
        if await request.is_disconnected():
            return
        await asyncio.sleep(0.5)
        
    yield {"event": "trace", "data": json.dumps({"message": "Human approval granted. Executing action..."})}
    
    # Step 5: Execute action via simulator
    await asyncio.sleep(1.5)
    if tool_name == "rollback_deployment":
        res = sim.rollback_deployment(**tool_args)
    else:
        res = sim.restart_service(**tool_args)
        
    yield {"event": "trace", "data": json.dumps({"message": f"Action result: {res['message']}"})}
    
    # Step 6: Final telemetry
    yield {"event": "telemetry", "data": json.dumps({"metrics": sim.metrics, "services": sim.services})}
    
    if sim.services.get("checkout-api", {}).get("status") == "healthy":
        yield {"event": "status", "data": json.dumps({"status": "resolved"})}
    else:
        yield {"event": "status", "data": json.dumps({"status": "failed"})}

@app.get("/api/incidents/{incident_id}/stream")
async def incident_stream(incident_id: str, request: Request):
    return EventSourceResponse(incident_event_generator(incident_id, request))

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "../../static")
os.makedirs(static_path, exist_ok=True)
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

