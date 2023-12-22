from fastapi import Request
from fastapi.responses import JSONResponse
from backend.services.exceptions import EventRegistrationException


# FastAPI Middleware Exception Handler for ReservationExceptions
def _event_registration_exception_handler(
    request: Request, e: EventRegistrationException
):
    return JSONResponse(status_code=422, content={"message": str(e)})


exception_handlers = [
    (EventRegistrationException, _event_registration_exception_handler)
]
