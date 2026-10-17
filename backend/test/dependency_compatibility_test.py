"""Exercise integrations that combine the upgraded security libraries."""

import json
from unittest.mock import Mock

import jwt
import pytest
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from github import Auth

from ..models import User
from ..services.github import GitHubService


def test_pygithub_can_sign_with_updated_pyjwt_and_cryptography():
    """Check PyGithub's existing RSA integration without making network calls."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    token = Auth.AppAuth(app_id=123, private_key=pem).token
    claims = jwt.decode(token, key.public_key(), algorithms=["RS256"])
    assert claims["iss"] == "123"
    assert claims["exp"] > claims["iat"]


@pytest.mark.parametrize("github_status", [200, 401])
def test_github_oauth_linking_with_updated_client(monkeypatch, github_status):
    """Exercise the real requests/PyGithub clients against a fake HTTP transport."""
    urls = []

    def send(session, request, **kwargs):
        urls.append(request.url)
        response = requests.Response()
        response.request = request
        response.headers["Content-Type"] = "application/json"
        if request.url == "https://github.com/login/oauth/access_token":
            assert request.method == "POST"
            response.status_code = 200
            payload = {"access_token": "synthetic-github-token"}
        elif request.url == "https://api.github.com:443/user":
            assert request.headers["Authorization"] == "token synthetic-github-token"
            response.status_code = github_status
            payload = {
                "login": "synthetic-user",
                "id": 123,
                "avatar_url": "https://example.com/avatar.png",
            }
        else:
            raise AssertionError(f"Unexpected outbound request: {request.url}")
        response._content = json.dumps(payload).encode()
        return response

    monkeypatch.setattr(requests.Session, "send", send)
    user_service = Mock()
    subject = User(id=1, onyen="synthetic-user")
    linked = GitHubService(user_service).link_with_user(
        subject, "synthetic-code", "http://localhost:1560/oauth/github"
    )
    assert len(urls) == 2
    assert linked is (github_status == 200)
    if linked:
        assert subject.github == "synthetic-user"
        assert subject.github_id == 123
        assert subject.github_avatar == "https://example.com/avatar.png"
        user_service.update.assert_called_once_with(subject, subject)
    else:
        user_service.update.assert_not_called()
