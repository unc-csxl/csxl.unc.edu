"""Tests for the Article Service."""

from unittest.mock import create_autospec
import pytest
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from ....services import ArticleService
from ....models.articles import WelcomeOverview
from ....models.pagination import PaginationParams

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


def test_get_welcome_unauthenticated(article_svc: ArticleService):
    """Ensures that logged out users are able to get the welcome overview."""
    welcome_overview = article_svc.get_welcome_overview(None)
    assert welcome_overview is not None
    assert isinstance(welcome_overview, WelcomeOverview)
    assert welcome_overview.announcement is not None
    assert len(welcome_overview.latest_news) == len(
        article_data.articles_no_announcement
    )


def test_get_by_slug(article_svc: ArticleService):
    """Ensures that users can get articles."""
    article = article_svc.get_article(article_data.article_one.slug)
    assert article is not None
    assert article.id == article_data.article_one.id


def test_get_by_slug_not_found(article_svc: ArticleService):
    """Ensures that users who search for blank articles get a null response."""
    article = article_svc.get_article("404")
    assert article is None


def test_list(article_svc: ArticleService):
    """Ensures that the admin can list all articles."""
    pagination_params = PaginationParams(page=0, page_size=10, filter="")
    articles = article_svc.list(user_data.root, pagination_params)
    assert articles is not None
    assert len(articles.items) == 3


def test_list_not_admin(article_svc: ArticleService):
    """Ensures that non-admins cannot access all articles."""
    with pytest.raises(UserPermissionException):
        pagination_params = PaginationParams(page=0, page_size=10, filter="")
        article_svc.list(user_data.student, pagination_params)


def test_create_article(article_svc: ArticleService):
    """Ensures that the admin can create an article"""
    article = article_svc.create_article(user_data.root, article_data.new_article)
    assert article is not None
    assert article.id == article_data.new_article.id


def test_create_article_no_permissions(article_svc: ArticleService):
    """Ensures that a student cannot create an article"""
    with pytest.raises(UserPermissionException):
        article_svc.create_article(user_data.student, article_data.new_article)


def test_edit_article(article_svc: ArticleService):
    """Ensures that the admin can edit an article"""
    edited_article = article_data.article_one
    edited_article.title = "New title"
    article = article_svc.edit_article(user_data.root, edited_article)
    assert article is not None
    assert article.id == edited_article.id
    assert article.title == edited_article.title


def test_edit_article_no_permissions(article_svc: ArticleService):
    """Ensures that a student cannot edit an article"""
    with pytest.raises(UserPermissionException):
        edited_article = article_data.article_one
        edited_article.title = "New title"
        article_svc.edit_article(user_data.student, edited_article)


def test_edit_article_does_not_exist(article_svc: ArticleService):
    """Ensures that the admin cannot edit an article that does not exist"""
    with pytest.raises(ResourceNotFoundException):
        article = article_svc.edit_article(user_data.root, article_data.new_article)


def test_delete_article(article_svc: ArticleService):
    """Ensures that the admin can delete an article"""
    article_svc.delete_article(user_data.root, article_data.article_one.id)


def test_delete_article_no_permissions(article_svc: ArticleService):
    """Ensures that a student cannot delete an article"""
    with pytest.raises(UserPermissionException):
        article_svc.delete_article(user_data.student, article_data.article_one.id)


def test_delete_article_does_not_exist(article_svc: ArticleService):
    """Ensures that the admin cannot delete an article that does not exist"""
    with pytest.raises(ResourceNotFoundException):
        article_svc.delete_article(user_data.root, article_data.new_article.id)
