"""Section Member APIs."""

from fastapi import APIRouter, Depends, HTTPException


from ..authentication import registered_user

from ...models.academics.section_member import SectionMember
from ...models.academics.section_member_details import SectionMemberDetails
from ...models.office_hours.course_site import CourseSite
from ...models.roster_role import RosterRole
from ...models import User

from ...services.academics import SectionMemberService

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
    id: int,
    subject: User = Depends(registered_user),
    section_member_svc: SectionMemberService = Depends(),
) -> SectionMember:
    """
    Args:
        id (int): The unique identifier of the SectionMember.
        subject (User): The currently logged-in user.
        section_member_svc (SectionMemberService): Service dependency to interact with Section Membership data.

    Returns:
        SectionMember: The SectionMember corresponding to the provided ID.

    Raises:
        HTTPException(404): If the SectionMember with the specified ID is not found.
    """
    try:
        return section_member_svc.get_section_member_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("", response_model=list[SectionMember], tags=["Academics"])
def add_user_memberships(
    oh_sections: list[CourseSite],
    subject: User = Depends(registered_user),
    section_member_svc: SectionMemberService = Depends(),
) -> list[SectionMember]:
    """
    Adds memberships for a user given a list of Office Hours sections.

    Args:
        oh_sections (list[CourseSite]): List of Office Hours sections to enroll the user into.
        subject (User): The currently logged-in user.
        section_membership (SectionMemberService): Service dependency to manage Section Membership data.

    Returns:
        list[SectionMember]: List of newly created SectionMember memberships for the user.

    Raises:
        HTTPException(404): When there was an issue adding the memberships.
    """
    try:
        return section_member_svc.add_user_section_memberships_by_oh_sections(
            subject, oh_sections
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post(
    "/instructor/{section_id}/{user_id}",
    response_model=SectionMember,
    tags=["Academics"],
)
def add_instructor(
    section_id: int,
    user_id: int,
    subject: User = Depends(registered_user),
    section_member_svc: SectionMemberService = Depends(),
) -> SectionMemberDetails:
    """
    Gets one section by its id

    Returns:
        SectionDetails: Section with the given ID
    """
    return section_member_svc.add_section_member(
        subject, section_id, user_id, RosterRole.INSTRUCTOR
    )
