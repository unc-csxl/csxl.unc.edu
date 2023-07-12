"""Confirm system health via monitorable API end points.

Production systems monitor these end points upon deployment, and at regular intervals, to ensure the service is running.
"""


from fastapi import APIRouter, Depends
from ..services.health import HealthService


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

openapi_tags = { "name": "System Health", "description": "Production systems monitor these end points upon deployment, and at regular intervals, to ensure the service is running."}

api = APIRouter(prefix="/api/health")


@api.get("", tags=["System Health"])
def health_check(health_svc: HealthService = Depends()) -> str:
    return health_svc.check()
