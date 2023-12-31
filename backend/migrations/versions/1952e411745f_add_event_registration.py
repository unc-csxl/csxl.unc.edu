"""Migration for feature/event-registration-frontend

Revision ID: 1952e411745f
Revises: 3b3cd40813a5
Create Date: 2023-12-31 12:21:27.507876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1952e411745f"
down_revision = "3b3cd40813a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_registration",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "registration_type",
            sa.Enum("ATTENDEE", "ORGANIZER", name="registrationtype"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["event.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("event_id", "user_id"),
    )
    op.add_column(
        "event",
        sa.Column(
            "registration_limit",
            sa.Integer(),
            nullable=False,
            default=0,
            server_default=sa.text("0"),
        ),
    )
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


def downgrade() -> None:
    op.drop_column("event", "can_register")
    op.drop_column("event", "registration_limit")
    op.drop_table("event_registration")
    op.execute("DROP TYPE registrationtype")
