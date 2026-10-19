"""User authentication over HTTP via Headers and/or HTTP JWT Bearer Tokens.

This module provides a `registered_user` dependency injection function for other routes
to use to both ensure a user is authenticated and resolve to the logged in User's model.
Further, this module provides the routes and logic for backend authentication.

The router provides the following authentication endpoints:

    /auth
        Redirects to the authentication server to authenticate the user.

    /auth/as/{uid}/{pid}
        Redirects to the authentication server to authenticate the user as
        another user. This route is only available in development mode.

    /verify
        Verifies a delegated handoff JWT and returns the decoded token. This is
        the end-point a development/staging server requests of the production server
        to verify the legitimacy of delegated authentication.

The implementation of auth routes are nuanced due to UNC Cloud Apps' Single Sign-On (SSO)
proxy service. In production, there is a proxy sitting in front of the app that
integrates with UNC's SSO/Shibboleth service for authentication. For more information
on this proxy service, see the [official CloudApps documentation](https://help.unc.edu/sp?id=kb_article_view&sysparm_article=KB0011256)

In production, the proxy intercepts all routes prefixed with `/auth`. Two paths follow:

1. If the user is not logged in, the proxy redirects the user to the authentication server.
2. If the user is logged in, the proxy sets the `uid` and `pid` headers to the user's
    Onyen and PID, respectively, and forwards the request to our app.

Once the request is forwarded to our app server, the `uid` and `pid` headers are used to
generate a JWT token and persist it in the client's local storage via a the _set_client_token
function. The frontend client code then uses this token, via JwtToken imported in AppModule,
to set the HTTP Authorization header on all subsequent API requests thanks to the @auth0/angular-jwt
library's [HTTP Interceptor](https://www.npmjs.com/package/@auth0/angular-jwt).

In development, the proxy is not present. Instead, there are two options for authentication:

1. If an unauthenticated user visits /auth in development, or staging, they are redirected
   to the production `csxl.unc.edu/auth` route with an additional query parameter `origin`.
    A. The production server authentication works as usual, but if an approved `origin`
       is supplied alongside the SSO headers, the user is redirected there with a five-minute
       handoff JWT. It is signed by production but cannot authenticate production API calls.
    B. Back on the development/staging server, we need to verify that the token given to the route
       was actually signed by the production server. If we did not do this, a malicious user could
       simply generate a token and pass it to the development server to gain access. Thus, an HTTP
       request from the development/stage server is made to the production server's `/verify` route
       to verify the token's validity. Existing clients may send just `token`; clients may
       also send `origin` to check that it matches the signed callback. If the token is valid,
       the development/staging server then
       issues a new `token` to the client that is signed by the development/staging server.
       This token is then used for all subsequent requests.
2. If an unauthenticated user visits /auth/as/{uid}/{pid} in development, they are authenticated
    as the user with the given `uid` and `pid`, which are their ONYEN and PID, respectively.
    This route is only available in development mode.

Finally, the `authenticated_pid` function ensures a user is authenticated with PID and Onyen,
but does not require that the user be registered in the database. This is only really useful
for routes used in the process of registering a user.
"""

import json
import os
import re
import secrets
import jwt
import requests
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlsplit
from fastapi import APIRouter, Header, HTTPException, Request, Response, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from ..env import getenv
from ..services import UserService, GitHubService
from ..models import User


__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter()

HOST = getenv("HOST")
AUTH_SERVER_HOST = "csxl.unc.edu"
_JWT_SECRET = getenv("JWT_SECRET")
_JST_ALGORITHM = "HS256"
_DELEGATION_AUDIENCE = "csxl-delegated-auth"


def registered_user(
    user_service: UserService = Depends(),
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
) -> User:
    """Returns the authenticated user or raises a 401 HTTPException if the user is not authenticated."""
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM]
            )
            user = user_service.get(auth_info["pid"])
            if user:
                return user
        except:
            ...
    raise HTTPException(status_code=401, detail="Unauthorized")


