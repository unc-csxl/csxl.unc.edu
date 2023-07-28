from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from backend.entities.org_role_entity import OrgRoleEntity
from backend.models.org_role import OrgRoleDetail, OrgRole
from ..database import db_session
from ..models import User
from .permission import PermissionService, UserPermissionError
from .organization import OrganizationService

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrgRoleService:
    """Service that performs all of the actions on the `Role` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
        organizations: OrganizationService = Depends(),
    ):
        """Initializes the `RoleService` session"""
        self._session = session
        self._permission = permission
        self._organizations = organizations

    def all(self) -> list[OrgRoleDetail]:
        """
        Retrieves all roles from the table

        Returns:
            list[Role]: List of all `Roles`
        """
        # Select all entries in `Role` table
        query = select(OrgRoleEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]

    def check_permissions(self, subject: User, role: OrgRole):
        # First, ensure that permissions fail if anyone except the site admin add someone with member type 2.
        adding_org_leader = role.membership_type == 2

        # Second, check if the subject is has executive permissions in the organization.
        # Also ensure that no current member of an organization is upgrading their own membership type.
        subject_org_permissions = [
            o_r for o_r in self.get_from_userid(subject.id) if o_r.org_id == role.org_id
        ]
        has_permission = (
            len(subject_org_permissions) > 0
            and subject_org_permissions[0].membership_type >= 1
        )
        is_not_upgrading_self = (
            len(subject_org_permissions) > 0
            and subject_org_permissions[0].user_id != role.user_id
        )
        is_joining_as_member = role.membership_type == 0

        # Third, check if a user is attempting to add themselves to a public organization only.
        org_is_public = self._organizations.get_from_id(role.org_id).public

        if adding_org_leader:
            self._permission.enforce(subject, "admin.create_orgrole", f"orgroles")
        elif has_permission and is_not_upgrading_self:
            ...  # Permission granted
        elif org_is_public and is_joining_as_member:
            ...  # Permission granted
        else:
            raise UserPermissionError("admin.create_orgrole", f"orgroles")

    def create(self, subject: User, role: OrgRole) -> OrgRoleDetail:
        """
        Creates a role based on the input object and adds it to the table.
        If the role's PID is unique to the table, a new entry is added.
        If the role's PID already exists in the table, the existing entry is updated.

        Parameters:
            role (OrgRoleDetail): Role to add to table
        Returns:
            OrgRoleDetail: Object added to table
        """
        # Ensure user has proper permissions to create a new role
        self.check_permissions(subject, role)

        # Checks if the role already exists in the table
        if role.id:
            # If so, update existing entry
            role_entity = self._session.query(OrgRoleEntity).get(
                (role.id, role.user_id, role.org_id)
            )
            self._session.execute(
                update(OrgRoleEntity)
                .where(OrgRoleEntity.id == role.id)
                .values(
                    id=role_entity.id,
                    user_id=role_entity.user_id,
                    org_id=role_entity.org_id,
                    membership_type=role.membership_type,
                    timestamp=role.timestamp,
                )
            )
        else:
            # Otherwise, create new object
            role_entity = OrgRoleEntity.from_model(role)

            # Add new object to table
            self._session.add(role_entity)

        # Commit changes
        self._session.commit()

        # Return updated/added object
        return role_entity.to_model()

    def get_from_userid(self, user_id: int) -> list[OrgRoleDetail]:
        """
        Get all roles matching the provided user id.
        If none retrieved, a debug description is displayed.

        Parameters:
            user_id (int): Unique user ID
        Returns:
            list[OrgRoleDetail]: All matching `Role` objects
        """

        # Query roles with matching user id
        roles = (
            self._session.query(OrgRoleEntity)
            .filter(OrgRoleEntity.user_id == user_id)
            .all()
        )

        # Check if result is null
        if roles:
            # Convert entries to a model and return
            return [role.to_model() for role in roles]
        else:
            # Return an empty list
            return []

    def get_from_orgid(self, org_id: int) -> list[OrgRoleDetail]:
        """
        Get all roles matching the provided organization id.
        If none retrieved, a debug description is displayed.

        Parameters:
            org_id (int): Unique organization ID
        Returns:
            list[OrgRoleDetail]: All matching `OrgRoleDetail` objects
        """

        # Query roles with matching organization id
        roles = (
            self._session.query(OrgRoleEntity)
            .filter(OrgRoleEntity.org_id == org_id)
            .all()
        )

        # Check if result is null
        if roles:
            # Convert entries to a model and return
            return [role.to_model() for role in roles]
        else:
            # Return empty list
            return []

    def delete(self, subject: User, id: int) -> None:
        """
        Delete the role based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            id (int): Unique role ID
        """

        # Find object to delete
        role = self._session.query(OrgRoleEntity).filter(OrgRoleEntity.id == id).first()
        subject_role = (
            self._session.query(OrgRoleEntity)
            .filter(
                OrgRoleEntity.org_id == role.org_id
                and OrgRoleEntity.user_id == subject.id
            )
            .first()
        )
        # Ensure object exists
        if role and subject_role:
            # Ensure user has proper permissions to delete a role
            if subject_role.membership_type >= 1:
                # Delete object and commit
                self._session.delete(role)
                self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No role found with ID: {id}")
