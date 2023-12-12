"""Section data for tests."""

import pytest
from sqlalchemy.orm import Session
from ....entities.courses import SectionEntity
from ....models.courses import Section
from ..reset_table_id_seq import reset_table_id_seq
from datetime import datetime

# Import the setup_teardown fixture explicitly to load entities in database
from .term_data import fake_data_fixture as insert_term_fake_data
from .course_data import fake_data_fixture as insert_course_fake_data

from . import course_data, term_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

comp_101_001 = Section(
    id=1,
    course_id=course_data.comp_110.id,
    number="001",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 12:00PM - 1:15PM",
)

comp_101_002 = Section(
    id=2,
    course_id=course_data.comp_110.id,
    number="002",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 1:30PM - 2:45PM",
)

comp_301_001 = Section(
    id=3,
    course_id=course_data.comp_301.id,
    number="001",
    term_id=term_data.f_23.id,
    meeting_pattern="TTh 8:00AM - 9:15AM",
)

edited_comp_110 = Section(
    id=2,
    course_id=course_data.comp_110.id,
    number="002",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
)

new_section = Section(
    id=4,
    course_id=course_data.comp_110.id,
    number="003",
    term_id=term_data.f_23.id,
    meeting_pattern="MW 1:30PM - 2:45PM",
)

sections = [comp_101_001, comp_101_002, comp_301_001]
comp_110_sections = [comp_101_001, comp_101_002]


def insert_fake_data(session: Session):
    for section in sections:
        entity = SectionEntity.from_model(section)
        session.add(entity)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    term_data.insert_fake_data(session)
    course_data.insert_fake_data(session)
    insert_fake_data(session)
    session.commit()
