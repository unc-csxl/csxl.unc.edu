"""Explicit arrange helpers for article service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.article_entity import ArticleEntity, article_author_table
from ....models.articles import ArticleDraft, ArticleState
from ....models.public_user import PublicUser
from ..auth_scenario import AuthScenario, arrange_auth_scenario
from ..reset_table_id_seq import reset_table_id_seq


@dataclass
class ArticleScenario:
    auth: AuthScenario
    announcement: ArticleDraft
    article_one: ArticleDraft
    article_two: ArticleDraft
    new_article: ArticleDraft

    @property
    def articles_no_announcement(self) -> list[ArticleDraft]:
        return [self.article_one, self.article_two]


def _author(user) -> PublicUser:
    return PublicUser(
        id=user.id,
        onyen=user.onyen,
        first_name=user.first_name,
        last_name=user.last_name,
        pronouns=user.pronouns,
        email=user.email,
        github_avatar=user.github_avatar,
        github=user.github,
        bio=user.bio,
        linkedin=user.linkedin,
        website=user.website,
    )


def arrange_article_scenario(session: Session) -> ArticleScenario:
    auth = arrange_auth_scenario(session)
    now = datetime.now().replace(microsecond=0)

    announcement = ArticleDraft(
        id=0,
        slug="my-announcement",
        state=ArticleState.PUBLISHED,
        title="Sample Announcement",
        image_url="https://example.com/announcement.png",
        synopsis="Announcement synopsis",
        body="Announcement body",
        published=now - timedelta(days=2),
        last_modified=now - timedelta(days=2),
        is_announcement=True,
        organization_id=None,
        authors=[_author(auth.root)],
    )
    article_one = ArticleDraft(
        id=1,
        slug="article-one",
        state=ArticleState.PUBLISHED,
        title="Article One",
        image_url="https://example.com/article-one.png",
        synopsis="Article one synopsis",
        body="Article one body",
        published=now - timedelta(days=1),
        last_modified=now - timedelta(days=1),
        is_announcement=False,
        organization_id=None,
        authors=[_author(auth.root)],
    )
    article_two = ArticleDraft(
        id=2,
        slug="article-two",
        state=ArticleState.PUBLISHED,
        title="Article Two",
        image_url="https://example.com/article-two.png",
        synopsis="Article two synopsis",
        body="Article two body",
        published=now,
        last_modified=now,
        is_announcement=False,
        organization_id=None,
        authors=[_author(auth.root)],
    )
    new_article = ArticleDraft(
        id=3,
        slug="article-three",
        state=ArticleState.PUBLISHED,
        title="Article Three",
        image_url="https://example.com/article-three.png",
        synopsis="Article three synopsis",
        body="Article three body",
        published=now + timedelta(minutes=1),
        last_modified=now + timedelta(minutes=1),
        is_announcement=False,
        organization_id=None,
        authors=[_author(auth.root)],
    )

    articles = [announcement, article_one, article_two]
    session.add_all(ArticleEntity.from_draft(article) for article in articles)
    reset_table_id_seq(session, ArticleEntity, ArticleEntity.id, 4)
    session.commit()

    for article in articles:
        for author in article.authors:
            session.execute(
                article_author_table.insert().values(
                    {"user_id": author.id, "article_id": article.id}
                )
            )
    session.commit()

    return ArticleScenario(
        auth=auth,
        announcement=announcement,
        article_one=article_one,
        article_two=article_two,
        new_article=new_article,
    )
