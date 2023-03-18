"""Health check routes are used by the production system to monitor whether the system is live and running."""

from fastapi import APIRouter, Depends
from ..services.health import HealthService


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = {"name": "System Health", "description": "Service health endpoints."}

api = APIRouter(prefix="/api/health")


@api.get("", tags=["System Health"])
def health_check(health_svc: HealthService = Depends()) -> str:
    return health_svc.check()
