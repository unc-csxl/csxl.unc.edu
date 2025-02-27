from fastapi import APIRouter
from starlette.types import Scope, Receive, Send
from fastapi.websockets import WebSocket, WebSocketDisconnect
from starlette.middleware.base import BaseHTTPMiddleware


class WebSocketMiddleware(BaseHTTPMiddleware):

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # type: ignore
        if scope["type"] == "websocket":
            websocket = WebSocket(scope, receive=receive, send=send)
            await websocket.accept()
        else:
            return await super().__call__(scope, receive, send)


api = APIRouter(prefix="/ws")


@api.websocket("/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_json()
            await websocket.send_json({"type": "echo", "data": message})
    except WebSocketDisconnect:
        ...
