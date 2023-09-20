from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.organization import Organization
from ..entities.organization_entity import OrganizationEntity
from ..models import User
from .permission import PermissionService, UserPermissionError

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

class OrganizationService:
    """Service that performs all of the actions on the `Organization` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `OrganizationService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    def all(self) -> list[Organization]:
        """
        Retrieves all organizations from the table

        Returns:
            list[Organization]: List of all `Organization`
        """
        # Select all entries in `Organization` table
        query = select(OrganizationEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def create(self, subject: User, organization: Organization) -> Organization:
        """
        Creates a organization based on the input object and adds it to the table.
        If the organization's ID is unique to the table, a new entry is added.
        If the organization's ID already exists in the table, it raises an error.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Object added to table
        """

        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.create", f"organization")

        # Checks if the organization already exists in the table
        if organization.id:
            # If so, raise an error
            raise Exception(f"Duplicate organization found with ID: {organization.id}")

        else:
            # Otherwise, create new object
            organization_entity = OrganizationEntity.from_model(organization)

            # Add new object to table and commit changes
            self._session.add(organization_entity)
            self._session.commit()

            # Return added object
            return organization_entity.to_model()

    def get_from_slug(self, slug: str) -> Organization:
        """
        Get the organization from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            Exception if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        organization = self._session.query(OrganizationEntity).filter(
            OrganizationEntity.slug == slug
        )[0]

        # Check if result is null
        if organization:
            # Convert entry to a model and return
            return organization.to_model()
        else:
            # Raise exception
            raise Exception(f"No organization found with slug: {slug}")

    def update(
        self, subject: User, organization: Organization
    ) -> Organization:
        """
        Update the organization
        If none found with that id, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Updated organization object
        """

        # Check if user has manager permissions for the organization
        org_roles = [
            o_r
            for o_r in organization.user_associations
            if o_r.user_id == subject.id
            and o_r.org_id == organization.id
            and o_r.membership_type > 0
        ]

        # If no role is found, raise an exception
        if len(org_roles) <= 0:
            raise UserPermissionError("organization.update", f"organization")

        # Query the organization with matching id
        obj = self._session.query(OrganizationEntity).get(organization.id)

        # Check if result is null
        if obj:
            # Update organization object
            obj.name = organization.name
            obj.shorthand = organization.shorthand
            obj.slug = organization.slug
            obj.logo = organization.logo
            obj.short_description = organization.short_description
            obj.long_description = organization.long_description
            obj.website = organization.website
            obj.email = organization.email
            obj.instagram = organization.instagram
            obj.linked_in = organization.linked_in
            obj.youtube = organization.youtube
            obj.heel_life = organization.heel_life
            obj.public = organization.public
            self._session.commit()
            # Return updated object
            return obj.to_model()
        else:
            # Raise exception
            raise Exception(f"No organization found with ID: {organization.id}")

    def delete(self, subject: User, slug: str) -> None:
        """
        Delete the organization based on the provided slug.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            slug: a string representing a unique organization slug

        Raises:
            Exception if no organization is found with the corresponding slug
        """
        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.create", f"organization")

        # Find object to delete
        obj = self._session.query(OrganizationEntity).filter(
            OrganizationEntity.slug == slug
        )[0]

        # Ensure object exists
        if obj:
            # Delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No organization found with slug: {slug}")