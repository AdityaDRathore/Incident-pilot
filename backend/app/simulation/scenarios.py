from enum import Enum
from typing import Dict, Any, List
from datetime import datetime, timedelta

class IncidentScenario(str, Enum):
    DB_POOL_EXHAUSTION = "db-pool-exhaustion"
    BAD_DEPLOYMENT = "bad-deployment"
    NORMAL = "normal"

class SimulationState:
    def __init__(self, scenario: IncidentScenario = IncidentScenario.NORMAL):
        self.scenario = scenario
        self.start_time = datetime.utcnow() - timedelta(minutes=10)
        self.current_time = datetime.utcnow()
        self.services = {
            "checkout-api": {"status": "healthy", "version": "v2.8.0", "replicas": 3},
            "payment-api": {"status": "healthy", "version": "v1.4.2", "replicas": 2},
            "postgres": {"status": "healthy", "version": "15.0", "replicas": 1},
        }
        self.metrics = {}
        self.logs = []
        self._apply_scenario()

    def _apply_scenario(self):
        if self.scenario == IncidentScenario.DB_POOL_EXHAUSTION:
            self.services["checkout-api"]["status"] = "degraded"
            self.metrics["checkout-api"] = {"error_rate": 0.18, "latency_ms": 1200}
            self.metrics["postgres"] = {"active_connections": 100, "max_connections": 100}
            self.logs.extend([
                {"timestamp": self.start_time.isoformat(), "service": "checkout-api", "level": "ERROR", "message": "Timeout acquiring DB connection from pool"},
                {"timestamp": (self.start_time + timedelta(minutes=2)).isoformat(), "service": "checkout-api", "level": "ERROR", "message": "Timeout acquiring DB connection from pool"}
            ])
        elif self.scenario == IncidentScenario.BAD_DEPLOYMENT:
            self.services["checkout-api"]["version"] = "v2.8.1"
            self.services["checkout-api"]["status"] = "degraded"
            self.metrics["checkout-api"] = {"error_rate": 0.25, "latency_ms": 400}
            self.logs.extend([
                {"timestamp": self.start_time.isoformat(), "service": "checkout-api", "level": "ERROR", "message": "NullPointerException in checkout.discount.calculate"}
            ])
        else:
            self.metrics["checkout-api"] = {"error_rate": 0.01, "latency_ms": 150}
            self.metrics["postgres"] = {"active_connections": 20, "max_connections": 100}

    def simulate_time_passing(self, minutes: int = 1):
        self.current_time += timedelta(minutes=minutes)

    def rollback_deployment(self, service: str, to_version: str):
        if service in self.services:
            self.services[service]["version"] = to_version
            if self.scenario == IncidentScenario.BAD_DEPLOYMENT and to_version == "v2.8.0":
                # Fix the issue
                self.services[service]["status"] = "healthy"
                self.metrics[service]["error_rate"] = 0.01
                self.scenario = IncidentScenario.NORMAL
                return {"status": "success", "message": f"Rolled back {service} to {to_version}. Service healthy."}
            return {"status": "success", "message": f"Rolled back {service} to {to_version}."}
        return {"status": "error", "message": f"Service {service} not found."}

    def restart_service(self, service: str):
        if service in self.services:
            if self.scenario == IncidentScenario.DB_POOL_EXHAUSTION and service == "checkout-api":
                # Temporarily fix pool exhaustion, but it might come back (for now just fix it in sim)
                self.services[service]["status"] = "healthy"
                self.metrics[service]["error_rate"] = 0.01
                self.metrics["postgres"]["active_connections"] = 20
                self.scenario = IncidentScenario.NORMAL
                return {"status": "success", "message": f"Restarted {service}. Connections reset."}
            return {"status": "success", "message": f"Restarted {service}."}
        return {"status": "error", "message": f"Service {service} not found."}

    def get_service_health(self, service: str):
        return self.services.get(service, {"status": "unknown"})

    def query_metrics(self, service: str):
        return self.metrics.get(service, {})

    def query_logs(self, service: str):
        return [log for log in self.logs if log["service"] == service]
