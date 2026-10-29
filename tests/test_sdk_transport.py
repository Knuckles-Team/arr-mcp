"""Capabilities through the SDK (CONN-ARR-MCP-SDK-CENTRALIZATION-R001)."""

from __future__ import annotations

import json
import pathlib
import re

import httpx
import pytest

from arr_mcp.api import (
    api_client_bazarr,
    api_client_chaptarr,
    api_client_lidarr,
    api_client_prowlarr,
    api_client_radarr,
    api_client_seerr,
    api_client_sonarr,
)

ID = "CONN-ARR-MCP-SDK-CENTRALIZATION-R001"
ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULES = (
    api_client_bazarr,
    api_client_chaptarr,
    api_client_lidarr,
    api_client_prowlarr,
    api_client_radarr,
    api_client_seerr,
    api_client_sonarr,
)


def _client(module, handler):
    api = module.Api(base_url="http://arr.test:8989", **{_key(module): "secret"})
    api._session = httpx.Client(
        transport=httpx.MockTransport(handler), auth=api._session.auth
    )
    return api


def _key(module) -> str:
    return "api_key" if module in (api_client_bazarr, api_client_seerr) else "token"


@pytest.mark.spec(f"{ID}.1")
@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__.rsplit("_", 1)[1])
def test_clients_are_governed_and_send_the_api_key(module) -> None:
    for path in (ROOT / "arr_mcp").rglob("*.py"):
        assert not re.search(
            r"^\s*(import|from) (requests|urllib3)\b", path.read_text(), re.M
        )
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"ok": True})

    api = _client(module, handler)
    assert isinstance(api._session, httpx.Client)
    assert api.request("GET", "/api/v3/system/status") == {"ok": True}
    assert seen[0].headers["X-Api-Key"] == "secret"


@pytest.mark.spec(f"{ID}.3")
def test_request_shapes_are_unchanged() -> None:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        status = {"/gone": 204, "/bad": 500}.get(request.url.path, 200)
        return httpx.Response(status, json=[1, 2])

    api = _client(api_client_sonarr, handler)
    assert api.request("POST", "/api/v3/series", params={"a": 1}, data={"x": 2}) == {
        "result": [1, 2]
    }
    assert str(seen[0].url) == "http://arr.test:8989/api/v3/series?a=1"
    assert json.loads(seen[0].content) == {"x": 2}
    assert api.request("DELETE", "/gone") == {"status": "success"}
    with pytest.raises(RuntimeError, match=r"API error: HTTP 500"):
        api.request("GET", "/bad")
    with pytest.raises(ValueError):
        api.request("GET", "https://evil.example/api")


@pytest.mark.spec(f"{ID}.4")
def test_dependencies_come_from_the_sdk() -> None:
    text = (ROOT / "pyproject.toml").read_text()
    assert not re.search(r'"(requests|urllib3)\s*[>=<~!]', text)
    floors = re.findall(r"scion-sdk\[mcp\]>=(\d+)\.(\d+)\.(\d+)", text)
    assert floors and all(tuple(map(int, f)) >= (0, 3, 11) for f in floors)
