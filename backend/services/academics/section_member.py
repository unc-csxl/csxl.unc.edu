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
from ...models.office_hours.course_site import (
    OfficeHoursSection,
)
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

    def add_user_section_memberships_by_oh_sections(
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

            # Check If Membership Exists
            membership = (
                self._session.query(SectionMemberEntity)
                .where(SectionMemberEntity.user_id == subject.id)
                .where(SectionEntity.office_hours_id == oh_section.id)
                .where(SectionMemberEntity.section_id == SectionEntity.id)
                .one_or_none()
            )

            if membership is not None:
                raise Exception(
                    f"User is already a member of office hours section id={oh_section.id}"
                )

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
