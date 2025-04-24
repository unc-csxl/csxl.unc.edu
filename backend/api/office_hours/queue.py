"""
Implements the office hours queue using websocket functionality.
"""

from typing import Optional
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from enum import Enum
from pydantic import BaseModel
from ..authentication import registered_user_from_websocket
from ...services.office_hours.office_hours import OfficeHoursService
from ...services.office_hours.ticket import OfficeHourTicketService
from ...services.user import UserService
from ...models.user import User
from ...models.office_hours.ticket import (
    NewOfficeHoursTicket,
    OfficeHoursTicketClosePayload,
)

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/ws/office-hours")


class UserWebSocketConnection:
    """Stores dat about the user and the web socket they are connected to."""

    user: User
    socket: WebSocket

    def __init__(self, user: User, socket: WebSocket):
        self.user = user
        self.socket = socket


# Define the websocket connection manager for the queue feature.
class QueueConnectionManager:
    """
    Manages all active connections to the office hours web socket and
    coordinates broadcasting updates to office hours queues to active
    member connections.
    """

    def __init__(self):
        # This internal field stores all of the active connections,
        # indexed by office hours ID (enabling easy and efficient
        # lookups and updates based on the office hours event).
        self._active_student_connections: dict[int, list[UserWebSocketConnection]] = {}
        self._active_staff_connections: dict[int, list[UserWebSocketConnection]] = {}

    async def queue_connect(
        self, office_hours_id: int, subject: User, websocket: WebSocket
    ):
        """
        Creates a new connection to the web socket by a staff member given
        an office hours ID taken as the websocket's query parameter.
        """
        # Wait for the new connection to be accepted
        await websocket.accept()
        # Create the new connection object
        connection = UserWebSocketConnection(user=subject, socket=websocket)
        # Register the new connection in the map of active connections.
        self._active_staff_connections[office_hours_id] = (
            self._active_staff_connections.get(office_hours_id, []) + [connection]
        )

    async def get_help_connect(
        self, office_hours_id: int, subject: User, websocket: WebSocket
    ):
        """
        Creates a new connection to the web socket by a student given
        an office hours ID taken as the websocket's query parameter.
        """
        # Wait for the new connection to be accepted
        await websocket.accept()
        # Create the new connection object
        connection = UserWebSocketConnection(user=subject, socket=websocket)
        # Register the new connection in the map of active connections.
        self._active_student_connections[office_hours_id] = (
            self._active_student_connections.get(office_hours_id, []) + [connection]
        )

    def queue_disconnect(self, office_hours_id: int, websocket: WebSocket):
        """
        Removes a staff's web socket connection from the list of active connections.
        """
        # Remove the web socket based on the providd office hours ID
        self._active_staff_connections[office_hours_id] = [
            connection
            for connection in self._active_staff_connections.get(office_hours_id, [])
            if connection.socket != websocket
        ]

    def get_help_disconnect(self, office_hours_id: int, websocket: WebSocket):
        """
        Removes a student's web socket connection from the list of active connections.
        """
        # Remove the web socket based on the providd office hours ID
        self._active_student_connections[office_hours_id] = [
            connection
            for connection in self._active_student_connections.get(office_hours_id, [])
            if connection.socket != websocket
        ]

    async def broadcast_queue_changes(
        self, office_hours_id: int, oh_event_svc: OfficeHoursService
    ):
        """
        Broadcasts changes in the queue for a given office hours ID to all active
        connections for that office hours event.
        """
        # Send new queue to all staff
        for connection in self._active_staff_connections.get(office_hours_id, []):
            queue = oh_event_svc.get_office_hour_queue(connection.user, office_hours_id)
            await connection.socket.send_json(queue.model_dump_json())

        # Send new queue data to all students
        for connection in self._active_student_connections.get(office_hours_id, []):
            overview = oh_event_svc.get_office_hour_get_help_overview(
                connection.user, office_hours_id
            )
            await connection.socket.send_json(overview.model_dump_json())


# Create the queue connection manager object
manager = QueueConnectionManager()

# Define the queue websockets


class QueueWebSocketAction(Enum):
    """Define the specific actions that staff can take."""

    CALL = "CALL"
    CLOSE = "CLOSE"
    CANCEL = "CANCEL"


