"""OH Section API

This API is used to access OH section data."""

from fastapi import APIRouter, Depends

from backend.models.office_hours.oh_section import OfficeHoursSection, OfficeHoursSectionDraft
from backend.models.office_hours.oh_section_details import OfficeHoursSectionDetails
from backend.services.office_hours.oh_section import OfficeHoursSectionService
from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Bailey DeSouza"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/office-hours/section")
openapi_tags = {
    "name": "Office Hours",
    "description": "Office hours section functionality",
}


@api.post("", response_model=OfficeHoursSectionDetails, tags=["Office Hours"])
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


@api.get("/{oh_section_id}", response_model=OfficeHoursSectionDetails, tags=["Office Hours"])
def get_oh_section_by_id(
    oh_section_id: int, subject: User = Depends(registered_user), oh_section_service: OfficeHoursSectionService = Depends()
) -> OfficeHoursSectionDetails:
    """
    Gets an OH section by OH section ID

    Returns:
        OfficeHoursSectionDetails: The OH section with the given OH section id
    """
    return oh_section_service.get_section_by_id(subject, oh_section_id)


@api.get("/term/{term_id}", response_model=list[OfficeHoursSectionDetails], tags=["Office Hours"])
def get_oh_sections_by_term_id(
    term_id: str, subject: User = Depends(registered_user), oh_section_service: OfficeHoursSectionService = Depends()
) -> list[OfficeHoursSectionDetails]:
    """
    Gets list of OH sections by term ID

    Returns:
        list[OfficeHoursSectionDetails]: OH sections within the given term
    """
    return oh_section_service.get_sections_by_term(subject, term_id)


@api.get("/user/term/{term_id}", response_model=list[OfficeHoursSectionDetails], tags=["Office Hours"])
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
    return oh_section_service.get_user_sections_by_term(subject, term_id)


@api.put("/{oh_section_id}", response_model=OfficeHoursSectionDetails, tags=["Office Hours"])
def update_oh_section(
    oh_section_id: int,
    oh_section: OfficeHoursSection,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> OfficeHoursSectionDetails:
    """
    Updates an OfficeHoursSection to the database

    Returns:
        OfficeHoursSectionDetails: OH Section updated
    """
    return oh_section_service.update(subject, oh_section_id, oh_section)


@api.delete("/{oh_section_id}", response_model=None, tags=["Office Hours"])
def delete_oh_section(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
):
    """
    Deletes an OfficeHoursSection from the database
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(oh_section_id)
    return oh_section_service.delete(subject, oh_section)
