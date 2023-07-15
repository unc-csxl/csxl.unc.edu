"""Reset the database by dropping all tables, creating tables, and inserting demo data."""

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.entities.org_role_entity import OrgRoleEntity
from ..database import engine
from ..env import getenv
from .. import entities

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)


# Insert Dev Data from `script.dev_data`

# Add Users
with Session(engine) as session:
    from .dev_data import users
    to_entity = entities.UserEntity.from_model
    session.add_all([to_entity(model) for model in users.models])
    session.execute(text(f'ALTER SEQUENCE {entities.UserEntity.__table__}_id_seq RESTART WITH {len(users.models) + 1}'))
    session.commit()

# Add Roles
with Session(engine) as session:
    from .dev_data import roles
    to_entity = entities.RoleEntity.from_model
    session.add_all([to_entity(model) for model in roles.models])
    session.execute(text(f'ALTER SEQUENCE {entities.RoleEntity.__table__}_id_seq RESTART WITH {len(roles.models) + 1}'))
    session.commit()

# Add Users to Roles
with Session(engine) as session:
    from ..entities import UserEntity, RoleEntity
    from .dev_data import user_roles
    for user, role in user_roles.pairs:
        user_entity = session.get(UserEntity, user.id)
        role_entity = session.get(RoleEntity, role.id)
        user_entity.roles.append(role_entity)
    session.commit()

# Add Permissions to Users/Roles
with Session(engine) as session:
    from ..entities import PermissionEntity
    from .dev_data import permissions
    for role, permission in permissions.pairs:
        entity = PermissionEntity.from_model(permission)
        entity.role = session.get(RoleEntity, role.id)
        session.add(entity)
    session.execute(text(f'ALTER SEQUENCE permission_id_seq RESTART WITH {len(permissions.pairs) + 1}'))
    session.commit()

# Add Organizations
with Session(engine) as session:
    from ..entities import OrganizationEntity
    from .dev_data import organizations
    for org in organizations.organizations:
        entity = OrganizationEntity.from_model(org)
        session.add(entity)
    session.commit()

# Add Events
with Session(engine) as session:
    from ..entities import EventEntity
    from .dev_data import events
    for event in events.models:
        entity = EventEntity.from_model(event)
        session.add(entity)
    session.commit()

# Add Registrations
with Session(engine) as session:
    from .dev_data import registrations
    to_entity = entities.RegistrationEntity.from_model
    session.add_all([to_entity(model) for model in registrations.models])
    session.execute(text(f'ALTER SEQUENCE {entities.RegistrationEntity.__table__}_id_seq RESTART WITH {len(registrations.models) + 1}'))
    session.commit()

# Add OrganizationDetail Roles
with Session(engine) as session:
    from .dev_data import org_roles
    to_entity = entities.OrgRoleEntity.from_model
    session.add_all([to_entity(model) for model in org_roles.models])
    session.execute(text(f'ALTER SEQUENCE {entities.OrgRoleEntity.__table__}_id_seq RESTART WITH {len(org_roles.models) + 1}'))
    session.commit()