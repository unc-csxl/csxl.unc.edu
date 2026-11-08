"""Allow full faculty email addresses without truncation.

Revision ID: b27e20261108
Revises: a9f09b49d862
Create Date: 2026-11-08

Production received this widening as an explicitly approved prerequisite to
faculty provisioning. Reapplying it through Alembic preserves the same type.
"""

import sqlalchemy as sa
from alembic import op

revision = "b27e20261108"
down_revision = "a9f09b49d862"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "user",
        "email",
        existing_type=sa.String(length=32),
        type_=sa.String(length=254),
        existing_nullable=False,
    )


def downgrade() -> None:
    # PostgreSQL must reject this if any address exceeds 32; never truncate data.
    op.alter_column(
        "user",
        "email",
        existing_type=sa.String(length=254),
        type_=sa.String(length=32),
        existing_nullable=False,
    )
