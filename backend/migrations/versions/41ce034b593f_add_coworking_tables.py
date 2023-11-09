"""Add coworking tables

Revision ID: 41ce034b593f
Revises: fe326bad2907
Create Date: 2023-10-17 00:02:43.658738

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "41ce034b593f"
down_revision = "fe326bad2907"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "coworking__operating_hours",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("start", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("end", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="coworking__operating_hours_pkey"),
    )
    op.create_index(
        "ix_coworking__operating_hours_start",
        "coworking__operating_hours",
        ["start"],
        unique=False,
    )
    op.create_index(
        "ix_coworking__operating_hours_end",
        "coworking__operating_hours",
        ["end"],
        unique=False,
    )
    op.create_index(
        "coworking__operating_hours_idx",
        "coworking__operating_hours",
        ["start", "end"],
        unique=False,
    )

    op.create_table(
        "coworking__room",
        sa.Column("id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("capacity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("building", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("room", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("nickname", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("reservable", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="coworking__room_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index(
        "ix_coworking__room_capacity", "coworking__room", ["capacity"], unique=False
    )

    op.create_table(
        "coworking__seat",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('coworking__seat_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("shorthand", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("reservable", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("has_monitor", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("sit_stand", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("x", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("y", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("room_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"], ["coworking__room.id"], name="coworking__seat_room_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="coworking__seat_pkey"),
        postgresql_ignore_search_path=False,
    )

    op.create_table(
        "coworking__reservation",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("start", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("end", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("state", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("walkin", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("room_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["coworking__room.id"],
            name="coworking__reservation_room_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="coworking__reservation_pkey"),
    )
    op.create_index(
        "coworking__reservation_time_idx",
        "coworking__reservation",
        ["start", "end", "state"],
        unique=False,
    )

    op.create_table(
        "coworking__reservation_seat",
        sa.Column("reservation_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("seat_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["coworking__reservation.id"],
            name="coworking__reservation_seat_reservation_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["seat_id"],
            ["coworking__seat.id"],
            name="coworking__reservation_seat_seat_id_fkey",
        ),
        sa.PrimaryKeyConstraint(
            "reservation_id", "seat_id", name="coworking__reservation_seat_pkey"
        ),
    )

    op.create_table(
        "coworking__reservation_user",
        sa.Column("reservation_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["coworking__reservation.id"],
            name="coworking__reservation_user_reservation_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name="coworking__reservation_user_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint(
            "reservation_id", "user_id", name="coworking__reservation_user_pkey"
        ),
    )


def downgrade() -> None:
    op.drop_index(
        "coworking__operating_hours_idx", table_name="coworking__operating_hours"
    )
    op.drop_index(
        "ix_coworking__operating_hours_end", table_name="coworking__operating_hours"
    )
    op.drop_index(
        "ix_coworking__operating_hours_start", table_name="coworking__operating_hours"
    )
    op.drop_table("coworking__operating_hours")

    op.drop_table("coworking__reservation_seat")
    op.drop_table("coworking__reservation_user")

    op.drop_index(
        "coworking__reservation_time_idx", table_name="coworking__reservation"
    )
    op.drop_table("coworking__reservation")

    op.drop_table("coworking__seat")

    op.drop_index("ix_coworking__room_capacity", table_name="coworking__room")
    op.drop_table("coworking__room")
