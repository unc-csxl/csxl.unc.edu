"""User authentication over HTTP via Headers and/or HTTP JWT Bearer Tokens.

This module provides a `registered_user` dependency injection function for other routes
to use to both ensure a user is authenticated and resolve to the logged in User's model.
Further, this module provides the routes and logic for backend authentication.

The router is mounted at `/auth` and provides the following endpoints:

    /auth
        Redirects to the authentication server to authenticate the user.

    /auth/as/{uid}/{pid}
        Redirects to the authentication server to authenticate the user as
        another user. This route is only available in development mode.

    /auth/verify
        Verifies the validity of a JWT token and returns the decoded token. This is
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
    A. The production server authentication works as usual, but if the `origin` parameter is
       detected alongside the SSO headers, the user will be redirected back to the `origin` 
       server with a JWT `token` query parameter. This token is signed by the production server.
    B. Back on the development/staging server, we need to verify that the token given to the route
       was actually signed by the production server. If we did not do this, a malicious user could
       simply generate a token and pass it to the development server to gain access. Thus, an HTTP
       request from the development/stage server is made to the production server's `/auth/verify` route
       to verify the token's validity. If the token is valid, the development/staging server then 
       issues a new `token` to the client that is signed by the development/staging server. 
       This token is then used for all subsequent requests.
2. If an unauthenticated user visits /auth/as/{uid}/{pid} in development, they are authenticated
    as the user with the given `uid` and `pid`, which are their ONYEN and PID, respectively. 
    This route is only available in development mode.

Finally, the `authenticated_pid` function ensures a user is authenticated with PID and Onyen, 
but does not require that the user be registered in the database. This is only really useful 
for routes used in the process of registering a user.
"""

import jwt
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter, Header, HTTPException, Request, Response, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from ..env import getenv
from ..services import UserService, GitHubService
from ..models import User


__authors__ = ['Kris Jordan']
__copyright__ = 'Copyright 2023'
__license__ = 'MIT'

openapi_tags = {'name': 'TODO', 'description': 'TODO'}

api = APIRouter()

HOST = getenv('HOST')
AUTH_SERVER_HOST = 'csxl.unc.edu'
_JWT_SECRET = getenv('JWT_SECRET')
_JST_ALGORITHM = 'HS256'


def registered_user(
    user_service: UserService = Depends(),
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())
) -> User:
    """Returns the authenticated user or raises a 401 HTTPException if the user is not authenticated."""
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM])
            user = user_service.get(auth_info['pid'])
            if user:
                return user
        except:
            ...
    raise HTTPException(status_code=401, detail='Unauthorized')


def authenticated_pid(
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())
) -> tuple[int, str]:
    """Returns the authenticated user's PID and Onyen or raises a 401 HTTPException if the user is not authenticated."""
    if token:
        try:
            auth_info = jwt.decode(
                token.credentials, _JWT_SECRET, algorithms=[_JST_ALGORITHM])
            return int(auth_info['pid']), auth_info['uid']
        except jwt.exceptions.InvalidSignatureError:
            ...
    raise HTTPException(status_code=401, detail='Unauthorized')


@api.get('/verify')
def auth_verify(token: str, continue_to: str = '/'):
    return jwt.decode(token, _JWT_SECRET, algorithms=[_JST_ALGORITHM], options={'verify_signature': True})


@api.get('/auth', include_in_schema=False)
@api.get('/auth/as/{uid}/{pid}', include_in_schema=False)
def bearer_token_bootstrap(
    request: Request,
    uid: str | None = Header(None),
    pid: int | None = Header(None),
    continue_to: str = '/',
    origin: str | None = None,
    token: str | None = None,
):
    """Handles authentication in both production and development. See the module docstring for more details."""
    if request.url.path.startswith('/auth/as/'):
        # Authenticate as another user in development using special route.
        if getenv('MODE') == 'development':
            testing_authentication = True
        else:
            onyen = request.headers['uid']
            raise HTTPException(
                status_code=400, detail=f'Tsk, tsk. That is a naughty request {onyen}.')

    if HOST == AUTH_SERVER_HOST or ('testing_authentication' in locals() and testing_authentication):
        # Production App Request
        if uid is not None and pid is not None:
            return _handle_auth_in_production(uid, pid, continue_to, origin)
        else:
            raise HTTPException(
                status_code=401, detail='You are not authenticated.')
    else:
        # Development / Delegated Staging Auth Request
        if not token:
            return _delegate_to_auth_server(continue_to)
        else:
            return _verify_delegated_auth_token(continue_to, token)


@api.get('/oauth/github_oauth_login_url', include_in_schema=False)
def github_oauth_login_url(subject: User = Depends(registered_user), github_service: GitHubService = Depends()) -> str:
    """Return the GitHub OAuth login URL with the appropriate callback URL."""
    redirect_uri = _github_oauth_redirect_uri
    return github_service.get_oauth_login_url(redirect_uri)


