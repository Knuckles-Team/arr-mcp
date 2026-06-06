import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")
"""
Arr MCP Server — Consolidated & Optimized.

This module implements a dynamic unified MCP server for the entire Arr stack.
It collapses hundreds of individual tools into 7 high-level, service-specific
action-routed tools.

MCP & Universal Skills
Action Execution Pipeline
"""

import importlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
)
from dotenv import load_dotenv
from fastmcp import Context
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

__version__ = "0.40.0"

logger = get_logger(name="ArrMCP")
logger.setLevel(logging.INFO)


def execute_arr_action(
    service_name: str,
    base_url: str | None,
    api_key: str | None,
    verify: bool,
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

    try:
        kwargs = json.loads(params_json) if params_json else {}
    except Exception as e:
        raise ValueError(f"Invalid params_json: {e}") from e

    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # Instantiate API client using correct auth keyword (token vs api_key)
    auth_args = {auth_kw: api_key}
    client = api_class(base_url=base_url, verify=verify, **auth_args)

    # Dynamic method lookup
    method = getattr(client, action, None)
    if method is None:
        raise ValueError(f"Unknown action '{action}' on {api_class.__name__}")

    res = method(**kwargs)
    if hasattr(res, "dict") and callable(res.dict):
        return res.dict()
    elif hasattr(res, "model_dump") and callable(res.model_dump):
        return res.model_dump()
    return res


def is_service_enabled(service: str) -> bool:
    """Determine if a service should be enabled based on environment overrides."""
    # Check if specifically enabled or disabled
    env_enabled = os.getenv(f"{service.upper()}_ENABLED")
    if env_enabled is not None:
        return to_boolean(env_enabled)

    # Check for legacy category tool configuration: if any category is disabled, we default to enabled.
    # We verify if there are any specific service tool settings that are explicitly disabled,
    # but by default all services are enabled.
    return True


def get_mcp_instance() -> tuple[Any, Any, Any, list[str]]:
    """Initialize and return the MCP instance, args, and middlewares."""
    load_dotenv(Path(__file__).parent.parent / ".env")

    args, mcp, middlewares = create_mcp_server(
        name="Arr",
        version=__version__,
        instructions="Arr Stack MCP Server — Dynamic unified server for Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Seerr, and Chaptarr.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    registered_tags = []

    # 1. Bazarr
    if is_service_enabled("bazarr"):

        @mcp.tool(tags=["bazarr"])
        async def bazarr_action(
            action: str = Field(
                description="The action/method name to execute on Bazarr (e.g. get_series, get_movies, get_system_status)"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            bazarr_base_url: str | None = Field(
                default=os.environ.get("BAZARR_BASE_URL", None),
                description="Bazarr Base URL",
            ),
            bazarr_api_key: str | None = Field(
                default=os.environ.get("BAZARR_API_KEY", None),
                description="Bazarr API Key",
            ),
            bazarr_verify: bool = Field(
                default=to_boolean(os.environ.get("BAZARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Bazarr API action."""
            if ctx:
                await ctx.info(f"Executing Bazarr action: {action}...")
            return execute_arr_action(
                "bazarr",
                bazarr_base_url,
                bazarr_api_key,
                bazarr_verify,
                action,
                params_json,
                "api_key",
            )

        registered_tags.append("bazarr")

    # 2. Chaptarr
    if is_service_enabled("chaptarr"):

        @mcp.tool(tags=["chaptarr"])
        async def chaptarr_action(
            action: str = Field(
                description="The action/method name to execute on Chaptarr"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            chaptarr_base_url: str | None = Field(
                default=os.environ.get("CHAPTARR_BASE_URL", None),
                description="Chaptarr Base URL",
            ),
            chaptarr_api_key: str | None = Field(
                default=os.environ.get("CHAPTARR_API_KEY", None),
                description="Chaptarr API Key",
            ),
            chaptarr_verify: bool = Field(
                default=to_boolean(os.environ.get("CHAPTARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Chaptarr API action."""
            if ctx:
                await ctx.info(f"Executing Chaptarr action: {action}...")
            return execute_arr_action(
                "chaptarr",
                chaptarr_base_url,
                chaptarr_api_key,
                chaptarr_verify,
                action,
                params_json,
                "token",
            )

        registered_tags.append("chaptarr")

    # 3. Lidarr
    if is_service_enabled("lidarr"):

        @mcp.tool(tags=["lidarr"])
        async def lidarr_action(
            action: str = Field(
                description="The action/method name to execute on Lidarr"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            lidarr_base_url: str | None = Field(
                default=os.environ.get("LIDARR_BASE_URL", None),
                description="Lidarr Base URL",
            ),
            lidarr_api_key: str | None = Field(
                default=os.environ.get("LIDARR_API_KEY", None),
                description="Lidarr API Key",
            ),
            lidarr_verify: bool = Field(
                default=to_boolean(os.environ.get("LIDARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Lidarr API action."""
            if ctx:
                await ctx.info(f"Executing Lidarr action: {action}...")
            return execute_arr_action(
                "lidarr",
                lidarr_base_url,
                lidarr_api_key,
                lidarr_verify,
                action,
                params_json,
                "token",
            )

        registered_tags.append("lidarr")

    # 4. Prowlarr
    if is_service_enabled("prowlarr"):

        @mcp.tool(tags=["prowlarr"])
        async def prowlarr_action(
            action: str = Field(
                description="The action/method name to execute on Prowlarr"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            prowlarr_base_url: str | None = Field(
                default=os.environ.get("PROWLARR_BASE_URL", None),
                description="Prowlarr Base URL",
            ),
            prowlarr_api_key: str | None = Field(
                default=os.environ.get("PROWLARR_API_KEY", None),
                description="Prowlarr API Key",
            ),
            prowlarr_verify: bool = Field(
                default=to_boolean(os.environ.get("PROWLARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Prowlarr API action."""
            if ctx:
                await ctx.info(f"Executing Prowlarr action: {action}...")
            return execute_arr_action(
                "prowlarr",
                prowlarr_base_url,
                prowlarr_api_key,
                prowlarr_verify,
                action,
                params_json,
                "token",
            )

        registered_tags.append("prowlarr")

    # 5. Radarr
    if is_service_enabled("radarr"):

        @mcp.tool(tags=["radarr"])
        async def radarr_action(
            action: str = Field(
                description="The action/method name to execute on Radarr (e.g. get_movies, add_movie, get_system_status)"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            radarr_base_url: str | None = Field(
                default=os.environ.get("RADARR_BASE_URL", None),
                description="Radarr Base URL",
            ),
            radarr_api_key: str | None = Field(
                default=os.environ.get("RADARR_API_KEY", None),
                description="Radarr API Key",
            ),
            radarr_verify: bool = Field(
                default=to_boolean(os.environ.get("RADARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Radarr API action."""
            if ctx:
                await ctx.info(f"Executing Radarr action: {action}...")
            return execute_arr_action(
                "radarr",
                radarr_base_url,
                radarr_api_key,
                radarr_verify,
                action,
                params_json,
                "token",
            )

        registered_tags.append("radarr")

    # 6. Seerr
    if is_service_enabled("seerr"):

        @mcp.tool(tags=["seerr"])
        async def seerr_action(
            action: str = Field(
                description="The action/method name to execute on Seerr"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            seerr_base_url: str | None = Field(
                default=os.environ.get("SEERR_BASE_URL", None),
                description="Seerr Base URL",
            ),
            seerr_api_key: str | None = Field(
                default=os.environ.get("SEERR_API_KEY", None),
                description="Seerr API Key",
            ),
            seerr_verify: bool = Field(
                default=to_boolean(os.environ.get("SEERR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Seerr API action."""
            if ctx:
                await ctx.info(f"Executing Seerr action: {action}...")
            return execute_arr_action(
                "seerr",
                seerr_base_url,
                seerr_api_key,
                seerr_verify,
                action,
                params_json,
                "api_key",
            )

        registered_tags.append("seerr")

    # 7. Sonarr
    if is_service_enabled("sonarr"):

        @mcp.tool(tags=["sonarr"])
        async def sonarr_action(
            action: str = Field(
                description="The action/method name to execute on Sonarr (e.g. get_series, add_series, get_system_status)"
            ),
            params_json: str = Field(
                default="{}",
                description="JSON string of parameters to pass to the action.",
            ),
            sonarr_base_url: str | None = Field(
                default=os.environ.get("SONARR_BASE_URL", None),
                description="Sonarr Base URL",
            ),
            sonarr_api_key: str | None = Field(
                default=os.environ.get("SONARR_API_KEY", None),
                description="Sonarr API Key",
            ),
            sonarr_verify: bool = Field(
                default=to_boolean(os.environ.get("SONARR_SSL_VERIFY", "False")),
                description="Verify SSL",
            ),
            ctx: Context | None = Field(
                default=None, description="MCP context for progress reporting"
            ),
        ) -> Any:
            """Execute any Sonarr API action."""
            if ctx:
                await ctx.info(f"Executing Sonarr action: {action}...")
            return execute_arr_action(
                "sonarr",
                sonarr_base_url,
                sonarr_api_key,
                sonarr_verify,
                action,
                params_json,
                "token",
            )

        registered_tags.append("sonarr")

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