def authenticated_pid(
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
) -> tuple[int, str]:
    """Returns the authenticated user's PID and Onyen or raises a 401 HTTPException if the user is not authenticated."""
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM]
            )
            return int(auth_info["pid"]), auth_info["uid"]
        except jwt.InvalidTokenError:
            ...
    raise HTTPException(status_code=401, detail="Unauthorized")


@api.get("/verify", include_in_schema=False)
def auth_verify(token: str, origin: str | None = None):
    """Verify the legitimacy of a token for delegated authentication purposes.

    This endpoint is used to facilitate SSO authentication in development and staging environments.
    For usage, see the helper function _verify_delegated_auth_token below.

    The staging environment will ultimately dispatch to the production environment's verify
    route, here, in order to verify the token (and then reissue using its own signing).
    """
    try:
        claims = jwt.decode(
            token,
            _JWT_SECRET,
            algorithms=[_JST_ALGORITHM],
            audience=_DELEGATION_AUDIENCE,
            options={"require": ["exp", "uid", "pid", "origin", "aud"]},
        )
        _delegated_auth_target(claims["origin"])
        if origin is not None and claims["origin"] != origin:
            raise HTTPException(status_code=401, detail="Invalid delegated login.")
        return Response(
            content=json.dumps(claims),
            media_type="application/json",
            headers={"Cache-Control": "no-store"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid delegated login.")


@api.get("/auth", include_in_schema=False)
def bearer_token_bootstrap(
    uid: str | None = Header(None),
    pid: int | None = Header(None),
    continue_to: str = "/",
    origin: str | None = None,
    token: str | None = None,
    development_authentication: bool = False,
):
    if development_authentication and getenv("MODE") != "development":
        raise HTTPException(
            status_code=400, detail="Development authentication is disabled."
        )
    if HOST == AUTH_SERVER_HOST or development_authentication:
        # Production headers must be supplied by the trusted SSO proxy. Direct
        # access to this backend must be blocked by the deployment (see docs/auth.md).
        if uid is not None and pid is not None:
            return _handle_auth_in_production(uid, pid, continue_to, origin)
        else:
            raise HTTPException(status_code=401, detail="You are not authenticated.")
    else:
        # Development / Delegated Staging Auth Request
        if not token:
            return _delegate_to_auth_server(continue_to)
        else:
            return _verify_delegated_auth_token(continue_to, token)


@api.get("/auth/as/{uid}/{pid}", include_in_schema=False)
def bearer_token_impersonate(
    request: Request,
    uid: str | None,
    pid: int | None,
    continue_to: str = "/",
    origin: str | None = None,
    token: str | None = None,
):
    """Authenticate as another user in development mode only using this special route."""
    if getenv("MODE") == "development":
        return bearer_token_bootstrap(uid, pid, continue_to, origin, token, True)
    else:
        raise HTTPException(
            status_code=400, detail="Development authentication is disabled."
        )


@api.get("/oauth/github_oauth_login_url", include_in_schema=False)
def github_oauth_login_url(
    subject: User = Depends(registered_user), github_service: GitHubService = Depends()
) -> str:
    """Return the GitHub OAuth login URL with the appropriate callback URL."""
    redirect_uri = _github_oauth_redirect_uri()
    return github_service.get_oauth_login_url(redirect_uri)


@api.get("/oauth/github", include_in_schema=False)
def github_oauth(code: str):
    """Upon return from GitHub with a code, this route produces bootstrapping HTML for linking the user's GitHub account.

    The reason this step is necessary is because the user's CSXL bearer token is only available in localStorage. Thus,
    it is not visible in the return from GitHub's OAuth page. The HTML produced by this route contains JavaScript that
    will extract the token from localStorage and then POST it to the /oauth/github route below.
    """
    return _link_github_html(code)


@api.post("/oauth/github", include_in_schema=False)
def github_link(
    code: str,
    subject: User = Depends(registered_user),
    github_service: GitHubService = Depends(),
):
    """Link the user's GitHub account with their CSXL account."""
    redirect_uri = _github_oauth_redirect_uri()
    if github_service.link_with_user(subject, code, redirect_uri):
        return "Successfully linked GitHub account."
    else:
        raise HTTPException(status_code=400, detail="Failed to link GitHub account.")


@api.delete("/oauth/github", include_in_schema=False)
def github_unlink(
    subject: User = Depends(registered_user), github_service: GitHubService = Depends()
):
    """Unlink user's GitHub account with their CSXL account."""
    github_service.remove_association(subject)
    return "Successfully unlinked GitHub account."


def _delegate_to_auth_server(continue_to: str):
    host_origin = f"{HOST}/auth"
    query = urlencode({"origin": host_origin, "continue_to": continue_to})
    return RedirectResponse(
        f"https://{AUTH_SERVER_HOST}/auth?{query}",
        headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
    )


def _verify_delegated_auth_token(continue_to: str, token: str):
    params = {"token": token, "origin": f"{HOST}/auth"}
    response = requests.get(
        f"https://{AUTH_SERVER_HOST}/verify", params=params, timeout=10
    )
    if response.status_code == requests.codes.ok:
        # Generate a token for development app based on verified information
        body = response.json()
        uid = body["uid"]
        pid = body["pid"]
        new_token = _generate_token(uid, pid)
        return _set_client_token(new_token, continue_to)
    else:
        raise HTTPException(status_code=401, detail="You are not authenticated.")


def _delegated_auth_target(origin: str) -> str:
    """Resolve a callback approved by domain policy or an exact allowlist entry.

    Callbacks accept absolute URLs or the existing host[:port]/path format.
    Allowlist entries remain scheme-free. Loopback development callbacks may
    use HTTP on any valid port; hosted callbacks require HTTPS.
    """
    allowed = {
        entry.strip()
        for entry in os.getenv("AUTH_ALLOWED_ORIGINS", "").split(",")
        if entry.strip()
    }
    has_scheme = origin.startswith(("https://", "http://"))
    try:
        parsed = urlsplit(origin if has_scheme else f"https://{origin}")
        port = parsed.port
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid authentication origin.")
    callback = f"{parsed.netloc}{parsed.path}"
    expected_origin = f"{parsed.scheme}://{callback}" if has_scheme else callback
    if (
        not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or not parsed.path.startswith("/")
        or any(part in (".", "..") for part in parsed.path.split("/"))
        or parsed.query
        or parsed.fragment
        or origin != expected_origin
        or any(character in origin for character in "\\%\r\n\t ")
        or port == 0
    ):
        raise HTTPException(status_code=400, detail="Invalid authentication origin.")
    loopback = parsed.hostname in ("localhost", "127.0.0.1", "::1")
    if has_scheme and parsed.scheme == "http" and not loopback:
        raise HTTPException(status_code=400, detail="Invalid authentication origin.")
    development_callback = (
        loopback
        and parsed.path in ("/auth", "/api/auth")
        and os.getenv("AUTH_ALLOW_LOOPBACK", "true").lower() == "true"
    )
    # Match complete DNS labels and the domain boundary, not a URL substring.
    # urlsplit normalizes hostname case; the bare unc.edu domain is not a subdomain.
    unc_callback = (
        os.getenv("AUTH_ALLOW_UNC_SUBDOMAINS", "true").lower() == "true"
        and len(parsed.hostname) <= 253
        and re.fullmatch(
            r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+unc\.edu",
            parsed.hostname,
        )
        is not None
    )
    if callback not in allowed and not development_callback and not unc_callback:
        raise HTTPException(status_code=400, detail="Unapproved authentication origin.")
    protocol = parsed.scheme if has_scheme else ("http" if loopback else "https")
    return f"{protocol}://{callback}"


def _handle_auth_in_production(
    uid: str | None = Header(None),
    pid: int | None = Header(None),
    continue_to: str = "/",
    origin: str | None = None,
):
    if origin is None:
        # Production Authentication Request
        return _set_client_token(_generate_token(uid, pid), continue_to)
    else:
        target = _delegated_auth_target(origin)
        # This handoff is deliberately not a production API bearer token. The
        # audience makes ordinary session decoding reject it, even before expiry.
        token = jwt.encode(
            {
                "uid": uid,
                "pid": pid,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
                "aud": _DELEGATION_AUDIENCE,
                "origin": origin,
            },
            _JWT_SECRET,
            algorithm=_JST_ALGORITHM,
        )
        query = urlencode({"token": token, "continue_to": continue_to})
        return RedirectResponse(
            f"{target}?{query}",
            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
        )


def _generate_token(uid: any, pid: any):
    token = jwt.encode(
        {"uid": uid, "pid": pid, "exp": datetime.now() + timedelta(days=90)},
        _JWT_SECRET,
        algorithm=_JST_ALGORITHM,
    )
    return token


def _github_oauth_redirect_uri():
    if HOST.startswith("localhost"):
        redirect_protocol = "http"
    else:
        redirect_protocol = "https"

    return f"{redirect_protocol}://{HOST}/oauth/github"


def _bootstrap_response(data: str, nonce: str) -> Response:
    """Allow only this response's bootstrap script and same-origin API calls."""
    return Response(
        content=data,
        media_type="text/html",
        headers={
            "Cache-Control": "no-store",
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": (
                f"default-src 'none'; script-src 'nonce-{nonce}'; "
                f"style-src 'nonce-{nonce}'; connect-src 'self'; "
                "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
            ),
        },
    )


def _link_github_html(code: str):
    current_time = datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
    nonce = secrets.token_urlsafe(32)
    # URL encoding handles HTML delimiters as well as quotes and query separators.
    # JSON encoding then produces a complete JavaScript string literal.
    link_url = json.dumps("/oauth/github?" + urlencode({"code": code}))
    data = f"""
    <html>
        <head>
            <title>CS Experience Labs at The University of North Carolina at Chapel Hill</title>
            <style nonce='{nonce}'>
                html {{
                    background: #303030;
                    color: white;
                    font: 400 14px/20px 'Helvetica Neue', sans-serif;
                    letter-spacing: normal;
                    text-align: center;
                    margin: 1em;
                }}
            </style>
        </head>
        <body>
            <h1 id='header'>Linking your GitHub account with CSXL ...</h1>
            <p id='message'>One sec while we associate your GitHub account with CSXL!</p>
            <script type='application/javascript' nonce='{nonce}'>
                let token = localStorage.getItem('bearerToken');
                fetch({link_url}, {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    }}
                }}).then(response => {{
                    if (response.status === 200) {{
                        window.location.href = '/profile?time={current_time}';
                    }} else {{
                        window.location.href = '/profile?error=github';
                    }}
                }});
            </script>
        </body>
    </html>
    """
    return _bootstrap_response(data, nonce)


def _set_client_token(token: str, continue_to: str):
    current_time = datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
    nonce = secrets.token_urlsafe(32)
    gate_url = json.dumps(
        "/gate?" + urlencode({"continue_to": continue_to, "time": current_time})
    )
    data = f"""
    <html>
        <head>
            <title>CS Experience Labs at The University of North Carolina at Chapel Hill</title>
            <style nonce='{nonce}'>
                html {{
                    background: #303030;
                    color: white;
                    font: 400 14px/20px 'Helvetica Neue', sans-serif;
                    letter-spacing: normal;
                    text-align: center;
                    margin: 1em;
                }}
            </style>
        </head>
        <body>
            <h1 id='header'>Loading CSXL ...</h1>
            <p id='message'>One sec while we load the CSXL app!</p>
            <script type='application/javascript' nonce='{nonce}'>
                localStorage.setItem('bearerToken', {json.dumps(token)});
                window.location.href = {gate_url};
            </script>
        </body>
    </html>
    """
    return _bootstrap_response(data, nonce)