@api.get('/oauth/github', include_in_schema=False)
def github_oauth(code: str):
    """Upon return from GitHub with a code, this route produces bootstrapping HTML for linking the user's GitHub account.
    
    The reason this step is necessary is because the user's CSXL bearer token is only available in localStorage. Thus,
    it is not visible in the return from GitHub's OAuth page. The HTML produced by this route contains JavaScript that
    will extract the token from localStorage and then POST it to the /oauth/github route below.
    """
    return _link_github_html(code)


@api.post('/oauth/github', include_in_schema=False)
def github_link(code: str, subject: User = Depends(registered_user), github_service: GitHubService = Depends()):
    """Link the user's GitHub account with their CSXL account."""
    redirect_uri = _github_oauth_redirect_uri()
    if github_service.link_with_user(subject, code, redirect_uri):
        return "Successfully linked GitHub account."
    else:
        raise HTTPException(
            status_code=400, detail="Failed to link GitHub account.")


@api.delete('/oauth/github', include_in_schema=False)
def github_unlink(subject: User = Depends(registered_user), github_service: GitHubService = Depends()):
    """Unlink user's GitHub account with their CSXL account."""
    github_service.remove_association(subject)
    return "Successfully unlinked GitHub account."


def _delegate_to_auth_server(continue_to: str):
    return RedirectResponse(
        f'https://{AUTH_SERVER_HOST}/auth?origin={HOST}&continue_to={continue_to}'
    )


def _verify_delegated_auth_token(continue_to: str, token: str):
    params = {'token': token}
    response = requests.get(
        f'https://{AUTH_SERVER_HOST}/verify', params=params)
    if response.status_code == requests.codes.ok:
        # Generate a token for development app based on verified information
        body = response.json()
        uid = body['uid']
        pid = body['pid']
        new_token = _generate_token(uid, pid)
        return _set_client_token(new_token, continue_to)
    else:
        raise HTTPException(
            status_code=401, detail='You are not authenticated.')


def _handle_auth_in_production(
    uid: str | None = Header(None),
    pid: int | None = Header(None),
    continue_to: str = '/',
    origin: str | None = None,
):
    token = _generate_token(uid, pid)
    if origin is None:
        # Production Authentication Request
        return _set_client_token(token, continue_to)
    else:
        # Development Authentication Request (origin is app in development)
        if origin.startswith('localhost'):
            target = 'http://localhost:1560/auth'  # TODO: Make this port an env variable
        else:
            target = f'https://{origin}/auth'
        return RedirectResponse(
            f'{target}?token={token}&continue_to={continue_to}',
            headers={'Cache-Control': 'no-cache'},
        )


def _generate_token(uid: any, pid: any):
    token = jwt.encode(
        {'uid': uid, 'pid': pid, 'exp': datetime.now() + timedelta(days=90)},
        _JWT_SECRET,
        algorithm=_JST_ALGORITHM,
    )
    return token


def _github_oauth_redirect_uri():
    if HOST.startswith('localhost'):
        redirect_protocol = 'http'
    else:
        redirect_protocol = 'https'

    return f'{redirect_protocol}://{HOST}/oauth/github'


def _set_client_token(token: str, continue_to: str):
    data = f'''
    <html>
        <head>
            <title>CS Experience Labs at The University of North Carolina at Chapel Hill</title>
            <style>
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
            <script type='application/javascript'>
                localStorage.setItem('bearerToken', '{token}');
                window.location.href = '/gate?continue_to={continue_to}';
            </script>
        </body>
    </html>
    '''
    return Response(
        content=data,
        media_type='text/html',
        headers={'Cache-Control': 'no-cache'},
    )


def _link_github_html(code: str):
    data = f'''
    <html>
        <head>
            <title>CS Experience Labs at The University of North Carolina at Chapel Hill</title>
            <style>
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
            <script type='application/javascript'>
                let token = localStorage.getItem('bearerToken');
                fetch('/oauth/github?code={code}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    }}
                }}).then(response => {{
                    if (response.status === 200) {{
                        window.location.href = '/profile';
                    }} else {{
                        window.location.href = '/profile?error=github';
                    }}
                }});
            </script>
        </body>
    </html>
    '''
    return Response(
        content=data,
        media_type='text/html',
        headers={'Cache-Control': 'no-cache'},
    )


def _set_client_token(token: str, continue_to: str):
    data = f'''
    <html>
        <head>
            <title>CS Experience Labs at The University of North Carolina at Chapel Hill</title>
            <style>
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
            <script type='application/javascript'>
                localStorage.setItem('bearerToken', '{token}');
                window.location.href = '/gate?continue_to={continue_to}';
            </script>
        </body>
    </html>
    '''
    return Response(
        content=data,
        media_type='text/html',
        headers={'Cache-Control': 'no-cache'},
    )
