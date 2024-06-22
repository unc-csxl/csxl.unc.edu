"""Fixtures used for testing the Office Hours Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ....services import PermissionService
from ....services.office_hours import OfficeHourTicketService, OfficeHoursService

__authors__ = ["Meghan Sun"]
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
def oh_ticket_svc(
    session: Session,
    permission_svc: PermissionService,
    oh_event_svc: OfficeHoursService,
):
    """OfficeHoursEventService fixture."""
    return OfficeHourTicketService(session, permission_svc, oh_event_svc)
