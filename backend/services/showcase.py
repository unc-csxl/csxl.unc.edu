"""
The Organizations Service allows the API to show COMP 423 projects.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.showcase_project import ShowcaseProject
from ..models import User
from .permission import PermissionService

from .exceptions import ResourceNotFoundException

from ..test.services.showcase.showcase_data import projects

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ShowcaseService:
    """Service that exposes COMP 423 showcase data"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `OrganizationService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    def all(self) -> list[ShowcaseProject]:
        """
        Retrieves all projects.

        Returns:
            list[ShowcaseProject]: List of all `ShowcaseProject`s
        """

        return projects
