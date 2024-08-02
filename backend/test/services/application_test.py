"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ...models.application import Application, CatalogSectionIdentity
from ...services import ApplicationService

# Injected Service Fixtures
from .fixtures import application_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .core_data import setup_insert_data_fixture as insert_order_0
from .academics.term_data import fake_data_fixture as insert_order_1
from .academics.course_data import fake_data_fixture as insert_order_2
from .academics.section_data import fake_data_fixture as insert_order_3
from .room_data import fake_data_fixture as insert_order_4
from .office_hours.office_hours_data import fake_data_fixture as insert_order_5
from .academics.hiring.hiring_data import fake_data_fixture as insert_order_6

# Data Models for Fake Data Inserted in Setup
from . import user_data
from .academics import term_data, section_data
from .academics.hiring import hiring_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions


def test_get_application(application_svc: ApplicationService):
    """Ensure that a user can access their application, if it exists."""
    application = application_svc.get_application(
        term_data.current_term.id, user_data.student
    )
    assert application is not None
    assert isinstance(application, Application)
    assert application.id == hiring_data.application_one.id
    assert len(application.preferred_sections) == 3


def test_create_application(application_svc: ApplicationService):
    """Ensure that a user can create an application."""
    application = application_svc.create(
        user_data.ambassador, hiring_data.new_application
    )
    assert application is not None
    assert isinstance(application, Application)
    assert len(application.preferred_sections) == 2


def test_create_application_other_user(application_svc: ApplicationService):
    """Ensure that users cannot create applications for other users."""
    with pytest.raises(UserPermissionException):
        application_svc.create(user_data.instructor, hiring_data.new_application)
        pytest.fail()


def test_create_application_other_user_root(application_svc: ApplicationService):
    """Ensure that root users can create applications for other users."""
    application = application_svc.create(user_data.root, hiring_data.new_application)
    assert application is not None
    assert isinstance(application, Application)
    assert len(application.preferred_sections) == 2


def test_update_application(application_svc: ApplicationService):
    """Ensure users can update their application."""
    updated_application = hiring_data.application_one
    updated_application.academic_hours = 888
    updated_application.preferred_sections = [
        CatalogSectionIdentity(
            id=section_data.comp_110_001_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="001",
            title="Introduction to Computer Science",
        )
    ]
    application = application_svc.update(user_data.student, updated_application)
    assert application is not None
    assert isinstance(application, Application)
    assert application.id == updated_application.id == hiring_data.application_one.id
    assert len(application.preferred_sections) == 1


def test_update_application_other_user(application_svc: ApplicationService):
    """Ensure that users cannot update applications for other users."""
    with pytest.raises(UserPermissionException):
        updated_application = hiring_data.application_one
        application_svc.update(user_data.instructor, updated_application)
        pytest.fail()


def test_update_application_not_found(application_svc: ApplicationService):
    """Ensure that users cannot update applications that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        updated_application = hiring_data.new_application
        updated_application.academic_hours = 888
        application_svc.update(user_data.ambassador, updated_application)
        pytest.fail()


def test_update_application_other_user_root(application_svc: ApplicationService):
    """Ensure that root users can update applications for other users."""
    updated_application = hiring_data.application_one
    updated_application.academic_hours = 888
    updated_application.preferred_sections = [
        CatalogSectionIdentity(
            id=section_data.comp_110_001_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="001",
            title="Introduction to Computer Science",
        )
    ]
    application = application_svc.update(user_data.root, updated_application)
    assert application is not None
    assert isinstance(application, Application)
    assert application.id == updated_application.id == hiring_data.application_one.id
    assert len(application.preferred_sections) == 1


def test_delete_application(application_svc: ApplicationService):
    """Ensure that the root user can delete an application."""
    application_svc.delete(hiring_data.application_one.id, user_data.root)


def test_delete_application_not_found(application_svc: ApplicationService):
    """Ensure that the root user can delete an application."""
    with pytest.raises(ResourceNotFoundException):
        application_svc.delete(404, user_data.root)


def test_delete_application_other_user(application_svc: ApplicationService):
    """Ensure that other users cannot delete an application."""
    with pytest.raises(UserPermissionException):
        application_svc.delete(hiring_data.application_one.id, user_data.student)


def test_eligible_sections(application_svc: ApplicationService):
    sections = application_svc.eligible_sections()
    assert len(sections) == 8
