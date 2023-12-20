"""Fixtures used for testing the Courses Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ....services import PermissionService
from ....services.courses import TermService, CourseService, SectionService

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def term_svc(session: Session, permission_svc: PermissionService):
    """TermService fixture."""
    return TermService(session, permission_svc)


@pytest.fixture()
def course_svc(session: Session, permission_svc: PermissionService):
    """CourseService fixture."""
    return CourseService(session, permission_svc)


@pytest.fixture()
def section_svc(session: Session, permission_svc: PermissionService):
    """CourseService fixture."""
    return SectionService(session, permission_svc)
