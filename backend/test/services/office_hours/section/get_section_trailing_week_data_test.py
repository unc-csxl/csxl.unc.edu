"""Tests for `get_section_trailing_week_data()` in Office Hours Section Service."""

import pytest

from backend.models.office_hours.section_data import OfficeHoursSectionTrailingWeekData

from .....models.academics.section_member import SectionMember
from .....models.office_hours.section import OfficeHoursSectionPartial

from .....services.exceptions import ResourceNotFoundException
from .....services.office_hours.section import OfficeHoursSectionService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_section_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ...core_data import setup_insert_data_fixture as insert_order_0
from ...room_data import fake_data_fixture as insert_order_1
from ...academics.term_data import fake_data_fixture as insert_order_2
from ...academics.course_data import fake_data_fixture as insert_order_3
from ...academics.section_data import fake_data_fixture as insert_order_4
from ..office_hours_data import fake_data_fixture as insert_order_5

# Import the fake model data in a namespace for test assertions
from .. import office_hours_data
from ...academics.section_data import (
    user__comp110_instructor,
    user__comp110_student_0,
    user__comp110_uta_0,
    user__comp110_non_member,
    comp110_members,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_section_trailing_week_data(oh_section_svc: OfficeHoursSectionService):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_instructor, office_hours_data.comp_110_oh_section.id
    )

    data = oh_section_svc.get_section_trailing_week_data(
        user__comp110_instructor, oh_section
    )

    # Future TODO: Calcalute Actual Stats From Demo Data
    assert isinstance(data, OfficeHoursSectionTrailingWeekData)
    assert data.number_of_students == 1
    assert data.number_of_tickets == len(office_hours_data.comp110_tickets)


def test_get_section_trailing_week_data_exception_by_student(
    oh_section_svc: OfficeHoursSectionService,
):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_section.id
    )

    with pytest.raises(PermissionError):
        oh_section_svc.get_section_trailing_week_data(
            user__comp110_student_0, oh_section
        )


def test_get_section_trailing_week_data_exception_by_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )

    with pytest.raises(PermissionError):
        oh_section_svc.get_section_trailing_week_data(user__comp110_uta_0, oh_section)


def test_get_section_trailing_week_data_exception_by_non_member(
    oh_section_svc: OfficeHoursSectionService,
):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_non_member, office_hours_data.comp_110_oh_section.id
    )

    with pytest.raises(PermissionError):
        oh_section_svc.get_section_trailing_week_data(
            user__comp110_non_member, oh_section
        )
