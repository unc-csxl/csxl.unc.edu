"""Add Events Entity

Revision ID: 63fc48273e15
Revises: 41ce034b593f
Create Date: 2023-10-22 21:31:55.595465

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "63fc48273e15"
down_revision = "41ce034b593f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("public", sa.Boolean(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organization.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("event")
