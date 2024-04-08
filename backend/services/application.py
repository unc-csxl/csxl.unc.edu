"""Service that manages applications for the COMP department"""

from fastapi import Depends
from sqlalchemy import update, delete, insert
from sqlalchemy.orm import Session
from backend.entities import section_application_table
from backend.entities.application_entity import ApplicationEntity, New_UTA_Entity
from backend.entities.section_application_table import section_application_table
from backend.entities.academics.section_entity import SectionEntity
from backend.models.application import Application, New_UTA
from backend.models.application_details import (
    ApplicationDetails,
    New_UTADetails,
    UTADetails,
    UserApplication,
)
from backend.models.user import User

from backend.services.exceptions import ResourceNotFoundException

from ..database import db_session

from typing import List


__authors__ = ["Ben Goulet"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationService:
    """ApplicationService is the access layer to TA applications."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes a new ApplicationService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session

    def list(self) -> list[New_UTADetails]:
        """Returns all TA applications.

        Returns:
            list[New_UTA]: List of all current and previously submitted applications.
        """
        entities = self._session.query(ApplicationEntity).all()

        return [entity.to_details_model() for entity in entities]

        # implement list() for all types here later

        # applications = []

        # for entity in entities:
        #     if entity.type == "new_uta": # type: ignore
        #         applications.append(
        #             entity.to_details_model()
        #         )
        #     elif entity.type == "returning_uta":
        #         applications.append(entity.to_details_model())
        #     elif entity.type == "uta":
        #         applications.append(entity.to_details_model())
        #     else:
        #         applications.append(entity.to_model())

        # return applications

    def get_application(self, subject: User) -> UserApplication:
        """Returns application(s) for a specific user

        Returns:
            list[Application]: List of all current applications for a specific user
        """

        application_entity = (
            self._session.query(ApplicationEntity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if application_entity is None:
            return None

        application = application_entity.to_details_model()

        sections = (
            self._session.query(section_application_table)
            .filter(section_application_table.c.application_id == application.id)
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

        return UserApplication(application=application, preferences=section_dict)

    def create_undergrad(self, application: New_UTADetails) -> New_UTADetails:
        """
        Creates an application based on the input object and adds it to the table.
        If the application's ID is unique to the table, a new entry is added.
        If the application's ID already exists in the table, it raises an error.

        Parameters:
            application (New_UTADetails): A new UTA application to add to table

        Returns:
            Application: Object added to table
        """

        if application.id:
            application.id = None

        application_entity = New_UTA_Entity.from_model(application)

        application_entity.preferred_sections = (
            self._session.query(SectionEntity)
            .filter(
                SectionEntity.id.in_(
                    section.id for section in application.preferred_sections
                )
            )
            .all()
        )
        # for index, preferred_section in enumerate(
        #     application_entity.preferred_sections
        # ):
        #     preferred_section.preference = index

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

    def update_undergrad(
        self, subject: User, application: New_UTADetails
    ) -> New_UTADetails:
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
            self._session.query(New_UTA_Entity)
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
            self._session.query(New_UTA_Entity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if original_application is None:
            raise ResourceNotFoundException(f"Application does not exist")

        self._session.delete(original_application)
        self._session.commit()
