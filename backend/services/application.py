"""Service that manages applications for the COMP department"""

from typing import List
from fastapi import Depends
from sqlalchemy import update, delete, select, or_
from sqlalchemy.orm import Session
from typing import Dict
from backend.entities import section_application_table
from backend.entities.application_entity import ApplicationEntity
from backend.entities.academics.hiring.hiring_assignment_entity import (
    HiringAssignmentEntity,
)
from backend.entities.academics.hiring.application_review_entity import (
    ApplicationReviewEntity,
)

from backend.entities.section_application_table import section_application_table
from backend.entities.academics.section_entity import SectionEntity
from backend.entities.academics.term_entity import TermEntity
from backend.entities.user_entity import UserEntity

from backend.models.academics.hiring.hiring_assignment import HiringAssignmentStatus
from backend.models.academics.section import Section, CatalogSectionIdentity
from backend.models.application import Application
from backend.models.user import User

from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)

from .permission import PermissionService

from ..database import db_session
from datetime import datetime

__authors__ = ["Ajay Gandecha", "Abdulaziz Al-Shayef", "Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationService:
    """ApplicationService is the access layer to TA applications."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes a new ApplicationService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session
        self._permission_svc = permission_svc

    def get_application(self, term_id: str, subject: User) -> Application | None:
        """Returns an application for a specific user during a specific term"""
        application_query = select(ApplicationEntity).where(
            ApplicationEntity.user_id == subject.id,
            ApplicationEntity.term_id == term_id,
        )
        application_entity = self._session.scalars(application_query).first()
        # Retrieve any assignments, if made.
        # NOTE: This includes a hard-coded release date of 8/18.
        assignments = []
        release_date = datetime(2025, 1, 9)
        if datetime.now() > release_date:
            assignments_query = (
                select(HiringAssignmentEntity)
                .where(HiringAssignmentEntity.status == HiringAssignmentStatus.FINAL)
                .where(HiringAssignmentEntity.user_id == subject.id)
            )
            assignments_entites = self._session.scalars(assignments_query).all()
            assignments = [
                assignment.to_released_hiring_assignment()
                for assignment in assignments_entites
            ]
        return application_entity.to_model(assignments) if application_entity else None

    def create(self, subject: User, application: Application) -> Application:
        """Creates a new application"""
        # Ensure that users cannot create applications for people other than themselves.
        if subject.id != application.user_id:
            self._permission_svc.enforce(
                subject,
                "applications.create",
                f"applications/{application.id}",
            )

        # Remove the application ID, if it exists
        if application.id:
            application.id = None

        # Create the new application
        application_entity = ApplicationEntity.from_model(application)
        self._session.add(application_entity)
        self._session.commit()

        # Add the user's section preferences to the new application
        for preference, section in enumerate(application.preferred_sections):
            self._session.execute(
                section_application_table.insert().values(
                    {
                        "section_id": section.id,
                        "application_id": application_entity.id,
                        "preference": preference,
                    }
                )
            )
            self._session.commit()  # This is an issue due to the table not being an entity.

        # Return the added data
        return application_entity.to_model()

    def update(self, subject: User, application: Application) -> Application:
        """Updates an application"""
        # Ensure that users cannot create applications for people other than themselves.
        if subject.id != application.user_id:
            self._permission_svc.enforce(
                subject,
                "applications.update",
                f"applications/{application.id}",
            )

        # Ensures that the application exists.
        application_query = select(ApplicationEntity).where(
            ApplicationEntity.id == application.id
        )
        application_entity = self._session.scalars(application_query).first()

        if application_entity is None:
            raise ResourceNotFoundException(
                f"Cannot update an application that does not exist."
            )

        # Update the application
        application_entity.extracurriculars = application.extracurriculars
        application_entity.expected_graduation = application.expected_graduation
        application_entity.program_pursued = application.program_pursued
        application_entity.other_programs = application.other_programs
        application_entity.gpa = application.gpa
        application_entity.comp_gpa = application.comp_gpa
        application_entity.comp_227 = application.comp_227
        application_entity.intro_video_url = application.intro_video_url
        application_entity.prior_experience = application.prior_experience
        application_entity.service_experience = application.service_experience
        application_entity.additional_experience = application.additional_experience
        application_entity.ta_experience = application.ta_experience
        application_entity.best_moment = application.best_moment
        application_entity.desired_improvement = application.desired_improvement
        application_entity.advisor = application.advisor

        # Save changes
        self._session.commit()

        # Update the user's section preferences
        self._session.execute(
            delete(section_application_table).filter(
                section_application_table.c.application_id == application.id
            )
        )
        self._session.commit()

        # Add the user's section preferences to the new application
        for preference, section in enumerate(application.preferred_sections):
            self._session.execute(
                section_application_table.insert().values(
                    {
                        "section_id": section.id,
                        "application_id": application_entity.id,
                        "preference": preference,
                    }
                )
            )
            self._session.commit()  # This is an issue due to the table not being an entity.

        # Return the modified data
        return application_entity.to_model()

    def delete(self, application_id: int, subject: User) -> None:
        """Deletes an application."""
        # Ensure that only admins can delete applications.
        self._permission_svc.enforce(
            subject,
            "applications.delete",
            f"applications/{application_id}",
        )

        # Find the original application
        application_query = select(ApplicationEntity).where(
            ApplicationEntity.id == application_id
        )
        application_entity = self._session.scalars(application_query).first()

        if application_entity is None:
            raise ResourceNotFoundException(
                f"Cannot update an application that does not exist."
            )

        # Delete the application and save
        self._session.delete(application_entity)
        self._session.commit()

    def eligible_sections(self) -> list[CatalogSectionIdentity]:
        """
        Returns the eligible sections for the current active application term.
        """
        term_query = select(TermEntity).where(
            TermEntity.applications_open <= datetime.now(),
            datetime.now() <= TermEntity.applications_close,
        )
        term_entities = self._session.scalars(term_query).all()
        return (
            [
                section.to_catalog_identity_model()
                for section in term_entities[0].course_sections
            ]
            if len(term_entities) > 0
            else []
        )
