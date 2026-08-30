"""API for managing standing room reservation blocks."""

from fastapi import APIRouter, Depends

from ...models import User
from ...models.coworking import NewRoomReservationBlock, RoomReservationBlock
from ...services.coworking import RoomReservationBlockService
from ..authentication import registered_user


api = APIRouter(prefix="/api/coworking/room-reservation-blocks")
openapi_tags = {
    "name": "Coworking",
    "description": "Standing blocks on coworking room reservations.",
}


@api.get("", response_model=list[RoomReservationBlock], tags=["Coworking"])
def get_room_reservation_blocks(
    room_id: str | None = None,
    include_disabled: bool = False,
    subject: User = Depends(registered_user),
    block_svc: RoomReservationBlockService = Depends(),
) -> list[RoomReservationBlock]:
    return block_svc.list_rules(subject, room_id, include_disabled)


@api.get("/{id}", response_model=RoomReservationBlock, tags=["Coworking"])
def get_room_reservation_block(
    id: int,
    subject: User = Depends(registered_user),
    block_svc: RoomReservationBlockService = Depends(),
) -> RoomReservationBlock:
    return block_svc.get(subject, id)


@api.post("", response_model=RoomReservationBlock, tags=["Coworking"])
def create_room_reservation_block(
    block: NewRoomReservationBlock,
    subject: User = Depends(registered_user),
    block_svc: RoomReservationBlockService = Depends(),
) -> RoomReservationBlock:
    return block_svc.create(subject, block)


@api.put("/{id}", response_model=RoomReservationBlock, tags=["Coworking"])
def update_room_reservation_block(
    id: int,
    block: NewRoomReservationBlock,
    subject: User = Depends(registered_user),
    block_svc: RoomReservationBlockService = Depends(),
) -> RoomReservationBlock:
    return block_svc.update(subject, id, block)


@api.delete("/{id}", response_model=None, tags=["Coworking"])
def delete_room_reservation_block(
    id: int,
    subject: User = Depends(registered_user),
    block_svc: RoomReservationBlockService = Depends(),
) -> None:
    block_svc.delete(subject, id)
