"""Tests for Courses Course Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import CourseService
from ....models.academics import CourseDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, course_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .course_data import fake_data_fixture as insert_course_fake_data

# Import the fake model data in a namespace for test assertions
from . import course_data
from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_all(course_svc: CourseService):
    courses = course_svc.all()

    assert len(courses) == len(course_data.courses)
    assert isinstance(courses[0], CourseDetails)


def test_get_by_id(course_svc: CourseService):
    course = course_svc.get_by_id(course_data.comp_110.id)

    assert isinstance(course, CourseDetails)
    assert course.id == course_data.comp_110.id


def test_get_by_id_not_found(course_svc: CourseService):
    with pytest.raises(ResourceNotFoundException):
        term = course_svc.get_by_id("COMP888")
        pytest.fail()  # Fail test if no error was thrown above


def test_get(course_svc: CourseService):
    course = course_svc.get("COMP", "110")

    assert isinstance(course, CourseDetails)
    assert course.id == course_data.comp_110.id


def test_get_not_found(course_svc: CourseService):
    with pytest.raises(ResourceNotFoundException):
        course = course_svc.get("COMP", "888")
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(course_svc: CourseService):
    permission_svc = create_autospec(PermissionService)
    course_svc._permission_svc = permission_svc

    course = course_svc.create(user_data.root, course_data.new_course)

    permission_svc.enforce.assert_called_with(
        user_data.root, "courses.course.create", "course/"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == course_data.new_course.id


def test_create_as_user(course_svc: CourseService):
    with pytest.raises(UserPermissionException):
        course = course_svc.create(user_data.user, course_data.new_course)
        pytest.fail()


def test_update_as_root(course_svc: CourseService):
    permission_svc = create_autospec(PermissionService)
    course_svc._permission_svc = permission_svc

    course = course_svc.update(user_data.root, course_data.edited_comp_110)

    permission_svc.enforce.assert_called_with(
        user_data.root, "courses.course.update", f"course/{course.id}"
    )
    assert isinstance(course, CourseDetails)
    assert course.id == course_data.edited_comp_110.id


def test_update_as_root_not_found(course_svc: CourseService):
    permission_svc = create_autospec(PermissionService)
    course_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        course = course_svc.update(user_data.root, course_data.new_course)
        pytest.fail()


def test_update_as_user(course_svc: CourseService):
    with pytest.raises(UserPermissionException):
        course = course_svc.create(user_data.user, course_data.edited_comp_110)
        pytest.fail()


def test_delete_as_root(course_svc: CourseService):
    permission_svc = create_autospec(PermissionService)
    course_svc._permission_svc = permission_svc

    course_svc.delete(user_data.root, course_data.comp_110)

    permission_svc.enforce.assert_called_with(
        user_data.root, "courses.course.delete", f"course/{course_data.comp_110.id}"
    )

    courses = course_svc.all()
    assert len(courses) == len(course_data.courses) - 1


def test_delete_as_root_not_found(course_svc: CourseService):
    permission_svc = create_autospec(PermissionService)
    course_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        course = course_svc.delete(user_data.root, course_data.new_course)
        pytest.fail()


def test_delete_as_user(course_svc: CourseService):
    with pytest.raises(UserPermissionException):
        course = course_svc.delete(user_data.user, course_data.comp_110)
        pytest.fail()
