"""Complete My Courses migration

Revision ID: aa567132afd4
Revises: 4582da0d11d3
Create Date: 2024-07-01 19:35:56.267019

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aa567132afd4"
down_revision = "4582da0d11d3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("office_hours", "date")


def downgrade() -> None:
    op.add_column(
        "office_hours",
        sa.Column("date", sa.DATE(), autoincrement=False, nullable=False),
    )
