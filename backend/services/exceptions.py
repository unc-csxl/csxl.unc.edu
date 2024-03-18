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
        super().__init__(f"Not authorized to perform `{action}` on `{resource}`")


class EventRegistrationException(Exception):
    """EventRegistrationException is raised when a user attempts to register and cannot (i.e., when the event is full)."""

    def __init__(self, event_id: int):
        super().__init__(f"Unable to register user for the event with id: {event_id}")
