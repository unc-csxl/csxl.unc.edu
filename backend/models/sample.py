"""API validation models for the sample endpoint"""

from pydantic import BaseModel


class GetSampleItemsResponse_Item(BaseModel):
    id: int
    name: str
    price: float


class GetSampleItemsResponse(BaseModel):
    items: list[GetSampleItemsResponse_Item]


class GetSampleItemResponse(BaseModel):
    id: int
    name: str
    price: float


class CreateSampleItemRequest(BaseModel):
    name: str
    starting_price: float


class CreateSampleItemResponse(BaseModel):
    id: int
