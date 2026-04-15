"""Explicit arrange helpers for article service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.article_entity import ArticleEntity, article_author_table
from ....entities.permission_entity import PermissionEntity
from ....entities.role_entity import RoleEntity
from ....entities.user_entity import UserEntity
from ....entities.user_role_table import user_role_table
from ....models.articles import ArticleDraft, ArticleState
from ....models import Permission, Role
from ....models.public_user import PublicUser
from ....models.user import User
from ..reset_table_id_seq import reset_table_id_seq


@dataclass(frozen=True)
class ArticleAuthScenario:
    root_role: Role
    root_permission: Permission
    root: User
    student: User


@dataclass
class ArticleScenario:
    auth: ArticleAuthScenario
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


def build_article_auth_scenario() -> ArticleAuthScenario:
    return ArticleAuthScenario(
        root_role=Role(id=1, name="root"),
        root_permission=Permission(id=1, action="*", resource="*"),
        root=User(
            id=1,
            pid=999999999,
            onyen="root",
            email="root@unc.edu",
            first_name="Rhonda",
            last_name="Root",
            pronouns="She / Her / Hers",
            accepted_community_agreement=True,
        ),
        student=User(
            id=2,
            pid=555555555,
            onyen="Stewie",
            email="stewie@unc.edu",
            first_name="Stewie",
            last_name="Student",
            pronouns="They / Them / Theirs",
            accepted_community_agreement=True,
        ),
    )


def arrange_article_scenario(session: Session) -> ArticleScenario:
    auth = build_article_auth_scenario()
    now = datetime.now().replace(microsecond=0)

    session.add(RoleEntity.from_model(auth.root_role))
    session.add_all(
        [UserEntity.from_model(auth.root), UserEntity.from_model(auth.student)]
    )
    session.flush()
    session.execute(
        user_role_table.insert().values(
            {"role_id": auth.root_role.id, "user_id": auth.root.id}
        )
    )
    session.add(
        PermissionEntity(
            id=auth.root_permission.id,
            role_id=auth.root_role.id,
            action=auth.root_permission.action,
            resource=auth.root_permission.resource,
        )
    )
    reset_table_id_seq(session, RoleEntity, RoleEntity.id, auth.root_role.id + 1)
    reset_table_id_seq(session, UserEntity, UserEntity.id, auth.student.id + 1)
    reset_table_id_seq(
        session,
        PermissionEntity,
        PermissionEntity.id,
        auth.root_permission.id + 1,
    )

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
