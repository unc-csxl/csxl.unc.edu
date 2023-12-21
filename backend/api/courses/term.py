"""Courses Term API

This API is used to access term data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.courses import TermService
from ...models import User
from ...models.courses import Term, TermDetails
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/courses/term")


@api.get("", response_model=list[TermDetails], tags=["Courses"])
def get_terms(term_service: TermService = Depends()) -> list[TermDetails]:
    """
    Get all terms

    Returns:
        list[TermDetails]: All `Term`s in the `Term` database table
    """
    return term_service.all()


@api.get("/current", response_model=TermDetails, tags=["Courses"])
def get_current_term(term_service: TermService = Depends()) -> TermDetails:
    """
    Gets the current term based on the current date

    Returns:
        TermDetails: Currently active term
    """
    return term_service.get_by_date(datetime.today())


@api.get("/{id}", response_model=TermDetails, tags=["Courses"])
def get_term_by_id(id: str, term_service: TermService = Depends()) -> TermDetails:
    """
    Gets one term by its id

    Returns:
        TermDetails: Term with the given ID
    """
    return term_service.get_by_id(id)


@api.post("", response_model=TermDetails, tags=["Courses"])
def new_term(
    term: Term,
    subject: User = Depends(registered_user),
    term_service: TermService = Depends(),
) -> TermDetails:
    """
    Adds a new term to the database

    Returns:
        TermDetails: Term created
    """
    return term_service.create(subject, term)


@api.put("", response_model=TermDetails, tags=["Courses"])
def update_term(
    term: Term,
    subject: User = Depends(registered_user),
    term_service: TermService = Depends(),
) -> TermDetails:
    """
    Updates a term to the database

    Returns:
        TermDetails: Term updated
    """
    return term_service.update(subject, term)


@api.delete("", response_model=None, tags=["Courses"])
def delete_term(
    term: Term,
    subject: User = Depends(registered_user),
    term_service: TermService = Depends(),
):
    """
    Deletes a term to the database
    """
    return term_service.delete(subject, term)
