"""Migration for office-hours

Revision ID: 1d7ab0cd0f58
Revises: 92214831537d
Create Date: 2024-05-13 16:22:22.137639

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1d7ab0cd0f58"
down_revision = "92214831537d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "academics__section",
        sa.Column("office_hours_id", sa.Integer(), nullable=True),
    )

    # Deal with the Academics <-> User Section ID Column
    op.execute("CREATE SEQUENCE academics__user_section_id_seq")
    op.add_column(
        "academics__user_section",
        sa.Column(
            "id",
            sa.Integer(),
            sa.Sequence("academics__user_section_id_seq"),
            autoincrement=True,
        ),
    )
    op.execute(
        "UPDATE academics__user_section SET id = nextval('academics__user_section_id_seq')"
    )
    op.create_unique_constraint(
        "academics__user_section_id_key", "academics__user_section", ["id"]
    )
    op.alter_column(
        "academics__user_section",
        "id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.create_table(
        "course_site",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "office_hours",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "OFFICE_HOURS",
                "TUTORING",
                "REVIEW_SESSION",
                name="office_hours__type",
            ),
            nullable=False,
        ),
        sa.Column(
            "mode",
            sa.Enum(
                "IN_PERSON",
                "VIRTUAL_STUDENT_LINK",
                "VIRTUAL_OUR_LINK",
                name="office_hours__mode",
            ),
            nullable=False,
        ),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("location_description", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("office_hours_section_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["office_hours_section_id"],
            ["course_site.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["room.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "office_hours__ticket",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "CONCEPTUAL_HELP", "ASSIGNMENT_HELP", name="office_hours__ticket__type"
            ),
            nullable=False,
        ),
        sa.Column(
            "state",
            sa.Enum(
                "QUEUED",
                "CALLED",
                "CLOSED",
                "CANCELED",
                name="office_hours__ticket__state",
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("called_at", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("have_concerns", sa.Boolean(), nullable=False),
        sa.Column("caller_notes", sa.String(), nullable=False),
        sa.Column("oh_event_id", sa.Integer(), nullable=False),
        sa.Column("caller_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["caller_id"],
            ["academics__user_section.id"],
        ),
        sa.ForeignKeyConstraint(
            ["oh_event_id"],
            ["office_hours.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "office_hours__user_created_ticket",
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["academics__user_section.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["office_hours__ticket.id"],
        ),
        sa.PrimaryKeyConstraint("ticket_id", "member_id"),
    )

    op.create_foreign_key(
        "academics_to_office_hours_fk",
        "academics__section",
        "course_site",
        ["office_hours_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "academics_to_office_hours_fk", "academics__section", type_="foreignkey"
    )
    op.drop_column("academics__section", "office_hours_id")
    op.drop_table("office_hours__user_created_ticket")
    op.drop_table("office_hours__ticket")

    # Remove the id column
    op.drop_column("academics__user_section", "id")
    op.execute("DROP SEQUENCE academics__user_section_id_seq")

    # Drop the event/section tables
    op.drop_table("office_hours")
    op.drop_table("course_site")

    # Clean-up the enum types
    op.execute("DROP TYPE office_hours__type")
    op.execute("DROP TYPE office_hours__mode")
    op.execute("DROP TYPE office_hours__ticket__type")
    op.execute("DROP TYPE office_hours__ticket__state")