class QueueWebSocketData(BaseModel):
    """Model to represent the data sent to the queue websocket."""

    action: QueueWebSocketAction
    close_payload: Optional[OfficeHoursTicketClosePayload] = {}
    id: int


@api.websocket("/{office_hours_id}/queue")
async def queue_websocket(
    websocket: WebSocket,
    office_hours_id: int,
    oh_ticket_svc: OfficeHourTicketService = Depends(),
    oh_event_svc: OfficeHoursService = Depends(),
    user_svc: UserService = Depends(),
):
    # Try to load the current user.
    token = websocket.query_params.get("token")
    subject = registered_user_from_websocket(token, user_svc)
    # Connect the new websocket connection to the manager.
    await manager.queue_connect(office_hours_id, subject, websocket)
    # Send the initial queue data.
    queue = oh_event_svc.get_office_hour_queue(subject, office_hours_id)
    await websocket.send_json(queue.model_dump_json())
    try:
        # Await receiving new data.
        while True:
            # When new data is sent to the websocket, read it as JSON
            # and cast to the correct data model with Pydantic.
            json_data = await websocket.receive_json()
            data = QueueWebSocketData.model_validate(json_data)
            # Depending on the type of request, call the respective
            # manager actions.
            if data.action == QueueWebSocketAction.CALL:
                # Talls a ticket
                oh_ticket_svc.call_ticket(subject, data.id)
                # Broadcast the changes using the mamanger.
                await manager.broadcast_queue_changes(office_hours_id, oh_event_svc)
            elif data.action == QueueWebSocketAction.CLOSE:
                # Close a ticket
                oh_ticket_svc.close_ticket(subject, data.id, data.close_payload)
                # Broadcast the changes using the mamanger.
                await manager.broadcast_queue_changes(office_hours_id, oh_event_svc)
            elif data.action == QueueWebSocketAction.CANCEL:
                # Close a ticket
                oh_ticket_svc.cancel_ticket(subject, data.id)
                # Broadcast the changes using the mamanger.
                await manager.broadcast_queue_changes(office_hours_id, oh_event_svc)
    except WebSocketDisconnect:
        # When the websocket disconnects, remove the connection
        # using the manager.
        manager.get_help_disconnect(office_hours_id, websocket)


class GetHelpWebSocketAction(Enum):
    """Define the specific actions that students can take."""

    CREATE = "CREATE"
    CANCEL = "CANCEL"


class GetHelpWebSocketData(BaseModel):
    """Model to represent the data sent to the get help websocket."""

    action: GetHelpWebSocketAction
    id: int | None
    new_ticket: NewOfficeHoursTicket | None


@api.websocket("/{office_hours_id}/get-help")
async def get_help_websocket(
    websocket: WebSocket,
    office_hours_id: int,
    oh_ticket_svc: OfficeHourTicketService = Depends(),
    oh_event_svc: OfficeHoursService = Depends(),
    user_svc: UserService = Depends(),
):
    # Try to load the current user.
    token = websocket.query_params.get("token")
    subject = registered_user_from_websocket(token, user_svc)
    # Connect the new websocket connection to the manager.
    await manager.get_help_connect(office_hours_id, subject, websocket)
    # Send the initial data.
    overview = oh_event_svc.get_office_hour_get_help_overview(subject, office_hours_id)
    await websocket.send_json(overview.model_dump_json())

    try:
        # Await receiving new data.
        while True:
            # When new data is sent to the websocket, read it as JSON
            # and cast to the correct data model with Pydantic.
            json_data = await websocket.receive_json()
            data = GetHelpWebSocketData.model_validate(json_data)
            # Depending on the type of request, call the respective
            # manager actions.
            if data.action == GetHelpWebSocketAction.CREATE and data.new_ticket:
                # Create a new ticket
                oh_ticket_svc.create_ticket(subject, data.new_ticket)
                # Broadcast the changes using the mamanger.
                await manager.broadcast_queue_changes(office_hours_id, oh_event_svc)
            elif data.action == GetHelpWebSocketAction.CANCEL:
                # Close a ticket
                oh_ticket_svc.cancel_ticket(subject, data.id)
                # Broadcast the changes using the mamanger.
                await manager.broadcast_queue_changes(office_hours_id, oh_event_svc)
    except WebSocketDisconnect:
        # When the websocket disconnects, remove the connection
        # using the manager.
        manager.get_help_disconnect(office_hours_id, websocket)
