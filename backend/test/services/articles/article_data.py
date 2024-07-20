"""Contains mock data for the live demo of the article feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.articles import *
from ....entities.article_entity import ArticleEntity, article_author_table
from datetime import datetime

from ..reset_table_id_seq import reset_table_id_seq

from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Sample Articles

announcement = ArticleDraft(
    id=0,
    slug="my-announcement",
    state=ArticleState.PUBLISHED,
    title="Sample Announcement",
    image_url="none",
    synopsis="Sample synopsis",
    body="This is a sample article body in **markdown!**",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=True,
    organization_slug=None,
    authors=[],
)

article_one = ArticleDraft(
    id=1,
    slug="article-one",
    state=ArticleState.PUBLISHED,
    title="Article One",
    image_url="none",
    synopsis="Sample synopsis",
    body="This is a sample article body in **markdown!**",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=False,
    organization_slug=None,
    authors=[],
)

article_two = ArticleDraft(
    id=2,
    slug="article-two",
    state=ArticleState.PUBLISHED,
    title="Article Two",
    image_url="none",
    synopsis="Sample synopsis",
    body="This is a sample article body in **markdown!**",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=False,
    organization_slug=None,
    authors=[],
)

articles = [announcement, article_one, article_two]
articles_no_announcement = [article_one, article_two]

author_associations = [
    (announcement, user_data.root),
    (article_one, user_data.root),
    (article_two, user_data.root),
]


def insert_fake_data(session: Session):

    # Step 1: Add articles to database
    for article in articles:
        entity = ArticleEntity.from_draft(article)
        session.add(entity)

    reset_table_id_seq(
        session,
        ArticleEntity,
        ArticleEntity.id,
        len(articles) + 1,
    )

    session.commit()

    # Step 2: Add authors to the datbase

    for article, author in author_associations:
        session.execute(
            article_author_table.insert().values(
                {"user_id": author.id, "article_id": article.id}
            )
        )
        session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
