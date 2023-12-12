"""Tests for Courses Term Service."""

from ....services.courses import TermService
from ....models.courses import TermDetails

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import term_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .term_data import fake_data_fixture as insert_term_fake_data

# Import the fake model data in a namespace for test assertions
from . import term_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_all(term_svc: TermService):
    terms = term_svc.all()

    assert len(terms) == len(term_data.terms)
    assert isinstance(terms[0], TermDetails)
