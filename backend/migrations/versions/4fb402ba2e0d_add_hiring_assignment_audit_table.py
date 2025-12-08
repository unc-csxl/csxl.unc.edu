"""Add hiring assignment audit table

Revision ID: 4fb402ba2e0d
Revises: 0a57afd03df5
Create Date: 2025-12-07 19:02:21.685299

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4fb402ba2e0d"
down_revision = "0a57afd03df5"


def upgrade() -> None:
    op.create_table(
        "academics__hiring__assignment_audit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("hiring_assignment_id", sa.Integer(), nullable=False),
        sa.Column("changed_by_user_id", sa.Integer(), nullable=False),
        sa.Column("change_timestamp", sa.DateTime(), nullable=False),
        sa.Column("change_details", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["changed_by_user_id"],
            ["user.id"],
            name=op.f("fk_academics__hiring__assignment_audit_changed_by_user_id_user"),
        ),
        sa.ForeignKeyConstraint(
            ["hiring_assignment_id"],
            ["academics__hiring__assignment.id"],
            name=op.f(
                "fk_academics__hiring__assignment_audit_hiring_assignment_id_assignment"
            ),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_academics__hiring__assignment_audit")
        ),
    )


def downgrade() -> None:
    op.drop_table("academics__hiring__assignment_audit")
