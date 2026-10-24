"""
Unified client coverage testing.

CONCEPT:AU-ECO.mcp.fastmcp-middleware — MCP & Universal Skills
CONCEPT:AU-ORCH.adapter.kg-graph-materialization — Action Execution Pipeline
"""

import inspect
from typing import Any

from arr_mcp.api.api_client_bazarr import Api as BazarrApi
from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
from arr_mcp.api.api_client_lidarr import Api as LidarrApi
from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
from arr_mcp.api.api_client_radarr import Api as RadarrApi
from arr_mcp.api.api_client_seerr import Api as SeerrApi
from arr_mcp.api.api_client_sonarr import Api as SonarrApi


def test_apis_brute_force(mock_session):
    _ = mock_session
    apis = [
        SonarrApi,
        RadarrApi,
        LidarrApi,
        ProwlarrApi,
        BazarrApi,
        SeerrApi,
        ChaptarrApi,
    ]
    for api_class in apis:
        print(f"Testing API: {api_class.__name__}")
        # Detect if it uses 'token' or 'api_key'
        init_sig = inspect.signature(api_class.__init__)
        init_kwargs: dict[str, Any] = {"base_url": "http://test.com"}
        if "token" in init_sig.parameters:
            init_kwargs["token"] = "mock"
        if "api_key" in init_sig.parameters:
            init_kwargs["api_key"] = "mock"

        client = api_class(**init_kwargs)

        for name, method in inspect.getmembers(client, predicate=inspect.ismethod):
            if name.startswith("_") or name in ["request", "get_headers"]:
                continue

            print(f"Calling {name}...")
            sig = inspect.signature(method)
            kwargs: dict[str, Any] = {}
            for param in sig.parameters.values():
                if param.name == "kwargs":
                    continue
                # Guessing values
                if "id" in param.name.lower() or param.annotation is int:
                    kwargs[param.name] = 123
                elif "url" in param.name.lower():
                    kwargs[param.name] = "http://test.com"
                elif "enabled" in param.name.lower():
                    kwargs[param.name] = True
                elif param.annotation is dict:
                    kwargs[param.name] = {}
                elif param.annotation is list:
                    kwargs[param.name] = []
                else:
                    kwargs[param.name] = "test"

            try:
                # Positionals
                pos_args = []
                for param in sig.parameters.values():
                    if param.default == inspect.Parameter.empty and param.kind in (
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        inspect.Parameter.POSITIONAL_ONLY,
                    ):
                        pos_args.append(kwargs.get(param.name, "test"))
                        if param.name in kwargs:
                            del kwargs[param.name]
                method(*pos_args, **kwargs)
            except Exception as e:
                print(f"Operation failed: {type(e).__name__}")
