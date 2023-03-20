import jwt
import requests
from datetime import datetime, timedelta
from fastapi import APIRouter, Header, HTTPException, Request, Response, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from ..env import getenv
from ..services import UserService
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
    if request.url.path.startswith('/auth/as/'):
        # Authenticate as another user in development using special route.
        if getenv('MODE') == 'development':
            testing_authentication = True
        else:
            onyen = request.headers['uid']
            raise HTTPException(status_code=400, detail=f'Tsk, tsk. That is a naughty request {onyen}.')

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
        if origin == 'localhost':
            target = 'http://localhost:1560/auth'  # TODO: Make this port an env variable
        else:
            target = f'https://{HOST}/auth'
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
