"""Fixtures used for testing the Courses Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from ....services.academics.section_member import SectionMemberService
from ....services import PermissionService
from ....services.academics import TermService, CourseService, SectionService
from ....services.academics.my_courses import MyCoursesService

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
    """SectionService fixture."""
    return SectionService(session, permission_svc)


@pytest.fixture()
def section_member_svc(session: Session, permission_svc: PermissionService):
    """SectionMemberService fixture."""
    return SectionMemberService(session, permission_svc)


@pytest.fixture()
def my_courses_svc(session: Session):
    """MyCoursesService fixture."""
    return MyCoursesService(session)
