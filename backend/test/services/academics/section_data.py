"""Section data for tests."""

import pytest
from sqlalchemy.orm import Session
from backend.entities.academics.section_room_entity import SectionRoomEntity
from backend.entities.academics.course_entity import CourseEntity
from backend.entities.room_entity import RoomEntity
from backend.models.room_assignment_type import RoomAssignmentType

from ....models.room import Room
from ....models.room_details import RoomDetails
from ....entities.academics import SectionEntity
from ....entities.academics import SectionMemberEntity
from ....models.academics import Section
from ....models.roster_role import RosterRole

from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime

# Import the setup_teardown fixture explicitly to load entities in database
from .term_data import fake_data_fixture as insert_term_fake_data
from .course_data import fake_data_fixture as insert_course_fake_data
from ..role_data import fake_data_fixture as insert_role_fake_data
from ..user_data import fake_data_fixture as insert_user_fake_data

from . import course_data, term_data
from .. import user_data, role_data, permission_data

__authors__ = [
    "Ajay Gandecha, Madelyn Andrews, Sadie Amato, Bailey DeSouza, Meghan Sun"
]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

virtual_room = RoomDetails(
    id="404",
    nickname="Virtual",
    building="Virtual",
    room="Virtual",
    capacity=999,
    reservable=False,
    seats=[],
)

comp_101_001 = Section(
    id=1,
    course_id=course_data.comp_110.id,
    number="001",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 12:00PM - 1:15PM",
    override_title="",
    override_description="",
)

comp_101_002 = Section(
    id=2,
    course_id=course_data.comp_110.id,
    number="002",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 1:30PM - 2:45PM",
    override_title="",
    override_description="",
)

comp_301_001 = Section(
    id=3,
    course_id=course_data.comp_301.id,
    number="001",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 8:00AM - 9:15AM",
    override_title="",
    override_description="",
)

edited_comp_110 = Section(
    id=2,
    course_id=course_data.comp_110.id,
    number="002",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
    override_title="",
    override_description="",
)

edited_comp_110_with_room = Section(
    id=2,
    course_id=course_data.comp_110.id,
    number="002",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
    override_title="",
    override_description="",
    lecture_room=virtual_room,
)

edited_comp_301_with_room = Section(
    id=3,
    course_id=course_data.comp_301.id,
    number="001",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 8:00AM - 9:15AM",
    override_title="",
    override_description="",
    lecture_room=virtual_room,
)

new_section = Section(
    id=4,
    course_id=course_data.comp_110.id,
    number="003",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
    override_title="",
    override_description="",
)

new_section_with_lecture_room = Section(
    id=4,
    course_id=course_data.comp_110.id,
    number="003",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
    override_title="",
    override_description="",
    lecture_room=virtual_room,
)

ta = SectionMemberEntity.from_draft_model(
    user_id=user_data.ambassador.id,
    section_id=comp_101_001.id,
    member_role=RosterRole.UTA,
)

room_assignment_110_001 = (
    comp_101_001.id,
    virtual_room.id,
    RoomAssignmentType.LECTURE_ROOM,
)

room_assignment_110_002 = (
    comp_101_002.id,
    virtual_room.id,
    RoomAssignmentType.LECTURE_ROOM,
)

sections = [comp_101_001, comp_101_002, comp_301_001]
assignments = [room_assignment_110_001, room_assignment_110_002]
comp_110_sections = [comp_101_001, comp_101_002]


def insert_fake_data(session: Session):
    room_entity = RoomEntity.from_model(virtual_room)
    session.add(room_entity)

    for section in sections:
        entity = SectionEntity.from_model(section)
        session.add(entity)

    session.add(ta)

    for assignment in assignments:
        section_id, room_id, assignment_type = assignment
        entity = SectionRoomEntity(
            section=session.get(SectionEntity, section_id),
            room=session.get(RoomEntity, room_id),
            assignment_type=assignment_type,
        )
        session.add(entity)

    reset_table_id_seq(session, SectionEntity, SectionEntity.id, len(sections) + 1)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
