"""Verify login reconciliation against the isolated test database."""

from unittest.mock import Mock

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api import authentication as auth
from backend.api import profile
from backend.entities import UserEntity
from backend.models import User
from backend.services import UserService
from backend.services.exceptions import UserIdentityConflictException


@pytest.fixture
def local_users(session: Session):
    first = UserEntity.from_model(
        User(
            id=900000301,
            pid=900000301,
            onyen="login-provisional",
            email="login-first@example.invalid",
            first_name="Synthetic",
            last_name="Faculty",
            accepted_community_agreement=False,
        )
    )
    second = UserEntity.from_model(
        User(
            id=900000302,
            pid=900000302,
            onyen="login-other",
            email="login-other@example.invalid",
        )
    )
    session.add_all([first, second])
    session.commit()
    permission = Mock()
    permission.get_permissions.return_value = []
    return session, UserService(session, permission), first, second


def test_fresh_login_reconciles_pid_and_old_tokens_cannot_revert(
    local_users, monkeypatch
):
    session, service, first, _ = local_users
    before = service.get(first.pid).model_dump()
    app = FastAPI()
    app.include_router(auth.api)
    app.include_router(profile.api)
    app.dependency_overrides[UserService] = lambda: service
    monkeypatch.setattr(auth, "HOST", auth.AUTH_SERVER_HOST)
    old_token = auth._generate_token(first.onyen, first.pid)
    with TestClient(app) as client:
        response = client.get(
            "/auth", headers={"uid": "verified-sso", "pid": str(first.pid)}
        )
        assert response.status_code == 200
        session.expire_all()
        after = service.get(first.pid).model_dump()
        assert after == {**before, "onyen": "verified-sso"}
        # Ordinary reads/profile edits with an older valid token must not undo login.
        headers = {"Authorization": f"Bearer {old_token}"}
        assert (
            client.get("/api/profile", headers=headers).json()["onyen"]
            == "verified-sso"
        )
        response = client.put(
            "/api/profile",
            headers=headers,
            json={
                "first_name": before["first_name"],
                "last_name": before["last_name"],
                "email": before["email"],
                "pronouns": "",
                "accepted_community_agreement": False,
            },
        )
        assert response.status_code == 200
        assert response.json()["onyen"] == "verified-sso"
        # Failed authentication cannot mutate the account.
        invalid = jwt.encode(
            {"pid": first.pid, "uid": "attacker"},
            "untrusted-secret-for-test-only-123",
            algorithm="HS256",
        )
        assert (
            client.get(
                "/api/profile", headers={"Authorization": f"Bearer {invalid}"}
            ).status_code
            == 401
        )
        assert service.get(first.pid).onyen == "verified-sso"


def test_repeat_unknown_pid_and_collision(local_users, monkeypatch):
    session, service, first, second = local_users
    commit = Mock(wraps=session.commit)
    monkeypatch.setattr(session, "commit", commit)
    service.sync_login_onyen(first.pid, first.onyen)
    service.sync_login_onyen(900000303, "unregistered")
    commit.assert_not_called()
    assert session.scalar(select(UserEntity).where(UserEntity.pid == 900000303)) is None
    with pytest.raises(UserIdentityConflictException):
        service.sync_login_onyen(first.pid, second.onyen)
    assert service.get(first.pid).onyen == "login-provisional"
    assert service.get(second.pid).onyen == "login-other"
    service.sync_login_onyen(first.pid, "verified-sso")
    assert service.get(first.pid).onyen == "verified-sso"


@pytest.mark.parametrize("onyen", ["", " ", " leading-space", "x" * 33])
def test_invalid_onyen_is_rejected(local_users, onyen):
    _, service, first, _ = local_users
    with pytest.raises(ValueError, match="Invalid authenticated onyen"):
        service.sync_login_onyen(first.pid, onyen)
    assert service.get(first.pid).onyen == "login-provisional"
