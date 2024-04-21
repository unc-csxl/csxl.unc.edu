"""Tests for Courses Term Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.permission import PermissionService
from ....services.academics import TermService
from ....models.academics import TermDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import permission_svc, term_svc

# Import core data to ensure all data loads for the tests.
from ..core_data import setup_insert_data_fixture

# Import the fake model data in a namespace for test assertions
from . import term_data
from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_all(term_svc: TermService):
    terms = term_svc.all()

    assert len(terms) == len(term_data.terms)
    assert isinstance(terms[0], TermDetails)


def test_get_by_id(term_svc: TermService):
    term = term_svc.get_by_id(term_data.sp_23.id)

    assert isinstance(term, TermDetails)
    assert term.id == term_data.sp_23.id


def test_get_by_id_not_found(term_svc: TermService):
    with pytest.raises(ResourceNotFoundException):
        term = term_svc.get_by_id("SP99")
        pytest.fail()  # Fail test if no error was thrown above


def test_get_by_date(term_svc: TermService):
    term = term_svc.get_by_date(term_data.today)

    assert isinstance(term, TermDetails)
    assert term.id == term_data.f_23.id


def test_get_by_date_not_found(term_svc: TermService):
    with pytest.raises(ResourceNotFoundException):
        term = term_svc.get_by_date(term_data.bad_day)
        pytest.fail()  # Fail test if no error was thrown above


def test_create_as_root(term_svc: TermService):
    permission_svc = create_autospec(PermissionService)
    term_svc._permission_svc = permission_svc

    term = term_svc.create(user_data.root, term_data.new_term)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.term.create", "term/"
    )
    assert isinstance(term, TermDetails)
    assert term.id == term_data.new_term.id


def test_create_as_user(term_svc: TermService):
    with pytest.raises(UserPermissionException):
        term = term_svc.create(user_data.user, term_data.new_term)
        pytest.fail()


def test_update_as_root(term_svc: TermService):
    permission_svc = create_autospec(PermissionService)
    term_svc._permission_svc = permission_svc

    term = term_svc.update(user_data.root, term_data.edited_f_23)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.term.update", f"term/{term.id}"
    )
    assert isinstance(term, TermDetails)
    assert term.id == term_data.edited_f_23.id


def test_update_as_root_not_found(term_svc: TermService):
    permission_svc = create_autospec(PermissionService)
    term_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        term = term_svc.update(user_data.root, term_data.new_term)
        pytest.fail()


def test_update_as_user(term_svc: TermService):
    with pytest.raises(UserPermissionException):
        term = term_svc.create(user_data.user, term_data.edited_f_23)
        pytest.fail()


def test_delete_as_root(term_svc: TermService):
    permission_svc = create_autospec(PermissionService)
    term_svc._permission_svc = permission_svc

    term_svc.delete(user_data.root, term_data.f_23.id)

    permission_svc.enforce.assert_called_with(
        user_data.root, "academics.term.delete", f"term/{term_data.f_23.id}"
    )

    terms = term_svc.all()
    assert len(terms) == len(term_data.terms) - 1


def test_delete_as_root_not_found(term_svc: TermService):
    permission_svc = create_autospec(PermissionService)
    term_svc._permission_svc = permission_svc

    with pytest.raises(ResourceNotFoundException):
        term = term_svc.delete(user_data.root, term_data.new_term.id)
        pytest.fail()


def test_delete_as_user(term_svc: TermService):
    with pytest.raises(UserPermissionException):
        term = term_svc.delete(user_data.user, term_data.f_23.id)
        pytest.fail()
