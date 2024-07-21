"""Articles API"""

from fastapi import APIRouter, Depends

from ..api.authentication import registered_user

from ..services.article import ArticleService

from ..models import User
from ..models.articles import WelcomeOverview, ArticleOverview
from ..models.pagination import Paginated, PaginationParams

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


@api.get("/list", tags=["Articles"])
def list(
    subject: User = Depends(registered_user),
    article_svc: ArticleService = Depends(),
    page: int = 0,
    page_size: int = 10,
    order_by: str = "",
    filter: str = "",
) -> Paginated[ArticleOverview]:
    """List paginated articles."""
    pagination_params = PaginationParams(
        page=page, page_size=page_size, order_by=order_by, filter=filter
    )
    return article_svc.list(subject, pagination_params)


@api.get("/{slug}", tags=["Articles"])
def get_article(
    slug: str,
    article_svc: ArticleService = Depends(),
) -> ArticleOverview:
    """Retrieves the welcome status."""
    return article_svc.get_article(slug)
