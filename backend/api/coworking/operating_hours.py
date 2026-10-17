"""Operating Hours API

This API manages the Operating Hours of the XL."""

from datetime import datetime, timedelta
from typing import Sequence
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from ...models import User
from ...models.coworking import OperatingHours, TimeRange
from ...services.coworking import OperatingHoursService
from ...services.coworking.exceptions import (
    OperatingHoursCannotDeleteException,
    OperatingHoursCannotOverlapException,
)
from ..authentication import registered_user

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking/operating_hours")
openapi_tags = {
    "name": "Coworking",
    "description": "The XL's coworking operating hours are managed via these endpoints.",
}


def operating_hours_conflict_handler(request: Request, error: Exception):
    """Return recoverable schedule conflicts using the app's error shape."""
    return JSONResponse(status_code=409, content={"message": str(error)})


exception_handlers = [
    (OperatingHoursCannotOverlapException, operating_hours_conflict_handler),
    (OperatingHoursCannotDeleteException, operating_hours_conflict_handler),
]


@api.get("", response_model=Sequence[OperatingHours], tags=["Coworking"])
def get_operating_hours(
    start: datetime | None = None,
    end: datetime | None = None,
    operating_hours_svc: OperatingHoursService = Depends(),
):
    """List operating hours over a given span of dates."""
    start = start or datetime.now(ZoneInfo("America/New_York"))
    end = end or start + timedelta(weeks=1)
    try:
        time_range = TimeRange(start=start, end=end)
    except ValidationError as error:
        raise RequestValidationError(error.errors()) from error
    return operating_hours_svc.schedule(time_range)


@api.post("", response_model=OperatingHours, tags=["Coworking"])
def new_operating_hours(
    operating_hours_range: TimeRange,
    subject: User = Depends(registered_user),
    operating_hours_svc: OperatingHoursService = Depends(),
):
    """Create new opening hours for the XL."""
    time_range = TimeRange(
        start=operating_hours_range.start, end=operating_hours_range.end
    )
    return operating_hours_svc.create(subject, time_range)


@api.put("/{id}", response_model=OperatingHours, tags=["Coworking"])
def update_operating_hours(
    id: int,
    operating_hours_range: TimeRange,
    subject: User = Depends(registered_user),
    operating_hours_svc: OperatingHoursService = Depends(),
):
    """Replace an existing interval's times, rejecting invalid or conflicting hours."""
    return operating_hours_svc.update(subject, id, operating_hours_range)


@api.delete("/{id}", tags=["Coworking"])
def delete_operating_hours(
    id: int,
    subject: User = Depends(registered_user),
    operating_hours_svc: OperatingHoursService = Depends(),
):
    """Delete operating hours for the XL."""
    operating_hours = operating_hours_svc.get_by_id(id)
    return operating_hours_svc.delete(subject, operating_hours)
