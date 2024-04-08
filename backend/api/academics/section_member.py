"""Section Member APIs."""

from fastapi import APIRouter, Depends, HTTPException

from ..authentication import registered_user

from ...models.academics.section_member import SectionMember
from ...models.office_hours.section import OfficeHoursSectionPartial
from ...models.office_hours.section_details import OfficeHoursSectionDetails
from ...models import User

from ...services.academics import SectionMembershipService

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/academics/section-member")
openapi_tags = {
    "name": "Academics",
    "description": "Academic Section Membership are managed via these endpoints.",
}


@api.get("/{id}", response_model=SectionMember, tags=["Academics"])
def get_section_member_by_id(
    id: int, section_member_svc: SectionMembershipService = Depends()
) -> SectionMember:
    """
    Args:
        id (int): The unique identifier of the SectionMember.
        section_member_svc (SectionMembershipService): Service dependency to interact with Section Membership data.

    Returns:
        SectionMember: The SectionMember corresponding to the provided ID.

    Raises:
        HTTPException(404): If the SectionMember with the specified ID is not found.
    """
    try:
        return section_member_svc.get_section_member_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/oh-section/{section_id}", response_model=SectionMember, tags=["Academics"])
def get_membership_by_user_and_oh_section_id(
    section_id: int,
    subject: User = Depends(registered_user),
    section_member_svc: SectionMembershipService = Depends(),
) -> SectionMember:
    """
    Retrieves a SectionMember's membership in an Office Hours section by section ID.

    Args:
        section_id (int): The ID of the Office Hours section.
        subject (User): The currently logged-in user.
        section_member_svc (SectionMembershipService): Service dependency to interact with Section Membership data.

    Returns:
        SectionMember: The SectionMember's membership in the specified Office Hours section.

    Raises:
        HTTPException(404): If the SectionMember's membership in the specified section is not found.
    """
    try:
        return section_member_svc.get_section_member_by_user_id_and_section_id(
            subject, id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("", response_model=list[SectionMember], tags=["Academics"])
def add_user_memberships(
    oh_sections: list[OfficeHoursSectionDetails],
    subject: User = Depends(registered_user),
    section_member_svc: SectionMembershipService = Depends(),
) -> list[SectionMember]:
    """
    Adds memberships for a user given a list of Office Hours sections.

    Args:
        oh_sections (list[OfficeHoursSectionDetails]): List of Office Hours sections to enroll the user into.
        subject (User): The currently logged-in user.
        section_membership (SectionMembershipService): Service dependency to manage Section Membership data.

    Returns:
        list[SectionMember]: List of newly created SectionMember memberships for the user.

    Raises:
        HTTPException(404): When there was an issue adding the memberships.
    """
    try:
        return section_member_svc.add_user_oh_memberships(subject, oh_sections)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
