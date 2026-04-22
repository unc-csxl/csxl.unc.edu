"""Update R.A.M. Engineering organization profile

Revision ID: c3d9f9e2a1b4
Revises: a9f09b49d862
Create Date: 2026-04-22 00:00:00.000000

"""

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "c3d9f9e2a1b4"
down_revision = "a9f09b49d862"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        text(
            """
            UPDATE organization
            SET
                name = 'R.A.M. Engineering',
                shorthand = 'R.A.M. Engineering',
                short_description = 'UNC''s premier Engineering club progressing innovation across Robotics, Aeronautics, and Microdevices. Engineering Greatness @Carolina.',
                long_description = 'UNC''s premier Engineering club progressing innovation across Robotics, Aeronautics, and Microdevices. Engineering Greatness @Carolina.'
            WHERE
                slug IN ('ram-engineering', 'r-a-m-engineering')
                OR lower(name) IN ('r.a.m engineering', 'r.a.m. engineering', 'ram engineering');
            """
        )
    )
    op.execute(
        text(
            """
            UPDATE organization
            SET logo = replace(
                replace(logo, 'https://github.com/', 'https://raw.githubusercontent.com/'),
                '/blob/',
                '/'
            )
            WHERE
                (slug IN ('ram-engineering', 'r-a-m-engineering')
                OR lower(name) IN ('r.a.m engineering', 'r.a.m. engineering', 'ram engineering'))
                AND logo LIKE 'https://github.com/%/blob/%';
            """
        )
    )


def downgrade() -> None:
    pass
