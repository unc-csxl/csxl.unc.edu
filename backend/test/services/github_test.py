"""Tests for the GitHubService class."""

from types import SimpleNamespace
from unittest.mock import create_autospec

import backend.services.github as github_module

from ...models.user import User
from ...services.github import GitHubService
from ...services.user import UserService


def test_link_with_user_updates_github_fields(monkeypatch):
    user_svc = create_autospec(UserService)
    subject = User(
        id=1,
        pid=1,
        onyen="user",
        email="user@unc.edu",
        first_name="Test",
        last_name="User",
    )
    service = GitHubService(user_svc)

    monkeypatch.setattr(
        service, "_get_github_oauth_token", lambda code, redirect: "token"
    )

    class FakeGithub:
        def __init__(self, token: str):
            assert token == "token"

        def get_user(self):
            return SimpleNamespace(
                login="octocat", id=123, avatar_url="https://avatar"
            )

    monkeypatch.setattr(github_module, "Github", FakeGithub)

    assert service.link_with_user(subject, "oauth-code", "https://redirect") is True
    assert subject.github == "octocat"
    assert subject.github_id == 123
    assert subject.github_avatar == "https://avatar"
    user_svc.update.assert_called_once_with(subject, subject)


def test_link_with_user_returns_false_on_failure(monkeypatch):
    service = GitHubService(create_autospec(UserService))
    subject = User(
        id=1,
        pid=1,
        onyen="user",
        email="user@unc.edu",
        first_name="Test",
        last_name="User",
    )

    def explode(_code: str, _redirect: str):
        raise RuntimeError("boom")

    monkeypatch.setattr(service, "_get_github_oauth_token", explode)

    assert service.link_with_user(subject, "oauth-code", "https://redirect") is False


def test_remove_association_clears_github_username():
    user_svc = create_autospec(UserService)
    subject = User(
        id=1,
        pid=1,
        onyen="user",
        email="user@unc.edu",
        first_name="Test",
        last_name="User",
        github="octocat",
    )
    service = GitHubService(user_svc)

    service.remove_association(subject)

    assert subject.github == ""
    user_svc.update.assert_called_once_with(subject, subject)


def test_get_oauth_login_url_uses_env_and_state(monkeypatch):
    monkeypatch.setattr(
        github_module, "getenv", lambda key: {"GITHUB_CLIENT_ID": "client-id"}[key]
    )
    monkeypatch.setattr(
        github_module.uuid, "uuid4", lambda: SimpleNamespace(hex="csrf-state")
    )

    url = GitHubService(create_autospec(UserService)).get_oauth_login_url(
        "https://redirect"
    )

    assert "client_id=client-id" in url
    assert "redirect_uri=https://redirect" in url
    assert "state=csrf-state" in url


def test_get_github_oauth_token_uses_access_token(monkeypatch):
    calls: dict[str, object] = {}

    class FakeResponse:
        def json(self):
            return {"access_token": "secret-token"}

    def fake_post(url: str, data: dict[str, str], headers: dict[str, str]):
        calls["url"] = url
        calls["data"] = data
        calls["headers"] = headers
        return FakeResponse()

    monkeypatch.setattr(
        github_module,
        "getenv",
        lambda key: {
            "GITHUB_CLIENT_ID": "client-id",
            "GITHUB_CLIENT_SECRET": "client-secret",
        }[key],
    )
    monkeypatch.setattr(github_module.requests, "post", fake_post)

    token = GitHubService(create_autospec(UserService))._get_github_oauth_token(
        "oauth-code", "https://redirect"
    )

    assert token == "secret-token"
    assert calls["url"] == "https://github.com/login/oauth/access_token"
    assert calls["headers"] == {"Accept": "application/json"}