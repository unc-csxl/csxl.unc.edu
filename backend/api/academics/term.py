"""Courses Term API

This API is used to access term data."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.academics import TermService
from ...models import User
from ...models.academics import Term, TermDetails
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/academics/term")


@api.get("", tags=["Academics"])
def get_terms(term_service: TermService = Depends()) -> list[Term]:
    """
    Get all terms

    Returns:
        list[Term]: All `Term`s in the `Term` database table
    """
    return term_service.all()


@api.get("/current", tags=["Academics"])
def get_current_term(term_service: TermService = Depends()) -> Term:
    """
    Gets the current term based on the current date

    Returns:
        Term: Currently active term
    """
    return term_service.get_by_date(datetime.today())


@api.get("/{id}", tags=["Academics"])
def get_term_by_id(id: str, term_service: TermService = Depends()) -> Term:
    """
    Gets one term by its id

    Returns:
        Term: Term with the given ID
    """
    return term_service.get_by_id(id)


@api.post("", response_model=TermDetails, tags=["Academics"])
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


@api.put("", response_model=TermDetails, tags=["Academics"])
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


@api.delete("/{term_id}", response_model=None, tags=["Academics"])
def delete_term(
    term_id: str,
    subject: User = Depends(registered_user),
    term_service: TermService = Depends(),
):
    """
    Deletes a term from the database
    """
    return term_service.delete(subject, term_id)
