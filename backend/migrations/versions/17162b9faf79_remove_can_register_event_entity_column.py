"""Migration for 232-remove-can-register-column-from-event

Revision ID: 17162b9faf79
Revises: 1952e411745f
Create Date: 2023-12-31 15:25:44.947516

"""
from alembic import op
import sqlalchemy as sa


revision = "17162b9faf79"
down_revision = "1952e411745f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("event", "can_register")


def downgrade() -> None:
    op.add_column(
        "event",
        sa.Column(
            "can_register",
            sa.Boolean(),
            nullable=False,
            default=False,
            server_default=sa.text("false"),
        ),
    )
