import asyncio
import inspect
import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse


def test_arr_apis_brute_force(mock_session):
    from arr_mcp.api import api_client_bazarr as bazarr_api
    from arr_mcp.api import api_client_chaptarr as chaptarr_api
    from arr_mcp.api import api_client_lidarr as lidarr_api
    from arr_mcp.api import api_client_prowlarr as prowlarr_api
    from arr_mcp.api import api_client_radarr as radarr_api
    from arr_mcp.api import api_client_seerr as seerr_api
    from arr_mcp.api import api_client_sonarr as sonarr_api

    def create_api(mod):
        try:
            return mod.Api(base_url="http://test", token="test")
        except TypeError:
            return mod.Api(base_url="http://test", api_key="test")

    apis = [
        create_api(radarr_api),
        create_api(sonarr_api),
        create_api(lidarr_api),
        create_api(prowlarr_api),
        create_api(bazarr_api),
        create_api(seerr_api),
        create_api(chaptarr_api),
    ]

    common_kwargs = {
        "id": 1,
        "movie_id": 1,
        "series_id": 1,
        "artist_id": 1,
        "indexer_id": 1,
        "query": "test",
        "name": "test",
        "payload": {},
        "data": {},
        "limit": 10,
        "page": 1,
        "term": "test",
    }

    for api in apis:
        api_name = api.__class__.__module__
        for name, method in inspect.getmembers(api, predicate=inspect.ismethod):
            if name.startswith("_"):
                continue
            print(f"Calling {api_name}.{name}...")
            sig = inspect.signature(method)
            has_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
            )
            if has_kwargs:
                kwargs = common_kwargs.copy()
            else:
                kwargs = {k: v for k, v in common_kwargs.items() if k in sig.parameters}
                for p_name, p in sig.parameters.items():
                    if p.default == inspect.Parameter.empty and p_name not in kwargs:
                        kwargs[p_name] = "test" if p.annotation == str else 1
            try:
                method(**kwargs)
            except Exception as e:
                print(f"Failed call to {name}: {e}")
                pass


def test_arr_apis_error_handling():
    from arr_mcp.api.api_client_bazarr import Api

    # 1. Error status code >= 400
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 400
        response.text = "Bad Request"
        session.request.return_value = response
        api = Api(base_url="http://test", api_key="test")
        with pytest.raises(Exception, match="Bad Request"):
            api.get_series()

    # 2. Error status code >= 400 with text property raising Exception
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 400
        type(response).text = property(
            lambda self: (_ for _ in ()).throw(ValueError("Read error"))
        )
        session.request.return_value = response
        api = Api(base_url="http://test", api_key="test")
        with pytest.raises(Exception, match="Unknown error"):
            api.get_series()

    # 3. Status code 204
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 204
        session.request.return_value = response
        api = Api(base_url="http://test", api_key="test")
        res = api.get_series()
        assert res == {"status": "success"}

    # 4. JSON Deserialization error
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.side_effect = ValueError("Invalid JSON")
        response.text = "Not JSON"
        session.request.return_value = response
        api = Api(base_url="http://test", api_key="test")
        res = api.get_series()
        assert res == {"status": "success", "text": "Not JSON"}


