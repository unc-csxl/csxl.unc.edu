"""Migration for hiring-migration

Revision ID: c7fef3274f15
Revises: aa567132afd4
Create Date: 2024-07-16 14:51:18.725944

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c7fef3274f15"
down_revision = "aa567132afd4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "academics__hiring__application_review",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("course_site_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "NOT_PREFERRED",
                "NOT_PROCESSED",
                "PREFERRED",
                name="applicationreviewstatus",
            ),
            nullable=False,
        ),
        sa.Column("preference", sa.Integer(), nullable=False),
        sa.Column("notes", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["application.id"],
        ),
        sa.ForeignKeyConstraint(
            ["course_site_id"],
            ["course_site.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "academics__hiring__application_review_course_idx",
        "academics__hiring__application_review",
        ["course_site_id", "status", "preference"],
        unique=False,
    )
    op.alter_column(
        "application", "intro_video_url", existing_type=sa.VARCHAR(), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "application", "intro_video_url", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_index(
        "academics__hiring__application_review_course_idx",
        table_name="academics__hiring__application_review",
    )
    op.drop_table("academics__hiring__application_review")
