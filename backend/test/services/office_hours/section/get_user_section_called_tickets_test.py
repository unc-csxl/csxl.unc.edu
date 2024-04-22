"""Tests for `get_user_section_called_tickets()` Office Hours Section Service."""

import pytest

from backend.models.office_hours.ticket_details import OfficeHoursTicketDetails

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
    user__comp110_student_1,
    user__comp110_uta_0,
    user__comp301_instructor,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_get_user_section_called_ticket_by_uta(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test to get called tickets for a UTA in a section."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_oh_section.id
    )
    called_tickets = oh_section_svc.get_user_section_called_tickets(
        user__comp110_uta_0, oh_section
    )

    assert isinstance(called_tickets[0], OfficeHoursTicketDetails)
    assert len(called_tickets) == 2

    # Latest Ticket First
    assert called_tickets[0].created_at > called_tickets[1].created_at


def test_get_user_section_called_ticket_by_student(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test to get called tickets for a student in a section."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_student_1, office_hours_data.comp_110_oh_section.id
    )
    called_tickets = oh_section_svc.get_user_section_called_tickets(
        user__comp110_student_1, oh_section
    )

    assert len(called_tickets) == 0


def test_get_user_section_called_ticket_exception_if_non_member(
    oh_section_svc: OfficeHoursSectionService,
):
    """Test to check if getting called tickets by a non-member raises an exception."""
    oh_section = oh_section_svc.get_section_by_id(
        user__comp110_non_member, office_hours_data.comp_110_oh_section.id
    )

    with pytest.raises(PermissionError):
        oh_section_svc.get_user_section_called_tickets(
            user__comp110_non_member, oh_section
        )
