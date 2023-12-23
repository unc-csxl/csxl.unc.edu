"""
The Course Service allows the API to manipulate courses data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...database import db_session
from ...models.academics import Course
from ...models.academics import CourseDetails
from ...models.user import User
from ...entities.academics import CourseEntity
from ..permission import PermissionService

from ...services.exceptions import ResourceNotFoundException
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class CourseService:
    """Service that performs all of the actions on the `Course` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def all(self) -> list[CourseDetails]:
        """Retrieves all courses from the table

        Returns:
            list[CourseDetails]: List of all `CourseDetails`
        """
        # Select all entries in `Course` table
        query = select(CourseEntity)

        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_details_model() for entity in entities]

    def get_by_id(self, id: str) -> CourseDetails:
        """Gets the course from the table for an id.

        Args:
            id: ID of the course to retrieve.
        Returns:
            CourseDetails: Course based on the id.
        """
        # Select all entries in the `Course` table and sort by end date
        query = select(CourseEntity).filter(CourseEntity.id == id)
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(f"Course with id: {id} does not exist.")

        # Return the model
        return entity.to_details_model()

    def get(self, subject_code: str, number: str) -> CourseDetails:
        """Gets a course based on its subject code and course number.

        Args:
            subject_code: Subject code to query by (ex. COMP)
            number: Course number to query by (ex. 110 in COMP 110)
        Returns:
            CourseDetails: Course for the parameters.
        """
        # Select all entries in the `Course` table that contains this date.
        query = select(CourseEntity).where(
            CourseEntity.subject_code == subject_code, CourseEntity.number == number
        )
        entity = self._session.scalars(query).one_or_none()

        # Rause an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(
                f"No course found for the given subject and number: {subject_code} {number}."
            )

        # Return the model
        return entity.to_details_model()

    def create(self, subject: User, course: Course) -> CourseDetails:
        """Creates a new course.

        Args:
            subject: a valid User model representing the currently logged in User
            course: Course to add to table

        Returns:
            CourseDetails: Object added to table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "courses.course.create", f"course/")

        # Create new object
        course_entity = CourseEntity.from_model(course)

        # Add new object to table and commit changes
        self._session.add(course_entity)
        self._session.commit()

        # Return added object
        return course_entity.to_details_model()

    def update(self, subject: User, course: Course) -> CourseDetails:
        """Updates a course.

        Args:
            subject: a valid User model representing the currently logged in User
            course: Course to update

        Returns:
            CourseDetails: Object updated in the table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "courses.course.update", f"course/{course.id}"
        )

        # Find the entity to update
        course_entity = self._session.get(CourseEntity, course.id)

        # Raise an error if no entity was found
        if course_entity is None:
            raise ResourceNotFoundException(
                f"Course with id: {course.id} does not exist."
            )

        # Update the entity
        course_entity.subject_code = course.subject_code
        course_entity.number = course.number
        course_entity.title = course.title
        course_entity.description = course.description

        # Commit changes
        self._session.commit()

        # Return edited object
        return course_entity.to_details_model()

    def delete(self, subject: User, course: Course) -> None:
        """Deletes a course.

        Args:
            subject: a valid User model representing the currently logged in User
            course: Course to delete
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "courses.course.delete", f"course/{course.id}"
        )

        # Find the entity to delete
        course_entity = self._session.get(CourseEntity, course.id)

        # Raise an error if no entity was found
        if course_entity is None:
            raise ResourceNotFoundException(
                f"Course with id: {course.id} does not exist."
            )

        # Delete and commit changes
        self._session.delete(course_entity)
        self._session.commit()
