"""
The Organizations Service allows the API to manipulate organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models import User, Organization
from ..models.organization_details import OrganizationDetails
from ..models.organization_membership import OrganizationMembership
from ..models.organization_join_type import OrganizationJoinType
from ..models.organization_role import OrganizationRole
from ..entities.organization_entity import OrganizationEntity
from ..entities.organization_membership_entity import OrganizationMembershipEntity
from ..entities.user_entity import UserEntity
from .permission import PermissionService

from .exceptions import ResourceNotFoundException, ResourceExistsException


__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrganizationService:
    """Service that performs all of the actions on the `Organization` table"""

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
            # Set id to None so database can handle setting the id
            organization.id = None

        # Otherwise, create new object
        organization_entity = OrganizationEntity.from_model(organization)

        # Add new object to table and commit changes
        self._session.add(organization_entity)
        self._session.commit()

        # Return added object
        return organization_entity.to_model()

    def get_by_slug(self, slug: str) -> OrganizationDetails:
        """
        Get the organization from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        # Check if result is null
        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )

        return organization.to_details_model()

    def add_member(
        self, subject: User, slug: str, user_id: int
    ) -> OrganizationMembership | None:
        """
        Add a new organization membership
        If either user or organization don't exist, a debug message is displayed

        Parameters:
            slug: a string representing a unique organization slug
            user_id: an int representing a unique user id

        Returns:
            OrganizationMembership: Object added to table

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
            ResourceExistsException if user is already in the organization
        """
        # TODO: authenticate and check that user exists in database

        # Check if organization exists
        organization = (
            self._session.query(OrganizationEntity).filter(
                OrganizationEntity.slug == slug
            )
        ).one_or_none()
        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )
        if organization.join_type == OrganizationJoinType.CLOSED:
            raise ResourceNotFoundException(
                f"Organization {slug} is not accepting new members"
            )

        # Check if user exists
        user = (
            self._session.query(UserEntity)
            .filter(UserEntity.id == user_id)
            .one_or_none()
        )
        if user is None:
            raise ResourceNotFoundException(
                f"No user found with matching id: {user_id}"
            )

        # Check if user has existing membership in this organization
        check_existing_membership = (
            self._session.query(OrganizationMembershipEntity)
            .filter(
                OrganizationMembershipEntity.user_id == user_id,
                OrganizationMembershipEntity.organization_id == organization.id,
            )
            .one_or_none()
        )
        if check_existing_membership:
            raise ResourceExistsException(
                f"User with id {user_id} already in the organization with slug: {slug}"
            )

        # Create membership according to organization join type (OPEN/APPLY)
        membership_model = OrganizationMembership(
            user=user.to_model(),
            organization_id=organization.id,
            organization_slug=organization.slug,
            organization_role=OrganizationRole.PENDING,
        )

        if organization.join_type.name == OrganizationJoinType.OPEN.name:
            membership_model.organization_role = OrganizationRole.MEMBER

        organization_membership_entity = OrganizationMembershipEntity.from_model(
            membership_model
        )

        # Add new object to table and commit changes
        self._session.add(organization_membership_entity)
        self._session.commit()

        # Return added object
        return organization_membership_entity.to_model()

    def remove_member(self, subject: User, slug: str, membership_id: int) -> None:
        # TODO: authenticate user for deleting
        """
        Remove an existing organization membership
        If the user isn't a part of the organization, a debug message is displayed

        Parameters:
            slug: a string representing a unique organization slug
            user_id: an int representing a unique membership id

        Raises:
            ResourceNotFoundException if no organization membership is found with the corresponding slug and membership id
        """
        former_membership = (
            self._session.query(OrganizationMembershipEntity)
            .filter(OrganizationMembershipEntity.id == membership_id)
            .one_or_none()
        )

        # Check if result is null
        if former_membership is None:
            raise ResourceNotFoundException(
                f"No organization membership found with id {membership_id}"
            )

        membership_user_id = former_membership.user_id
        if membership_user_id != subject.id:
            self._permission.enforce(
                subject, "organization.update", f"organization/{slug}"
            )

        self._session.delete(former_membership)
        self._session.commit()

    def update_member_role(
        self,
        subject: User,
        slug: str,
        membership_id: int,
        new_role: OrganizationRole,
    ) -> OrganizationMembership:
        """
        Update a member's role in an organization
        """
        self._permission.enforce(subject, "organization.update", f"organization/{slug}")

        query = select(OrganizationMembershipEntity).where(
            OrganizationMembershipEntity.id == membership_id
        )
        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            raise ResourceNotFoundException(
                f"No organization membership found with id: {membership_id}"
            )
        if entity.organization_role != new_role:
            entity.organization_role = new_role
        self._session.commit()
        return entity.to_model()

    def get_roster(
        self, subject: User, organization_slug: str
    ) -> list[OrganizationMembership]:
        # TODO: authenticate

        """
        Get an organization roster
        If the organization doesn't exist, a debug message is displayed

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            list[OrganizationMembership]: list of'OrganizationMembership' objects

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == organization_slug)
            .one_or_none()
        )

        # Check if result is null
        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {organization_slug}"
            )

        # Select all entries in `Organization` table
        query = select(OrganizationMembershipEntity).filter(
            OrganizationMembershipEntity.organization_id == organization.id
        )
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def update(self, subject: User, organization: Organization) -> Organization:
        """
        Update the organization
        If none found with that id, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Updated organization object

        Raises:
            ResourceNotFoundException: If no organization is found with the corresponding ID
        """

        # Check if user has admin permissions
        self._permission.enforce(
            subject, "organization.update", f"organization/{organization.slug}"
        )

        # Query the organization with matching id
        obj = (
            self._session.get(OrganizationEntity, organization.id)
            if organization.id
            else None
        )

        # Check if result is null
        if obj is None:
            raise ResourceNotFoundException(
                f"No organization found with matching ID: {organization.id}"
            )

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
        obj.join_type = organization.join_type

        # Save changes
        self._session.commit()

        # Return updated object
        return obj.to_model()

    def delete(self, subject: User, slug: str) -> None:
        """
        Delete the organization based on the provided slug.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            slug: a string representing a unique organization slug

        Raises:
            ResourceNotFoundException: If no organization is found with the corresponding slug
        """
        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.delete", f"organization")

        # Find object to delete
        obj = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        # Ensure object exists
        if obj is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )

        # Delete object and commit
        self._session.delete(obj)
        # Save changes
        self._session.commit()
