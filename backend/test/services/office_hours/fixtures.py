"""Fixtures used for testing the Office Hours Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from ....services.office_hours.office_hours_recurrence import (
    OfficeHoursRecurrenceService,
)
from ....services import PermissionService
from ....services.office_hours import (
    OfficeHourTicketService,
    OfficeHoursService,
    OfficeHoursStatisticsService,
)

__authors__ = ["Meghan Sun", "Jade Keegan"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def oh_svc(session: Session):
    """OfficeHoursEventService fixture."""
    return OfficeHoursService(session)


@pytest.fixture()
def oh_svc_mock():
    """This mocks the OfficeHoursEventService class to avoid testing its implementation here."""
    return create_autospec(OfficeHoursService)


@pytest.fixture()
def oh_ticket_svc(session: Session):
    """OfficeHoursEventService fixture."""
    return OfficeHourTicketService(session)


@pytest.fixture()
def oh_recurrence_svc(session: Session):
    """OfficeHoursRecurrenceService fixture."""
    return OfficeHoursRecurrenceService(session, OfficeHoursService(session))


@pytest.fixture()
def oh_statistics_svc(session: Session):
    """OfficeHoursStatisticsService fixture."""
    return OfficeHoursStatisticsService(session, OfficeHoursService(session))
