"""
GitHub user authentication service.
"""

import requests
import uuid
from fastapi import Depends
from github import Github
from ..models import User
from .user import UserService
from ..env import getenv

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class GitHubService:
    """GitHubService is the access layer to the GitHub OAuth2 API."""

    _user_svc: UserService

    def __init__(self, user_svc: UserService = Depends(UserService)):
        """Initialize a new GitHubService instance.

        Both arguments are optional and will be typically be injected.

        Args:
            user_svc (UserService): The UserService contains the logic for User management.
        """
        self._user_svc = user_svc

    def link_with_user(self, subject: User, oauth_code: str, redirect_uri: str) -> bool:
        """Authenticate a user via GitHub OAuth2.

        Args:
            subject (User): The user making the GitHub link request.
            oauth_code (str): The OAuth2 code from GitHub.
            redirect_uri (str): The URI to redirect the user to after authenticating with GitHub.

        Returns:
            bool: True if the user was successfully authenticated, False otherwise."""
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

    def remove_association(self, subject: User) -> None:
        """Remove the GitHub association for a user.

        Args:
            subject (User): The user to remove the GitHub association for

        Returns:
            None"""
        subject.github = ""
        self._user_svc.update(subject, subject)

    def get_oauth_login_url(self, redirect_uri: str) -> str:
        """Get the GitHub OAuth2 link for a user.

        Args:
            redirect_uri (str): The URI to redirect the user to after authenticating with GitHub.

        Returns:
            str: The GitHub OAuth2 link for a user."""
        client_id = getenv("GITHUB_CLIENT_ID")
        random_string = uuid.uuid4().hex  # Random String to prevent CSRF
        uri = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={random_string}"
        return uri

    def _get_github_oauth_token(self, oauth_code: str, redirect_uri: str) -> str:
        result = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": getenv("GITHUB_CLIENT_ID"),
                "client_secret": getenv("GITHUB_CLIENT_SECRET"),
                "code": oauth_code,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
        )

        json = result.json()
        token = json["access_token"]
        return token
