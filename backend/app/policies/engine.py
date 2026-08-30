from enum import Enum

class RiskLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    CRITICAL = "CRITICAL"

class Role(str, Enum):
    VIEWER = "VIEWER"
    ENGINEER = "ENGINEER"
    INCIDENT_COMMANDER = "INCIDENT_COMMANDER"
    ADMIN = "ADMIN"

class SecurityError(Exception):
    pass

class AuthError(Exception):
    pass

def check_tool_permission(user_role: str, tool_name: str, risk_level: str, requires_approval: bool, allowed_roles: list[str]):
    """
    Deterministic policy engine to intercept unauthorized tool execution.
    """
    if user_role not in allowed_roles:
        raise AuthError(f"User role {user_role} is not authorized to use tool {tool_name}. Allowed: {allowed_roles}")
    
    if risk_level in [RiskLevel.MEDIUM, RiskLevel.CRITICAL] and not requires_approval:
        # System safety invariant
        raise SecurityError(f"System Configuration Error: Tool {tool_name} is marked high risk but does not require approval.")
