"""Migration for 484-profile-page-m3

Revision ID: 3da4a0776787
Revises: 909fe23fc93f
Create Date: 2024-07-23 18:32:25.724472
"""

from alembic import op
import sqlalchemy as sa


revision = "3da4a0776787"
down_revision = "909fe23fc93f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user", sa.Column("bio", sa.String(), nullable=False, server_default="")
    )
    op.add_column(
        "user", sa.Column("linkedin", sa.String(), nullable=False, server_default="")
    )
    op.add_column(
        "user", sa.Column("website", sa.String(), nullable=False, server_default="")
    )


def downgrade() -> None:
    op.drop_column("user", "website")
    op.drop_column("user", "linkedin")
    op.drop_column("user", "bio")
