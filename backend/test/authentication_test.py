"""Authentication regressions for Santosh Kumar Puppala's security report.

Exercise the real router with synthetic identities and no external services.
"""

import json
import re
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit

import jwt
import pytest
from bs4 import BeautifulSoup
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from ..api import authentication as auth


IDENTITY = {"uid": "synthetic_user", "pid": "999999999"}
PAYLOADS = [
    "</script><img src=x onerror=alert(document.domain)>",
    "'+alert(document.domain)+'",
    "');alert(document.domain);//",
    "</ScRiPt><script>alert(document.domain)</script>",
    'a&origin=evil.example/auth#fragment"\\\n\u2028\u2029',
]


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(auth, "HOST", auth.AUTH_SERVER_HOST)
    monkeypatch.setattr(auth, "_JWT_SECRET", "synthetic-auth-regression-secret")
    monkeypatch.setenv("MODE", "production")
    monkeypatch.setenv("AUTH_ALLOW_LOOPBACK", "true")
    monkeypatch.setenv("AUTH_ALLOW_UNC_SUBDOMAINS", "true")
    monkeypatch.setenv(
        "AUTH_ALLOWED_ORIGINS", "localhost:1560/auth,stage.example.edu/auth"
    )
    app = FastAPI()
    app.include_router(auth.api)
    app.dependency_overrides[auth.UserService] = lambda: object()
    app.dependency_overrides[auth.GitHubService] = lambda: object()

    @app.get("/protected")
    def protected(identity=Depends(auth.authenticated_pid)):
        return identity

    with TestClient(app, follow_redirects=False) as test_client:
        yield test_client


def test_existing_pyjwt_2_8_session_remains_valid(client):
    """A previously issued session must survive the dependency upgrade.

    Generated with PyJWT 2.8.0 and this module's synthetic secret, with a
    fixed 2100 expiry to avoid wall-clock-dependent test failures.
    """
    token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJ1aWQiOiJzeW50aGV0aWNfdXNlciIsInBpZCI6Ijk5OTk5OTk5OSIsImV4cCI6NDEwMjQ0NDgwMH0."
        "0mKSwW3ilxTxlYb3D2lpWLQMZ8kAff8g7F9tWXUyaiM"
    )
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [999999999, "synthetic_user"]


def script_literal(response, pattern):
    """Inspect browser-parsed script text and recover one JSON string literal."""
    soup = BeautifulSoup(response.text, "html.parser")
    assert len(soup.find_all("script")) == 1
    assert soup.find("img") is None
    match = re.search(pattern, soup.script.string)
    assert match is not None
    return json.loads(match[1])


@pytest.mark.parametrize("code", PAYLOADS + ["valid-github-code"])
def test_github_callback_treats_code_as_url_data(client, code):
    response = client.get("/oauth/github", params={"code": code})

    assert response.status_code == 200
    target = script_literal(response, r"fetch\((.*), \{")
    parsed = urlsplit(target)
    assert parsed.path == "/oauth/github"
    assert parsed.netloc == ""
    assert parsed.fragment == ""
    assert parse_qs(parsed.query) == {"code": [code]}


@pytest.mark.parametrize("continue_to", PAYLOADS + ["/events?term=fall&limit=10"])
def test_login_treats_continuation_as_url_data(client, continue_to):
    response = client.get(
        "/auth", headers=IDENTITY, params={"continue_to": continue_to}
    )

    assert response.status_code == 200
    target = script_literal(response, r"window.location.href = (.*);")
    parsed = urlsplit(target)
    assert parsed.path == "/gate"
    assert parsed.netloc == ""
    assert parsed.fragment == ""
    assert parse_qs(parsed.query)["continue_to"] == [continue_to]


