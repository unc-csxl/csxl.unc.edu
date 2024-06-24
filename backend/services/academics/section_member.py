"""
The Section Member Service allows the API to manipulate section member data in the database.
"""

from io import StringIO
import csv

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pydantic import BaseModel

from ...entities.academics.section_member_entity import SectionMemberEntity
from ...models.academics.section_member import (
    SectionMember,
    SectionMemberDraft,
)
from ...models.academics.section_member_details import SectionMemberDetails
from ...models.office_hours.course_site import CourseSite
from ...models.roster_role import RosterRole

from ...database import db_session
from ...models import User
from ...entities.academics import SectionEntity
from ...entities import UserEntity
from ..permission import PermissionService

from ..exceptions import ResourceNotFoundException, CoursePermissionException

__authors__ = ["Meghan Sun, Sadie Amato", "Ajay Gandecha"]
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
        oh_sections: list[CourseSite],
    ) -> list[SectionMember]:
        """Add section memberships for a user to multiple office hours sections.

        Args:
            subject (User): The user for whom to add section memberships.
            oh_sections (list[CourseSite]): List of office hours sections to enroll the user into.

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

    def import_users_from_csv(self, subject: User, section_id: int, csv_data: str):
        """
        Creates section members for a course section based on an inputted CSV file.
        """
        # Get the user membership of the course
        membership_query = select(SectionMemberEntity).where(
            SectionMemberEntity.user_id == subject.id,
            SectionMemberEntity.section_id == section_id,
        )
        membership_entity = self._session.scalars(membership_query).one_or_none()

        # Ensure the user is an instructor in the course
        if (
            membership_entity is None
            or membership_entity.member_role != RosterRole.INSTRUCTOR
        ):
            raise CoursePermissionException(
                "Cannot create students for a course you are not an instructor of."
            )

        # Read the csv data
        file = StringIO(csv_data)
        reader = csv.DictReader(file)

        # Parse each row
        students: list[StudentMemberJson] = []

        try:
            for row in reader:
                if reader.line_num != 2:
                    name = row["Student"]
                    pid = int(row["SIS User ID"])
                    onyen = row["SIS Login ID"]
                    students.append(StudentMemberJson(name=name, pid=pid, onyen=onyen))
        except:
            raise HTTPException(
                status_code=422, detail="CSV is not formatted correctly."
            )

        student_pids = [student.pid for student in students]

        # There are three cases:
        #  Case 1: Student is already on the roster - we do not need to make any changes.
        #  Case 2: Students are not on the roster, but user profiles exist - just add a SectionMemberEntity.
        #  Case 3: User is not in the system - create a user and a relationship.

        # Case 1: Determine students that are already on the roster
        existing_roster_members_query = (
            select(SectionMemberEntity)
            .join(UserEntity)
            .where(UserEntity.pid.in_(student_pids))
            .where(SectionMemberEntity.section_id == section_id)
        )
        existing_roster_member_entities = self._session.scalars(
            existing_roster_members_query
        ).all()
        existing_roster_member_pids = [
            member.pid for member in existing_roster_member_entities
        ]

        # Case 2: Determine students that are not on the roster, but that exist in the database.
        existing_users_query = select(UserEntity).where(
            UserEntity.pid.in_(student_pids),
            UserEntity.pid.not_in(existing_roster_member_pids),
        )
        existing_user_entities = self._session.scalars(existing_users_query).all()
        existing_users_pids = [member.pid for member in existing_user_entities]
        for user in existing_user_entities:
            draft = SectionMemberDraft(user_id=user.id, section_id=section_id)
            section_membership = SectionMemberEntity.from_draft_model(draft)
            self._session.add(section_membership)

        # Case 3: Find remaining students that do not exist
        nonexisting_students = [
            student for student in students if student.pid not in existing_users_pids
        ]
        new_student_entities = []

        for student in nonexisting_students:
            name_segments = student.name.split(",")
            last_name = name_segments[0].strip() if len(name_segments) > 0 else ""
            first_name = name_segments[1].strip() if len(name_segments) > 1 else ""
            new_student = User(
                pid=student.pid,
                onyen=student.onyen,
                first_name=first_name,
                last_name=last_name,
                email=f"{student.onyen}@ad.unc.edu",
            )
            new_student_entity = UserEntity.from_model(new_student)
            new_student_entities.append(new_student_entity)
            self._session.add(new_student_entity)

        # Commit to save new students
        self._session.commit()

        # Finish Case 3, adding memberships for new members
        for new_student in new_student_entities:
            draft = SectionMemberDraft(user_id=new_student.id, section_id=section_id)
            section_membership = SectionMemberEntity.from_draft_model(draft)
            self._session.add(section_membership)

        # Commit changes a final time
        self._session.commit()


class CSVModel(BaseModel):
    csv_data: str


class StudentMemberJson(BaseModel):
    name: str
    pid: int
    onyen: str
