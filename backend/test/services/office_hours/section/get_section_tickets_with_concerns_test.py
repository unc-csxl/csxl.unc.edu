"""Tests for `get_sections_tickets_with_concerns()` in Office Hours Section Service."""

import pytest

from .....models.office_hours.ticket_details import OfficeHoursTicketDetails

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
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_sections_tickets_with_concerns_by_instructor(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test case for retrieving sections by term and validating section details and count."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_instructor, office_hours_data.comp_110_oh_section.id
    )
    tickets = oh_section_svc.get_section_tickets_with_concerns(
        user__comp110_instructor, oh_section
    )

    assert len(tickets) > 0
    assert isinstance(tickets[0], OfficeHoursTicketDetails)
    assert tickets[0].have_concerns is True


def test_get_sections_tickets_with_concerns_no_ticket_concerns(
    oh_section_svc: OfficeHoursSectionService,
):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_instructor, office_hours_data.comp_523_oh_section.id
    )
    tickets = oh_section_svc.get_section_tickets_with_concerns(
        user__comp110_instructor, oh_section
    )

    assert len(tickets) == 0


def test_get_sections_tickets_with_concerns_exception_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    with pytest.raises(PermissionError):
        oh_section_svc.get_section_tickets_with_concerns(
            user__comp110_uta_0, oh_section
        )


def test_get_sections_tickets_with_concerns_exception_student(
    oh_section_svc: OfficeHoursSectionService,
):

    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_student_0, office_hours_data.comp_110_oh_section.id
    )
    with pytest.raises(PermissionError):
        oh_section_svc.get_section_tickets_with_concerns(
            user__comp110_student_0, oh_section
        )


def test_get_sections_tickets_with_concerns_exception_non_member(
    oh_section_svc: OfficeHoursSectionService,
):

    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_non_member, office_hours_data.comp_110_oh_section.id
    )
    with pytest.raises(PermissionError):
        oh_section_svc.get_section_tickets_with_concerns(
            user__comp110_non_member, oh_section
        )
