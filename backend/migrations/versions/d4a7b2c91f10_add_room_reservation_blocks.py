"""Add room reservation blocks.

Revision ID: d4a7b2c91f10
Revises: a9f09b49d862
Create Date: 2026-08-30
"""

from alembic import op
import sqlalchemy as sa


revision = "d4a7b2c91f10"
down_revision = "a9f09b49d862"
branch_labels = None
depends_on = None


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


def downgrade() -> None:
    op.drop_index(
        "coworking__room_reservation_block_schedule_idx",
        table_name="coworking__room_reservation_block",
    )
    op.drop_table("coworking__room_reservation_block")
