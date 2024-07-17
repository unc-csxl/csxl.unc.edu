"""This API is for administrative purposes only."""

from fastapi import APIRouter, Depends, HTTPException
from ...services import RoleService, UserPermissionException, PermissionService
from ...entities import UserEntity, RoleEntity, RoomEntity, OrganizationEntity
from ...entities.academics import TermEntity, CourseEntity, SectionEntity
from ..authentication import registered_user
from ...models import User, Paginated, PaginationParams
from pydantic import BaseModel
from ...database import db_session
from sqlalchemy.orm import Session


__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

openapi_tags = {
    "name": "(Admin) Facts",
    "description": "Retrieve an overview of CSXL data.",
}

api = APIRouter(prefix="/api/admin/facts")


class FactsModel(BaseModel):
    users: int
    roles: int
    terms: int
    courses: int
    sections: int
    rooms: int
    organizations: int


@api.get("", tags=["(Admin) Facts"])
def get_facts(
    subject: User = Depends(registered_user),
    session: Session = Depends(db_session),
    permission_service: PermissionService = Depends(),
) -> FactsModel:
    """List counts for all of the major data points."""
    permission_service.enforce(subject, "*", "*")

    users_count = session.query(UserEntity).count()
    roles_count = session.query(RoleEntity).count()
    terms_count = session.query(TermEntity).count()
    courses_count = session.query(CourseEntity).count()
    sections_count = session.query(SectionEntity).count()
    rooms_count = session.query(RoomEntity).count()
    organizations_count = session.query(OrganizationEntity).count()

    return FactsModel(
        users=users_count,
        roles=roles_count,
        terms=terms_count,
        courses=courses_count,
        sections=sections_count,
        rooms=rooms_count,
        organizations=organizations_count,
    )
