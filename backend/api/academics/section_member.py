"""Section Member APIs."""

from fastapi import APIRouter, Depends, HTTPException


from ..authentication import registered_user

from ...models.academics.section_member import SectionMember
from ...models.academics.section_member_details import SectionMemberDetails
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


@api.get("/oh-section/{section_id}", response_model=SectionMember, tags=["Academics"])
def get_membership_by_user_and_oh_section_id(
    section_id: int,
    subject: User = Depends(registered_user),
    section_member_svc: SectionMemberService = Depends(),
) -> SectionMember:
    """
    Retrieves a SectionMember's membership in an Office Hours section by section ID.

    Args:
        section_id (int): The ID of the Office Hours section.
        subject (User): The currently logged-in user.
        section_member_svc (SectionMemberService): Service dependency to interact with Section Membership data.

    Returns:
        SectionMember: The SectionMember's membership in the specified Office Hours section.

    Raises:
        HTTPException(404): If the SectionMember's membership in the specified section is not found.
    """
    try:
        return section_member_svc.get_section_member_by_user_id_and_oh_section_id(
            subject, section_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/instructor-memberships/", response_model=list[SectionMember], tags=["Academics"]
)
def check_instructor_memberships(
    subject: User = Depends(registered_user),
    section_member_svc: SectionMemberService = Depends(),
) -> list[SectionMember]:
    """
    Main indicator if User is an instructor. Searches all instructor memberships for a given user.

    Args:
        subject (User): The user object representing the user to find memberships.
        section_member_svc (SectionMemberService): An instance of SectionMembershipService.

    Returns:
        List[SectionMember]: A list of SectionMember objects representing all instructor memberships of the given user. If not instructor, returns an empty list.
    """

    return section_member_svc.search_instructor_memberships(subject)


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
