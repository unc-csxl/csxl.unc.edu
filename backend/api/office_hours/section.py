"""OH Section API

This API is used to access OH section data."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from ...models.academics.section_member_details import SectionMemberDetails
from ...models.academics.section_member import SectionMember, SectionMemberPartial
from ...models.coworking.time_range import TimeRange
from ...models.office_hours.ticket_details import OfficeHoursTicketDetails
from ...services.office_hours.ticket import OfficeHoursTicketService
from ...models.office_hours.event_details import OfficeHoursEvent
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
    academic_ids: list[int],
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> OfficeHoursSectionDetails:
    """
    Adds a new OH section to the database

    Returns:
        OfficeHoursSectionDetails: OH Section created
    """
    try:
        return oh_section_service.create(subject, oh_section, academic_ids)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("", response_model=list[OfficeHoursSectionDetails], tags=["Office Hours"])
def get_all_sections(
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursSectionDetails]:
    """
    Gets all OH sections

    Returns:
        list[OfficeHoursSectionDetails]: A list of all OH sections
    """
    try:
        return oh_section_service.get_all_sections(subject)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


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
    "/{oh_section_id}/events/past",
    response_model=list[OfficeHoursEvent],
    tags=["Office Hours"],
)
def get_past_oh_section_events(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursEvent]:
    """
    Gets all past events for a given section based on OH section id.

    Returns:
        list[OfficeHoursEvent]: List of past events for the given section
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        subject, oh_section_id
    )
    return oh_section_service.get_past_events_by_section(subject, oh_section)


@api.get(
    "/{oh_section_id}/events/upcoming",
    response_model=list[OfficeHoursEvent],
    tags=["Office Hours"],
)
def get_upcoming_oh_section_events(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
    start: datetime = datetime.now(),
    end: datetime = datetime.now() + timedelta(weeks=1),
) -> list[OfficeHoursEvent]:
    """
    Gets a list of upcoming OH events within a time range.

    Returns:
        list[OfficeHoursEvent]: OH events associated with a given section in a time range
    """

    time_range = TimeRange(start=start, end=end)
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        subject, oh_section_id
    )
    return oh_section_service.get_upcoming_events_by_section(
        subject, oh_section, time_range
    )


@api.get(
    "/{oh_section_id}/events/current",
    response_model=list[OfficeHoursEvent],
    tags=["Office Hours"],
)
def get_current_oh_section_events(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursEvent]:
    """
    Gets a list of current OH events within a time range.

    Returns:
        list[OfficeHoursEvent]: OH events associated with a given section in a time range
    """
    oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
        subject, oh_section_id
    )
    return oh_section_service.get_current_events_by_section(subject, oh_section)


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
    try:
        return oh_section_service.get_user_sections_by_term(subject, term_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/user/not-enrolled",
    response_model=list[OfficeHoursSection],
    tags=["Office Hours"],
)
def get_user_not_enrolled_sections(
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursSection]:
    """
    Gets list of OH sections the currrent user not apart of.

    Returns:
        list[OfficeHoursSection]: User's OH sections within the given term
    """
    try:
        return oh_section_service.get_user_not_enrolled_sections(subject)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/user/term/{term_id}/not-enrolled",
    response_model=list[OfficeHoursSection],
    tags=["Office Hours"],
)
def get_user_not_enrolled_sections(
    term_id: str,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursSection]:
    """
    Gets list of OH sections the currrent user not apart of.

    Returns:
        list[OfficeHoursSection]: User's OH sections within the given term
    """
    try:
        return oh_section_service.get_user_not_enrolled_sections_by_term(
            subject, term_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


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
    try:
        oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
            subject, oh_section_id
        )
        return oh_section_service.get_section_tickets(subject, oh_section)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/{oh_section_id}/user/created_tickets",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_user_section_created_tickets(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH section and creator

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section and for the specific creator
    """
    try:
        oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
            subject, oh_section_id
        )
        return oh_section_service.get_user_section_created_tickets(subject, oh_section)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/{oh_section_id}/user/called_tickets",
    response_model=list[OfficeHoursTicketDetails],
    tags=["Office Hours"],
)
def get_user_section_called_tickets(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[OfficeHoursTicketDetails]:
    """
    Gets list of OH tickets by OH section and caller

    Returns:
        list[OfficeHoursTicketDetails]: OH tickets within the given section and for the specific caller
    """
    try:
        oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
            subject, oh_section_id
        )
        return oh_section_service.get_user_section_called_tickets(subject, oh_section)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/{oh_section_id}/people",
    response_model=list[SectionMember],
    tags=["Office Hours"],
)
def get_oh_section_members(
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> list[SectionMember]:
    """
    Gets list of OH section members

    Returns:
        list[SectionMember]: List of all `SectionMember` in an OHsection
    """
    try:
        oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
            subject, oh_section_id
        )
        return oh_section_service.get_oh_section_members(subject, oh_section)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "/{oh_section_id}/update-role", response_model=SectionMember, tags=["Office Hours"]
)
def update_oh_section_member_role(
    user_to_modify: SectionMemberPartial,
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> SectionMember:
    """
    Updates a SectionMember in an OH Section to the database

    Returns:
        SectionMember: SectionMember updated
    """
    return oh_section_service.update_oh_section_member_role(
        subject, user_to_modify, oh_section_id
    )


@api.put(
    "/{oh_section_id}/update-role", response_model=SectionMember, tags=["Office Hours"]
)
def update_oh_section_member_role(
    user_to_modify: SectionMemberPartial,
    oh_section_id: int,
    subject: User = Depends(registered_user),
    oh_section_service: OfficeHoursSectionService = Depends(),
) -> SectionMember:
    """
    Updates a SectionMember in an OH Section to the database

    Returns:
        SectionMember: SectionMember updated
    """
    return oh_section_service.update_oh_section_member_role(
        subject, user_to_modify, oh_section_id
    )


# @api.put(
#     "/{oh_section_id}", response_model=OfficeHoursSectionDetails, tags=["Office Hours"]
# )
# def update_oh_section(
#     oh_section: OfficeHoursSection,
#     subject: User = Depends(registered_user),
#     oh_section_service: OfficeHoursSectionService = Depends(),
# ) -> OfficeHoursSectionDetails:
#     """
#     Updates an OfficeHoursSection to the database

#     Returns:
#         OfficeHoursSectionDetails: OH Section updated
#     """
#     return oh_section_service.update(subject, oh_section)


# @api.delete("/{oh_section_id}", response_model=None, tags=["Office Hours"])
# def delete_oh_section(
#     oh_section_id: int,
#     subject: User = Depends(registered_user),
#     oh_section_service: OfficeHoursSectionService = Depends(),
# ):
#     """
#     Deletes an OfficeHoursSection from the database
#     """
#     oh_section: OfficeHoursSectionDetails = oh_section_service.get_section_by_id(
#         oh_section_id
#     )
#     return oh_section_service.delete(subject, oh_section)