@pytest.mark.parametrize("path", ["/auth", "/oauth/github?code=valid"])
def test_bootstrap_pages_restrict_scripts_and_do_not_cache_credentials(client, path):
    first = client.get(path, headers=IDENTITY)
    second = client.get(path, headers=IDENTITY)

    for response in (first, second):
        soup = BeautifulSoup(response.text, "html.parser")
        nonce = soup.script.get("nonce")
        assert nonce
        policy = response.headers["content-security-policy"]
        assert f"script-src 'nonce-{nonce}'" in policy
        assert "'unsafe-inline'" not in policy
        assert "default-src 'none'" in policy
        assert "connect-src 'self'" in policy
        assert "base-uri 'none'" in policy
        assert "frame-ancestors 'none'" in policy
        assert response.headers["cache-control"] == "no-store"
        assert response.headers["referrer-policy"] == "no-referrer"
    assert (
        first.headers["content-security-policy"]
        != second.headers["content-security-policy"]
    )


@pytest.mark.parametrize(
    "origin",
    [
        "evil.example",
        "evil.example/auth",
        "localhost.evil.example/auth",
        "localhost:1560@evil.example/auth",
        "localhost:1560/auth@evil.example",
        "localhost:1560/auth?next=https://evil.example",
        "localhost:1560/auth#fragment",
        "localhost:1560/auth/../redirect",
        "localhost:1560/auth%3fnext=evil.example",
        "localhost:1560\\@evil.example/auth",
        "localhost:9999/redirect",
        "localhost:0/auth",
        "localhost:65536/auth",
        "localhost:notaport/auth",
        "[::1/auth",
        "127.0.0.1.evil.example/auth",
        "127.1/auth",
        "localhost:1560/auth\n",
        "stage.example.edu.evil.example/auth",
        "unc.edu/auth",
        "evilunc.edu/auth",
        "unc.edu.evil.example/auth",
        "service.unc.edu.evil.example/auth",
        "service.unc.edu@evil.example/auth",
        "evil.example@service.unc.edu/auth",
        "service.unc.edu\\@evil.example/auth",
        "evil.example\\.unc.edu/auth",
        "service%2eunc.edu/auth",
        "service.unc.edu./auth",
        ".unc.edu/auth",
        "service..unc.edu/auth",
        "-service.unc.edu/auth",
        "service-.unc.edu/auth",
        "service_name.unc.edu/auth",
        "sérvice.unc.edu/auth",
        "service.unc.edu:65536/auth",
        "service.unc.edu/auth?next=https://evil.example",
        "service.unc.edu/auth#fragment",
        "service.unc.edu/auth/../redirect",
        "service.unc.edu/auth\n",
        "//service.unc.edu/auth",
        "//evil.example/auth",
        "",
    ],
)
@pytest.mark.parametrize("prefix", ["", "https://", "http://"])
def test_auth_rejects_untrusted_origins_before_minting(
    client, monkeypatch, origin, prefix
):
    mint = Mock(return_value="unexpected-session")
    monkeypatch.setattr(auth, "_generate_token", mint)
    response = client.get(
        "/auth", headers=IDENTITY, params={"origin": f"{prefix}{origin}"}
    )

    assert response.status_code == 400
    assert "location" not in response.headers
    assert "token" not in response.text
    mint.assert_not_called()


@pytest.mark.parametrize("mode", ["production", "staging", "test"])
@pytest.mark.parametrize("host", ["stage.example.edu", "csxl.unc.edu"])
def test_development_flag_cannot_mint_outside_development(
    client, monkeypatch, mode, host
):
    monkeypatch.setenv("MODE", mode)
    monkeypatch.setattr(auth, "HOST", host)

    response = client.get(
        "/auth", headers=IDENTITY, params={"development_authentication": "true"}
    )

    assert response.status_code == 400
    assert "location" not in response.headers
    assert "bearerToken" not in response.text


@pytest.mark.parametrize("headers", [{}, IDENTITY])
def test_impersonation_is_disabled_in_production(client, headers):
    response = client.get("/auth/as/synthetic_user/999999999", headers=headers)
    assert response.status_code == 400


