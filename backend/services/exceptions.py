"""Common exceptions found in the service layer."""

class ResourceNotFoundException(Exception):
    ...

class UserPermissionException(Exception):
    """UserPermissionException is raised when a user attempts to perform an action they are not authorized to perform."""

    def __init__(self, action: str, resource: str):
        super().__init__(
            f'Not authorized to perform `{action}` on `{resource}`')

