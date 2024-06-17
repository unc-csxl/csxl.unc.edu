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
)
from ...models.academics.section_member_details import SectionMemberDetails
from ...models.roster_role import RosterRole

from ...database import db_session
from ...models import User
from ...entities.academics import SectionEntity
from ..permission import PermissionService

from ..exceptions import ResourceNotFoundException

__authors__ = ["Meghan Sun, Sadie Amato"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class SectionMemberService:
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

    def add_section_member(
        self, subject: User, section_id: int, user_id: int, member_role: RosterRole
    ) -> SectionMemberDetails:
        """Add one member to a section

        Args:
            subject (User): The user for whom to add section memberships.
            section_id (int): ID of the section to add a member to.
            user_id (int): ID of the user to add a member to.

        Returns:
            SectionMember: Newly created section member.

        Raises:
            ResourceNotFoundException: If no academic section is found for any of the specified office hours sections.
        """
        self._permission_svc.enforce(
            subject, "academics.section_member.create", f"section/{section_id}"
        )

        draft = SectionMemberDraft(
            user_id=user_id, section_id=section_id, member_role=member_role
        )
        section_membership = SectionMemberEntity.from_draft_model(draft)

        self._session.add(section_membership)
        self._session.commit()

        return section_membership.to_details_model()

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
