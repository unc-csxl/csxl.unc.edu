"""OH Section API

This API is used to access OH section data."""

from datetime import datetime
from fastapi import APIRouter, Depends
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...services.office_hours.ticket import OfficeHoursTicketService
from ...models.office_hours.event_details import OfficeHoursEventDetails
from ...models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionDraft,
)
from ...models.office_hours.section_details import OfficeHoursSectionDetails
from ...services.office_hours.section import OfficeHoursSectionService
from ..authentication import registered_user
from ...models import User


__authors__ = ["Sadie Amato", "Madelyn Andrews", "Bailey DeSouza", "Meghan Sun"]
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


@api.get(
    "/{oh_section_id}", response_model=OfficeHoursSectionDetails, tags=["Office Hours"]
)
def get_oh_section_by_id(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> OfficeHoursSectionDetails:
    """
    Gets an OH section by OH section ID

    Returns:
        OfficeHoursSectionDetails: The OH section with the given OH section id
    """
    return oh_section_service.get_section_by_id(subject, oh_section_id)


@api.get(
    "/{oh_section_id}/events",
    response_model=list[OfficeHoursEventDetails],
    tag=["Office Hours"],
)
def get_oh_section_events(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursEventDetails]:
    """
    Gets all events for a given section based on OH section id.

    Returns:
        list[OfficeHoursEventDetails]: List of events for the given section
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        oh_section_id
    )
    return oh_section_service.get_events_by_section(subject, oh_section)


@api.get(
    "/{oh_section_id}/events/upcoming",
    response_model=list[OfficeHoursEventDetails],
    tag=["Office Hours"],
)
def get_oh_section_upcoming_events(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
    start: datetime = datetime.now(),
    end: datetime = datetime.now() + datetime.timedelta(weeks=1),
) -> list[OfficeHoursEventDetails]:
    """
    Gets a list of upcoming OH events within a time range.

    Returns:
        list[OfficeHoursEventDetails]: OH events associated with a given user in a time range
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        oh_section_id
    )
    return oh_section_service.get_events_by_section(subject, oh_section)


@api.get(
    "/term/{term_id}",
    response_model=list[OfficeHoursSectionDetails],
    tags=["Office Hours"],
)
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
    "/user/term/{term_id}",
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
    return oh_section_service.get_user_sections_by_term(subject, term_id)


@api.get(
    "/{oh_section_id}/tickets",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_oh_section_tickets(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets from an OH section

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        oh_section_id
    )
    return oh_section_service.get_section_tickets(subject, oh_section)


@api.get(
    "/{oh_section_id}/user/tickets",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_oh_tickets_by_section_and_user(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH section and user

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section and for the specific user
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        oh_section_id
    )
    return oh_section_service.get_tickets_by_section_and_user(subject, oh_section)


@api.put(
    "/{oh_section_id}", response_model=OfficeHoursSectionDetails, tags=["Office Hours"]
)
def update_oh_section(
    oh_section: OfficeHoursSection,
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
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        oh_section_id
    )
    return oh_section_service.delete(subject, oh_section)