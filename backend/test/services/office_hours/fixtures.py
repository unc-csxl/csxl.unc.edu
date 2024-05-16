"""Fixtures used for testing the Office Hours Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ....services import PermissionService
from ....services.office_hours import (
    OfficeHoursTicketService,
    OfficeHoursEventService,
    OfficeHoursSectionService,
)

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def oh_event_svc(session: Session, permission_svc: PermissionService):
    """OfficeHoursEventService fixture."""
    return OfficeHoursEventService(session, permission_svc)


@pytest.fixture()
def oh_ticket_svc(
    session: Session,
    permission_svc: PermissionService,
    oh_event_svc: OfficeHoursEventService,
):
    """OfficeHoursEventService fixture."""
    return OfficeHoursTicketService(session, permission_svc, oh_event_svc)


@pytest.fixture()
def oh_section_svc(session: Session, permission_svc: PermissionService):
    """OfficeHoursSectionService fixture."""
    return OfficeHoursSectionService(session, permission_svc)
