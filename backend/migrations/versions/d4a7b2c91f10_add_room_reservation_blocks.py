"""Add room reservation blocks.

Revision ID: d4a7b2c91f10
Revises: a9f09b49d862
Create Date: 2026-08-30
"""

from datetime import date, time

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import Connection


revision = "d4a7b2c91f10"
down_revision = "a9f09b49d862"
branch_labels = None
depends_on = None


# Frozen from PolicyService.OH_HOURS at cutover. Temporary COMP211 entries are
# bounded to the requested week so they never become indefinite policy.
LONG_LIVED_START = date(2026, 8, 30)


def _block(
    room_id: str,
    label: str,
    weekday: int,
    start_time: time,
    end_time: time,
    starts_on: date = LONG_LIVED_START,
    ends_on: date | None = None,
) -> dict[str, object]:
    return {
        "room_id": room_id,
        "label": label,
        "weekday": weekday,
        "start_time": start_time,
        "end_time": end_time,
        "starts_on": starts_on,
        "ends_on": ends_on,
        "enabled": True,
    }


INITIAL_ROOM_RESERVATION_BLOCKS = [
    _block("SN141", "Office Hours", 0, time(10), time(12)),
    _block("SN141", "Office Hours", 0, time(16), time(17)),
    _block("SN147", "Office Hours", 0, time(13), time(14)),
    _block("SN135", "Office Hours", 1, time(12), time(16)),
    _block(
        "SN147",
        "COMP211 Check-off",
        1,
        time(11, 30),
        time(17),
        date(2026, 9, 1),
        date(2026, 9, 1),
    ),
    _block("SN141", "Office Hours", 2, time(10), time(12)),
    _block(
        "SN141",
        "COMP211 Check-off",
        2,
        time(13, 30),
        time(15, 30),
        date(2026, 9, 2),
        date(2026, 9, 2),
    ),
    _block("SN141", "Office Hours", 2, time(16), time(18)),
    _block(
        "SN147",
        "COMP211 Check-off",
        2,
        time(11, 30),
        time(14),
        date(2026, 9, 2),
        date(2026, 9, 2),
    ),
    _block("SN147", "Office Hours", 2, time(14), time(15)),
    _block(
        "SN147",
        "COMP211 Check-off",
        2,
        time(15),
        time(17),
        date(2026, 9, 2),
        date(2026, 9, 2),
    ),
    _block("SN135", "Office Hours", 3, time(12), time(17)),
    _block(
        "SN147",
        "COMP211 Check-off",
        3,
        time(11, 30),
        time(17),
        date(2026, 9, 3),
        date(2026, 9, 3),
    ),
    _block("SN141", "Office Hours", 4, time(13), time(18)),
    _block(
        "SN147",
        "COMP211 Check-off",
        4,
        time(11, 30),
        time(15, 30),
        date(2026, 9, 4),
        date(2026, 9, 4),
    ),
]


def _backfill_room_reservation_blocks(connection: Connection) -> None:
    """Insert frozen policy rows when their room exists."""
    statement = sa.text(
        """
        INSERT INTO coworking__room_reservation_block
            (room_id, label, weekday, start_time, end_time, starts_on, ends_on,
             enabled, created_at, updated_at)
        SELECT
            :room_id, :label, :weekday, :start_time, :end_time,
            :starts_on, :ends_on, :enabled, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        WHERE EXISTS (SELECT 1 FROM room WHERE id = :room_id)
        """
    )
    for block in INITIAL_ROOM_RESERVATION_BLOCKS:
        connection.execute(statement, block)


def upgrade() -> None:
    op.create_table(
        "coworking__room_reservation_block",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("room_id", sa.String(), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("weekday", sa.SmallInteger(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=True),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint(
            "weekday BETWEEN 0 AND 6",
            name="coworking__room_reservation_block_weekday_check",
        ),
        sa.CheckConstraint(
            "start_time < end_time",
            name="coworking__room_reservation_block_time_range_check",
        ),
        sa.CheckConstraint(
            "ends_on IS NULL OR ends_on >= starts_on",
            name="coworking__room_reservation_block_date_range_check",
        ),
        sa.CheckConstraint(
            "length(trim(label)) > 0",
            name="coworking__room_reservation_block_label_check",
        ),
        sa.CheckConstraint(
            "EXTRACT(MINUTE FROM start_time) IN (0, 30) "
            "AND EXTRACT(SECOND FROM start_time) = 0 "
            "AND EXTRACT(MINUTE FROM end_time) IN (0, 30) "
            "AND EXTRACT(SECOND FROM end_time) = 0",
            name="coworking__room_reservation_block_half_hour_check",
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["room.id"],
            name="coworking__room_reservation_block_room_id_fkey",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "coworking__room_reservation_block_schedule_idx",
        "coworking__room_reservation_block",
        ["room_id", "weekday", "starts_on", "ends_on"],
        unique=False,
    )
    _backfill_room_reservation_blocks(op.get_bind())


def downgrade() -> None:
    op.drop_index(
        "coworking__room_reservation_block_schedule_idx",
        table_name="coworking__room_reservation_block",
    )
    op.drop_table("coworking__room_reservation_block")
