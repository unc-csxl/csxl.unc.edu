"""Operating-hours editing, API, and persistence regressions."""

from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, tzinfo
from threading import Barrier
from unittest.mock import create_autospec
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from ....api.authentication import registered_user
from ....entities.coworking import OperatingHoursEntity
from ....main import app
from ....models.coworking import OperatingHours, TimeRange
from ....script.deployments.operating_hours_permissions import grant_permissions
from ....services import PermissionService
from ....services.coworking import OperatingHoursService
from ....services.coworking.exceptions import (
    OperatingHoursCannotDeleteException,
    OperatingHoursCannotOverlapException,
)
from ....services.exceptions import ResourceNotFoundException, UserPermissionException
from .. import user_data
from ..core_data import setup_insert_data_fixture as insert_order_0
from . import operating_hours_data
from .fixtures import operating_hours_svc, permission_svc
from .operating_hours_data import fake_data_fixture as insert_order_1
from .time import time


@pytest.mark.parametrize("record", ["today", "tomorrow"])
def test_update_retains_id_and_excludes_self(
    operating_hours_svc: OperatingHoursService, record: str
):
    original: OperatingHours = getattr(operating_hours_data, record)
    assert original.id is not None
    unchanged = operating_hours_svc.update(user_data.ambassador, original.id, original)
    assert unchanged == original
    proposed = TimeRange(start=original.start, end=original.end + timedelta(minutes=30))
    result = operating_hours_svc.update(user_data.ambassador, original.id, proposed)
    assert result.id == original.id
    assert result.start == proposed.start
    assert result.end == proposed.end


@pytest.mark.parametrize(
    "offsets",
    [(-30, 30), (30, 240), (-30, 240), (30, 60), (0, 180), (-30, 0), (180, 240)],
)
def test_update_rejects_other_hours_and_preserves_record(
    operating_hours_svc: OperatingHoursService, offsets: tuple[int, int]
):
    original = operating_hours_data.tomorrow
    assert original.id is not None
    other = operating_hours_data.future
    proposed = TimeRange(
        start=other.start + timedelta(minutes=offsets[0]),
        end=other.start + timedelta(minutes=offsets[1]),
    )
    with pytest.raises(OperatingHoursCannotOverlapException):
        operating_hours_svc.update(user_data.ambassador, original.id, proposed)
    assert operating_hours_svc.get_by_id(original.id) == original


def test_update_permissions_and_missing_record(
    operating_hours_svc: OperatingHoursService,
):
    original = operating_hours_data.tomorrow
    assert original.id is not None
    with pytest.raises(UserPermissionException):
        operating_hours_svc.update(user_data.user, original.id, original)
    with pytest.raises(ResourceNotFoundException):
        operating_hours_svc.update(user_data.ambassador, 999999, original)
    permission = create_autospec(PermissionService)
    operating_hours_svc._permission_svc = permission
    operating_hours_svc.update(user_data.ambassador, original.id, original)
    permission.enforce.assert_called_once_with(
        user_data.ambassador,
        "coworking.operating_hours.update",
        f"coworking/operating_hours/{original.id}",
    )


@pytest.mark.parametrize("start_delta", [-120, -30, 0])
def test_delete_rejects_past_active_and_exact_start(
    operating_hours_svc: OperatingHoursService,
    session: Session,
    monkeypatch: pytest.MonkeyPatch,
    start_delta: int,
):
    now = datetime(2030, 6, 1, 12)

    class Clock:
        @staticmethod
        def now(tz: tzinfo):
            return now.replace(tzinfo=tz)

    monkeypatch.setattr("backend.services.coworking.operating_hours.datetime", Clock)
    entity = OperatingHoursEntity(
        start=now + timedelta(minutes=start_delta),
        end=now + timedelta(minutes=start_delta + 60),
    )
    session.add(entity)
    session.commit()
    with pytest.raises(OperatingHoursCannotDeleteException):
        operating_hours_svc.delete(user_data.ambassador, entity.to_model())
    assert operating_hours_svc.get_by_id(entity.id)


def test_delete_uses_stored_times(operating_hours_svc: OperatingHoursService):
    original = operating_hours_data.tomorrow
    assert original.id is not None
    past = TimeRange(start=datetime(2000, 1, 1), end=datetime(2000, 1, 1, 1))
    operating_hours_svc.update(user_data.ambassador, original.id, past)
    with pytest.raises(OperatingHoursCannotDeleteException):
        operating_hours_svc.delete(user_data.ambassador, original)


@pytest.fixture
def client(operating_hours_svc: OperatingHoursService) -> Iterator[TestClient]:
    overrides = app.dependency_overrides.copy()
    app.dependency_overrides[registered_user] = lambda: user_data.ambassador
    app.dependency_overrides[OperatingHoursService] = lambda: operating_hours_svc
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    app.dependency_overrides.update(overrides)


