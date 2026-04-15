"""Tests for the ApplicationService class."""

# PyTest
import pytest

from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ...models.application import Application, CatalogSectionIdentity
from ...services import ApplicationService

# Injected Service Fixtures
from .fixtures import application_svc
from .application_scenario import ApplicationScenario, arrange_application_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def application_scenario(session) -> ApplicationScenario:
    return arrange_application_scenario(session)


def test_get_application(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that a user can access their application, if it exists."""
    application = application_svc.get_application(
        application_scenario.current_term.id, application_scenario.auth.student
    )
    assert application is not None
    assert isinstance(application, Application)
    assert application.id == application_scenario.application_one.id
    assert len(application.preferred_sections) == 3


def test_create_application(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that a user can create an application."""
    application = application_svc.create(
        application_scenario.auth.ambassador,
        application_scenario.new_application.model_copy(deep=True),
    )
    assert application is not None
    assert isinstance(application, Application)
    assert len(application.preferred_sections) == 2


def test_create_application_other_user(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that users cannot create applications for other users."""
    with pytest.raises(UserPermissionException):
        application_svc.create(
            application_scenario.auth.instructor,
            application_scenario.new_application.model_copy(deep=True),
        )
        pytest.fail()


def test_create_application_other_user_root(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that root users can create applications for other users."""
    application = application_svc.create(
        application_scenario.auth.root,
        application_scenario.new_application.model_copy(deep=True),
    )
    assert application is not None
    assert isinstance(application, Application)
    assert len(application.preferred_sections) == 2


def test_update_application(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure users can update their application."""
    updated_application = application_scenario.application_one.model_copy(deep=True)
    updated_application.academic_hours = 888
    updated_application.preferred_sections = [
        CatalogSectionIdentity(
            id=application_scenario.comp_110_001_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="001",
            title="Introduction to Computer Science",
        )
    ]
    application = application_svc.update(
        application_scenario.auth.student, updated_application
    )
    assert application is not None
    assert isinstance(application, Application)
    assert (
        application.id
        == updated_application.id
        == application_scenario.application_one.id
    )
    assert len(application.preferred_sections) == 1


def test_update_application_other_user(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that users cannot update applications for other users."""
    with pytest.raises(UserPermissionException):
        updated_application = application_scenario.application_one.model_copy(deep=True)
        application_svc.update(
            application_scenario.auth.instructor, updated_application
        )
        pytest.fail()


def test_update_application_not_found(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that users cannot update applications that do not exist."""
    with pytest.raises(ResourceNotFoundException):
        updated_application = application_scenario.new_application.model_copy(deep=True)
        updated_application.academic_hours = 888
        application_svc.update(
            application_scenario.auth.ambassador, updated_application
        )
        pytest.fail()


def test_update_application_other_user_root(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that root users can update applications for other users."""
    updated_application = application_scenario.application_one.model_copy(deep=True)
    updated_application.academic_hours = 888
    updated_application.preferred_sections = [
        CatalogSectionIdentity(
            id=application_scenario.comp_110_001_current_term.id,
            subject_code="COMP",
            course_number="110",
            section_number="001",
            title="Introduction to Computer Science",
        )
    ]
    application = application_svc.update(
        application_scenario.auth.root, updated_application
    )
    assert application is not None
    assert isinstance(application, Application)
    assert (
        application.id
        == updated_application.id
        == application_scenario.application_one.id
    )
    assert len(application.preferred_sections) == 1


def test_delete_application(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that the root user can delete an application."""
    application_svc.delete(
        application_scenario.application_one.id, application_scenario.auth.root
    )


def test_delete_application_not_found(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that the root user can delete an application."""
    with pytest.raises(ResourceNotFoundException):
        application_svc.delete(404, application_scenario.auth.root)


def test_delete_application_other_user(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    """Ensure that other users cannot delete an application."""
    with pytest.raises(UserPermissionException):
        application_svc.delete(
            application_scenario.application_one.id,
            application_scenario.auth.student,
        )


def test_eligible_sections(
    application_svc: ApplicationService, application_scenario: ApplicationScenario
):
    sections = application_svc.eligible_sections()
    assert len(sections) == 8
