"""Migration for 526-welcome-page

Revision ID: bc68e4844a24
Revises: 3da4a0776787
Create Date: 2024-07-23 18:57:22.572728

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bc68e4844a24"
down_revision = "3da4a0776787"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column(
            "state",
            sa.Enum("DRAFT", "PUBLISHED", "ARCHIVED", name="articlestate"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("synopsis", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("published", sa.DateTime(), nullable=False),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("is_announcement", sa.Boolean(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "article_author",
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["article.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("article_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table("article_author")
    op.drop_table("article")
