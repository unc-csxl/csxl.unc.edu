from fastapi import Request
from fastapi.responses import JSONResponse
from ...services.coworking.reservation import ReservationException

# FastAPI Middleware Exception Handler for ReservationExceptions
def _reservation_exception_handler(request: Request, e: ReservationException):
    return JSONResponse(status_code=422, content={"message": str(e)})


# This variable is exposed for consumption in `backend/main.py`. It captures tuples
# of Feature-specific Exception and corresponding Exception Handler for HTTP Error purposes.
exception_handlers = [(ReservationException, _reservation_exception_handler)]