def test_put_api_returns_same_id_and_offset(client: TestClient):
    original = operating_hours_data.tomorrow
    response = client.put(
        f"/api/coworking/operating_hours/{original.id}",
        json={
            "start": original.start.isoformat(),
            "end": original.end.isoformat(),
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == original.id
    assert datetime.fromisoformat(response.json()["start"]).tzinfo is not None


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"start": "invalid", "end": "2030-01-01T12:00"},
        {"start": "2030-01-01T12:00", "end": "2030-01-01T12:00"},
        {"start": "2030-01-01T12:00", "end": "2030-01-01T11:00"},
    ],
)
def test_put_invalid_times(client: TestClient, payload: dict[str, str]):
    response = client.put(
        f"/api/coworking/operating_hours/{operating_hours_data.tomorrow.id}",
        json=payload,
    )
    assert response.status_code == 422


def test_api_conflicts_missing_and_permissions(client: TestClient):
    original = operating_hours_data.tomorrow
    other = operating_hours_data.future
    payload = {"start": other.start.isoformat(), "end": other.end.isoformat()}
    for method, path in [("put", f"/{original.id}"), ("post", "")]:
        response = getattr(client, method)(
            f"/api/coworking/operating_hours{path}", json=payload
        )
        assert response.status_code == 409
        assert "conflict" in response.json()["message"]
    assert (
        client.put("/api/coworking/operating_hours/999999", json=payload).status_code
        == 404
    )
    app.dependency_overrides[registered_user] = lambda: user_data.user
    assert (
        client.put(
            f"/api/coworking/operating_hours/{original.id}", json=payload
        ).status_code
        == 403
    )


def test_delete_api_rejects_past(
    client: TestClient, operating_hours_svc: OperatingHoursService
):
    original = operating_hours_data.tomorrow
    assert original.id is not None
    operating_hours_svc.update(
        user_data.ambassador,
        original.id,
        TimeRange(start=datetime(2000, 1, 1), end=datetime(2000, 1, 1, 1)),
    )
    assert (
        client.delete(f"/api/coworking/operating_hours/{original.id}").status_code
        == 409
    )


def test_get_validates_query_and_normalizes_offsets(client: TestClient):
    assert (
        client.get(
            "/api/coworking/operating_hours",
            params={"start": "2030-01-01T12:00Z", "end": "2030-01-01T11:00Z"},
        ).status_code
        == 422
    )
    original = operating_hours_data.tomorrow
    response = client.get(
        "/api/coworking/operating_hours",
        params={
            "start": original.start.replace(
                tzinfo=ZoneInfo("America/New_York")
            ).isoformat(),
            "end": original.end.replace(
                tzinfo=ZoneInfo("America/New_York")
            ).isoformat(),
        },
    )
    assert response.status_code == 200
    assert [row["id"] for row in response.json()] == [original.id]


@pytest.mark.parametrize(
    "operations", [("create", "create"), ("create", "update"), ("update", "update")]
)
def test_concurrent_writes_cannot_overlap(
    test_engine: Engine, operations: tuple[str, str]
):
    """Competing writers recheck conflicts after acquiring the schedule lock."""
    proposed = TimeRange(start=datetime(2050, 1, 1, 10), end=datetime(2050, 1, 1, 12))
    barrier = Barrier(2, timeout=10)
    ids = [operating_hours_data.tomorrow.id, operating_hours_data.future.id]

    def write(index: int):
        with Session(test_engine) as session:
            service = OperatingHoursService(session, PermissionService(session))
            lock = service._lock_schedule

            def synchronized_lock():
                barrier.wait()
                lock()

            service._lock_schedule = synchronized_lock
            try:
                if operations[index] == "create":
                    service.create(user_data.ambassador, proposed)
                else:
                    id = ids[index]
                    assert id is not None
                    service.update(user_data.ambassador, id, proposed)
                return "saved"
            except OperatingHoursCannotOverlapException:
                # A rolled-back session can still read the winning interval.
                assert len(service.schedule(proposed)) == 1
                return "conflict"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(write, range(2)))
    assert sorted(results) == ["conflict", "saved"]


@pytest.mark.parametrize("method", ["create", "update"])
def test_service_revalidates_times(
    operating_hours_svc: OperatingHoursService, method: str
):
    from pydantic import ValidationError

    original = operating_hours_data.tomorrow
    assert original.id is not None
    invalid = TimeRange(start=original.start, end=original.end)
    invalid.end = invalid.start
    with pytest.raises(ValidationError):
        if method == "create":
            operating_hours_svc.create(user_data.ambassador, invalid)
        else:
            operating_hours_svc.update(user_data.ambassador, original.id, invalid)
    assert operating_hours_svc.get_by_id(original.id) == original


def test_permission_provisioning_is_idempotent(session: Session):
    from ....entities.permission_entity import PermissionEntity

    session.query(PermissionEntity).filter(
        PermissionEntity.action.like("coworking.operating_hours.%")
    ).delete()
    session.commit()
    assert grant_permissions(session) == 3
    assert grant_permissions(session) == 0
