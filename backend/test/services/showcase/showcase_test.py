"""Tests for the ShowcaseService class."""

import pytest

# Tested Dependencies
from ....services.showcase import ShowcaseService

# Fixture
from ..fixtures import showcase_svc

# Data Models for Fake Data Inserted in Setup
from .showcase_data import projects

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_list(showcase_svc: ShowcaseService):
    all = showcase_svc.all()

    assert len(all) == len(projects)
