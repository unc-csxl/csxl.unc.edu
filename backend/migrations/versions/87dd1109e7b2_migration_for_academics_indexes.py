"""Adds Indexes to Academics for common query patterns.

Revision ID: 87dd1109e7b2
Revises: eb379629af4f
Create Date: 2024-06-08 07:17:36.113064
Author: Kris Jordan
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "87dd1109e7b2"
down_revision = "eb379629af4f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add indices to the academics__section and academics__user_section tables for common query patterns.
    op.create_index(
        "ix_academics__section__by_course",
        "academics__section",
        ["course_id", "term_id"],
        unique=False,
    )
    op.create_index(
        "ix_academics__section__by_term",
        "academics__section",
        ["term_id", "course_id"],
        unique=False,
    )

    op.create_index(
        "ix_academics__user_section__by_section",
        "academics__user_section",
        ["section_id", "member_role"],
        unique=False,
    )
    op.create_index(
        "ix_academics__user_section__by_user",
        "academics__user_section",
        ["user_id", "section_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_academics__user_section__by_user", table_name="academics__user_section"
    )
    op.drop_index(
        "ix_academics__user_section__by_section", table_name="academics__user_section"
    )
    op.drop_index("ix_academics__section__by_term", table_name="academics__section")
    op.drop_index("ix_academics__section__by_course", table_name="academics__section")
