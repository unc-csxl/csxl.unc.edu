from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from ..database import db_session
from ..models.organization import Organization
from ..models.organization_detail import OrganizationDetail
from ..entities.organization_entity import OrganizationEntity
from ..models import User
from .permission import PermissionService, UserPermissionError

class OrganizationService:
    """Service that performs all of the actions on the `Organization` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        """Initializes the `OrganizationService` session"""
        self._session = session
        self._permission = permission

    def all(self) -> list[OrganizationDetail]:
        """
        Retrieves all organizations from the table

        Returns:
            list[OrganizationDetail]: List of all `OrganizationDetail`
        """
        # Select all entries in `OrganizationDetail` table
        query = select(OrganizationEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def create(self, subject: User, organization: Organization) -> OrganizationDetail:
        """
        Creates a organization based on the input object and adds it to the table.
        If the organization's ID is unique to the table, a new entry is added.
        If the organization's ID already exists in the table, it raises an error.

        Parameters:
            organization (OrganizationDetail): OrganizationDetail to add to table
        Returns:
            OrganizationDetail: Object added to table
        """

        # Check if user has manager permissions for the organization
        org_roles = [org_role for org_role in subject.organization_associations if
            org_role.org_id == organization.id and org_role.membership_type > 0]
        
        # If no role is found, raise an exception
        if(len(org_roles) <=0):
            raise UserPermissionError('organization.create', f'organizations')

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

    def get_from_id(self, id: int) -> OrganizationDetail:
        """
        Get the organization from an id
        If none retrieved, a debug description is displayed.

        Parameters:
            id (int): Unique organization ID
        Returns:
            OrganizationDetail: Object with corresponding ID
        """

        # Query the organization with matching id
        organization = self._session.query(OrganizationEntity).get(id)

        # Check if result is null
        if organization:
            # Convert entry to a model and return
            return organization.to_model()
        else:
            # Raise exception
            raise Exception(f"No organization found with ID: {id}")

    def get_from_name(self, name: str) -> OrganizationDetail:
        """
        Get the organization from name (string)
        If none retrieved, a debug description is displayed.

        Parameters:
            name (str): OrganizationDetail name
        Returns:
            OrganizationDetail: Object with corresponding name
        """

        # Query the organization with matching id
        organization = self._session.query(OrganizationEntity).filter(OrganizationEntity.name == name)[0]

        # Check if result is null
        if organization:
            # Convert entry to a model and return
            return organization.to_model()
        else:
            # Raise exception
            raise Exception(f"No organization found with name: {name}")

    def update(self, subject: User, organization: OrganizationDetail) -> OrganizationDetail:
        """
        Update the organization
        If none found with that id, a debug description is displayed.

        Parameters:
            organization (OrganizationDetail): OrganizationDetail to add to table
        Returns:
            OrganizationDetail: Updated organization object
        """

        # Check if user has manager permissions for the organization
        org_roles = [org_role for org_role in subject.organization_associations if
            org_role.org_id == organization.id and org_role.membership_type > 0]
        
        # If no role is found, raise an exception
        if(len(org_roles) <=0):
            raise UserPermissionError('organization.update', f'organizations')

        # Query the organization with matching id
        obj = self._session.query(OrganizationEntity).get(organization.id)

        # Check if result is null
        if obj:
            # Update organization object
            obj.name=organization.name
            obj.logo=organization.logo
            obj.short_description=organization.short_description
            obj.long_description=organization.long_description
            obj.website=organization.website
            obj.email=organization.email
            obj.instagram=organization.instagram
            obj.linked_in=organization.linked_in
            obj.youtube=organization.youtube
            obj.heel_life=organization.heel_life
            self._session.commit()
            # Return updated object
            return obj.to_model()
        else:
            # Raise exception
            raise Exception(f"No organization found with ID: {organization.id}")

    
    def delete(self, subject: User, id: int) -> None:
        """
        Delete the organization based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            id (int): Unique organization ID
        """

        # Find object to delete
        obj=self._session.query(OrganizationEntity).get(id)

        # Ensure object exists
        if obj:
             # Check if user has manager permissions for the organization
            org_roles = [org_role for org_role in subject.organization_associations if
                org_role.org_id == obj.id and org_role.membership_type > 0]
        
            # If no role is found, raise an exception
            if(len(org_roles) <=0):
                raise UserPermissionError('organization.delete', f'organizations/{id}')
            
            # Delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No organization found with ID: {id}")