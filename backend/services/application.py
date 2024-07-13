"""Service that manages applications for the COMP department"""

from typing import List
from fastapi import Depends
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from typing import Dict
from backend.entities import section_application_table
from backend.entities.application_entity import (
    ApplicationEntity,
    NewUTAApplicationEntity,
)
from backend.entities.section_application_table import section_application_table
from backend.entities.academics.section_entity import SectionEntity
from backend.entities.user_entity import UserEntity

from backend.models.academics.section import Section
from backend.models.application import SectionApplicant

from backend.models.application_details import (
    UTAApplicationDetails,
    NewUTAApplicationDetails,
)
from backend.models.user import User

from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)

from .permission import PermissionService

from ..database import db_session

__authors__ = ["Ben Goulet, Abdulaziz Al-Shayef"]
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

    def get_application(self, subject: User) -> NewUTAApplicationDetails:
        """Returns an application for a specific user during a specific term

        Returns:
            list[Application]: List of all current applications for a specific user


        This method currently returns the first application that is found in the table, however
        future implementation will be taking the current term into consideration and querying based off
        of that term. If a user doesn't have an application during that term then None would be returned.
        """

        application_entity = (
            self._session.query(ApplicationEntity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if application_entity is None:
            return None

        sections = (
            self._session.query(section_application_table)
            .filter(section_application_table.c.application_id == application_entity.id)
            .order_by(section_application_table.c.preference)
            .all()
        )

        section_ids = [section[1] for section in sections]

        sections_entity = []
        for id in section_ids:
            sections_entity.append(
                self._session.query(SectionEntity)
                .filter(SectionEntity.id == id)
                .first()
            )

        section_dict = {
            i: section.to_model() for i, section in enumerate(sections_entity)
        }

        application = application_entity.map_application_to_detail_model(section_dict)

        return application

    def get_applications_for_section(
        self, section_id: int, subject: User
    ) -> list[SectionApplicant]:

        self._permission_svc.enforce(
            subject,
            "applications.get",
            f"applications/",
        )
        section_applicants = (
            self._session.query(section_application_table)
            .filter(section_application_table.c.section_id == section_id)
            .order_by(section_application_table.c.preference)
            .all()
        )

        applicants: list[SectionApplicant] = []

        for applicant in section_applicants:
            application = (
                self._session.query(ApplicationEntity)
                .filter(ApplicationEntity.id == applicant[2])
                .first()
            )
            application_model = application = application.to_model()
            user = (
                self._session.query(UserEntity)
                .filter(UserEntity.id == application_model.user_id)
                .first()
            )
            applicants.append(
                SectionApplicant(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    preference_rank=applicant[0],
                    application=application_model,
                )
            )

        return applicants

    def create_uta_application(
        self, subject: User, application: NewUTAApplicationDetails
    ) -> NewUTAApplicationDetails:
        """
        Creates an application based on the input object and adds it to the table.
        If the application's ID is unique to the table, a new entry is added.
        If the application's ID already exists in the table, it raises an error.

        Parameters:
            application (New_UTADetails): A new UTA application to add to table

        Returns:
            Application: Object added to table
        """

        if subject.id != application.user_id:
            self._permission_svc.enforce(
                subject,
                "applications.create",
                f"applications/{application.id}",
            )

        if application.id:
            application.id = None

        application_entity = NewUTAApplicationEntity.from_model(application)

        application_entity.preferred_sections = (
            self._session.query(SectionEntity)
            .filter(
                SectionEntity.id.in_(
                    section.id for section in application.preferred_sections
                )
            )
            .all()
        )

        self._session.add(application_entity)
        self._session.commit()

        for index, section in enumerate(application.preferred_sections):

            self._session.execute(
                update(section_application_table)
                .filter(
                    section_application_table.c.application_id == application_entity.id,
                    section_application_table.c.section_id == section.id,
                )
                .values(preference=index)
            )

        self._session.commit()

        return application_entity.to_details_model()

    def update_uta_application(
        self, subject: User, application: NewUTAApplicationDetails
    ) -> NewUTAApplicationDetails:
        """
        Updates an application for a user based on the application sent in.
        The application id must exist or an error is raised.

        Parameters:
            subject (User): The User that would like to update their application
            application (New_UTADetails: The Application with the updated values

        Returns:
            New_UTADetails: Updated application
        """

        original_application = (
            self._session.query(NewUTAApplicationEntity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if original_application is None:
            raise ResourceNotFoundException(f"Application does not exist")

        self._session.execute(
            delete(section_application_table).filter(
                section_application_table.c.application_id == original_application.id
            )
        )

        original_application.update(
            application,
            self._session.query(SectionEntity)
            .filter(
                SectionEntity.id.in_(
                    section.id for section in application.preferred_sections
                )
            )
            .all(),
        )

        self._session.commit()

        for index, section in enumerate(application.preferred_sections):

            self._session.execute(
                update(section_application_table)
                .filter(
                    section_application_table.c.application_id
                    == original_application.id,
                    section_application_table.c.section_id == section.id,
                )
                .values(preference=index)
            )
        self._session.commit()

        return original_application.to_details_model()

    def delete_application(self, subject: User) -> None:
        """
        Deletes an application from the Application table.
        Raises an error if user doesn't have an associated application.
        """

        original_application = (
            self._session.query(NewUTAApplicationEntity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if original_application is None:
            raise ResourceNotFoundException(f"Application does not exist")

        self._session.delete(original_application)
        self._session.commit()
