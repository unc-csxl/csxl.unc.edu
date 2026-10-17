"""Protect production SPA delivery when upgrading Starlette."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..api.static_files import StaticFileMiddleware


@pytest.fixture
def client(tmp_path):
    assets = tmp_path / "static"
    assets.mkdir()
    (assets / "index.html").write_text("<html>CSXL application</html>")
    (assets / "main.hash.js").write_text("console.log('CSXL');")
    (tmp_path / "outside.txt").write_text("outside the static root")
    app = FastAPI()
    app.mount("/", StaticFileMiddleware(directory=assets))
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize("path", ["/", "/index.html", "/coworking/reservation"])
def test_spa_entry_and_deep_links_are_not_cached(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert response.text == "<html>CSXL application</html>"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["content-type"].startswith("text/html")


def test_fingerprinted_assets_support_conditional_requests(client):
    response = client.get("/main.hash.js")
    assert response.status_code == 200
    assert response.text == "console.log('CSXL');"
    assert "no-store" not in response.headers.get("cache-control", "")
    cached = client.get(
        "/main.hash.js", headers={"If-None-Match": response.headers["etag"]}
    )
    assert cached.status_code == 304
    assert cached.content == b""


def test_static_file_ranges_still_work(client):
    response = client.get("/main.hash.js", headers={"Range": "bytes=0-6"})
    assert response.status_code == 206
    assert response.text == "console"


def test_encoded_traversal_cannot_read_outside_static_root(client):
    response = client.get("/%2e%2e/outside.txt")
    assert "outside the static root" not in response.text
