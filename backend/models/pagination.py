from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 0
    page_size: int = 10
    order_by: str = ""
    filter: str = ""


class Paginated(GenericModel, Generic[T]):
    """Generic, abstract class for paginating models."""
    items: list[T]
    length: int
    params: PaginationParams
