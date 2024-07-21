"""Migration for 482-events

Revision ID: 909fe23fc93f
Revises: c8183d46ed69
Create Date: 2024-07-20 20:45:42.827629

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "909fe23fc93f"
down_revision = "c8183d46ed69"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("event", sa.Column("image_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("event", "image_url")
