"""Tests for the LogService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.exceptions import ResourceNotFoundException

# Tested Dependencies
from ....models.log import LogDetails
from ....services.log import LogService

# Injected Service Fixtures
from ..fixtures import log_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .log_test_data import logs

from ..user_data import root, user

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Test Functions

# Test `LogService.all()`


def test_get_all(log_svc_integration: LogService):
    """Test that all logs can be retrieved."""
    fetched_logs = log_svc_integration.all()
    assert fetched_logs is not None
    assert len(fetched_logs) == len(logs)
    assert isinstance(fetched_logs[0], LogDetails)


# Test `LogService.create()`


def test_create(log_svc_integration: LogService):
    """Test that a log can be created."""
    created_log = log_svc_integration.create(user, "Test log created!")
    assert created_log is not None
    assert created_log.id is not None


def test_create_no_user(log_svc_integration: LogService):
    """Test that a log cannot be created without a valid user."""
    with pytest.raises(ResourceNotFoundException):
        log_svc_integration.create(None, "Test log created!")
        pytest.fail()  # Fail test if no error was thrown above