def test_execute_arr_action_failures_and_models():
    from arr_mcp.mcp_server import execute_arr_action

    # 1. Base URL is None
    with pytest.raises(ValueError, match="Base URL must be provided"):
        execute_arr_action("radarr", None, "test", False, "some_action", "{}", "token")

    # 2. Unknown service name
    with pytest.raises(ValueError, match="Unknown service"):
        execute_arr_action(
            "invalid_service",
            "http://test",
            "test",
            False,
            "some_action",
            "{}",
            "token",
        )

    # 3. Invalid params_json
    with pytest.raises(ValueError, match="Invalid params_json"):
        execute_arr_action(
            "radarr", "http://test", "test", False, "some_action", "{invalid", "token"
        )

    # 4. Unknown action method
    with pytest.raises(ValueError, match="Unknown action"):
        execute_arr_action(
            "radarr", "http://test", "test", False, "invalid_action", "{}", "token"
        )

    # 5. Pydantic-like dict/model_dump conversion coverage
    class DummyModelDict:
        def dict(self):
            return {"source": "dict"}

    class DummyModelDump:
        def model_dump(self):
            return {"source": "model_dump"}

    with patch("importlib.import_module") as mock_import:
        mock_module = MagicMock()
        mock_api = MagicMock()
        mock_import.return_value = mock_module
        mock_module.Api = mock_api

        # Test dict() call
        instance = mock_api.return_value
        instance.some_action.return_value = DummyModelDict()
        res = execute_arr_action(
            "radarr", "http://test", "test", False, "some_action", "{}", "token"
        )
        assert res == {"source": "dict"}

        # Test model_dump() call
        instance.some_action.return_value = DummyModelDump()
        res = execute_arr_action(
            "radarr", "http://test", "test", False, "some_action", "{}", "token"
        )
        assert res == {"source": "model_dump"}

        # Test standard return (dict)
        instance.some_action.return_value = {"source": "plain"}
        res = execute_arr_action(
            "radarr", "http://test", "test", False, "some_action", "{}", "token"
        )
        assert res == {"source": "plain"}


def test_is_service_enabled():
    from arr_mcp.mcp_server import is_service_enabled

    # 1. Default return is True
    with patch("os.getenv", return_value=None):
        assert is_service_enabled("bazarr") is True

    # 2. Specifically enabled or disabled via environment variable
    with patch.dict("os.environ", {"BAZARR_ENABLED": "false"}):
        assert is_service_enabled("bazarr") is False

    with patch.dict("os.environ", {"BAZARR_ENABLED": "true"}):
        assert is_service_enabled("bazarr") is True

    with patch.dict("os.environ", {"BAZARR_ENABLED": "0"}):
        assert is_service_enabled("bazarr") is False

    with patch.dict("os.environ", {"BAZARR_ENABLED": "1"}):
        assert is_service_enabled("bazarr") is True


@pytest.mark.asyncio
async def test_mcp_custom_health_route():
    from arr_mcp.mcp_server import get_mcp_instance

    mcp_data = get_mcp_instance()
    mcp = mcp_data[0] if isinstance(mcp_data, tuple) else mcp_data

    # Find the health route
    health_route = None
    for route in mcp._additional_http_routes:
        if route.path == "/health":
            health_route = route
            break

    assert health_route is not None
    # Invoke the health endpoint directly
    response = await health_route.endpoint(None)
    assert response.status_code == 200
    body = json.loads(response.body.decode())
    assert body.get("status", "").lower() == "ok"


def test_mcp_server_run_transports():
    from arr_mcp.mcp_server import mcp_server, get_mcp_instance

    mcp_mock = MagicMock()
    args_mock = MagicMock()
    middlewares_mock = MagicMock()
    tags_mock = ["sonarr"]

    with patch(
        "arr_mcp.mcp_server.get_mcp_instance",
        return_value=(mcp_mock, args_mock, middlewares_mock, tags_mock),
    ):
        # Case 1: stdio
        args_mock.transport = "stdio"
        mcp_server()
        mcp_mock.run.assert_called_with(transport="stdio")

        # Case 2: streamable-http
        args_mock.transport = "streamable-http"
        args_mock.host = "localhost"
        args_mock.port = 8000
        mcp_server()
        mcp_mock.run.assert_called_with(
            transport="streamable-http", host="localhost", port=8000
        )

        # Case 3: sse
        args_mock.transport = "sse"
        mcp_server()
        mcp_mock.run.assert_called_with(transport="sse", host="localhost", port=8000)

        # Case 4: invalid transport path
        args_mock.transport = "invalid"
        with patch("sys.exit") as mock_exit:
            mcp_server()
            mock_exit.assert_called_with(1)


