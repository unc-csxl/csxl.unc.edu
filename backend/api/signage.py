"""Signage API"""

from fastapi import APIRouter, Depends
from ..services import SignageService
from ..models import SignageOverviewFast, SignageOverviewSlow

__authors__ = ["Will Zahrt", "Andrew Lockard", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/signage")
openapi_tags = {
    "name": "Signage",
    "description": "Retrieve signage information.",
}


@api.get("/slow", tags=["Signage"])
def get_slow_signage(signage_svc: SignageService = Depends()) -> SignageOverviewSlow:
    """Gets signage data that does not need to be updated frequently.
    
    Parameters:
        None

    Returns:
        SignageOverviewSlow - contains news, top users, events, and announcements
    """
    return signage_svc.get_slow_data()


@api.get("/fast", tags=["Signage"])
def get_fast_signage(signage_svc: SignageService = Depends()) -> SignageOverviewFast:
    """Gets signage data that needs to be updated in real time.

    Parameters:
        None
    
    Returns:
        SignageOverviewFast - contains office hours information for queue time, room and seat availability
    """
    return signage_svc.get_fast_data()
