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
from datetime import datetime, timedelta

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

TERM_LENGTH = timedelta(weeks=17)
TERM_GAP = timedelta(weeks=1)
NOW = datetime.now().replace(microsecond=0)
PREVIOUS_TERM = Term(
    id="Prev",
    name="Previous Term",
    start=NOW - TERM_GAP - TERM_LENGTH,
    end=NOW - TERM_GAP,
    applications_open=NOW - TERM_GAP - TERM_LENGTH,
    applications_close=NOW - TERM_GAP,
)
CURRENT_TERM = Term(
    id="Curr",
    name="Current Term",
    start=NOW,
    end=NOW + TERM_LENGTH,
    applications_open=NOW,
    applications_close=NOW + TERM_LENGTH,
)
CURRENT_TERM_EDITED = CURRENT_TERM.model_copy(update={"name": "Current Term Edited"})
FUTURE_TERM = Term(
    id="Future",
    name="Future Term",
    start=CURRENT_TERM.end + TERM_GAP,
    end=CURRENT_TERM.end + TERM_GAP + TERM_LENGTH,
    applications_open=CURRENT_TERM.applications_open + TERM_GAP,
    applications_close=CURRENT_TERM.applications_close + TERM_GAP + TERM_LENGTH,
)
TERMS = [PREVIOUS_TERM, CURRENT_TERM]
TODAY = NOW
BAD_DAY = datetime.max


def make_term_service(
    session: Session, permission_svc: PermissionService | None = None
) -> TermService:
    return TermService(session, permission_svc or create_autospec(PermissionService))


def arrange_terms(session: Session) -> None:
    # Arrange
    session.add_all(
        [
            TermEntity.from_model(PREVIOUS_TERM),
            TermEntity.from_model(CURRENT_TERM),
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
    assert len(terms) == len(TERMS)
    assert isinstance(terms[0], Term)


def test_get_by_id(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act
    term = term_svc.get_by_id(PREVIOUS_TERM.id)

    # Assert
    assert isinstance(term, Term)
    assert term.id == PREVIOUS_TERM.id


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
    term = term_svc.get_by_date(TODAY)

    # Assert
    assert isinstance(term, Term)
    assert term.id == CURRENT_TERM.id


def test_get_by_date_not_found(session: Session):
    # Arrange
    arrange_terms(session)
    term_svc = make_term_service(session)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.get_by_date(BAD_DAY)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term = term_svc.create(ROOT_USER, FUTURE_TERM)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.create", "term/"
    )
    assert isinstance(term, TermDetails)
    assert term.id == FUTURE_TERM.id


def test_create_as_user(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.create", "term/"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.create(STANDARD_USER, FUTURE_TERM)
        pytest.fail()


def test_update_as_root(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term = term_svc.update(ROOT_USER, CURRENT_TERM_EDITED)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.update", f"term/{term.id}"
    )
    assert isinstance(term, TermDetails)
    assert term.id == CURRENT_TERM_EDITED.id


def test_update_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.update(ROOT_USER, FUTURE_TERM)
        pytest.fail()


def test_update_as_user(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.update", f"term/{CURRENT_TERM_EDITED.id}"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.update(STANDARD_USER, CURRENT_TERM_EDITED)
        pytest.fail()


def test_delete_as_root(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act
    term_svc.delete(ROOT_USER, CURRENT_TERM.id)

    # Assert
    permission_svc.enforce.assert_called_with(
        ROOT_USER, "academics.term.delete", f"term/{CURRENT_TERM.id}"
    )

    terms = term_svc.all()
    assert len(terms) == len(TERMS) - 1


def test_delete_as_root_not_found(session: Session):
    # Arrange
    permission_svc = create_autospec(PermissionService)
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(ResourceNotFoundException):
        term_svc.delete(ROOT_USER, FUTURE_TERM.id)
        pytest.fail()


def test_delete_as_user(session: Session):
    # Arrange
    arrange_terms(session)
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.side_effect = UserPermissionException(
        "academics.term.delete", f"term/{CURRENT_TERM.id}"
    )
    term_svc = make_term_service(session, permission_svc)

    # Act / Assert
    with pytest.raises(UserPermissionException):
        term_svc.delete(STANDARD_USER, CURRENT_TERM.id)
        pytest.fail()
