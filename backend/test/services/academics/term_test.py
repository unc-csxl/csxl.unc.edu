"""Tests for Courses Term Service."""

from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from ....entities.academics import TermEntity
from ....models.user import User
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import TermService
from ....models.academics import TermDetails, Term

# Import the fake model data in a namespace for test assertions
from . import term_data

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


def make_term_service(
    session: Session, permission_svc: PermissionService | None = None
) -> TermService:
    return TermService(session, permission_svc or create_autospec(PermissionService))


def arrange_terms(session: Session) -> None:
    # Arrange
    session.add_all(
        [
            TermEntity.from_model(term_data.previous_term),
            TermEntity.from_model(term_data.current_term),
        ]
    )
    session.commit()


def test_all(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act
    terms = term_svc.all()

    # Assert
    assert len(terms) == len(term_data.terms)
    assert isinstance(terms[0], Term)


def test_get_by_id(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act
    term = term_svc.get_by_id(term_data.previous_term.id)

    # Assert
    assert isinstance(term, Term)
    assert term.id == term_data.previous_term.id


def test_get_by_id_not_found(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.get_by_id("SP99")
        pytest.fail()  # Fail test if no error was thrown above


def test_get_by_date(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act
    term = term_svc.get_by_date(term_data.today)

    # Assert
    assert isinstance(term, Term)
    assert term.id == term_data.current_term.id


def test_get_by_date_not_found(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.get_by_date(term_data.bad_day)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term = term_svc.create(ROOT_USER, term_data.future_term)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.create", "term/"
    )
    assert isinstance(term, TermDetails)
    assert term.id == term_data.future_term.id


def test_create_as_user(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.create", "term/"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.create(STANDARD_USER, term_data.future_term)
        pytest.fail()


def test_update_as_root(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term = term_svc.update(ROOT_USER, term_data.current_term_edited)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.update", f"term/{term.id}"
    )
    assert isinstance(term, TermDetails)
    assert term.id == term_data.current_term_edited.id


def test_update_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.update(ROOT_USER, term_data.future_term)
        pytest.fail()


def test_update_as_user(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.update", f"term/{term_data.current_term_edited.id}"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.update(STANDARD_USER, term_data.current_term_edited)
        pytest.fail()


def test_delete_as_root(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term_svc.delete(ROOT_USER, term_data.current_term.id)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.delete", f"term/{term_data.current_term.id}"
    )

    terms = term_svc.all()
    assert len(terms) == len(term_data.terms) - 1


def test_delete_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.delete(ROOT_USER, term_data.future_term.id)
        pytest.fail()


def test_delete_as_user(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.delete", f"term/{term_data.current_term.id}"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.delete(STANDARD_USER, term_data.current_term.id)
        pytest.fail()
