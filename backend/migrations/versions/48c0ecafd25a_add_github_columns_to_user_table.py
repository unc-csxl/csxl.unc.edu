"""Add GitHub integration columns to user table

Revision ID: 48c0ecafd25a
Revises: 
Create Date: 2023-04-01 09:28:21.368072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "48c0ecafd25a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("github", sa.String(length=32), nullable=False, server_default=""),
    )
    op.add_column("user", sa.Column("github_id", sa.Integer(), nullable=True))
    op.add_column("user", sa.Column("github_avatar", sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column("user", "github")
    op.drop_column("user", "github_id")
    op.drop_column("user", "github_avatar")
