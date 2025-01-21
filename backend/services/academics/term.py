"""
The Terms Service allows the API to manipulate terms data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...database import db_session
from ...models.academics import Term
from ...models.academics import TermDetails
from ...models import User
from ...entities.academics import TermEntity
from ..permission import PermissionService

from ...services.exceptions import ResourceNotFoundException
from datetime import datetime

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class TermService:
    """Service that performs all of the actions on the `Term` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initializes the database session."""
        self._session = session
        self._permission_svc = permission_svc

    def all(self) -> list[Term]:
        """Retrieves all terms from the table

        Returns:
            list[Term]: List of all `TermDetails`
        """
        # Select all entries in `Term` table
        query = select(TermEntity).order_by(TermEntity.start)

        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def get_by_id(self, id: str) -> Term:
        """Gets the term from the table for an id.

        Args:
            id: ID of the term to retrieve.
        Returns:
            Term: Term based on the id.
        """
        # Select all entries in the `Term` table and sort by end date
        query = select(TermEntity).filter(TermEntity.id == id).limit(1)
        entity = self._session.scalars(query).one_or_none()

        # Raise an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(f"Term with id: {id} does not exist.")

        # Return the model
        return entity.to_model()

    def get_by_date(self, date: datetime) -> Term:
        """Gets the active term for a given date, if it exists.

        Args:
            date: Date to query the active term for.
        Returns:
            Term: Term based on the provided date.
        """
        # Select all entries in the `Term` table that contains this date.
        # This query either selects the most current term, or the upcoming term if there
        # is no currently active term
        query = (
            select(TermEntity).where(date < TermEntity.end).order_by(TermEntity.start)
        )
        entity = self._session.scalars(query).first()

        # Rause an error if no entity was found.
        if entity is None:
            raise ResourceNotFoundException(
                f"No active term found for the provided date: {date}."
            )

        # Return the model
        return entity.to_model()

    def create(self, subject: User, term: Term) -> TermDetails:
        """Creates a new term.

        Args:
            subject: a valid User model representing the currently logged in User
            term (Term): Term to add to table

        Returns:
            TermDetails: Object added to table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "academics.term.create", f"term/")

        # Create new object
        term_entity = TermEntity.from_model(term)

        # Add new object to table and commit changes
        self._session.add(term_entity)
        self._session.commit()

        # Return added object
        return term_entity.to_details_model()

    def update(self, subject: User, term: Term) -> TermDetails:
        """Updates a term.

        Args:
            subject: a valid User model representing the currently logged in User
            term (Term): Term to update

        Returns:
            TermDetails: Object updated in the table
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(
            subject, "academics.term.update", f"term/{term.id}"
        )

        # Find the entity to update
        term_entity = self._session.get(TermEntity, term.id)

        # Raise an error if no entity was found
        if term_entity is None:
            raise ResourceNotFoundException(f"Term with id: {term.id} does not exist.")

        # Update the entity
        term_entity.name = term.name
        term_entity.start = term.start
        term_entity.end = term.end
        term_entity.applications_open = term.applications_open
        term_entity.applications_close = term.applications_close

        # Commit changes
        self._session.commit()

        # Return edited object
        return term_entity.to_details_model()

    def delete(self, subject: User, id: str) -> None:
        """Deletes a term.

        Args:
            subject: a valid User model representing the currently logged in User
            id (str): ID for term to delete
        """

        # Check if user has admin permissions
        self._permission_svc.enforce(subject, "academics.term.delete", f"term/{id}")

        # Find the entity to delete
        term_entity = self._session.get(TermEntity, id)

        # Raise an error if no entity was found
        if term_entity is None:
            raise ResourceNotFoundException(f"Term with id: {id} does not exist.")

        # Delete and commit changes
        self._session.delete(term_entity)
        self._session.commit()
