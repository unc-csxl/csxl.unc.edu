"""Migration for MyCourses and CourseSite

Revision ID: 4582da0d11d3
Revises: 87dd1109e7b2
Create Date: 2024-06-29 12:40:21.984905

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4582da0d11d3"
down_revision = "87dd1109e7b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_table_academics_section_enrollments()
    upgrade_table_office_hours_section_to_course_site()
    upgrade_course_site_add_term_column()
    upgrade_table_oh_event_to_office_hours()


def downgrade() -> None:
    downgrade_table_office_hours_to_oh_event()
    downgrade_course_site_remove_term_columns()
    downgrade_course_site_to_office_hours_section()
    downgrade_table_academics_section_enrollments()


def upgrade_table_academics_section_enrollments():
    op.add_column(
        "academics__section",
        sa.Column("enrolled", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "academics__section",
        sa.Column("total_seats", sa.Integer(), nullable=False, server_default="0"),
    )


def upgrade_table_office_hours_section_to_course_site():
    # Workaround for custom fk constraint in prod (via migration) diverging from dev
    old_constraint_name = "academics_to_office_hours_fk"
    if not constraint_exists("academics__section", old_constraint_name):
        old_constraint_name = "academics__section_office_hours_id_fkey"
    op.drop_constraint(old_constraint_name, "academics__section", type_="foreignkey")
    # Rename Office Hours Section to Course Site
    op.rename_table("office_hours__section", "course_site")
    # Upgrade Academics/Section to CourseSite relationship
    op.alter_column(
        "academics__section", "office_hours_id", new_column_name="course_site_id"
    )
    # Add FK back
    op.create_foreign_key(
        "academics__section_course_site_id_fkey",
        "academics__section",
        "course_site",
        ["course_site_id"],
        ["id"],
    )


def upgrade_course_site_add_term_column():
    op.add_column(
        "course_site", sa.Column("term_id", sa.String(length=6), nullable=True)
    )
    op.create_foreign_key(
        "course_site_term_id_fkey",
        "course_site",
        "academics__term",
        ["term_id"],
        ["id"],
    )
    op.execute(
        "UPDATE course_site SET term_id = (SELECT id FROM academics__term ORDER BY start DESC LIMIT 1) WHERE term_id IS NULL"
    )
    op.alter_column("course_site", "term_id", nullable=False)


def upgrade_table_oh_event_to_office_hours():
    # 1. Drop FK relationships to Office Hours
    op.drop_constraint(
        "office_hours__event_office_hours_section_id_fkey",
        "office_hours__event",
        type_="foreignkey",
    )
    op.drop_constraint(
        "office_hours__ticket_oh_event_id_fkey",
        "office_hours__ticket",
        type_="foreignkey",
    )

    # 2. Rename Table
    op.rename_table("office_hours__event", "office_hours")

    # 3. Change FK column names to reflect `office_hours`
    op.alter_column(
        "office_hours", "office_hours_section_id", new_column_name="course_site_id"
    )
    op.alter_column(
        "office_hours__ticket", "oh_event_id", new_column_name="office_hours_id"
    )

    # 4. Reinstate foreign keys
    op.create_foreign_key(
        "office_hours_course_site_id_fkey",
        "office_hours",
        "course_site",
        ["course_site_id"],
        ["id"],
    )
    op.create_foreign_key(
        "office_hours__ticket_office_hours_id_fkey",
        "office_hours__ticket",
        "office_hours",
        ["office_hours_id"],
        ["id"],
    )


def downgrade_table_office_hours_to_oh_event():
    # 1. Drop FK relationships to office_hours
    op.drop_constraint(
        "office_hours_course_site_id_fkey",
        "office_hours",
        type_="foreignkey",
    )
    op.drop_constraint(
        "office_hours__ticket_office_hours_id_fkey",
        "office_hours__ticket",
        type_="foreignkey",
    )

    # 2. Rename Table back to office_hours__event
    op.rename_table("office_hours", "office_hours__event")

    # 3. Change FK column names to reflect `office_hours__event`
    op.alter_column(
        "office_hours__event",
        "course_site_id",
        new_column_name="office_hours_section_id",
    )
    op.alter_column(
        "office_hours__ticket", "office_hours_id", new_column_name="oh_event_id"
    )

    # 4. Reinstate foreign keys
    op.create_foreign_key(
        "office_hours__event_office_hours_section_id_fkey",
        "office_hours__event",
        "course_site",
        ["office_hours_section_id"],
        ["id"],
    )
    op.create_foreign_key(
        "office_hours__ticket_oh_event_id_fkey",
        "office_hours__ticket",
        "office_hours__event",
        ["oh_event_id"],
        ["id"],
    )


def downgrade_course_site_remove_term_columns():
    op.drop_constraint("course_site_term_id_fkey", "course_site")
    op.drop_column("course_site", "term_id")


def downgrade_course_site_to_office_hours_section():
    op.drop_constraint(
        "academics__section_course_site_id_fkey",
        "academics__section",
        type_="foreignkey",
    )
    op.alter_column(
        "academics__section", "course_site_id", new_column_name="office_hours_id"
    )
    op.rename_table("course_site", "office_hours__section")
    op.create_foreign_key(
        "academics_to_office_hours_fk",
        "academics__section",
        "office_hours__section",
        ["office_hours_id"],
        ["id"],
    )


def downgrade_table_academics_section_enrollments():
    op.drop_column("academics__section", "enrolled")
    op.drop_column("academics__section", "total_seats")


def constraint_exists(table_name: str, constraint_name: str) -> bool:
    insp = sa.engine.reflection.Inspector.from_engine(op.get_bind())
    constraints = insp.get_foreign_keys(table_name)
    for constraint in constraints:
        if constraint["name"] == constraint_name:
            return True
    return False


# def upgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#
#     # op.rename_table('office_hours__event', 'office_hours')
#     # op.alter_column('office_hours', 'office_hours_section_id', new_column_name='course_site_id')
#
#
#     # op.create_table('office_hours',
#     # sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
#     # sa.Column('type', sa.Enum('OFFICE_HOURS', 'TUTORING', 'REVIEW_SESSION', name='officehourseventtype'), nullable=False),
#     # sa.Column('mode', sa.Enum('IN_PERSON', 'VIRTUAL_STUDENT_LINK', 'VIRTUAL_OUR_LINK', name='officehourseventmodetype'), nullable=False),
#     # sa.Column('description', sa.String(), nullable=False),
#     # sa.Column('location_description', sa.String(), nullable=False),
#     # sa.Column('start_time', sa.DateTime(), nullable=False),
#     # sa.Column('end_time', sa.DateTime(), nullable=False),
#     # sa.Column('course_site_id', sa.Integer(), nullable=False),
#     # sa.Column('room_id', sa.String(), nullable=False),
#     # sa.ForeignKeyConstraint(['course_site_id'], ['course_site.id'], ),
#     # sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
#     # sa.PrimaryKeyConstraint('id')
#     # )
#     # op.drop_table('office_hours__section')
#     # op.drop_table('office_hours__event')

#     # op.add_column('office_hours__ticket', sa.Column('office_hours_id', sa.Integer(), nullable=False))
#     # op.drop_constraint('office_hours__ticket_oh_event_id_fkey', 'office_hours__ticket', type_='foreignkey')
#     # op.create_foreign_key(None, 'office_hours__ticket', 'office_hours', ['office_hours_id'], ['id'])
#     # op.drop_column('office_hours__ticket', 'oh_event_id')
#     # ### end Alembic commands ###
#
#
# def downgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     # op.add_column('office_hours__ticket', sa.Column('oh_event_id', sa.INTEGER(), autoincrement=False, nullable=False))
#     # op.drop_constraint(None, 'office_hours__ticket', type_='foreignkey')
#     # op.create_foreign_key('office_hours__ticket_oh_event_id_fkey', 'office_hours__ticket', 'office_hours__event', ['oh_event_id'], ['id'])
#     # op.drop_column('office_hours__ticket', 'office_hours_id')
#     # op.add_column('academics__section', sa.Column('office_hours_id', sa.INTEGER(), autoincrement=False, nullable=True))
#     # op.drop_constraint(None, 'academics__section', type_='foreignkey')
#     # op.create_foreign_key('academics__section_office_hours_id_fkey', 'academics__section', 'office_hours__section', ['office_hours_id'], ['id'])
#     # op.drop_column('academics__section', 'total_seats')
#     # op.drop_column('academics__section', 'enrolled')
#     # op.drop_column('academics__section', 'course_site_id')
#     # op.create_table('office_hours__event',
#     # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
#     # sa.Column('type', postgresql.ENUM('OFFICE_HOURS', 'TUTORING', 'REVIEW_SESSION', name='officehourseventtype'), autoincrement=False, nullable=False),
#     # sa.Column('mode', postgresql.ENUM('IN_PERSON', 'VIRTUAL_STUDENT_LINK', 'VIRTUAL_OUR_LINK', name='officehourseventmodetype'), autoincrement=False, nullable=False),
#     # sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
#     # sa.Column('location_description', sa.VARCHAR(), autoincrement=False, nullable=False),
#     # sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
#     # sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
#     # sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
#     # sa.Column('office_hours_section_id', sa.INTEGER(), autoincrement=False, nullable=False),
#     # sa.Column('room_id', sa.VARCHAR(), autoincrement=False, nullable=False),
#     # sa.ForeignKeyConstraint(['office_hours_section_id'], ['office_hours__section.id'], name='office_hours__event_office_hours_section_id_fkey'),
#     # sa.ForeignKeyConstraint(['room_id'], ['room.id'], name='office_hours__event_room_id_fkey'),
#     # sa.PrimaryKeyConstraint('id', name='office_hours__event_pkey')
#     # )
#     # op.create_table('office_hours__section',
#     # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
#     # sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
#     # sa.PrimaryKeyConstraint('id', name='office_hours__section_pkey')
#     # )
#     # op.drop_table('office_hours')
#     # op.drop_table('course_site')
#     # ### end Alembic commands ###
#
