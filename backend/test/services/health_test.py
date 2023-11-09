"""Tests for the HealthService class."""

# Tested Dependencies
from ...services.health import HealthService

# Library Requirements
from datetime import datetime, timezone
from sqlalchemy.orm import Session

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_health_check(session: Session):
    health_service = HealthService(session)
    now = str(datetime.now(tz=timezone.utc))[:16]
    result = health_service.check()
    assert f"OK @ {now}" in health_service.check()
