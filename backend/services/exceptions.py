"""
This file contains exceptions found in the service layer.

These custom exceptions can then be handled peoperly
at the API level.
"""

class ResourceNotFoundException(Exception):
    """ResourceNotFoundException is raised when a user attempts to access a resource that does not exist."""
    ...

class UserPermissionException(Exception):
    """UserPermissionException is raised when a user attempts to perform an action they are not authorized to perform."""

    def __init__(self, action: str, resource: str):
        super().__init__(
            f'Not authorized to perform `{action}` on `{resource}`')

class EventNotFoundException(Exception):
    """EventNotFoundException is raised when trying to access an event that does not exist."""

    def __init__(self, id: str):
        super().__init__(
            f'No event found with matching ID: {id}')
        
class OrganizationNotFoundException(Exception):
    """OrganizationNotFoundException is raised when trying to access an organization that does not exist."""

    def __init__(self, id: str):
        super().__init__(
            f'No organization found matching slug/id: {id}')
