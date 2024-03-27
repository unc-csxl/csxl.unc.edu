"""Fixtures used for testing the Courses Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from backend.services.office_hours.event import OfficeHoursEventService
from backend.services.office_hours.ticket import OfficeHoursTicketService
from ....services import PermissionService
from ....services.academics import TermService, CourseService, SectionService

__authors__ = ["Meghan Sun"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def oh_ticket_svc(session: Session, permission_svc: PermissionService):
    """OfficeHoursEventService fixture."""
    return OfficeHoursTicketService(session, permission_svc)
