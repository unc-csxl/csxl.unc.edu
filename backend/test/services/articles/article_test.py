"""Tests for the Article Service."""

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
from .scenario import ArticleScenario, arrange_article_scenario

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def article_scenario(session) -> ArticleScenario:
    return arrange_article_scenario(session)


def test_get_welcome_overview(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that users are able to get the welcome overview."""
    welcome_overview = article_svc.get_welcome_overview(article_scenario.auth.student)
    assert welcome_overview is not None
    assert isinstance(welcome_overview, WelcomeOverview)
    assert welcome_overview.announcement is not None
    assert len(welcome_overview.latest_news) == len(
        article_scenario.articles_no_announcement
    )


def test_get_welcome_unauthenticated(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that logged out users are able to get the welcome overview."""
    welcome_overview = article_svc.get_welcome_overview(None)
    assert welcome_overview is not None
    assert isinstance(welcome_overview, WelcomeOverview)
    assert welcome_overview.announcement is not None
    assert len(welcome_overview.latest_news) == len(
        article_scenario.articles_no_announcement
    )


def test_get_by_slug(article_svc: ArticleService, article_scenario: ArticleScenario):
    """Ensures that users can get articles."""
    article = article_svc.get_article(article_scenario.article_one.slug)
    assert article is not None
    assert article.id == article_scenario.article_one.id


def test_get_by_slug_not_found(article_svc: ArticleService):
    """Ensures that users who search for blank articles get a null response."""
    article = article_svc.get_article("404")
    assert article is None


def test_list(article_svc: ArticleService, article_scenario: ArticleScenario):
    """Ensures that the admin can list all articles."""
    pagination_params = PaginationParams(page=0, page_size=10, filter="")
    articles = article_svc.list(article_scenario.auth.root, pagination_params)
    assert articles is not None
    assert len(articles.items) == 3


def test_list_not_admin(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that non-admins cannot access all articles."""
    with pytest.raises(UserPermissionException):
        pagination_params = PaginationParams(page=0, page_size=10, filter="")
        article_svc.list(article_scenario.auth.student, pagination_params)


def test_create_article(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that the admin can create an article"""
    article = article_svc.create_article(
        article_scenario.auth.root,
        article_scenario.new_article.model_copy(deep=True),
    )
    assert article is not None
    assert article.id == article_scenario.new_article.id


def test_create_article_no_permissions(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that a student cannot create an article"""
    with pytest.raises(UserPermissionException):
        article_svc.create_article(
            article_scenario.auth.student,
            article_scenario.new_article.model_copy(deep=True),
        )


def test_edit_article(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that the admin can edit an article"""
    edited_article = article_scenario.article_one.model_copy(deep=True)
    edited_article.title = "New title"
    article = article_svc.edit_article(article_scenario.auth.root, edited_article)
    assert article is not None
    assert article.id == edited_article.id
    assert article.title == edited_article.title


def test_edit_article_no_permissions(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that a student cannot edit an article"""
    with pytest.raises(UserPermissionException):
        edited_article = article_scenario.article_one.model_copy(deep=True)
        edited_article.title = "New title"
        article_svc.edit_article(article_scenario.auth.student, edited_article)


def test_edit_article_does_not_exist(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that the admin cannot edit an article that does not exist"""
    with pytest.raises(ResourceNotFoundException):
        article_svc.edit_article(
            article_scenario.auth.root,
            article_scenario.new_article.model_copy(deep=True),
        )


def test_delete_article(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that the admin can delete an article"""
    article_svc.delete_article(
        article_scenario.auth.root, article_scenario.article_one.id
    )


def test_delete_article_no_permissions(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that a student cannot delete an article"""
    with pytest.raises(UserPermissionException):
        article_svc.delete_article(
            article_scenario.auth.student, article_scenario.article_one.id
        )


def test_delete_article_does_not_exist(
    article_svc: ArticleService, article_scenario: ArticleScenario
):
    """Ensures that the admin cannot delete an article that does not exist"""
    with pytest.raises(ResourceNotFoundException):
        article_svc.delete_article(
            article_scenario.auth.root, article_scenario.new_article.id
        )
