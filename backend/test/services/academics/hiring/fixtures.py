"""Fixtures used for testing the Hiring services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from .....services.academics.hiring import HiringService
from .....services.permission import PermissionService

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def hiring_svc(session: Session):
    """HiringService fixture."""
    return HiringService(session, PermissionService(session))
