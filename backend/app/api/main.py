from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="IncidentPilot API", version="0.1.0")

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str
    service: str

@app.post("/api/incidents")
async def create_incident(incident: IncidentCreate):
    incident_id = str(uuid.uuid4())
    # In a real app, save to database and initialize simulator state
    return {"id": incident_id, "status": "created", "details": incident.dict()}

@app.post("/api/incidents/{incident_id}/investigate")
async def investigate(incident_id: str):
    # This would normally enqueue a background task to run the LangGraph workflow
    return {"id": incident_id, "status": "investigation_started"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}
