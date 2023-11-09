"""Add shorthand to organization

Revision ID: fe326bad2907
Revises: f7ad0c30eb78
Create Date: 2023-09-30 16:47:32.931411

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "fe326bad2907"
down_revision = "f7ad0c30eb78"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("organization", sa.Column("shorthand", sa.String()))
    # Default the shorthand of an org to name. Can be edited in admin later.
    op.execute(text("UPDATE organization SET shorthand = name"))
    op.alter_column("organization", "shorthand", nullable=False)


def downgrade() -> None:
    op.drop_column("organization", "shorthand")
