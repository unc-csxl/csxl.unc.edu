"""Migration for authentication-race-condition-fix

Revision ID: 684f2df8b00e
Revises: 8fff82538f2e
Create Date: 2024-08-18 20:45:13.475404

"""

from datetime import timedelta
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "684f2df8b00e"
down_revision = "8fff82538f2e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("event", "time", new_column_name="start")

    # Add end column as nullable
    op.add_column("event", sa.Column("end", sa.DateTime(), nullable=True))

    # Populate past events to have an end time one hour later
    event_table = table(
        "event",
        column("id", sa.Integer()),
        column("start", sa.DateTime()),
        column("end", sa.DateTime()),
    )
    conn = op.get_bind()
    events = conn.execute(sa.select(event_table.c.id, event_table.c.start))
    for event in events:
        # Calculate the end time as one hour after the start time
        end_time = event.start + timedelta(hours=1)
        conn.execute(
            event_table.update()
            .where(event_table.c.id == event.id)
            .values(end=end_time)
        )

    # Update end column as non-nullable
    op.alter_column("event", "end", nullable=False)

    op.add_column(
        "event", sa.Column("override_registration_url", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("event", "override_registration_url")
    op.drop_column("event", "end")
    op.alter_column("event", "start", new_column_name="time")
