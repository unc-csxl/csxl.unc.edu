# Authentication and Authorization

This document is for CSXL Developers who need authentication and authorization in their feature work.

## Table of Contents

* [Authentication](#authentication)
* [Authorization](#authorization)
  * [Feature-specific rules](#1-feature-specific-rules)
  * [Administrative Permission Rules](#2-administrative-permission-rules)
* [Common Development Concerns](#common-development-concerns)
  * [Backend Routes Requiring a Registered User](#backend-routes-requiring-a-registered-user)
  * [Testing Protected Routes via OpenAPI](#testing-authenticated-routes-via-openapi)
  * [Protecting Backend Service Methods](#protecting-backend-service-methods)
  * [Frontend Features Requiring a Registered User](#frontend-features-requiring-a-registered-user)
  * [Frontend Features Requiring Authorization](#frontend-features-requiring-authorization)

## Authentication

Authentication in `csxl.unc.edu` is integrated with UNC's Single Sign-on (SSO) Shibboleth service. This allows username, password, and UNC affinity to be handled by UNC ITS and our application takes a dependency upon it. For more information on SSO, see ITS' [official documentation](https://its.unc.edu/2017/07/24/shibboleth/). For the implementation details on *how* authentication works in this application, see [backend/api/authentication.py](backend/api/authentication.py).

Authentication is verifying *who* the "subject" accessing a system is. The term "subject" is chosen intentionally in the security lexicon. A subject may be a person, but alternatively an automated program accessing a system on behalf of a person, group, or organization. The CSXL application is, for now, foremost a user-facing application that serves the people of the computer science department at UNC. Thus, a "subject" is a person and user of the CSXL application for our concerns.

## Authorization

Authorization is verifying a subject/user *has permission* to carry out an *action* on a *resource* within the system. For example, the leader of a workshop may have permission to edit a workshop's details, whereas a registered participant of a workshop would not. Additionally, a site administrator may every permission possible, whereas a newly registered user does not.

Authorization concerns in the `csxl.unc.edu` application can be thought of as the union of two distinct rule sets:

## 1. Feature-specific Rules

When a feature of the website, via one or more of its models, is related to one or more users in the system, it is likely these users will need authorization to carry out specific actions on these models. This authorization is achieved via feature-specific rules. For example, a user who has registered for a workshop should be able to unregister themselves if a conflict has arisen. This user should not be able to unregister *other* users, though. A workshop leader may be able to modify the details of *their* workshop, but not someone else's.

The logic for enforcing feature-specific concerns should be specified in the feature's backend service layer methods. Developers are encouraged to factor out this logic into reusable helper functions; it is likely many service methods will rely upon the same logic.

All backend service layer methods with authorization concerns should accept a `subject: User` as their first parameter. This represents the user attempting to carry out the action and whose authorization needs verification. If your backend service layer method determines the subject does not have permission to carry out the operation, raise a [`backend.services.permission.UserPermissionException`](backend/services/permission.py). Example usage of this exception:

```python
raise UserPermissionException('workshops.update', f'workshops/{workshop.id}`)
```

For administrative concerns discussed next, the first argument is conventionally specified as `service.method` and the second as the target *path* of the primary model being operated on, without the leading `api/`. In the above example, you could assume `/api/workshops/1` was the FastAPI path to the model being operated on.

## 2. Administrative Permission Rules

The second kind of authorization rules are administrative permissions. For example, a site administrator needs permission to carry out any action on every resource. Alternatively, the Workshop Administrator needs to be able to create new workshops, assign workshop leads, and edit any of them. Administrative permissions are built into the site via Roles and Permissions.

The facilities for this kind of authorization is built into the site. Feature developers need to use the Permission API to check for administrative permissions where appropriate. Generally, there are two appropriate places for administrative permisssion rule enforcement:

A. Everywhere there is feature-specific authorization rule there should be a check for administrative permission. Rule-of-thumb, everywhere your feature raises a `UserPermissionException`, you should also check for the corresponding administrative permission rule before raising the error.

B. Admin-only aspects of a feature.

Permissions are assigned to Roles and Users can be members of many Roles. A Permission *grants* access to carry out action(s) over resource(s). The action and resource are specified as strings where the action refers to a protected backend service method and the resource refers to a model's path. Permissions strings can be specified with wildcard asterisks implying "match all".

To see how administrative permissions are managed in the app, in the development environment, after resetting the database, sign in as the [Super User](http://localhost:1560/auth/as/root/999999999) and go to the Admin > Roles page. Open the Staff role to see it has permissions to action `role.*` on resource `*`. The `*` implies "matches anything following". Thus, users with the Staff role have permission to carry out any action in the `services.role` service on all roles. You can see "Merritt Manager" is a user who has "Staff" role capabilities. If you navigate back to Roles and then to the "Sudoers" role, you will see the "Super User" you are signed in as has authorization for all actions on all resources.

## Common Development Concerns

### Backend Routes Requiring a Registered User

Thanks to FastAPI's dependency injection system and the `registered_user` helper function in [backend/api/authentication.py], adding authentication to a route is as easy as adding a parameter. For example, [backend/api/roles.py]'s `list_roles` function is defined as:

```python
@api.get("", tags=["Roles"])
def list_roles(
    subject: User = Depends(registered_user),
    role_service: RoleService = Depends(),
) -> list[Role]:
    ...
```

By adding the parameter `subject`, which *depends* on the `registered_user` helper function, FastAPI's dependency injection system automatically calls `registered_user`, which in turn depends on the authentication bearer token set during sign in and a corresponding registered user existing in the database. Thus, within the route function, `subject` is bound to the current signed in User. By adding this parameter, you will see the OpenAPI routes automatically become protected.

### Testing Authenticated Routes via OpenAPI

To use authorization protected routes via OpenAPI at `/docs`, you will need to authenticate yourself by adding your signed-in HTTP Bearer Token.

To find your token, which our application persists in `localStorage`:

1. Login to your development application via the front-end
2. Open Developer Tools
3. Go to Application > Storage > Local Storage > localhost:1560
4. Copy the *full* value associated with the `bearerToken` key.

In the OpenAPI user interface found at `/docs`, look for the Green Authorize button and paste in your bearer token.

### Protecting Backend Service Methods

Backend service methods are _the most important place_ to correctly verify authorization. Failing to properly verify authorization here means users will be able to take actions they should not have permission to.

As an example, consider _updating a user's profile details_. The "feature" is a user's profile. The feature-specific rule is _a user can update their own profile_. This verification is implemented in [backend/services/user.py](https://github.com/unc-csxl/csxl.unc.edu/blob/e349bd727f5525a07dc85ed602916470b285e24f/backend/services/user.py#L145). Notice the negation of the rule is specified in the `if` such that if the rule is `True` (the user is the subject), execution carries on into the method. However, if the feature-specific rule does not hold, we then call the [`PermissionService`](backend/services/permission.py)'s `enforce` method, giving it the `subject` user, action string (`user.update`), and resource (`user/{id}`). This method handles the logic for checking whether `subject` has administrative access to carry out this action on the resource. If the `subject` does, this procedure returns nothing. If they do not, it raises a `UserPermissionException` for you. This demonstrates an idiomatic way of verifying the `subject` is authorized.

If your feature-specific rules are more involved than a simple equality check, you should refactor these rules out into a method of its own with a well chosen name. This will help keep your service's methods easier to read and reason through. Additionally, it makes it easier to write unit tests specifically targetting your feature-specific rule logic.

### Frontend Features Requiring a Registered User

To test whether a user is signed in on the frontend Angular application, your Component can
use dependency injection to gain access to the [`ProfileService`](https://github.com/unc-csxl/csxl.unc.edu/blob/main/frontend/src/app/profile/profile.service.ts). The `ProfileService` provides a public member `profile$`, of type `Observable<Profile | undefined>` which your components can subscribe to from their templates. 

As an example of this, consider [`NavigationComponent`](frontend/src/app/navigation):

1. [The `NavigationComponent` projects `profile$` as a public property of its own. This property is initialized in the constructor.](https://github.com/unc-csxl/csxl.unc.edu/blob/e349bd727f5525a07dc85ed602916470b285e24f/frontend/src/app/navigation/navigation.component.ts#L39)
2. [The `NavigationComponent`'s template subscribes to `profile$` with an async pipe and uses `ngIf` to show "Sign In" versus the navigation items shown to a user who is signed in.](https://github.com/unc-csxl/csxl.unc.edu/blob/main/frontend/src/app/navigation/navigation.component.html#L11)

### Frontend Features Requiring Authorization

For feature-specific rule authorization, the alpha version of the CSXL web app that COMP590 Spring 2023 is starting from does not yet have an idiomatic example in the frontend. As a feature developer, you will need to come up with a solution of how your frontend UI will handle feature-specific authorization concerns.

For administrative permission rule authorization, the [PermissionService](frontend/src/app/permission.service.ts) provides helper methods for verifying administrative permissions. For an idiomatic example use case for administrative permission checking, see [`NavigationComponent`](frontend/src/app/navigation)'s `adminPermission$` `Observable<boolean>`:

1. [The permission is initialized in the constructor via `PermissionService`'s `check` method.](https://github.com/unc-csxl/csxl.unc.edu/blob/e349bd727f5525a07dc85ed602916470b285e24f/frontend/src/app/navigation/navigation.component.ts#L41)
2. [The permission is checked in the HTML template using an async pipe.](https://github.com/unc-csxl/csxl.unc.edu/blob/main/frontend/src/app/navigation/navigation.component.html#L13)