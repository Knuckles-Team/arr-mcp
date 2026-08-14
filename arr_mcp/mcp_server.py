"""
Arr MCP Server — Consolidated & Optimized.

This module implements a dynamic unified MCP server for the entire Arr stack.
It collapses hundreds of individual tools into 7 high-level, service-specific
action-routed tools.

MCP & Universal Skills
Action Execution Pipeline
"""

import importlib
import logging
import sys
from typing import Any

from agent_utilities.core.config import load_config, setting
from agent_utilities.core.transport_security import resolve_tls_profile
from agent_utilities.mcp.action_dispatch import dispatch, parse_json_object
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from fastmcp.utilities.logging import get_logger
from starlette.requests import Request
from starlette.responses import JSONResponse

import arr_mcp.mcp as _arr_tools
from arr_mcp.api.api_client_bazarr import Api as BazarrApi
from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
from arr_mcp.api.api_client_lidarr import Api as LidarrApi
from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
from arr_mcp.api.api_client_radarr import Api as RadarrApi
from arr_mcp.api.api_client_seerr import Api as SeerrApi
from arr_mcp.api.api_client_sonarr import Api as SonarrApi
from arr_mcp.auth import (
    get_bazarr_client,
    get_chaptarr_client,
    get_lidarr_client,
    get_prowlarr_client,
    get_radarr_client,
    get_seerr_client,
    get_sonarr_client,
)

__version__ = "2.1.0"

logger = get_logger(name="ArrMCP")
logger.setLevel(logging.INFO)


def execute_arr_action(
    service_name: str,
    base_url: str | None,
    api_key: str | None,
    action: str,
    params_json: str,
    auth_kw: str,
) -> Any:
    """Instantiate the API client and dynamically dispatch the requested action.

    MCP & Universal Skills
    Action Execution Pipeline
    """
    if not base_url:
        raise ValueError(
            "Base URL must be provided (either via environment variable or parameters)."
        )

    _SERVICE_MODULES = {
        "sonarr": "arr_mcp.api.api_client_sonarr",
        "radarr": "arr_mcp.api.api_client_radarr",
        "lidarr": "arr_mcp.api.api_client_lidarr",
        "prowlarr": "arr_mcp.api.api_client_prowlarr",
        "bazarr": "arr_mcp.api.api_client_bazarr",
        "seerr": "arr_mcp.api.api_client_seerr",
        "chaptarr": "arr_mcp.api.api_client_chaptarr",
    }

    module_path = _SERVICE_MODULES.get(service_name)
    if module_path is None:
        raise ValueError(f"Unknown service '{service_name}'")

    module = importlib.import_module(module_path)
    api_class: type[Any] = module.Api

    kwargs = parse_json_object(params_json)

    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Instantiate API client using correct auth keyword (token vs api_key)
    auth_args = {auth_kw: api_key}
    client = api_class(
        base_url=base_url,
        tls_profile=resolve_tls_profile(service_name),
        **auth_args,
    )

    return dispatch(
        client,
        action,
        kwargs,
        service=service_name,
        result_coercer=lambda result: (
            result.model_dump()
            if hasattr(result, "model_dump") and callable(result.model_dump)
            else result
        ),
    )


def is_service_enabled(service: str) -> bool:
    """Return the centrally configured service enablement decision."""
    return bool(setting(f"{service.upper()}_ENABLED", True))


def get_mcp_instance() -> tuple[Any, Any, Any, list[str]]:
    """Initialize and return the MCP instance, args, and middlewares.

    Wires the whole tool surface through the central ``register_tool_surface``
    helper (CONCEPT:AU-ECO.mcp.tool-mode-standardization): one condensed action-routed tool per *arr service
    (gated by ``<SVC>TOOL``, default on) plus, in verbose/both mode, the 1:1
    ``<svc>_<method>`` surface for each service's client.
    """
    load_config()

    args, mcp, middlewares = create_mcp_server(
        name="Arr",
        version=__version__,
        instructions="Arr Stack MCP Server — Dynamic unified server for Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Seerr, and Chaptarr.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"}, headers={"Cache-Control": "no-store"})

    registered_tags = register_tool_surface(
        mcp,
        service="arr-mcp",
        tools_module=_arr_tools,
        verbose_targets=[
            {
                "client_cls": SonarrApi,
                "get_client": get_sonarr_client,
                "tool_prefix": "sonarr",
            },
            {
                "client_cls": RadarrApi,
                "get_client": get_radarr_client,
                "tool_prefix": "radarr",
            },
            {
                "client_cls": LidarrApi,
                "get_client": get_lidarr_client,
                "tool_prefix": "lidarr",
            },
            {
                "client_cls": ProwlarrApi,
                "get_client": get_prowlarr_client,
                "tool_prefix": "prowlarr",
            },
            {
                "client_cls": BazarrApi,
                "get_client": get_bazarr_client,
                "tool_prefix": "bazarr",
            },
            {
                "client_cls": SeerrApi,
                "get_client": get_seerr_client,
                "tool_prefix": "seerr",
            },
            {
                "client_cls": ChaptarrApi,
                "get_client": get_chaptarr_client,
                "tool_prefix": "chaptarr",
            },
        ],
    )

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares, registered_tags


def mcp_server() -> None:
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    print(f"{'arr-mcp'} MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {len(set(registered_tags))}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
