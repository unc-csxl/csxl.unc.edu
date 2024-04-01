"""
The Section Service allows the API to manipulate sections data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.entities.academics.section_member_entity import SectionMemberEntity
from backend.models.academics.section_member import SectionMember
from backend.models.academics.section_member_details import SectionMemberDetails
from backend.models.office_hours.section import (
    OfficeHoursSectionDraft,
    OfficeHoursSectionPartial,
)

from ...database import db_session
from ...models.academics import Section
from ...models.academics import SectionDetails
from ...models import User, Room
from ...models.room_assignment_type import RoomAssignmentType
from ...entities.academics import SectionEntity
from ...entities.academics import CourseEntity
from ...entities.academics import SectionRoomEntity
from ..permission import PermissionService

from ..exceptions import ResourceNotFoundException
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionMembershipService:
    """Service that performs all of the actions on the `Section` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def add_user_oh_memberships(
        self,
        subject: User,
        oh_sections: list[OfficeHoursSectionPartial],
    ) -> list[SectionMember]:
        """Retrieves all sections from the table

        Returns:
            list[SectionDetails]: List of all `SectionDetails`
        """
        # TODO: Permissions
        section_memberships: list[SectionMemberEntity] = []
        for oh_section in oh_sections:
            academic_sections = (
                self._session.query(SectionEntity)
                .filter(SectionEntity.office_hours_id == oh_section.id)
                .all()
            )

            if len(academic_sections) == 0:
                raise Exception("No Academic Section Found")

            section_membership = SectionMemberEntity.from_draft_model(
                user_id=subject.id, section_id=academic_sections[0].id
            )

            self._session.add(section_membership)
            self._session.commit()

            section_memberships.append(section_membership)

        return [
            section_membership.to_flat_model()
            for section_membership in section_memberships
        ]
