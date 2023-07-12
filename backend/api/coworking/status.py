"""Coworking Status API

This API is used to retrieve and update a user's profile."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.coworking import StatusService
from ...models import User
from ...models.coworking import Status

__authors__ = ['Kris Jordan']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'


api = APIRouter(prefix="/api/coworking/status")
openapi_tags = { "name": "Coworking", "description": "TODO"}


@api.get("", response_model=Status, tags=['Coworking'])
def get_coworking_status(subject: User = Depends(registered_user), status_svc: StatusService = Depends()):
    """TODO DOCUMENT"""
    return status_svc.get_coworking_status(subject)
