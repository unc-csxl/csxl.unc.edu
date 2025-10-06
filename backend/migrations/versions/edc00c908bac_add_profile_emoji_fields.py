"""add_profile_emoji_fields

Revision ID: edc00c908bac
Revises: a9f09b49d862
Create Date: 2025-10-04 13:30:55.791927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc00c908bac'
down_revision = 'a9f09b49d862'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("profile_emoji", sa.String(10), nullable=True))
    op.add_column("user", sa.Column("emoji_expiration", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "emoji_expiration")
    op.drop_column("user", "profile_emoji")
