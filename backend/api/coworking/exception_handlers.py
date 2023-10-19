from fastapi import Request
from fastapi.responses import JSONResponse
from ...services.coworking.reservation import ReservationException


# FastAPI Middleware Exception Handler for ReservationExceptions
def _reservation_exception_handler(request: Request, e: ReservationException):
    return JSONResponse(status_code=422, content={"message": str(e)})


exception_handlers = [(ReservationException, _reservation_exception_handler)]
