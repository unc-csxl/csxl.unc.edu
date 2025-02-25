"""Tests for the OfficeHoursStatisticsService."""

import pytest

from ....services.exceptions import (
    CoursePermissionException,
    RecurringOfficeHourEventException,
    ResourceNotFoundException,
)

from ....services.office_hours import OfficeHoursStatisticsService
from ....models.pagination import TicketPaginationParams

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import oh_statistics_svc

# Import the setup_teardown fixture explicitly to load entities in database
from ..core_data import setup_insert_data_fixture as insert_order_0
from ..academics.term_data import fake_data_fixture as insert_order_1
from ..academics.course_data import fake_data_fixture as insert_order_2
from ..academics.section_data import fake_data_fixture as insert_order_3
from ..room_data import fake_data_fixture as insert_order_4
from ..office_hours.office_hours_data import fake_data_fixture as insert_order_5
from ..event.event_demo_data import date_maker

# Important fake model data in namespace for test assertions
from .. import user_data
from ..office_hours import office_hours_data

__authors__ = ["Jade Keegan", "Ajay Gandecha"]
__copyright__ = "Copyright 2025"
__license__ = "MIT"


def test_get_paginated_tickets(oh_statistics_svc: OfficeHoursStatisticsService):
    """Ensures that users with the appropriate site permissions can get paginated tickets."""
    ticket_params = TicketPaginationParams(
        range_start="",
        range_end="",
        student_ids=[],
        staff_ids=[],
    )

    ticket_history = oh_statistics_svc.get_paginated_tickets(
        user_data.instructor,
        office_hours_data.comp_110_site.id,
        ticket_params,
    )

    assert len(ticket_history.items) == 1
