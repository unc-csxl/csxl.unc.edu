class OperatingHoursCannotOverlapException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class OperatingHoursCannotDeleteException(Exception):
    """Only future operating hours can be deleted."""
