"""Section Course API

This API is used to access course data."""

from fastapi import APIRouter, Depends, HTTPException

from backend.models.academics.section_member import SectionMember
from backend.models.office_hours.section import OfficeHoursSectionPartial
from backend.models.office_hours.section_details import OfficeHoursSectionDetails
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


@api.post("", response_model=list[SectionMember], tags=["Academics"])
def add_user_memberships(
    oh_sections: list[OfficeHoursSectionDetails],
    subject: User = Depends(registered_user),
    section_membership: SectionMembershipService = Depends(),
) -> list[SectionMember]:
    """
    Get all sections

    Returns:
        list[SectionDetails]: All `Section`s in the `Section` database table
    """
    try:
        return section_membership.add_user_oh_memberships(subject, oh_sections)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
