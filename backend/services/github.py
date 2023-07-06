"""GitHub user authentication service."""

import requests
import uuid
from fastapi import Depends
from github import Github
from ..database import Session, db_session
from ..models import User
from .user import UserService
from ..env import getenv


class GitHubService:
    _session: Session
    _user_svc: UserService

    def __init__(self, session: Session = Depends(db_session), user_svc: UserService = Depends(UserService)):
        self._session = session
        self._user_svc = user_svc

    def link_with_user(self, subject: User, oauth_code: str, redirect_uri: str):
        """Authenticate a user via GitHub OAuth2."""
        try:
            token = self._get_github_oauth_token(oauth_code, redirect_uri)
            github = Github(token)
            github_user = github.get_user()
            subject.github = github_user.login
            subject.github_id = github_user.id
            subject.github_avatar = github_user.avatar_url
            self._user_svc.update(subject, subject)
            return True
        except:
            return False

    def remove_association(self, subject: User):
        """Remove the GitHub association for a user."""
        subject.github = ""
        self._user_svc.update(subject, subject)

    def get_oauth_login_url(self, redirect_uri: str) -> str:
        """Get the GitHub OAuth2 link for a user."""
        client_id = getenv('GITHUB_CLIENT_ID')
        random_string = uuid.uuid4().hex  # Random String to prevent CSRF
        uri = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={random_string}'
        return uri

    def _get_github_oauth_token(self, oauth_code: str, redirect_uri: str) -> str:
        result = requests.post('https://github.com/login/oauth/access_token', data={
            'client_id': getenv('GITHUB_CLIENT_ID'),
            'client_secret': getenv('GITHUB_CLIENT_SECRET'),
            'code': oauth_code,
            'redirect_uri': redirect_uri,
        }, headers={'Accept': 'application/json'})

        json = result.json()
        token = json['access_token']
        return token
