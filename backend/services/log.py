"""
The Logs Service allows the API to manipulate the audit log in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.services.exceptions import ResourceNotFoundException

from ..database import db_session
from ..models.log import Log, LogDetails
from ..entities.log_entity import LogEntity
from ..models import User

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class LogService:
    """Service that performs all of the actions on the `Log` table"""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `LogService` session"""
        self._session = session

    def all(self) -> list[LogDetails]:
        """
        Retrieves all organizations from the table

        Returns:
            list[Log]: List of all `Log`s
        """
        # Select all entries in `Organization` table
        query = select(LogEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_detail_model() for entity in entities]

    def create(self, subject: User | None, log_message: str) -> LogDetails | None:
        """
        Creates a organization based on the input object and adds it to the table.

        Parameters:
            subject: a valid User model representing the currently logged in User
            log (Log): Log to add to table

        Returns:
            Log: Object added to table
        """

        # First, ensure that a valid user exists
        # (unauthenticated users cannot add to log)
        # NOTE: This has been added a safeguard but should never run
        # because permission errors would occur before this runs.
        if not subject or not subject.id:
            raise ResourceNotFoundException("User not found.")

        # Create log
        log = Log(description=log_message, user_id=subject.id)
        log_entity = LogEntity.from_model(log)

        # Add to session
        self._session.add(log_entity)
        self._session.commit()

        # Return added log
        return log_entity.to_detail_model()
