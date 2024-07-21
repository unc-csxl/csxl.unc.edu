"""Articles API"""

from fastapi import APIRouter, Depends

from ..api.authentication import registered_user

from ..services.article import ArticleService

from ..models import User
from ..models.articles import WelcomeOverview, ArticleOverview

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/articles")
openapi_tags = {
    "name": "Articles",
    "description": "Create, update, delete, and retrieve articles.",
}


@api.get("/welcome", tags=["Articles"])
def get_welcome_status(
    subject: User = Depends(registered_user), article_svc: ArticleService = Depends()
) -> WelcomeOverview:
    """Retrieves the welcome status."""
    return article_svc.get_welcome_overview(subject)


@api.get("/{slug}", tags=["Articles"])
def get_article(
    slug: str,
    article_svc: ArticleService = Depends(),
) -> ArticleOverview:
    """Retrieves the welcome status."""
    return article_svc.get_article(slug)
