"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware

from backend.services.coworking.reservation import ReservationException

from .api.events import events

from .api import (
    health,
    organizations,
    static_files,
    profile,
    authentication,
    user,
    room,
    application,
    article,
)
from .api.coworking import status, reservation, ambassador, operating_hours
from .api.academics import section_member, term, course, section, my_courses, hiring
from .api.office_hours import (
    office_hours as office_hours_event,
    ticket as office_hours_ticket,
)
from .api.admin import users as admin_users
from .api.admin import roles as admin_roles
from .api.admin import facts as admin_facts

from .services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
    CoursePermissionException,
    CourseDataScrapingException,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

description = """
Welcome to the UNC Computer Science **Experience Labs** RESTful Application Programming Interface.
"""

# Metadata to improve the usefulness of OpenAPI Docs /docs API Explorer
app = FastAPI(
    title="UNC CS Experience Labs API",
    version="0.0.1",
    description=description,
    openapi_tags=[
        profile.openapi_tags,
        user.openapi_tags,
        organizations.openapi_tags,
        events.openapi_tags,
        section_member.openapi_tags,
        course.openapi_tags,
        room.openapi_tags,
        reservation.openapi_tags,
        application.openapi_tags,
        admin_users.openapi_tags,
        admin_roles.openapi_tags,
        health.openapi_tags,
        my_courses.openapi_tags,
        hiring.openapi_tags,
        admin_facts.openapi_tags,
        article.openapi_tags,
    ],
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Plugging in each of the router APIs
feature_apis = [
    status,
    reservation,
    operating_hours,
    events,
    user,
    organizations,
    ambassador,
    my_courses,
    term,
    course,
    section,
    room,
    section_member,
    profile,
    admin_users,
    admin_roles,
    application,
    authentication,
    health,
    office_hours_event,
    office_hours_ticket,
    hiring,
    admin_facts,
    article,
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving Angular front-end in production, as well as static assets
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))


# Add application-wide exception handling middleware for commonly encountered API Exceptions
@app.exception_handler(UserPermissionException)
def permission_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=403, content={"message": str(e)})


@app.exception_handler(CoursePermissionException)
def permission_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=403, content={"message": str(e)})


@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(
    request: Request, e: ResourceNotFoundException
):
    return JSONResponse(status_code=404, content={"message": str(e)})


@app.exception_handler(CourseDataScrapingException)
def resource_not_found_exception_handler(
    request: Request, e: CourseDataScrapingException
):
    return JSONResponse(status_code=500, content={"message": str(e)})


# Add feature-specific exception handling middleware
from .api import coworking
from .api import events

feature_exception_handlers = [coworking.exception_handlers, events.exception_handlers]

for feature_exception_handler in feature_exception_handlers:
    for exception, handler in feature_exception_handler:

        @app.exception_handler(exception)
        def _handler_wrapper(request: Request, e: Exception):
            return handler(request, e)
