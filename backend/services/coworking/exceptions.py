class OperatingHoursCannotOverlapException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RoomReservationBlockConflictException(Exception):
    """Raised when a block or reservation overlaps an active room block."""

    pass