@pytest.mark.parametrize(
    "path",
    ["/auth/as/synthetic_user/999999999", "/auth?development_authentication=true"],
)
def test_development_authentication_still_works(client, monkeypatch, path):
    monkeypatch.setenv("MODE", "development")
    monkeypatch.setattr(auth, "HOST", "localhost:1560")

    response = client.get(path, headers=IDENTITY)

    assert response.status_code == 200
    token = script_literal(response, r"localStorage.setItem\('bearerToken', (.*)\);")
    claims = jwt.decode(token, auth._JWT_SECRET, algorithms=["HS256"])
    assert claims["uid"] == IDENTITY["uid"]
    assert claims["pid"] == int(IDENTITY["pid"])


def test_production_requires_sso_headers(client):
    assert client.get("/auth").status_code == 401


@pytest.mark.parametrize("method", ["post", "delete"])
def test_github_mutations_still_require_authentication(client, method):
    # HTTPBearer uses 401 in recent FastAPI releases and 403 in older ones.
    assert getattr(client, method)("/oauth/github?code=valid").status_code in (401, 403)


def test_delegation_encodes_query_parameters(client, monkeypatch):
    monkeypatch.setattr(auth, "HOST", "localhost:1560")
    continuation = "/events&origin=evil.example/auth#fragment"

    response = client.get(
        "/auth", headers=IDENTITY, params={"continue_to": continuation}
    )

    assert response.status_code == 307
    target = urlsplit(response.headers["location"])
    assert target.netloc == auth.AUTH_SERVER_HOST
    assert target.path == "/auth"
    assert target.fragment == ""
    assert parse_qs(target.query) == {
        "origin": ["localhost:1560/auth"],
        "continue_to": [continuation],
    }


@pytest.mark.parametrize(
    ("origin", "expected_target"),
    [
        ("localhost:1560/auth", "http://localhost:1560/auth"),
        ("stage.example.edu/auth", "https://stage.example.edu/auth"),
        ("https://stage.example.edu/auth", "https://stage.example.edu/auth"),
        ("http://localhost:1560/auth", "http://localhost:1560/auth"),
        ("https://localhost:1560/auth", "https://localhost:1560/auth"),
        ("http://[::1]:1560/auth", "http://[::1]:1560/auth"),
    ],
)
def test_approved_delegation_uses_short_lived_non_session_token(
    client, origin, expected_target
):
    continuation = "/events?term=fall&limit=10#details"
    response = client.get(
        "/auth",
        headers=IDENTITY,
        params={"origin": origin, "continue_to": continuation},
    )

    assert response.status_code == 307
    target = urlsplit(response.headers["location"])
    assert f"{target.scheme}://{target.netloc}{target.path}" == expected_target
    assert target.fragment == ""
    query = parse_qs(target.query)
    assert query["continue_to"] == [continuation]
    token = query["token"][0]
    claims = jwt.decode(
        token,
        auth._JWT_SECRET,
        algorithms=["HS256"],
        audience="csxl-delegated-auth",
    )
    assert claims["origin"] == origin
    remaining = claims["exp"] - datetime.now(timezone.utc).timestamp()
    assert 0 < remaining <= 300
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/protected", headers=headers).status_code == 401
    assert client.post("/oauth/github?code=valid", headers=headers).status_code == 401

    verified = client.get("/verify", params={"token": token, "origin": origin})
    assert verified.status_code == 200
    assert verified.json() == claims
    assert verified.headers["cache-control"] == "no-store"


def test_delegated_login_reissues_a_local_session(client, monkeypatch):
    origin = "localhost:1560/auth"
    response = client.get("/auth", headers=IDENTITY, params={"origin": origin})
    token = parse_qs(urlsplit(response.headers["location"]).query)["token"][0]
    verified = client.get("/verify", params={"token": token, "origin": origin})
    assert verified.status_code == 200
    verify = Mock(return_value=verified)
    monkeypatch.setattr(auth.requests, "get", verify)
    monkeypatch.setattr(auth, "HOST", "localhost:1560")
    monkeypatch.setattr(auth, "_JWT_SECRET", "separate-local-session-secret")

    response = client.get("/auth", params={"token": token, "continue_to": "/events"})

    assert response.status_code == 200
    verify.assert_called_once_with(
        "https://csxl.unc.edu/verify",
        params={"token": token, "origin": origin},
        timeout=10,
    )
    local_token = script_literal(
        response, r"localStorage.setItem\('bearerToken', (.*)\);"
    )
    claims = jwt.decode(local_token, auth._JWT_SECRET, algorithms=["HS256"])
    assert claims["uid"] == IDENTITY["uid"]
    assert claims["pid"] == int(IDENTITY["pid"])
    assert "aud" not in claims


