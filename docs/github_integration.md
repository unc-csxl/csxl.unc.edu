# GitHub Integration

## Overview

CSXL accounts can be linked with GitHub accounts for two interesting purposes:

1. To enable GitHub avatars to serve as a user's CSXL profile picture. This allows us to avoid the need to host user profile pictures on our own servers, and also allows users to change their profile picture by changing their GitHub profile picture.
2. To enable future extensions which integrate with GitHub, including:
    * Login via GitHub rather than UNC SSO (this would give a path toward alumni and industry partners using the CSXL without a UNC SSO account)
    * Public CSXL profiles that link to GitHub projects
    * Course integrations, notably COMP423 sprint tracking, etc.

## Implementation Notes

Three fields were added to UserEntity:

* `github` - the GitHub username of the user
* `github_avatar_url` - the URL of the user's GitHub avatar
* `github_id` - the GitHub user ID of the user

Routes were added to `api/authentication.py` to handle the GitHub OAuth flow.

1. `GET /auth/github_oauth_login_url` - This produces the URL the client is redirected to in order to initiate the GitHub OAuth flow. The URL is constructed using the `GITHUB_CLIENT_ID` environment variable.
2. `GET /auth/github` - Upon return from GitHub, the user is redirected to this route with a code. This page produces some HTML to bootstrap the linkage of the CSXL account with the GitHub account. This is necessary due to the CSXL JWT bearer token stored in localStorage.
3. `POST /auth/github` - The bootstrapped HTML initiates a POST request to this route, which completes the linkage of the CSXL account with the GitHub account.
4. `DELETE /auth/github` - This route unlinks the CSXL account from the GitHub account.

From the user interface, a user can visit their profile to manage the link / unlink with their GitHub account.

## Development Concerns

To utilize the GitHub integration in development, you will need to create a GitHub OAuth app on your personal account and add the appropriate environment variables to your `.env` file, as follows.

1. Go to GitHub > Settings > Developer Settings > Oauth Apps > New OAuth App

2. Fill out the form as follows:

    * Application name: CSXL
    * Homepage URL: `https://csxl.unc.edu`
    * Authorization callback URL: `http://localhost:1560/auth/github`
    * After creating the app, copy the client secret

3. In `backend/.env`, add the following environment variables, with the information from the GitHub OAuth app:

* `GITHUB_CLIENT_ID`
* `GITHUB_CLIENT_SECRET`

4. Finally, you will need to either reset the database or run `alembic upgrade head` to add the fields to `user`.

## Deployment Concerns

In production, the official CSXL GitHub OAuth app's Client ID and secret need to be added to the environment of the deployment:

* `GITHUB_CLIENT_ID`
* `GITHUB_CLIENT_SECRET`

Additionally, the migration 48c0e needs to be run against on the production database: `alembic upgrade head`.

## Future Work

For deeper GitHub integration, we will need to store each user's GitHub OAuth token in some kind of store (ephemeral/redis or the database). This will require caution to avoid token leakage through the API.