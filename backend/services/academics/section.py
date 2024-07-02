"""
The Section Service allows the API to manipulate sections data in the database.
"""

import requests
from bs4 import BeautifulSoup

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...database import db_session
from ...models.academics import Section, CatalogSection
from ...models.academics import SectionDetails
from ...models.academics.section import EditedSection
from ...models.roster_role import RosterRole
from ...models import User, Room
from ...models.room_assignment_type import RoomAssignmentType
from ...entities.academics import SectionEntity, SectionMemberEntity
from ...entities.academics import CourseEntity
from ...entities.academics import SectionRoomEntity
from ..permission import PermissionService

from ...services.academics.section_member import SectionMemberService

from ...services.exceptions import (
    ResourceNotFoundException,
    CourseDataScrapingException,
)
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class SectionService:
    """Service that performs all of the actions on the `Section` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
        section_member_svc: SectionMemberService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc
        self._section_member_svc = section_member_svc

    def get_by_term(self, term_id: str) -> list[CatalogSection]:
        """Retrieves all sections from the table by a term.

        Args:
            term_id: ID of the term to query by.
        Returns:
            list[CatalogSection]: List of all `CatalogSection`
        """
        # Select all entries in the section table
        query = (
            select(SectionEntity)
            .where(SectionEntity.term_id == term_id)
            .order_by(SectionEntity.course_id, SectionEntity.number)
        )
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_catalog_model() for entity in entities]

    def get_by_id(self, id: int) -> Section:
        """Gets the section from the table for an id.

        Args:
            id: ID of the section to retrieve.
        Returns:
            CatalogSection: Section based on the id.
        """
        # Select all entries in the `Section` table and sort by end date
        query = select(SectionEntity).filter(SectionEntity.id == id)
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(f"Section with id: {id} does not exist.")

        # Return the model
        return entity.to_model()

    def get(
        self, subject_code: str, course_number: str, section_number: str
    ) -> CatalogSection:
        """Gets a course based on its subject code, course number, and section number.

        Args:
            subject_code: Subject code to query by (ex. COMP)
            course_number: Course number to query by (ex. 110 in COMP 110)
            section_number: Section number to query by (ex. 003 in COMP 110-003)
        Returns:
            CatalogSection: Section for the parameters.
        """
        # Select all entries in the `Section` table that contains this date.
        query = (
            select(SectionEntity)
            .where(SectionEntity.number == section_number)
            .join(CourseEntity)
            .where(
                CourseEntity.subject_code == subject_code,
                CourseEntity.number == course_number,
            )
        )
        entity = self._session.scalars(query).one_or_none()

        # Rause an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(
                f"No section found for the given subject and number: {subject_code} {course_number}-{section_number}."
            )

        # Return the model
        return entity.to_catalog_model()

    def create(self, subject: User, section: EditedSection) -> SectionDetails:
        """Creates a new section.

        Args:
            subject: a valid User model representing the currently logged in User
            section: Section to add to table

        Returns:
            SectionDetails: Object added to table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "academics.section.create", f"section/")

        # Create new object
        section_entity = SectionEntity.from_edited_model(section)

        # Add new object to table and commit changes
        self._session.add(section_entity)

        self._session.commit()

        # Find added object
        added_section = section_entity.to_details_model()

        # Now, attempt to add the lecture room
        if section.lecture_room is not None:
            # Check if user has admin permissions
            self._permission_svc.enforce(
                subject, "academics.section.create", f"section/"
            )

            # Then, attempt to create room relation
            section_room_entity = SectionRoomEntity(
                section_id=added_section.id,
                room_id=section.lecture_room.id,
                assignment_type=RoomAssignmentType.LECTURE_ROOM,
            )
            self._session.add(section_room_entity)
            self._session.commit()

        # Add the instructors.
        for instructor in section.instructors:
            self._section_member_svc.add_section_member(
                subject, section.id, instructor.id, RosterRole.INSTRUCTOR
            )

        # Now, refresh the data and return.
        return self._session.get(SectionEntity, added_section.id).to_details_model()

    def update(self, subject: User, section: EditedSection) -> SectionDetails:
        """Updates a section.

        Args:
            subject: a valid User model representing the currently logged in User
            section: Section to update

        Returns:
            SectionDetails: Object updated in the table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "academics.section.update", f"section/{section.id}"
        )

        # Find the entity to update
        section_entity = self._session.get(SectionEntity, section.id)

        # Raise an error if no entity was found
        if section_entity is None:
            raise ResourceNotFoundException(
                f"Section with id: {section.id} does not exist."
            )

        # Update the entity
        section_entity.course_id = section.course_id
        section_entity.number = section.number
        section_entity.term_id = section.term_id
        section_entity.meeting_pattern = section.meeting_pattern
        section_entity.override_title = section.override_title
        section_entity.override_description = section.override_description

        query = select(SectionRoomEntity).where(
            SectionRoomEntity.section_id == section.id,
            SectionRoomEntity.assignment_type == RoomAssignmentType.LECTURE_ROOM,
        )
        section_room_entity = self._session.scalars(query).one_or_none()

        if section.lecture_room is not None:
            if section_room_entity is not None:
                section_room_entity.room_id = section.lecture_room.id
            else:
                section_room_entity = SectionRoomEntity(
                    section_id=section.id,
                    room_id=section.lecture_room.id,
                    assignment_type=RoomAssignmentType.LECTURE_ROOM,
                )
                self._session.add(section_room_entity)

        # Change instructors
        instructors_query = select(SectionMemberEntity).where(
            SectionMemberEntity.section_id == section.id,
            SectionMemberEntity.member_role == RosterRole.INSTRUCTOR,
        )

        existing_instructors = self._session.scalars(instructors_query).all()

        for instructor in existing_instructors:
            self._session.delete(instructor)

        for new_instructor in section.instructors:
            self._section_member_svc.add_section_member(
                subject,
                section.id,
                new_instructor.id,
                member_role=RosterRole.INSTRUCTOR,
            )

        # Commit changes
        self._session.commit()

        # Return edited object
        return section_entity.to_details_model()

    def delete(self, subject: User, id: int) -> None:
        """Deletes a section.

        Args:
            subject: a valid User model representing the currently logged in User
            id: ID of section to delete
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "academics.section.delete", f"section/{id}"
        )

        # Find the entity to delete
        section_entity = self._session.get(SectionEntity, id)

        # Raise an error if no entity was found
        if section_entity is None:
            raise ResourceNotFoundException(f"Section with id: {id} does not exist.")

        # Delete and commit changes
        self._session.delete(section_entity)
        self._session.commit()

    def update_enrollment_totals(self, subject: User):
        """
        Updates the enrollment totals for COMP course sections in the database.
        """
        # Currently active terms.
        # This is hard-coded based on the availability and representation
        # of course enrollment data from UNC's course database.
        AVAILABLE_TERMS = {"2024+Summer+II": "SuII24", "2024+Fall": "F24"}

        # Store updates to make.
        updates: dict[tuple[str, str], SectionEnrollmentData] = {}

        # Update enrolllment totals for every available term.
        for term in list(AVAILABLE_TERMS.keys()):
            try:
                # Retrieve the data from the UNC Reports site
                html = requests.get(
                    f"https://reports.unc.edu/class-search/tiled/?subject=COMP&term={term}"
                ).content

                # Create HTML parser
                soup = BeautifulSoup(html, "html.parser")

                # Find cards
                cards = soup.find_all("div", class_="card")

                # Iterate over all course cards
                for card in cards:
                    # Find the course code and section number from title <h2>
                    title_components = card.find("h2").text.split(" ")
                    subject_code = title_components[0]
                    course_number = title_components[2]
                    section_number = title_components[3]

                    # Find the available seats
                    seat_status = (
                        card.find("p", class_="card-available-seats")
                        .text.strip()
                        .split(" ")[0]
                        .split("/")
                    )
                    remaining_seats = seat_status[0]
                    total_seats = seat_status[1]

                    # Find section to update
                    course_id = subject_code.lower() + course_number

                    # Add items to list to update
                    updates[(course_id, section_number)] = SectionEnrollmentData(
                        enrolled=int(total_seats) - int(remaining_seats),
                        total_seats=int(total_seats),
                    )

                # Make updates for the term
                course_ids = list(set([update[0] for update in list(updates.keys())]))
                section_numbers = list(
                    set([update[1] for update in list(updates.keys())])
                )
                sections_query = select(SectionEntity).where(
                    SectionEntity.term_id == AVAILABLE_TERMS[term],
                    SectionEntity.course_id.in_(course_ids),
                    SectionEntity.number.in_(section_numbers),
                )

                section_entities = self._session.scalars(sections_query).all()

                # For every section, update the data
                for section_entity in section_entities:
                    if (section_entity.course_id, section_entity.number) in updates:
                        new_enrollment_data = updates[
                            (section_entity.course_id, section_entity.number)
                        ]
                        section_entity.enrolled = new_enrollment_data.enrolled
                        section_entity.total_seats = new_enrollment_data.total_seats

                # Save changes
                self._session.commit()
            except:
                raise CourseDataScrapingException(
                    f"Error reading COMP data from UNC's database for term: {term}"
                )


class SectionEnrollmentData(BaseModel):
    enrolled: int
    total_seats: int