@pytest.mark.parametrize("kind", ["session", "expired", "wrong-origin", "tampered"])
def test_delegated_verification_rejects_invalid_tokens(client, kind):
    claims = {
        "uid": IDENTITY["uid"],
        "pid": int(IDENTITY["pid"]),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
        "aud": "csxl-delegated-auth",
        "origin": "localhost:1560/auth",
    }
    secret = auth._JWT_SECRET
    if kind == "session":
        del claims["aud"]
        del claims["origin"]
    elif kind == "expired":
        claims["exp"] = datetime.now(timezone.utc) - timedelta(seconds=1)
    elif kind == "wrong-origin":
        claims["origin"] = "stage.example.edu/auth"
    elif kind == "tampered":
        secret = "attacker-controlled-secret"
    token = jwt.encode(claims, secret, algorithm="HS256")

    response = client.get(
        "/verify", params={"token": token, "origin": "localhost:1560/auth"}
    )

    assert response.status_code == 401


def test_failed_delegated_verification_does_not_mint_session(client, monkeypatch):
    monkeypatch.setattr(auth, "HOST", "localhost:1560")
    monkeypatch.setattr(auth.requests, "get", Mock(return_value=Mock(status_code=401)))
    mint = Mock()
    monkeypatch.setattr(auth, "_generate_token", mint)

    response = client.get("/auth", params={"token": "invalid"})

    assert response.status_code == 401
    mint.assert_not_called()


def test_normal_production_session_still_authenticates(client):
    response = client.get("/auth", headers=IDENTITY)
    token = script_literal(response, r"localStorage.setItem\('bearerToken', (.*)\);")

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == [int(IDENTITY["pid"]), IDENTITY["uid"]]


def test_empty_allowlist_disables_delegation(client, monkeypatch):
    monkeypatch.setenv("AUTH_ALLOWED_ORIGINS", "")
    monkeypatch.setenv("AUTH_ALLOW_LOOPBACK", "false")
    monkeypatch.setenv("AUTH_ALLOW_UNC_SUBDOMAINS", "false")
    response = client.get(
        "/auth", headers=IDENTITY, params={"origin": "localhost:1560/auth"}
    )
    assert response.status_code == 400


def test_default_allowlist_rejects_unapproved_hosted_callbacks(client, monkeypatch):
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    assert (
        client.get(
            "/auth", headers=IDENTITY, params={"origin": "localhost:1560/auth"}
        ).status_code
        == 307
    )
    assert (
        client.get(
            "/auth", headers=IDENTITY, params={"origin": "stage.example.edu/auth"}
        ).status_code
        == 400
    )


@pytest.mark.parametrize(
    "origin",
    [
        "service.unc.edu/api/auth",
        "localhost/auth",
        "localhost:1560/auth",
        "localhost:54321/auth",
        "localhost:4200/api/auth",
        "localhost:8000/api/auth",
        "127.0.0.1:1560/auth",
        "[::1]:1560/auth",
    ],
)
def test_existing_delegated_clients_can_verify_without_origin(
    client, monkeypatch, origin
):
    """Match existing delegated clients' token-only /verify contract."""
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    response = client.get("/auth", headers=IDENTITY, params={"origin": origin})
    assert response.status_code == 307
    target = urlsplit(response.headers["location"])
    assert f"{target.netloc}{target.path}" == origin
    loopback = target.hostname in ("localhost", "127.0.0.1", "::1")
    assert target.scheme == ("http" if loopback else "https")
    token = parse_qs(target.query)["token"][0]

    # Delegated clients read these fields and mint their own sessions; they neither
    # decode the handoff locally nor use it as a production XL API bearer token.
    verified = client.get("/verify", params={"token": token})
    assert verified.status_code == 200
    assert verified.json()["uid"] == IDENTITY["uid"]
    assert int(verified.json()["pid"]) == int(IDENTITY["pid"])


