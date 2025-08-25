"""Sample API to show off OpenAPI integration"""

from fastapi import APIRouter
from ..models.sample import (
    GetSampleItemsResponse,
    GetSampleItemsResponse_Item,
    GetSampleItemResponse,
    CreateSampleItemRequest,
    CreateSampleItemResponse,
)

api = APIRouter(prefix="/api/sample")
tag = "Sample Endpoint"
openapi_tags = {
    "name": tag,
    "description": "Sample API endpoint for showing off OpenAPI integration.",
}


@api.get("", tags=[tag])
def get_all() -> GetSampleItemsResponse:
    return GetSampleItemsResponse(
        items=[
            GetSampleItemsResponse_Item(id=1, name="One", price=99.99),
            GetSampleItemsResponse_Item(id=2, name="Two", price=199.99),
        ]
    )


@api.get("/{id}", tags=[tag])
def get(id: int) -> GetSampleItemResponse:
    return GetSampleItemResponse(id=1, name="One", price=99.99)


@api.post("", tags=[tag])
def create(_: CreateSampleItemRequest) -> CreateSampleItemResponse:
    return CreateSampleItemResponse(id=1)
