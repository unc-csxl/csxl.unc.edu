"""Add autoincrement id to academics__user_section

Revision ID: eb379629af4f
Revises: 1d7ab0cd0f58
Create Date: 2024-05-16 03:41:25.710040

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb379629af4f"
down_revision = "1d7ab0cd0f58"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE academics__user_section ALTER COLUMN id SET DEFAULT nextval('academics__user_section_id_seq')"
    )
    pass


def downgrade() -> None:
    pass
