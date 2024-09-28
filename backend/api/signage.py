"""Signage API"""

from fastapi import APIRouter, Depends

from ..api.authentication import registered_user

from ..services import SignageService

from ..models import SignageOverviewFast, SignageOverviewSlow

__authors__ = ["Will Zahrt"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/signage")
openapi_tags = {
    "name": "Signage",
    "description": "Retrieve signage information.",
}


@api.get("/slow", tags=["Signage"])
def get_slow_signage(
    signage_svc: SignageService = Depends()
) -> SignageOverviewSlow:
    """Retrieves the welcome status."""
    return signage_svc.get_slow_data()


@api.get("/fast", tags=["Signage"])
def get_fast_signage(
    signage_svc: SignageService = Depends()
) -> SignageOverviewFast:
    """Retrieves the welcome status."""
    return signage_svc.get_fast_data()
