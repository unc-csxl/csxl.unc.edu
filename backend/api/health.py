"""Confirm system health via monitorable API end points.

Production systems monitor these end points upon deployment, and at regular intervals, to ensure the service is running.
"""

from typing import Annotated
from fastapi import APIRouter, Depends
from ..models.openai_test_response import OpenAITestResponse
from ..services.health import HealthService


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"

openapi_tags = {
    "name": "System Health",
    "description": "Production systems monitor these end points upon deployment, and at regular intervals, to ensure the service is running.",
}

api = APIRouter(prefix="/api/health")


@api.get("", tags=["System Health"])
def health_check(health_svc: Annotated[HealthService, Depends()]) -> str:
    """Check the health status of the system.

    Args:
        health_svc: Service that performs health checks.

    Returns:
        str: Status message indicating system health.
    """
    return health_svc.check()


@api.get("/openai", tags=["System Health"])
def openai_check(health_svc: Annotated[HealthService, Depends()]) -> OpenAITestResponse:
    """Check the OpenAI service integration.

    Returns:
        OpenAITestResponse: Response containing basketball player information.
    """
    return health_svc.check_openai()
