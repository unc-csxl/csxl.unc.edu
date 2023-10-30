"""Operating Hours API

This API manages the Operating Hours of the XL."""

from datetime import datetime, timedelta
from typing import Sequence
from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...models import User
from ...models.coworking import OperatingHours, TimeRange
from ...services.coworking import OperatingHoursService

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking/operating_hours")
openapi_tags = {
    "name": "Coworking",
    "description": "The XL's coworking operating hours are managed via these endpoints.",
}


@api.get("", response_model=Sequence[OperatingHours], tags=["Coworking"])
def get_operating_hours(
    start: datetime = datetime.now(),
    end: datetime = datetime.now() + timedelta(weeks=1),
    operating_hours_svc: OperatingHoursService = Depends(),
):
    """List operating hours over a given span of dates."""
    time_range = TimeRange(start=start, end=end)
    return operating_hours_svc.schedule(time_range)
