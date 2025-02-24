from fastapi import Response
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.types import Scope
import os

from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket

class StaticFileMiddleware(StaticFiles):
    def __init__(self, directory: os.PathLike, index: str = "index.html") -> None:
        self.index = index
        super().__init__(directory=directory, packages=None, html=True, check_dir=True)

    async def __call__(self, scope, receive, send):  # type: ignore
        if scope["type"] == "websocket":
            websocket = WebSocket(scope, receive=receive, send=send)
            await websocket.accept()
        else:
            return await super().__call__(scope, receive, send)

    def lookup_path(self, path: str) -> tuple[str, os.stat_result | None]:
        """Returns the index file when no match is found.

        Args:
            path (str): Resource path.

        Returns:
            tuple[str, os.stat_result | None]: Returns a full path and stat result or None if file not found.
        """
        full_path, stat_result = super().lookup_path(path)

        if stat_result is None:
            full_path, stat_result = super().lookup_path(self.index)
            return (full_path, stat_result)
        else:
            return (full_path, stat_result)

    async def get_response(self, path: str, scope: Scope) -> Response:
        """Override get_response to set cache-control headers for index.html."""

        # Explicitly handle the root path ("/")
        if path in ["", "/", "."]:
            path = self.index  # Treat the root as a request for index.html

        full_path, _ = self.lookup_path(path)

        # If serving index.html, set cache-control header to prevent caching
        if full_path.endswith(self.index):
            response = FileResponse(full_path)
            response.headers["Cache-Control"] = "no-store"
            return response

        # For other static files, let the default caching behavior handle it
        return await super().get_response(path, scope)
