"""OH Section API

This API is used to access OH section data."""

from fastapi import APIRouter, Depends

from backend.models.office_hours.oh_section import OfficeHoursSectionDraft
from backend.models.office_hours.oh_section_details import OfficeHoursSectionDetails
from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours section, event, and ticket functionality",
}


@api.post("/section", response_model=OfficeHoursSectionDetails, tags=["Office Hours"])
def new_oh_section(
    oh_section: OfficeHoursSectionDraft,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> OfficeHoursSectionDetails:
    """
    Adds a new OH section to the database

    Returns:
        OfficeHoursSectionDetails: OH Section created
    """
    return oh_section_service.create(subject, oh_section)


@api.get("", response_model=list[OfficeHoursSectionDetails], tags=["Office Hours"])
def get_oh_sections_by_term_id(
    term_id: str,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursSectionDetails]:
    """
    Gets list of OH sections by term ID

    Returns:
        list[OfficeHoursSectionDetails]: OH sections within the given term
    """
    return oh_section_service.get_sections_by_term(subject, term_id)


@api.get(
    "api/office-hours/term/",
    response_model=list[OfficeHoursSectionDetails],
    tags=["Office Hours"],
)
def get_oh_sections_by_user_and_term(
    term_id: str,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursSectionDetails]:
    """
    Gets list of OH sections the currrent user is in during a given term

    Returns:
        list[OfficeHoursSectionDetails]: User's OH sections within the given term
    """
    return oh_section_service.get_user_sections_by_term(term_id, subject)


@api.put("", response_model=OfficeHoursSectionDetails, tags=["Academics"])
def update_oh_section(
    oh_section: OfficeHoursSectionDraft,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> OfficeHoursSectionDetails:
    """
    Updates an OfficeHoursSection to the database

    Returns:
        OfficeHoursSectionDetails: OH Section updated
    """
    return oh_section_service.update(subject, oh_section)


@api.delete("/{oh_section_id}", response_model=None, tags=["Office Hours"])
def delete_oh_section(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
):
    """
    Deletes an OfficeHoursSection from the database
    """
    return oh_section_service.delete(subject, oh_section_id)
