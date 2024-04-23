"""
The Section Member Service allows the API to manipulate section member data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...entities.academics.section_member_entity import SectionMemberEntity
from ...models.academics.section_member import (
    SectionMember,
    SectionMemberDraft,
    SectionMemberPartial,
)
from ...models.academics.section_member_details import SectionMemberDetails
from ...models.office_hours.section import (
    OfficeHoursSection,
    OfficeHoursSectionDraft,
    OfficeHoursSectionPartial,
)
from ...models.office_hours.section_details import OfficeHoursSectionDetails
from ...models.roster_role import RosterRole

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

__authors__ = ["Meghan Sun, Sadie Amato"]
__copyright__ = "Copyright 2024"
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

    def get_section_member_by_id(self, id: int) -> SectionMember:
        """Retrieve a section membership by its unique ID.

        Args:
            id (int): The ID of the section membership to retrieve.

        Returns:
            SectionMember: The SectionMember object corresponding to the provided ID.

        Raises:
            ResourceNotFoundException: If no section membership is found with the specified ID.
        """
        query = select(SectionMemberEntity).filter(SectionMemberEntity.id == id)
        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException("Section Membership Not Found for id={id} ")

        return entity.to_flat_model()

    def get_section_member_by_user_id_and_oh_section_id(
        self, subject: User, oh_section_id: int
    ) -> SectionMember:
        """Retrieve a section membership by user ID and office hours section ID.

        Args:
            subject (User): The user for whom to retrieve the section membership.
            oh_section_id (int): The ID of the office hours section.

        Returns:
            SectionMember: The SectionMember object corresponding to the provided user ID and section ID.

        Raises:
            ResourceNotFoundException: If no section membership is found for the user and office hours section.
        """
        query = (
            select(SectionMemberEntity)
            .filter(SectionEntity.office_hours_id == oh_section_id)
            .filter(SectionEntity.id == SectionMemberEntity.section_id)
            .filter(SectionMemberEntity.user_id == subject.id)
        )
        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"Section Membership Not Found for User (id={subject.id}) and Office Hours Section (id={oh_section_id})"
            )

        return entity.to_flat_model()

    def add_user_oh_memberships(
        self,
        subject: User,
        oh_sections: list[OfficeHoursSection],
    ) -> list[SectionMember]:
        """Add section memberships for a user to multiple office hours sections.

        Args:
            subject (User): The user for whom to add section memberships.
            oh_sections (list[OfficeHoursSection]): List of office hours sections to enroll the user into.

        Returns:
            list[SectionMember]: List of newly created SectionMember objects representing the user's memberships.

        Raises:
            ResourceNotFoundException: If no academic section is found for any of the specified office hours sections.
        """

        section_memberships: list[SectionMemberEntity] = []
        for oh_section in oh_sections:
            academic_sections = (
                self._session.query(SectionEntity)
                .filter(SectionEntity.office_hours_id == oh_section.id)
                .all()
            )

            if len(academic_sections) == 0:
                raise ResourceNotFoundException("No Academic Section Found")
            draft = SectionMemberDraft(
                user_id=subject.id, section_id=academic_sections[0].id
            )
            section_membership = SectionMemberEntity.from_draft_model(draft)

            self._session.add(section_membership)
            self._session.commit()

            section_memberships.append(section_membership)

        return [
            section_membership.to_flat_model()
            for section_membership in section_memberships
        ]

    def search_instructor_memberships(self, subject: User) -> list[SectionMemberEntity]:
        """
        Find all instructor memberships for a given user. If not an instructor, returns empty list.

        Args:
            subject (User): The user object representing the user for whom to find memberships.

        Returns:
            List[SectionMemberEntity]: A list of SectionMemberEntity objects representing
                all instructor memberships of the given user.
        """

        query = (
            select(SectionMemberEntity)
            .filter(SectionMemberEntity.user_id == subject.id)
            .filter(SectionMemberEntity.member_role == RosterRole.INSTRUCTOR)
        )
        entities = self._session.scalars(query).all()

        section_memberships = [entity.to_flat_model() for entity in entities]

        return section_memberships
