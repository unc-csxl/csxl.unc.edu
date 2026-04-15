"""Tests for Courses Course Service."""

from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from ....entities.academics import CourseEntity
from ....models.user import User
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import CourseService
from ....models.academics import Course, CourseDetails

# Import the fake model data in a namespace for test assertions
from . import course_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


pytestmark = pytest.mark.integration


ROOT_USER = User(
    id=1,
    pid=999999999,
    onyen="root",
    email="root@unc.edu",
    first_name="Rhonda",
    last_name="Root",
)

STANDARD_USER = User(
    id=2,
    pid=111111111,
    onyen="user",
    email="user@unc.edu",
    first_name="Sally",
    last_name="Student",
)


def make_course_service(
    session: Session, permission_svc: PermissionService | None = None
) -> CourseService:
    return CourseService(session, permission_svc or create_autospec(PermissionService))


def arrange_courses(session: Session) -> None:
    # Arrange
    session.add_all(
        [CourseEntity.from_model(course) for course in course_data.courses]
    )
    session.commit()


def test_all(session: Session):
    # Arrange
    arrange_courses(session)
    course_svc = make_course_service(session)

    # Act
    courses = course_svc.all()

    # Assert
    assert len(courses) == len(course_data.courses)
    assert isinstance(courses[0], Course)


def test_get_by_id(session: Session):
    # Arrange
    arrange_courses(session)
    course_svc = make_course_service(session)

    # Act
    course = course_svc.get_by_id(course_data.comp_110.id)

    # Assert
    assert isinstance(course, CourseDetails)
    assert course.id == course_data.comp_110.id


def test_get_by_id_not_found(session: Session):
    # Arrange
    arrange_courses(session)
    course_svc = make_course_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        course_svc.get_by_id("COMP888")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act
    course = course_svc.create(ROOT_USER, course_data.new_course)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.create", "course/"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == course_data.new_course.id


def test_create_as_user(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.create", "course/"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.create(STANDARD_USER, course_data.new_course)
        pytest.fail()


def test_update_as_root(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act
    course = course_svc.update(ROOT_USER, course_data.edited_comp_110)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.update", f"course/{course.id}"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == course_data.edited_comp_110.id


def test_update_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        course_svc.update(ROOT_USER, course_data.new_course)
        pytest.fail()


def test_update_as_user(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.update", f"course/{course_data.edited_comp_110.id}"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.update(STANDARD_USER, course_data.edited_comp_110)
        pytest.fail()


def test_delete_as_root(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act
    course_svc.delete(ROOT_USER, course_data.comp_110.id)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.delete", f"course/{course_data.comp_110.id}"
    )

    courses = course_svc.all()
    assert len(courses) == len(course_data.courses) - 1


def test_delete_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        course_svc.delete(ROOT_USER, course_data.new_course.id)
        pytest.fail()


def test_delete_as_user(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.delete", f"course/{course_data.comp_110.id}"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.delete(STANDARD_USER, course_data.comp_110.id)
        pytest.fail()
