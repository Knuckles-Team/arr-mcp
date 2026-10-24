import inspect
from unittest.mock import MagicMock, patch

import pytest


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
                        kwargs[p_name] = "test" if p.annotation is str else 1
            try:
                method(**kwargs)
            except Exception as e:
                print(f"Operation failed: {type(e).__name__}")
                pass


def test_arr_apis_error_handling():
    from arr_mcp.api.api_client_bazarr import Api

    # 1. Error status code >= 400
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 400
        response.text = "Bad Request"
        session.send.return_value = response
        api = Api(base_url="http://test", api_key="test")
        with pytest.raises(RuntimeError, match="API error: HTTP 400"):
            api.get_series()

    # 2. Error status code >= 400 with text property raising Exception
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 400
        type(response).text = property(
            lambda self: (_ for _ in ()).throw(ValueError("Read error"))
        )
        session.send.return_value = response
        api = Api(base_url="http://test", api_key="test")
        with pytest.raises(RuntimeError, match="API error: HTTP 400"):
            api.get_series()

    # 3. Status code 204
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 204
        session.send.return_value = response
        api = Api(base_url="http://test", api_key="test")
        res = api.get_series()
        assert res == {"status": "success"}

    # 4. JSON Deserialization error
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.side_effect = ValueError("Invalid JSON")
        response.text = "Not JSON"
        session.send.return_value = response
        api = Api(base_url="http://test", api_key="test")
        res = api.get_series()
        assert res == {"status": "success", "text": "Not JSON"}


def test_execute_arr_action_failures_and_models():
    from arr_mcp.mcp_server import execute_arr_action

    # 1. Base URL is None
    with pytest.raises(ValueError, match="Base URL must be provided"):
        execute_arr_action("radarr", None, "test", "some_action", "{}", "token")

    # 2. Unknown service name
    with pytest.raises(ValueError, match="Unknown service"):
        execute_arr_action(
            "invalid_service",
            "http://test",
            "test",
            "some_action",
            "{}",
            "token",
        )

    # 3. Invalid params_json
    with pytest.raises(ValueError, match="params_json must be valid JSON"):
        execute_arr_action(
            "radarr", "http://test", "test", "some_action", "{invalid", "token"
        )

    # 4. Unknown action method
    with pytest.raises(ValueError, match="Unknown action"):
        execute_arr_action(
            "radarr", "http://test", "test", "invalid_action", "{}", "token"
        )

    # 5. Current Pydantic model_dump conversion coverage
    class DummyModelDump:
        def model_dump(self):
            return {"source": "model_dump"}

    with patch("importlib.import_module") as mock_import:
        mock_module = MagicMock()
        mock_api = MagicMock()
        mock_import.return_value = mock_module
        mock_module.Api = mock_api

        instance = mock_api.return_value
        instance.some_action.return_value = DummyModelDump()
        res = execute_arr_action(
            "radarr", "http://test", "test", "some_action", "{}", "token"
        )
        assert res == {"source": "model_dump"}

        # Test standard return (dict)
        instance.some_action.return_value = {"source": "plain"}
        res = execute_arr_action(
            "radarr", "http://test", "test", "some_action", "{}", "token"
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
        with patch("httpx.Client") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 400
            type(response).text = property(
                lambda self: (_ for _ in ()).throw(ValueError("Read error"))
            )
            session.send.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            with pytest.raises(RuntimeError, match="API error: HTTP 400"):
                getattr(api, method_name)()

        # Case 2: Status 204
        with patch("httpx.Client") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 204
            session.send.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"status": "success"}

        # Case 3: List response
        with patch("httpx.Client") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = [{"id": 1}]
            session.send.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"result": [{"id": 1}]}

        # Case 4: Non-JSON Response (JSON decode failure)
        with patch("httpx.Client") as mock_sess:
            session = mock_sess.return_value
            response = MagicMock()
            response.status_code = 200
            response.json.side_effect = ValueError("Invalid JSON")
            response.text = "Plain Text Response"
            session.send.return_value = response
            api = mod.Api(base_url="http://test", **init_kwargs)
            res = getattr(api, method_name)()
            assert res == {"status": "success", "text": "Plain Text Response"}


def test_sonarr_radarr_lookup_empty():
    from arr_mcp.api.api_client_radarr import Api as RadarrApi
    from arr_mcp.api.api_client_sonarr import Api as SonarrApi

    # Sonarr lookup empty
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = []
        session.send.return_value = response
        api = SonarrApi(base_url="http://test", token="test")
        res = api.add_series(
            term="unknown", root_folder_path="/data", quality_profile_id=1
        )
        assert "error" in res

    # Sonarr lookup success and add series
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        resp_lookup = MagicMock()
        resp_lookup.status_code = 200
        resp_lookup.json.return_value = [
            {"title": "Test Title", "tvdbId": 123, "titleSlug": "test-title"}
        ]
        resp_add = MagicMock()
        resp_add.status_code = 200
        resp_add.json.return_value = {"id": 456, "title": "Test Title"}
        session.send.side_effect = [resp_lookup, resp_add]
        api = SonarrApi(base_url="http://test", token="test")
        res = api.add_series(
            term="test", root_folder_path="/data", quality_profile_id=1
        )
        assert res == {"id": 456, "title": "Test Title"}

    # Radarr lookup empty
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = []
        session.send.return_value = response
        radarr_api = RadarrApi(base_url="http://test", token="test")
        res = radarr_api.add_movie(
            term="unknown", root_folder_path="/data", quality_profile_id=1
        )
        assert "error" in res

    # Radarr lookup success and add movie
    with patch("httpx.Client") as mock_sess:
        session = mock_sess.return_value
        resp_lookup = MagicMock()
        resp_lookup.status_code = 200
        resp_lookup.json.return_value = [
            {"title": "Test Movie", "tmdbId": 789, "titleSlug": "test-movie"}
        ]
        resp_add = MagicMock()
        resp_add.status_code = 200
        resp_add.json.return_value = {"id": 101, "title": "Test Movie"}
        session.send.side_effect = [resp_lookup, resp_add]
        radarr_api = RadarrApi(base_url="http://test", token="test")
        res = radarr_api.add_movie(
            term="test", root_folder_path="/data", quality_profile_id=1
        )
        assert res == {"id": 101, "title": "Test Movie"}


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
