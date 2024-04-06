"""Service that manages applications for the COMP department"""

from fastapi import Depends
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
            raise ResourceNotFoundException(f"Application does not exist")

        application = application_entity.to_details_model()

        subquery = (
            self._session.query(section_application_table)
            .filter(section_application_table.c.application_id == application.id)
            .order_by(section_application_table.c.preference)
            .all()
        )

        section_ids = [section[1] for section in subquery]

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

        existing_sections = []

        for section in application.preferred_sections:
            existing_sections.append(
                self._session.query(SectionEntity)
                .filter(SectionEntity.id == section.id)
                .first()
            )

        application_entity.preferred_sections = existing_sections

        # This for loop forces the objects to be loaded by the ORM, this process establishes the correct order of preferences.
        for section in application_entity.preferred_sections:
            section.to_model()

        self._session.add(application_entity)
        self._session.commit()

        return application_entity.to_details_model()

        if application.id:
            application.id = None

        application_entity = New_UTA_Entity.from_model(application)

        existing_sections = []

        for section in application.preferred_sections:
            existing_sections.append(
                self._session.query(SectionEntity)
                .filter(SectionEntity.id == section.id)
                .first()
            )

        application_entity.preferred_sections = existing_sections

        # This for loop forces the objects to be loaded by the ORM, this process establishes the correct order of preferences.
        for section in application_entity.preferred_sections:
            section.to_model()

        self._session.add(application_entity)
        self._session.commit()

        # for section in application.preferred_sections:
        #     existing_sections.append(
        #         self._session.query(SectionEntity)
        #         .filter(SectionEntity.id == section.id)
        #         .first()
        #     )
        for index, section in enumerate(application.preferred_sections):
            print("66666666666")
            # existing_sections.append(
            #     self._session.query(SectionEntity)
            #     .filter(SectionEntity.id == section.id)
            #     .first()
            # )
            print("7777777777777")

            association = {
                "preference": index,
                "section_id": section.id,
                "application_id": application_entity.id,
            }
            print("88888888888")
            self._session.execute(
                section_application_table.update().values(**association)
            )
            print("9999999999999")

        self._session.commit()

        return application_entity.to_details_model()

    def update_undergrad(
        self, subject: User, application: New_UTADetails
    ) -> New_UTADetails:
        """
        Updates an application for a user based on the input object and adds it to the table.
        We have to delete the original application and create a new entry with how current ordinaility is working.
        The application id must exist or an error is raised.

        Parameters:
            subject (User): The User that would like to update their applicaiton
            application (New_UTADetails: The Applicaiton with the updated values

        Returns:
            New_UTADetails: Updated application
        """

        original_application = (
            self._session.query(ApplicationEntity)
            .filter(ApplicationEntity.user_id == subject.id)
            .first()
        )

        if original_application is None:
            raise ResourceNotFoundException(f"Application does not exist")

        self._session.delete(original_application)
        self._session.commit()

        return self.create_undergrad(application)
