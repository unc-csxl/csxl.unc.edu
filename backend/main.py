"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""


from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from .api import (
    events,
    health,
    organizations,
    static_files,
    profile,
    authentication,
    user,
)
from .api.coworking import status, reservation, ambassador, operating_hours
from .api.admin import users as admin_users
from .api.admin import roles as admin_roles
from .services.exceptions import UserPermissionException, ResourceNotFoundException

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
        reservation.openapi_tags,
        health.openapi_tags,
        admin_users.openapi_tags,
        admin_roles.openapi_tags,
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
    profile,
    organizations,
    health,
    ambassador,
    authentication,
    admin_users,
    admin_roles,
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving Angular front-end in production, as well as static assets
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))


# Add application-wide exception handling middleware for commonly encountered API Exceptions
@app.exception_handler(UserPermissionException)
def permission_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=403, content={"message": str(e)})


@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(
    request: Request, e: ResourceNotFoundException
):
    return JSONResponse(status_code=404, content={"message": str(e)})


# Add feature-specific exception handling middleware
from .api import coworking

feature_exception_handlers = [coworking.exception_handlers]

for feature_exception_handler in feature_exception_handlers:
    for exception, handler in feature_exception_handler:

        @app.exception_handler(exception)
        def _handler_wrapper(request: Request, e: exception):
            return handler(request, e)
