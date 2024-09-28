"""Signage API"""

from fastapi import APIRouter, Depends

from ..api.authentication import registered_user

from ..services.article import ArticleService

from ..models import User
from ..models.articles import WelcomeOverview, ArticleOverview, ArticleDraft
from ..models.pagination import Paginated, PaginationParams

__authors__ = ["Will Zahrt"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/signage")
openapi_tags = {
    "name": "Signage",
    "description": "Retrieve signage information.",
}


@api.get("/slow", tags=["Signage"])
def get_welcome_status(
    subject: User = Depends(registered_user), article_svc: ArticleService = Depends()
) -> WelcomeOverview:
    """Retrieves the welcome status."""
    return article_svc.get_welcome_overview(subject)


@api.get("/fast", tags=["Signage"])
def get_welcome_status(
    subject: User = Depends(registered_user), article_svc: ArticleService = Depends()
) -> WelcomeOverview:
    """Retrieves the welcome status."""
    return article_svc.get_welcome_overview(subject)
