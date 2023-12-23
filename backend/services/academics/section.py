"""
The Section Service allows the API to manipulate sections data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...database import db_session
from ...models.academics import Section
from ...models.academics import SectionDetails
from ...models.user import User
from ...entities.academics import SectionEntity
from ...entities.academics import CourseEntity
from ..permission import PermissionService

from ...services.exceptions import ResourceNotFoundException
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
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def all(self) -> list[SectionDetails]:
        """Retrieves all sections from the table

        Returns:
            list[SectionDetails]: List of all `SectionDetails`
        """
        # Select all entries in `Section` table
        query = select(SectionEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_details_model() for entity in entities]

    def get_by_term(self, term_id: str) -> list[SectionDetails]:
        """Retrieves all sections from the table by a term.

        Args:
            term_id: ID of the term to query by.
        Returns:
            list[SectionDetails]: List of all `SectionDetails`
        """
        # Select all entries in the `Section` tabl
        query = select(SectionEntity).where(SectionEntity.term_id == term_id)
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_details_model() for entity in entities]

    def get_by_subject(self, subject_code: str) -> list[SectionDetails]:
        """Retrieves all sections from the table by subject code.

        Args:
            subject_code: subject to query by.
        Returns:
            list[SectionDetails]: List of all `SectionDetails`
        """
        # Select all entries in the `Section` table
        query = (
            select(SectionEntity)
            .join(CourseEntity)
            .where(CourseEntity.subject_code == subject_code)
        )
        entities = self._session.scalars(query).all()

        # Return the model
        return [entity.to_details_model() for entity in entities]

    def get_by_id(self, id: int) -> SectionDetails:
        """Gets the section from the table for an id.

        Args:
            id: ID of the section to retrieve.
        Returns:
            SectionDetails: Section based on the id.
        """
        # Select all entries in the `Section` table and sort by end date
        query = select(SectionEntity).filter(SectionEntity.id == id)
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(f"Section with id: {id} does not exist.")

        # Return the model
        return entity.to_details_model()

    def get(
        self, subject_code: str, course_number: str, section_number: str
    ) -> SectionDetails:
        """Gets a course based on its subject code, course number, and section number.

        Args:
            subject_code: Subject code to query by (ex. COMP)
            course_number: Course number to query by (ex. 110 in COMP 110)
            section_number: Section number to query by (ex. 003 in COMP 110-003)
        Returns:
            SectionDetails: Section for the parameters.
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
        return entity.to_details_model()

    def create(self, subject: User, section: Section) -> SectionDetails:
        """Creates a new section.

        Args:
            subject: a valid User model representing the currently logged in User
            section: Section to add to table

        Returns:
            SectionDetails: Object added to table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "courses.section.create", f"section/")

        # Create new object
        section_entity = SectionEntity.from_model(section)

        # Add new object to table and commit changes
        self._session.add(section_entity)
        self._session.commit()

        # Return added object
        return section_entity.to_details_model()

    def update(self, subject: User, section: Section) -> SectionDetails:
        """Updates a section.

        Args:
            subject: a valid User model representing the currently logged in User
            section: Section to update

        Returns:
            SectionDetails: Object updated in the table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "courses.section.update", f"section/{section.id}"
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

        # Commit changes
        self._session.commit()

        # Return edited object
        return section_entity.to_details_model()

    def delete(self, subject: User, section: Section) -> None:
        """Deletes a section.

        Args:
            subject: a valid User model representing the currently logged in User
            section: Section to delete
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "courses.section.delete", f"section/{section.id}"
        )

        # Find the entity to delete
        section_entity = self._session.get(SectionEntity, section.id)

        # Raise an error if no entity was found
        if section_entity is None:
            raise ResourceNotFoundException(
                f"Section with id: {section.id} does not exist."
            )

        # Delete and commit changes
        self._session.delete(section_entity)
        self._session.commit()
