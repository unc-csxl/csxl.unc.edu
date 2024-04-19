"""Tests for `check_staff_helping_status()` in Office Hours Event Service."""

import pytest

from .....models.office_hours.event_status import StaffHelpingStatus

from .....services.office_hours.event import OfficeHoursEventService

# Imported fixtures provide dependencies injected for the tests as parameters.
from ..fixtures import permission_svc, oh_event_svc

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
    user__comp110_uta_0,
    user__comp110_gta,
    user__comp110_non_member,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_check_staff_helping_status(oh_event_svc: OfficeHoursEventService):
    """Test case to check the staff helping status for an ongoing event."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_uta_0, office_hours_data.comp_110_current_oh_event.id
    )
    status = oh_event_svc.check_staff_helping_status(user__comp110_uta_0, oh_event)

    assert isinstance(status, StaffHelpingStatus)
    assert status.ticket_id == office_hours_data.comp110_called_ticket.id


def test_check_staff_helping_status_not_currently_helping(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to check the staff helping status when not currently helping."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_gta, office_hours_data.comp_110_current_oh_event.id
    )
    status = oh_event_svc.check_staff_helping_status(user__comp110_gta, oh_event)

    assert isinstance(status, StaffHelpingStatus)
    assert status.ticket_id is None


def test_check_staff_helping_status_exception_if_non_member(
    oh_event_svc: OfficeHoursEventService,
):
    """Test case to check an expection is raised if a non member."""
    oh_event = oh_event_svc.get_event_by_id(
        user__comp110_gta, office_hours_data.comp_110_current_oh_event.id
    )

    with pytest.raises(PermissionError):
        oh_event_svc.check_staff_helping_status(user__comp110_non_member, oh_event)
