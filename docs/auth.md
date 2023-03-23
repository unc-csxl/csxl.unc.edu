# Authentication and Authorization

This document serves CSXL Developers who need authentication and authorization functionality
in their feature work.

Authentication in `csxl.unc.edu` is integrated with UNC's Single Sign-on (SSO) Shibboleth
service. This allows username, password, and UNC affinity to be handled by UNC ITS and
our application is able to depend upon it. For more information on SSO, see ITS' [official
documentation](https://its.unc.edu/2017/07/24/shibboleth/). For the implementation details
on _how_ authentication works in this application, see [backend/api/authentication.py].

## Authentication

Authentication is verifying _who_ the "subject" accessing a system is. The term "subject" is
chosen in the security world as this is not always a person. A subject may also be an automated 
program accessing a system on behalf of a person, group, or organization. The CSXL application 
is, for now, foremost a user-facing application that serves the people of the computer science 
department at UNC. Thus, a "subject" is a person and user of the application for our concerns.

## Authorization

Authorization is verifying _what_ a subject/user _has permission_ to do within the system.
For example, the leader of a workshop may have permission to edit a workshop's details,
whereas a registered participant of a workshop would not. Additionally, a site administrator
may every permission possible, whereas a standard user does not.

Authorization concerns in the `csxl.unc.edu` application should be thought of as the union
of two different rule sets:

1. Feature and Model-specific Rules

When a feature of the website, in one or more of its models, is related to one or more
users in the system, it is likely these users will need authorization to carry out specific
actions on these models. For example, a user who has registered for a workshop should
be able to unregister themselves if a conflict has arisen. This user should not be able to
unregister other users, though. A workshop leader may be able to modify the details of
_their_ workshop, but not someone else's.

The logic for enforcing feature and model-specific concerns should be specified in 
backend service layer methods. Developers are encouraged to factor this logic out into
reusable helper functions as it is likely many service methods will rely upon the same
logic. All backend service layer methods which have authorization concerns should accept 
a `subject: User` as their first parameter. This represents the user attempting to
carry out the action and whose authorization should be verified.  If your backend service 
layer method determines the subject does not have permission to carry out the operation,
you should raise a `backend.services.permission.UserPermissionError`. Example usage
of this exception:

```python
raise UserPermissionError('workshops.update', f'workshops/{workshop.id}`)
```

For administrative concerns discussed next, the first argument is conventionally specified 
as `service.method` and the second as the target _path_ of the model being operated on,
without the leading `api/`.  In the above example, you could assume `/api/workshops/1` was
the FastAPI path to the model being operated on.

2. Administrative Concerns

The second kind of authorization concern to support are administrative permissions orthogonal
to the feature and model-specific rules. For example, a site administrator needs to be
able to carry out any action on any model. Alternatively, a CSXL Workshop Manager needs
to be able to create new workshops, assign workshop leads, and edit any of them. Administrative
permissions are built into the site via Roles and Permissions.

In the development environment, after resetting the database, sign in as the [Super User](http://localhost:1560/auth/as/root/999999999) and go to the Admin > Roles page. If you open the Staff
role, you will see it has permissions to action `role.*` on resource `*`. The `*` implies 
"matches anything following". Thus, users with the Staff role have permission to carry out
any action in the `services.role` service on all roles. You can see "Merritt Manager" is a user
who has "Staff" role capabilities. If you navigate back to Roles and then to the "Sudoers" role,
you will see why the "Super User" you are signed in as has authorization for all actions on
all resources.



## Common Development Concerns

### Backend Routes Requiring a Registered User

### Testing Authenticated Routes via FastAPI

### Protecting Backend Service Methods

### Frontend Features Requiring a Registered User

### Frontend Features Requiring Authorization