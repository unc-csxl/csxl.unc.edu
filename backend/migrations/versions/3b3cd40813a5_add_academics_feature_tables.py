"""Add Academics Feature Tables

Revision ID: 3b3cd40813a5
Revises: 63fc48273e15
Create Date: 2023-12-30 08:36:42.253188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3b3cd40813a5"
down_revision = "63fc48273e15"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("coworking__room", "room")

    op.create_table(
        "academics__course",
        sa.Column("id", sa.String(length=9), nullable=False),
        sa.Column("subject_code", sa.String(length=4), nullable=False),
        sa.Column("number", sa.String(length=4), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("credit_hours", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "academics__term",
        sa.Column("id", sa.String(length=6), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("start", sa.DateTime(), nullable=False),
        sa.Column("end", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "academics__section",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("course_id", sa.String(length=9), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("term_id", sa.String(length=6), nullable=False),
        sa.Column("meeting_pattern", sa.String(), nullable=False),
        sa.Column("override_title", sa.String(), nullable=False),
        sa.Column("override_description", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["academics__course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["term_id"],
            ["academics__term.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "academics__section_room",
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.String(), nullable=False),
        sa.Column(
            "assignment_type",
            sa.Enum("LECTURE_ROOM", "OFFICE_HOURS", name="roomassignmenttype"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["room.id"],
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["academics__section.id"],
        ),
        sa.PrimaryKeyConstraint("section_id", "room_id"),
    )
    op.create_table(
        "academics__user_section",
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "member_role",
            sa.Enum("STUDENT", "UTA", "GTA", "INSTRUCTOR", name="rosterrole"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["academics__section.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("section_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table("academics__user_section")
    op.execute("DROP TYPE rosterrole")

    op.drop_table("academics__section_room")
    op.execute("DROP TYPE roomassignmenttype")

    op.drop_table("academics__section")

    op.drop_table("academics__term")

    op.drop_table("academics__course")

    op.rename_table("room", "coworking__room")
