"""Section Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends

from backend.models.academics.section_member import SectionMember
from backend.models.office_hours.section import OfficeHoursSectionPartial
from ..authentication import registered_user
from ...services.academics import SectionMembershipService
from ...models import User
from ...models.academics import Section, SectionDetails

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


api = APIRouter(prefix="/api/academics/section-member")
openapi_tags = {
    "name": "Academics",
    "description": "Academic and course information are managed via these endpoints.",
}


@api.post("", response_model=SectionMember, tags=["Academics"])
def add_user_membership(
    oh_section: OfficeHoursSectionPartial,
    subject: User = Depends(registered_user),
    section_membership: SectionMembershipService = Depends(),
) -> SectionMember:
    """
    Get all sections

    Returns:
        list[SectionDetails]: All `Section`s in the `Section` database table
    """
    return section_membership.add_user_oh_membership(subject, oh_section)
