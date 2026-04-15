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

COMP_110 = Course(
    id="comp110",
    subject_code="COMP",
    number="110",
    title="Introduction to Programming and Data Science",
    description="Introduces students to programming and data science.",
    credit_hours=3,
)
COMP_210 = Course(
    id="comp210",
    subject_code="COMP",
    number="210",
    title="Data Structures and Analysis",
    description="Data structures and analysis.",
    credit_hours=3,
)
COMP_211 = Course(
    id="comp211",
    subject_code="COMP",
    number="211",
    title="Systems Fundamentals",
    description="Systems fundamentals.",
    credit_hours=3,
)
COMP_301 = Course(
    id="comp301",
    subject_code="COMP",
    number="301",
    title="Foundations of Programming",
    description="Foundations of programming.",
    credit_hours=3,
)
COMP_311 = Course(
    id="comp311",
    subject_code="COMP",
    number="311",
    title="Computer Organization",
    description="Computer organization.",
    credit_hours=3,
)
COMP_523 = Course(
    id="comp523",
    subject_code="COMP",
    number="523",
    title="Software Engineering Laboratory",
    description="Software engineering laboratory.",
    credit_hours=4,
)
EDITED_COMP_110 = COMP_110.model_copy(update={"title": "Introduction to Programming"})
NEW_COURSE = Course(
    id="comp423",
    subject_code="COMP",
    number="423",
    title="Foundations of Software Engineering",
    description="Best course in the department : )",
    credit_hours=3,
)
COURSES = [COMP_110, COMP_210, COMP_211, COMP_301, COMP_311, COMP_523]


def make_course_service(
    session: Session, permission_svc: PermissionService | None = None
) -> CourseService:
    return CourseService(session, permission_svc or create_autospec(PermissionService))


def arrange_courses(session: Session) -> None:
    # Arrange
    session.add_all([CourseEntity.from_model(course) for course in COURSES])
    session.commit()


def test_all(session: Session):
    # Arrange
    arrange_courses(session)
    course_svc = make_course_service(session)

    # Act
    courses = course_svc.all()

    # Assert
    assert len(courses) == len(COURSES)
    assert isinstance(courses[0], Course)


def test_get_by_id(session: Session):
    # Arrange
    arrange_courses(session)
    course_svc = make_course_service(session)

    # Act
    course = course_svc.get_by_id(COMP_110.id)

    # Assert
    assert isinstance(course, CourseDetails)
    assert course.id == COMP_110.id


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
    course = course_svc.create(ROOT_USER, NEW_COURSE)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.create", "course/"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == NEW_COURSE.id


def test_create_as_user(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.create", "course/"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.create(STANDARD_USER, NEW_COURSE)
        pytest.fail()


def test_update_as_root(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act
    course = course_svc.update(ROOT_USER, EDITED_COMP_110)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.update", f"course/{course.id}"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == EDITED_COMP_110.id


def test_update_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        course_svc.update(ROOT_USER, NEW_COURSE)
        pytest.fail()


def test_update_as_user(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.update", f"course/{EDITED_COMP_110.id}"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.update(STANDARD_USER, EDITED_COMP_110)
        pytest.fail()


def test_delete_as_root(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act
    course_svc.delete(ROOT_USER, COMP_110.id)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.course.delete", f"course/{COMP_110.id}"
    )

    courses = course_svc.all()
    assert len(courses) == len(COURSES) - 1


def test_delete_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        course_svc.delete(ROOT_USER, NEW_COURSE.id)
        pytest.fail()


def test_delete_as_user(session: Session):
    # Arrange
    arrange_courses(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.course.delete", f"course/{COMP_110.id}"
    )
    course_svc = make_course_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        course_svc.delete(STANDARD_USER, COMP_110.id)
        pytest.fail()
