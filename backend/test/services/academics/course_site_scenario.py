"""Explicit arrange helpers for course site service tests."""

from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ....entities.academics.section_entity import SectionEntity
from ....entities.office_hours.course_site_entity import CourseSiteEntity
from ....entities.office_hours.office_hours_entity import OfficeHoursEntity
from ....models.office_hours.course_site import (
    CourseSite,
    NewCourseSite,
    UpdatedCourseSite,
)
from ....models.office_hours.event_type import (
    OfficeHoursEventModeType,
    OfficeHoursEventType,
)
from ....models.office_hours.office_hours import OfficeHours
from ..reset_table_id_seq import reset_table_id_seq
from ..room_scenario import RoomScenario, arrange_room_scenario
from .scenario import AcademicsScenario, arrange_academics_scenario


@dataclass
class CourseSiteScenario:
    academics: AcademicsScenario
    rooms: RoomScenario
    comp_110_site: CourseSite
    comp_301_site: CourseSite
    comp_110_current_office_hours: OfficeHours
    comp_110_future_office_hours: OfficeHours
    comp_110_past_office_hours: OfficeHours
    new_course_site: NewCourseSite
    new_course_site_term_mismatch: NewCourseSite
    new_course_site_term_nonmember: NewCourseSite
    new_course_site_term_noninstructor: NewCourseSite
    new_course_site_term_already_in_site: NewCourseSite
    updated_comp_110_site: UpdatedCourseSite
    updated_comp_110_site_term_mismatch: UpdatedCourseSite
    updated_course_site_term_nonmember: UpdatedCourseSite
    updated_course_does_not_exist: UpdatedCourseSite
    updated_course_site_term_noninstructor: UpdatedCourseSite
    updated_course_site_term_already_in_site: UpdatedCourseSite
    new_site_other_user: NewCourseSite


def arrange_course_site_scenario(session: Session) -> CourseSiteScenario:
    academics = arrange_academics_scenario(session)
    rooms = arrange_room_scenario(session)
    now = datetime.now().replace(microsecond=0)

    comp_110_site = CourseSite(
        id=1, title="COMP 110", term_id=academics.current_term.id
    )
    comp_301_site = CourseSite(
        id=2, title="COMP 301", term_id=academics.current_term.id
    )
    session.add_all(
        [
            CourseSiteEntity.from_model(comp_110_site),
            CourseSiteEntity.from_model(comp_301_site),
        ]
    )
    session.flush()

    section_entities = {
        section.id: session.get(SectionEntity, section.id)
        for section in [
            academics.comp_110_001_current_term,
            academics.comp_110_002_current_term,
            academics.comp_301_001_current_term,
        ]
    }
    section_entities[academics.comp_110_001_current_term.id].course_site_id = (
        comp_110_site.id
    )
    section_entities[academics.comp_110_002_current_term.id].course_site_id = (
        comp_110_site.id
    )
    section_entities[academics.comp_301_001_current_term.id].course_site_id = (
        comp_301_site.id
    )

    office_hours = [
        OfficeHours(
            id=1,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Current COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(hours=2),
            end_time=now + timedelta(hours=1),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=2,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=3,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Past COMP 110 office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(days=1, hours=3),
            end_time=now - timedelta(days=1),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=4,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Current recurring office hours",
            location_description="Sitterson 135",
            start_time=now - timedelta(minutes=30),
            end_time=now + timedelta(hours=2),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=5,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 1",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=2),
            end_time=now + timedelta(days=2, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=6,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 2",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=3),
            end_time=now + timedelta(days=3, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=7,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 3",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=4),
            end_time=now + timedelta(days=4, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=8,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 4",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=5),
            end_time=now + timedelta(days=5, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=9,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 5",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=6),
            end_time=now + timedelta(days=6, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
        OfficeHours(
            id=10,
            type=OfficeHoursEventType.OFFICE_HOURS,
            mode=OfficeHoursEventModeType.IN_PERSON,
            description="Future recurring office hours 6",
            location_description="Sitterson 135",
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=3),
            course_site_id=comp_110_site.id,
            room_id=rooms.group_a.id,
            recurrence_pattern_id=None,
        ),
    ]
    session.add_all(OfficeHoursEntity.from_model(event) for event in office_hours)
    reset_table_id_seq(session, CourseSiteEntity, CourseSiteEntity.id, 3)
    reset_table_id_seq(session, OfficeHoursEntity, OfficeHoursEntity.id, 11)
    session.commit()

    return CourseSiteScenario(
        academics=academics,
        rooms=rooms,
        comp_110_site=comp_110_site,
        comp_301_site=comp_301_site,
        comp_110_current_office_hours=office_hours[0],
        comp_110_future_office_hours=office_hours[1],
        comp_110_past_office_hours=office_hours[2],
        new_course_site=NewCourseSite(
            title="Ina's COMP 301",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_301_002_current_term.id],
        ),
        new_course_site_term_mismatch=NewCourseSite(
            title="Ina's COMP 301",
            term_id=academics.previous_term.id,
            section_ids=[academics.comp_301_002_current_term.id],
        ),
        new_course_site_term_nonmember=NewCourseSite(
            title="Ina's COMP 3x1",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_311_001_current_term.id,
            ],
        ),
        new_course_site_term_noninstructor=NewCourseSite(
            title="Ina's COMP 3x1",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
        ),
        new_course_site_term_already_in_site=NewCourseSite(
            title="Ina's COMP courses",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_002_current_term.id,
                academics.comp_110_001_current_term.id,
            ],
        ),
        updated_comp_110_site=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_110_001_current_term.id],
            utas=[],
            gtas=[],
        ),
        updated_comp_110_site_term_mismatch=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_110_001_current_term.id, academics.comp_101_001.id],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_nonmember=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_110_001_current_term.id,
                academics.comp_311_001_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_does_not_exist=UpdatedCourseSite(
            id=404,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_110_001_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_noninstructor=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_311_001_current_term.id,
                academics.comp_311_002_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        updated_course_site_term_already_in_site=UpdatedCourseSite(
            id=1,
            title="New Course Site",
            term_id=academics.current_term.id,
            section_ids=[
                academics.comp_301_001_current_term.id,
                academics.comp_110_001_current_term.id,
            ],
            utas=[],
            gtas=[],
        ),
        new_site_other_user=NewCourseSite(
            title="Rhonda",
            term_id=academics.current_term.id,
            section_ids=[academics.comp_311_001_current_term.id],
        ),
    )