def test_loopback_exception_does_not_allow_arbitrary_paths(client, monkeypatch):
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    assert (
        client.get(
            "/auth", headers=IDENTITY, params={"origin": "localhost:1560/redirect"}
        ).status_code
        == 400
    )


@pytest.mark.parametrize(
    "callback",
    [
        "service.unc.edu/auth",
        "student.cs.unc.edu/auth",
        "app.cloudapps.unc.edu/sso/callback",
        "MixedCase.UnC.EDU/api/auth",
        "service.unc.edu:8443/auth",
        "new-service.unc.edu/auth",
        "learnwithai.unc.edu/api/auth/callback/test-state-123",
    ],
)
@pytest.mark.parametrize("prefix", ["", "https://"])
def test_unc_subdomains_can_delegate_without_an_explicit_entry(
    client, monkeypatch, callback, prefix
):
    origin = f"{prefix}{callback}"
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    monkeypatch.delenv("AUTH_ALLOW_UNC_SUBDOMAINS")
    response = client.get("/auth", headers=IDENTITY, params={"origin": origin})

    assert response.status_code == 307
    target = urlsplit(response.headers["location"])
    assert target.scheme == "https"
    assert f"{target.netloc}{target.path}" == callback
    token = parse_qs(target.query)["token"][0]
    verified = client.get("/verify", params={"token": token})
    assert verified.status_code == 200
    assert verified.json()["uid"] == IDENTITY["uid"]
    assert verified.json()["origin"] == origin
    assert 0 < verified.json()["exp"] - datetime.now(timezone.utc).timestamp() <= 300
    assert (
        client.get(
            "/protected", headers={"Authorization": f"Bearer {token}"}
        ).status_code
        == 401
    )


def test_unc_subdomain_policy_can_be_disabled(client, monkeypatch):
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    monkeypatch.setenv("AUTH_ALLOW_UNC_SUBDOMAINS", "false")
    assert (
        client.get(
            "/auth", headers=IDENTITY, params={"origin": "service.unc.edu/auth"}
        ).status_code
        == 400
    )


@pytest.mark.parametrize("prefix", ["", "https://"])
def test_explicit_callback_remains_allowed_when_unc_subdomain_policy_is_disabled(
    client, monkeypatch, prefix
):
    monkeypatch.setenv("AUTH_ALLOW_UNC_SUBDOMAINS", "false")
    monkeypatch.setenv("AUTH_ALLOWED_ORIGINS", "service.unc.edu/auth")
    assert (
        client.get(
            "/auth",
            headers=IDENTITY,
            params={"origin": f"{prefix}service.unc.edu/auth"},
        ).status_code
        == 307
    )


@pytest.mark.parametrize("prefix", ["", "https://"])
def test_disabled_unc_subdomain_policy_rejects_previous_handoffs(
    client, monkeypatch, prefix
):
    monkeypatch.delenv("AUTH_ALLOWED_ORIGINS")
    response = client.get(
        "/auth", headers=IDENTITY, params={"origin": f"{prefix}service.unc.edu/auth"}
    )
    assert response.status_code == 307
    token = parse_qs(urlsplit(response.headers["location"]).query)["token"][0]
    monkeypatch.setenv("AUTH_ALLOW_UNC_SUBDOMAINS", "false")
    assert client.get("/verify", params={"token": token}).status_code == 400


@pytest.mark.parametrize(
    "origin",
    [
        "http://learnwithai.unc.edu/api/auth/callback/test-state-123",
        "http://stage.example.edu/auth",
        "ftp://service.unc.edu/auth",
        "javascript://service.unc.edu/auth",
    ],
)
def test_hosted_callbacks_require_https_even_when_allowlisted(
    client, monkeypatch, origin
):
    monkeypatch.setenv("AUTH_ALLOWED_ORIGINS", origin.split("://", 1)[1])
    response = client.get("/auth", headers=IDENTITY, params={"origin": origin})
    assert response.status_code == 400
    assert "location" not in response.headers
