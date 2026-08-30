from .scenarios import SimulationState, IncidentScenario
from datetime import timedelta

# Global simulation state for the single instance app, in a real app this would be tied to the incident ID
_active_simulations = {}

def get_simulator(incident_id: str) -> SimulationState:
    if incident_id not in _active_simulations:
        # Default to normal if not initialized, but typically initialized when incident is created
        _active_simulations[incident_id] = SimulationState(IncidentScenario.NORMAL)
    return _active_simulations[incident_id]

def initialize_incident(incident_id: str, scenario_name: str):
    try:
        scenario = IncidentScenario(scenario_name)
    except ValueError:
        scenario = IncidentScenario.NORMAL
    _active_simulations[incident_id] = SimulationState(scenario)

def search_logs(incident_id: str, service: str, query: str = "", time_window: str = "1h"):
    sim = get_simulator(incident_id)
    logs = sim.query_logs(service)
    if query:
        logs = [l for l in logs if query.lower() in l["message"].lower()]
    return logs

def query_metrics(incident_id: str, service: str, metric: str = "", time_window: str = "1h"):
    sim = get_simulator(incident_id)
    metrics = sim.query_metrics(service)
    if metric and metric in metrics:
        return {metric: metrics[metric]}
    return metrics

def get_service_health(incident_id: str, service: str):
    sim = get_simulator(incident_id)
    return sim.get_service_health(service)

def get_recent_deployments(incident_id: str, service: str, limit: int = 5):
    sim = get_simulator(incident_id)
    svc = sim.services.get(service)
    if not svc:
        return []
    
    if sim.scenario == IncidentScenario.BAD_DEPLOYMENT and service == "checkout-api":
        return [
            {"version": "v2.8.1", "timestamp": sim.start_time.isoformat(), "status": "active"},
            {"version": "v2.8.0", "timestamp": (sim.start_time - timedelta(days=2)).isoformat(), "status": "superseded"}
        ]
    else:
        return [
            {"version": svc["version"], "timestamp": (sim.start_time - timedelta(days=5)).isoformat(), "status": "active"}
        ]

def rollback_deployment(incident_id: str, service: str, to_version: str):
    sim = get_simulator(incident_id)
    return sim.rollback_deployment(service, to_version)

def restart_service(incident_id: str, service: str):
    sim = get_simulator(incident_id)
    return sim.restart_service(service)