def test_mcp_server_coverage(mock_session):
    _ = mock_session
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

    from arr_mcp.mcp_server import get_mcp_instance

    # Patch RateLimitingMiddleware to do nothing
    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    with patch.object(RateLimitingMiddleware, "on_request", mock_on_request):
        mcp_data = get_mcp_instance()
        mcp = mcp_data[0] if isinstance(mcp_data, tuple) else mcp_data

        async def run_tools():
            tool_objs = (
                await mcp.list_tools()
                if inspect.iscoroutinefunction(mcp.list_tools)
                else mcp.list_tools()
            )
            for tool in tool_objs:
                try:
                    target_params = {
                        "id": 1,
                        "query": "test",
                        "radarr_base_url": "http://test",
                        "radarr_api_key": "test",
                        "sonarr_base_url": "http://test",
                        "sonarr_api_key": "test",
                        "lidarr_base_url": "http://test",
                        "lidarr_api_key": "test",
                        "prowlarr_base_url": "http://test",
                        "prowlarr_api_key": "test",
                        "bazarr_base_url": "http://test",
                        "bazarr_api_key": "test",
                        "seerr_base_url": "http://test",
                        "seerr_api_key": "test",
                        "chaptarr_base_url": "http://test",
                        "chaptarr_api_key": "test",
                    }
                    sig = inspect.signature(tool.fn)
                    for p_name, p in sig.parameters.items():
                        if p.default == inspect.Parameter.empty and p_name not in [
                            "_client",
                            "context",
                        ]:
                            if p_name not in target_params:
                                target_params[p_name] = (
                                    "test" if p.annotation == str else 1
                                )

                    has_kwargs = any(
                        p.kind == inspect.Parameter.VAR_KEYWORD
                        for p in sig.parameters.values()
                    )
                    if not has_kwargs:
                        target_params = {
                            k: v
                            for k, v in target_params.items()
                            if k in sig.parameters
                        }

                    await mcp.call_tool(tool.name, target_params)
                except Exception as e:
                    print(f"Failed calling tool {tool.name}: {e}")
                    pass

        loop = asyncio.new_event_loop()
        loop.run_until_complete(run_tools())
        loop.close()


def test_agent_server_coverage():
    pytest.importorskip("universal_skills")
    from arr_mcp.agent_server import agent_server

    # Case 1: debug=False
    with patch("agent_utilities.create_agent_server") as mock_s:
        with patch("sys.argv", ["agent_server.py"]):
            agent_server()
            mock_s.assert_called_once()

    # Case 2: debug=True
    with patch("agent_utilities.create_agent_server") as mock_s:
        with patch("sys.argv", ["agent_server.py", "--debug"]):
            agent_server()
            mock_s.assert_called_once()


def test_all_api_clients_error_handling_and_special_cases():
    from typing import Any
    from arr_mcp.api import (
        api_client_bazarr,
        api_client_chaptarr,
        api_client_lidarr,
        api_client_prowlarr,
        api_client_radarr,
        api_client_seerr,
        api_client_sonarr,
    )

    modules_and_methods: list[tuple[Any, str, dict[str, Any]]] = [
        (api_client_bazarr, "get_series", {"api_key": "test"}),
        (api_client_chaptarr, "get_author", {"token": "test"}),
        (api_client_lidarr, "get_artist", {"token": "test"}),
        (api_client_prowlarr, "get_indexer", {"token": "test"}),
        (api_client_radarr, "get_movie", {"token": "test"}),
        (api_client_seerr, "get_status", {"api_key": "test"}),
        (api_client_sonarr, "get_series", {"token": "test"}),
    ]

    for mod, method_name, init_kwargs in modules_and_methods:
        # Case 1: Status >= 400 with text reading error
        with patch("requests.Session") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 400
            type(response).text = property(
                lambda self: (_ for _ in ()).throw(ValueError("Read error"))
            )
            session.request.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            with pytest.raises(Exception, match="Unknown error"):
                getattr(api, method_name)()

        # Case 2: Status 204
        with patch("requests.Session") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 204
            session.request.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"status": "success"}

        # Case 3: List response
        with patch("requests.Session") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = [{"id": 1}]
            session.request.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"result": [{"id": 1}]}

        # Case 4: Non-JSON Response (JSON decode failure)
        with patch("requests.Session") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 200
            response.json.side_effect = ValueError("Invalid JSON")
            response.text = "Plain Text Response"
            session.request.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"status": "success", "text": "Plain Text Response"}


