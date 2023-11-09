"""Add Organization Table

Revision ID: f7ad0c30eb78
Revises: 48c0ecafd25a
Create Date: 2023-09-12 10:28:16.426542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f7ad0c30eb78"
down_revision = "48c0ecafd25a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organization",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False, unique=True),
        sa.Column("logo", sa.String(), nullable=True),
        sa.Column("short_description", sa.String(), nullable=True),
        sa.Column("long_description", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("instagram", sa.String(), nullable=True),
        sa.Column("linked_in", sa.String(), nullable=True),
        sa.Column("youtube", sa.String(), nullable=True),
        sa.Column("heel_life", sa.String(), nullable=True),
        sa.Column("public", sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("organization")
