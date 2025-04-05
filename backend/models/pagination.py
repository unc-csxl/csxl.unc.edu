"""Models for paginating results via the API."""

from typing import Generic, TypeVar
from pydantic import BaseModel

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Parameters passed from the client to paginate results."""

    page: int = 0
    page_size: int = 10
    order_by: str = ""
    filter: str = ""


class TicketPaginationParams(PaginationParams):
    """Parameters passed from the client to paginate ticket results."""

    range_start: str = ""
    range_end: str = ""
    student_ids: list[int]
    staff_ids: list[int]


class EventPaginationParams(PaginationParams):
    """Parameters passed from the client to paginate event results."""

    order_by: str = ""
    ascending: str = "true"
    filter: str = ""
    range_start: str = ""
    range_end: str = ""


class Paginated(BaseModel, Generic[T]):
    """Generic class for returning paginating results to the client."""

    items: list[T]
    length: int
    params: PaginationParams | EventPaginationParams | TicketPaginationParams
