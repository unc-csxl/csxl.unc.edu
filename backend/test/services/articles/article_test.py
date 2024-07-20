"""Tests for the Article Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from ....services import ArticleService
from ....models.articles import WelcomeOverview

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import article_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_fake_data_one
from .article_data import fake_data_fixture as insert_fake_data_two

# Import the fake model data in a namespace for test assertions
from .. import user_data
from . import article_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_welcome_overview(article_svc: ArticleService):
    """Ensures that users are able to get the welcome overview."""
    welcome_overview = article_svc.get_welcome_overview(user_data.student)
    assert welcome_overview is not None
    assert isinstance(welcome_overview, WelcomeOverview)
    assert welcome_overview.announcement is not None
    assert len(welcome_overview.latest_news) == len(
        article_data.articles_no_announcement
    )