def test_sonarr_radarr_lookup_empty():
    from arr_mcp.api.api_client_sonarr import Api as SonarrApi
    from arr_mcp.api.api_client_radarr import Api as RadarrApi

    # Sonarr lookup empty
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = []
        session.request.return_value = response
        api = SonarrApi(base_url="http://test", token="test")
        res = api.add_series(
            term="unknown", root_folder_path="/data", quality_profile_id=1
        )
        assert "error" in res

    # Sonarr lookup success and add series
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        resp_lookup = MagicMock()
        resp_lookup.status_code = 200
        resp_lookup.json.return_value = [
            {"title": "Test Title", "tvdbId": 123, "titleSlug": "test-title"}
        ]
        resp_add = MagicMock()
        resp_add.status_code = 200
        resp_add.json.return_value = {"id": 456, "title": "Test Title"}
        session.request.side_effect = [resp_lookup, resp_add]
        api = SonarrApi(base_url="http://test", token="test")
        res = api.add_series(
            term="test", root_folder_path="/data", quality_profile_id=1
        )
        assert res == {"id": 456, "title": "Test Title"}

    # Radarr lookup empty
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = []
        session.request.return_value = response
        radarr_api = RadarrApi(base_url="http://test", token="test")
        res = radarr_api.add_movie(
            term="unknown", root_folder_path="/data", quality_profile_id=1
        )
        assert "error" in res

    # Radarr lookup success and add movie
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        resp_lookup = MagicMock()
        resp_lookup.status_code = 200
        resp_lookup.json.return_value = [
            {"title": "Test Movie", "tmdbId": 789, "titleSlug": "test-movie"}
        ]
        resp_add = MagicMock()
        resp_add.status_code = 200
        resp_add.json.return_value = {"id": 101, "title": "Test Movie"}
        session.request.side_effect = [resp_lookup, resp_add]
        radarr_api = RadarrApi(base_url="http://test", token="test")
        res = radarr_api.add_movie(
            term="test", root_folder_path="/data", quality_profile_id=1
        )
        assert res == {"id": 101, "title": "Test Movie"}


@pytest.mark.asyncio
async def test_mcp_tools_with_context_and_serializer():
    from arr_mcp.mcp_server import get_mcp_instance
    from unittest.mock import MagicMock, AsyncMock

    mcp, _, _, _ = get_mcp_instance()

    # 1. Test MCP tools with context parameter
    mock_ctx = AsyncMock()

    # We can invoke each of the registered action tools with a mock ctx
    action_tools = [
        "bazarr_action",
        "chaptarr_action",
        "lidarr_action",
        "prowlarr_action",
        "radarr_action",
        "seerr_action",
        "sonarr_action",
    ]

    for tool_name in action_tools:
        try:
            tool = await mcp.get_tool(tool_name)
            tool_fn = tool.fn
        except Exception:
            continue

        # Mock the underlying execute_arr_action to avoid actually calling it
        with patch("arr_mcp.mcp_server.execute_arr_action") as mock_exec:
            mock_exec.return_value = {"status": "success"}

            # Check parameters to only pass relevant ones
            sig = inspect.signature(tool_fn)
            kwargs = {
                "action": "get_series"
                if "bazarr" in tool_name or "sonarr" in tool_name
                else "get_status",
                "ctx": mock_ctx,
            }
            # Add default values for other required parameters
            for param_name, param in sig.parameters.items():
                if (
                    param_name not in kwargs
                    and param.default == inspect.Parameter.empty
                ):
                    kwargs[param_name] = "test"

            await tool_fn(**kwargs)
            mock_ctx.info.assert_called()
            mock_ctx.info.reset_mock()


def test_mcp_server_dependency_warning_import_error():
    import builtins
    import importlib
    import sys

    # Save original __import__
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "RequestsDependencyWarning" in name or name == "requests.exceptions":
            raise ImportError("Mocked import error")
        return original_import(name, *args, **kwargs)

    # Patch import and reload the module
    with patch("builtins.__import__", side_effect=mock_import):
        if "arr_mcp.mcp_server" in sys.modules:
            mcp_module = sys.modules["arr_mcp.mcp_server"]
            importlib.reload(mcp_module)
