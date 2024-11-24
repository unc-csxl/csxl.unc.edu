from datetime import datetime
from fastapi import Depends
from sqlalchemy import func, select, and_, exists, or_
from sqlalchemy.orm import Session, aliased

from backend.database import db_session
from backend.entities.academic_advising.drop_in_entity import DropInEntity
from backend.models.academic_advising.drop_in import DropIn




__authors__ = ["Emmalyn Foster"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class DropInService:
    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initializes the `DropInService` session"""
        self._session = session

    def create(self, event_data) -> DropIn: # type: ignore
        """ Create an entity from API event data, inserts it into the session, and returns the model
        
        Args: 

            event_data: data from an individual event returned from the API

        Returns: 
            returns the model type of a DropIn object
        
        """
        drop_in_entity = DropInEntity(
                title=event_data["summary"],
                date=event_data["date"],  # This is a date object (YYYY-MM-DD)
                start=event_data["start"],  # This is a time object (HH:MM:SS)
                end=event_data["end"],      # This is a time object (HH:MM:SS)
                link=event_data["link"],
            )
        
        self._session.add(drop_in_entity)
        return drop_in_entity.to_model()    

    def insert_all_events(self, events_dict: dict) -> list[DropIn]:
        """Inserts all events from events_dict into the database, returned from Google Calendar API

        Args:
            events_dict (dict): A dictionary of events where each key is the event_id and
                                the value is a dictionary containing event data like title, date,
                                start_time, end_time, and link.

        Returns:
            list: A list of the inserted DropInEntity objects.
        """

        inserted_events = []  # To store the inserted DropInEntity objects

        for event_id, event_data in events_dict.items():
            drop_in = self.create(event_data)
            inserted_events.append(drop_in)

        # Commit the transaction
        self._session.commit()
        return inserted_events
    
    def all(self) -> list[DropIn]:
        """
        Retrieves all DropIns from the table

        Returns:
            list[DropIn]: List of all `DropIn`
        """
        # Select all entries in `DropIn` table
        query = select(DropInEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

