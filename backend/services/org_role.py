from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from backend.entities.org_role_entity import OrgRoleEntity
from backend.models.org_role import OrgRole
from ..database import db_session

class OrgRoleService:
    """Service that performs all of the actions on the `Role` table"""

    # Current SQLAlchemy Session
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `RoleService` session"""
        self._session = session

    def all(self) -> list[OrgRole]:
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

    def create(self, role: OrgRole) -> OrgRole:
        """
        Creates a role based on the input object and adds it to the table.
        If the role's PID is unique to the table, a new entry is added.
        If the role's PID already exists in the table, the existing entry is updated.

        Parameters:
            role (OrgRole): Role to add to table
        Returns:
            OrgRole: Object added to table
        """

        # Checks if the role already exists in the table
        if self._session.get(OrgRoleEntity, role.id):

            # If so, update existing entry
            role_entity = OrgRoleEntity.from_model(role)
            self._session.execute(
                update(OrgRoleEntity)
                .where(OrgRoleEntity.id == role.id)
                .values(
                    id = role_entity.id,
                    user_id = role_entity.user_id,
                    org_id = role_entity.org_id,
                    membership_type = role_entity.membership_type
            ))

            # Commit changes
            self._session.commit()

            # Return updated object
            return role_entity.to_model()
        else:
            # Otherwise, create new object
            role_entity = OrgRoleEntity.from_model(role)

            # Add new object to table and commit changes
            self._session.add(role_entity)
            self._session.commit()

            # Return added object
            return role_entity.to_model()

    def get_from_userid(self, user_id: int) -> list[OrgRole]:
        """
        Get all roles matching the provided user id.
        If none retrieved, a debug description is displayed.

        Parameters:
            user_id (int): Unique user ID
        Returns:
            list[OrgRole]: All matching `Role` objects
        """

        # Query roles with matching user id
        roles = self._session.query(OrgRoleEntity).filter(OrgRoleEntity.user_id == user_id).all()

        # Check if result is null
        if roles:
            # Convert entries to a model and return
            return [role.to_model() for role in roles]
        else:
            # Raise exception
            raise Exception(f"No role found with User ID: {user_id}")

    def get_from_orgid(self, org_id: int) -> list[OrgRole]:
        """
        Get all roles matching the provided organization id.
        If none retrieved, a debug description is displayed.

        Parameters:
            org_id (int): Unique organization ID
        Returns:
            list[OrgRole]: All matching `OrgRole` objects
        """

        # Query roles with matching organization id
        roles = self._session.query(OrgRoleEntity).filter(OrgRoleEntity.org_id == org_id).all()

        # Check if result is null
        if roles:
            # Convert entries to a model and return
            return [role.to_model() for role in roles]
        else:
            # Raise exception
            raise Exception(f"No role found with Organization ID: {org_id}")

    def delete(self, id: int) -> None:
        """
        Delete the role based on the provided ID.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            id (int): Unique role ID
        """

        # Find object to delete
        obj=self._session.query(OrgRoleEntity).filter(OrgRoleEntity.id == id).first()

        # Ensure object exists
        if obj:
            # Delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # Raise exception
            raise Exception(f"No role found with ID: {id}")