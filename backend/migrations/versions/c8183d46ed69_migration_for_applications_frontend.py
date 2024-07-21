"""Migration for applications-frontend

Revision ID: c8183d46ed69
Revises: c7fef3274f15
Create Date: 2024-07-20 10:09:42.200482

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c8183d46ed69"
down_revision = "c7fef3274f15"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "academics__term", sa.Column("applications_open", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "academics__term", sa.Column("applications_close", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "application",
        sa.Column("term_id", sa.String(length=6), nullable=False, server_default="24F"),
    )
    op.add_column("application", sa.Column("advisor", sa.String(), nullable=True))
    op.alter_column(
        "application", "academic_hours", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "application", "expected_graduation", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "application", "program_pursued", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "application",
        "gpa",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.create_foreign_key(
        "application__academics_term_fk",
        "application",
        "academics__term",
        ["term_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "application__academics_term_fk", "application", type_="foreignkey"
    )
    op.alter_column(
        "application",
        "gpa",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "application", "program_pursued", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "application", "expected_graduation", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "application", "academic_hours", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_column("application", "advisor")
    op.drop_column("application", "term_id")
    op.drop_column("academics__term", "applications_close")
    op.drop_column("academics__term", "applications_open")
