"""Grant ambassadors hours-management access, safely rerunnable on existing data.

Run with: python -m backend.script.deployments.operating_hours_permissions
"""

from sqlalchemy.orm import Session

from ...database import engine
from ...entities.permission_entity import PermissionEntity
from ...entities.role_entity import RoleEntity


def grant_permissions(session: Session) -> int:
    """Add only missing hours permissions to the existing ambassadors role."""
    role = (
        session.query(RoleEntity).filter(RoleEntity.name == "ambassadors").one_or_none()
    )
    if role is None:
        raise RuntimeError(
            "The ambassadors role must exist before granting permissions."
        )
    added = 0
    for action in ("create", "update", "delete"):
        permission_action = f"coworking.operating_hours.{action}"
        resource = "coworking/operating_hours" + ("" if action == "create" else "/*")
        existing = (
            session.query(PermissionEntity)
            .filter_by(role_id=role.id, action=permission_action, resource=resource)
            .first()
        )
        if existing is None:
            session.add(
                PermissionEntity(
                    role_id=role.id, action=permission_action, resource=resource
                )
            )
            added += 1
    session.commit()
    return added


if __name__ == "__main__":
    with Session(engine) as session:
        print(
            f"Added {grant_permissions(session)} ambassador operating-hours permissions."
        )
