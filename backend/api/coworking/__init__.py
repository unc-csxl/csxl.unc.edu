from fastapi import Request
from fastapi.responses import JSONResponse
from backend.services.coworking.exceptions import OperatingHoursCannotOverlapException


def _operating_hours_overlap_exception(
    request: Request, e: OperatingHoursCannotOverlapException
):
    return JSONResponse(status_code=400, content={"message": str(e)})


exception_handlers = [
    (OperatingHoursCannotOverlapException, _operating_hours_overlap_exception)
]
