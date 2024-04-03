"""Service that manages applications for the COMP department"""

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.entities import section_application_table
from backend.entities.application_entity import ApplicationEntity, New_UTA_Entity
from backend.entities.academics.section_entity import SectionEntity
from backend.models.application import Application, New_UTA
from backend.models.application_details import (
    ApplicationDetails,
    New_UTADetails,
    UTADetails,
)
from backend.models.user import User
from ..database import db_session


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

    def create_undergrad(self, application: New_UTADetails) -> New_UTADetails:
        """
        Creates an application based on the input object and adds it to the table.
        If the application's ID is unique to the table, a new entry is added.
        If the application's ID already exists in the table, it raises an error.

        Parameters:
            subject: a valid User model representing the currently logged in User
            application (Application): Application to add to table

        Returns:
            Application: Object added to table
        """

        if application.id:
            application.id = None

        application_entity = New_UTA_Entity.from_model(application)

        self._session.add(application_entity, self._session)
        self._session.flush()  # This will assign an ID to application_entity without committing the transaction

        # Now that application_entity has an ID, you can create the section_application relationships
        for index, section in enumerate(application.preferred_sections):
            # Ensure the section exists in the database and fetch its entity
            section_entity = self._session.query(SectionEntity).filter_by(id=section.id).one()

            # Create the association with position
            association = {
                'section_id': section_entity.id,
                'application_id': application_entity.id,
                'position': index
            }
            self._session.execute(section_application_table.insert().values(**association))

        # Commit the transaction to save the application and its associated sections
        self._session.commit()

        # Convert the application entity back to a Pydantic model and return
        return application_entity.to_details_model()
