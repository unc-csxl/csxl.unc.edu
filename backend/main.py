"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from pathlib import Path
from fastapi import FastAPI
from .api import health, organizations, static_files, profile, authentication, user
from .api.coworking import status, reservation, ambassador
from .api.admin import users as admin_users
from .api.admin import roles as admin_roles

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

description = """
Welcome to the UNC Computer Science **Experience Labs** RESTful Application Programming Interface.
"""

app = FastAPI(
    title="UNC CS Experience Labs API",
    version="0.0.1",
    description=description,
    openapi_tags=[
        profile.openapi_tags,
        user.openapi_tags,
        organizations.openapi_tags,
        reservation.openapi_tags,
        reservation.openapi_tags,
        health.openapi_tags,
        admin_users.openapi_tags,
        admin_roles.openapi_tags,
    ],
)

app.include_router(status.api)
app.include_router(reservation.api)
app.include_router(user.api)
app.include_router(profile.api)
app.include_router(organizations.api)
app.include_router(health.api)
app.include_router(ambassador.api)
app.include_router(authentication.api)
app.include_router(admin_users.api)
app.include_router(admin_roles.api)

app.mount("/", static_files.StaticFileMiddleware(directory="./static"))