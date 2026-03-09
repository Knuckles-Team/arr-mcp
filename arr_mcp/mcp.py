"""
Arr MCP Server — Consolidated & Optimized.

This module implements a dynamic unified MCP server for the entire Arr stack.
It uses metaprogramming to dynamically generate FastMCP tool wrappers at runtime
by reading the API method signatures and `tool_tags.json`.

Environment Variables:
    <SERVICE>_<CATEGORY>TOOL (e.g. SONARR_CATALOGTOOL)
"""

import os
import sys
import logging
import json
import inspect
from pathlib import Path
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
)

from arr_mcp.sonarr_api import Api as SonarrApi
from arr_mcp.radarr_api import Api as RadarrApi
from arr_mcp.lidarr_api import Api as LidarrApi
from arr_mcp.prowlarr_api import Api as ProwlarrApi
from arr_mcp.bazarr_api import Api as BazarrApi
from arr_mcp.seerr_api import Api as SeerrApi
from arr_mcp.chaptarr_api import Api as ChaptarrApi

__version__ = "0.2.37"

logger = get_logger(name="ArrMCP")
logger.setLevel(logging.INFO)

API_CLASSES = {
    "sonarr": SonarrApi,
    "radarr": RadarrApi,
    "lidarr": LidarrApi,
    "prowlarr": ProwlarrApi,
    "bazarr": BazarrApi,
    "seerr": SeerrApi,
    "chaptarr": ChaptarrApi,
}


def load_tool_config() -> Dict[str, Dict[str, str]]:
    """Load the tool methods to tag mapping."""
    config_path = Path(__file__).parent / "tool_tags.json"
    if not config_path.exists():
        logger.error(f"Missing {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_dynamic_tool(
    service: str, method_name: str, tag: str, api_class: type
) -> Optional[Any]:
    """
    Dynamically compile a wrapper function for an API method using exec().
    This allows FastMCP/Pydantic to perfectly parse standard python signatures.
    """
    method = getattr(api_class, method_name)
    sig = inspect.signature(method)
    docstring = method.__doc__ or f"Call {service} {method_name}"

    # Analyze parameters (skip `self`)
    params_code = []
    call_args = []

    for name, param in list(sig.parameters.items())[1:]:
        # Get type annotation string safely
        if param.annotation is inspect.Parameter.empty:
            type_str = "Any"
        else:
            try:
                # Basic representation of common types (Dict, List, int, str, bool, Optional, Any)
                type_str = str(param.annotation).replace("typing.", "")
                # Clean up <class 'int'> -> int
                if "class" in type_str:
                    type_str = param.annotation.__name__
            except Exception:
                type_str = "Any"

        # Handle defaults via pydantic Field
        if param.default is inspect.Parameter.empty:
            field_def = f"Field(..., description='{name}')"
        else:
            # We must repr the default so strings get quotes, None gets None, etc.
            field_def = f"Field(default={repr(param.default)}, description='{name}')"

        params_code.append(f"    {name}: {type_str} = {field_def}")
        call_args.append(f"{name}={name}")

    params_str = ",\n".join(params_code)
    call_args_str = ", ".join(call_args)
    if params_str:
        params_str += ",\n"

    svc_upper = service.upper()

    # Prefix tool names to ensure global uniqueness (e.g. lidarr_get_series)
    tool_name = f"{service}_{method_name}"

    # We compile the function exactly as if a human wrote it
    # We add the required base_url, api_key, and verify fields
    func_source = f'''
async def {tool_name}(
{params_str}
    {service}_base_url: str = Field(default=os.environ.get("{svc_upper}_BASE_URL", None), description="Base URL"),
    {service}_api_key: Optional[str] = Field(default=os.environ.get("{svc_upper}_API_KEY", None), description="API Key"),
    {service}_verify: bool = Field(default=to_boolean(os.environ.get("{svc_upper}_VERIFY", "False")), description="Verify SSL")
) -> Dict:
    """{docstring}"""
    # Initialize the specific API client
    client = api_class(
        base_url={service}_base_url,
        token={service}_api_key,
        verify={service}_verify
    )
    # Execute the underlying method
    return client.{method_name}({call_args_str})
'''

    # Required globals for the exec environment
    local_env = {}
    global_env = {
        "os": os,
        "Field": Field,
        "Optional": Optional,
        "Dict": Dict,
        "List": List,
        "Any": Any,
        "to_boolean": to_boolean,
        "api_class": api_class,
    }

    try:
        exec(func_source, global_env, local_env)
        wrapper_func = local_env[tool_name]
        return wrapper_func
    except Exception as e:
        logger.error(f"Failed to compile dynamic tool {service}.{method_name}: {e}")
        return None


def register_dynamic_tools(
    mcp: FastMCP, filter_tags: Optional[List[str]] = None
) -> List[str]:
    """Read configuration, evaluate env vars, and dynamically register allowed tools."""
    tool_config = load_tool_config()
    registered_tags = set()

    for service, methods in tool_config.items():
        if service not in API_CLASSES:
            continue

        api_class = API_CLASSES[service]

        for method_name, tag in methods.items():
            if filter_tags and tag not in filter_tags:
                continue

            wrapper_func = _generate_dynamic_tool(service, method_name, tag, api_class)
            if wrapper_func:
                mcp.add_tool(wrapper_func)
                registered_tags.add(tag)

    return sorted(list(registered_tags))


def mcp_server():
    load_dotenv(Path(__file__).parent.parent / ".env")

    args, mcp, middlewares = create_mcp_server(
        name="Arr",
        version=__version__,
        instructions="Arr Stack MCP Server — Dynamic unified server for Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Seerr, and Chaptarr.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    # Dynamic Registration of API Tools with Explicit Toggles
    registered_tags = []

    DEFAULT_BAZARR_CATALOGTOOL = to_boolean(os.getenv("BAZARR_CATALOGTOOL", "True"))
    if DEFAULT_BAZARR_CATALOGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["bazarr-catalog"])
        )

    DEFAULT_BAZARR_HISTORYTOOL = to_boolean(os.getenv("BAZARR_HISTORYTOOL", "True"))
    if DEFAULT_BAZARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["bazarr-history"])
        )

    DEFAULT_BAZARR_SYSTEMTOOL = to_boolean(os.getenv("BAZARR_SYSTEMTOOL", "True"))
    if DEFAULT_BAZARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["bazarr-system"])
        )

    DEFAULT_CHAPTARR_CONFIGTOOL = to_boolean(os.getenv("CHAPTARR_CONFIGTOOL", "True"))
    if DEFAULT_CHAPTARR_CONFIGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-config"])
        )

    DEFAULT_CHAPTARR_DOWNLOADSTOOL = to_boolean(
        os.getenv("CHAPTARR_DOWNLOADSTOOL", "True")
    )
    if DEFAULT_CHAPTARR_DOWNLOADSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-downloads"])
        )

    DEFAULT_CHAPTARR_HISTORYTOOL = to_boolean(os.getenv("CHAPTARR_HISTORYTOOL", "True"))
    if DEFAULT_CHAPTARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-history"])
        )

    DEFAULT_CHAPTARR_INDEXERTOOL = to_boolean(os.getenv("CHAPTARR_INDEXERTOOL", "True"))
    if DEFAULT_CHAPTARR_INDEXERTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-indexer"])
        )

    DEFAULT_CHAPTARR_OPERATIONSTOOL = to_boolean(
        os.getenv("CHAPTARR_OPERATIONSTOOL", "True")
    )
    if DEFAULT_CHAPTARR_OPERATIONSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-operations"])
        )

    DEFAULT_CHAPTARR_PROFILESTOOL = to_boolean(
        os.getenv("CHAPTARR_PROFILESTOOL", "True")
    )
    if DEFAULT_CHAPTARR_PROFILESTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-profiles"])
        )

    DEFAULT_CHAPTARR_QUEUETOOL = to_boolean(os.getenv("CHAPTARR_QUEUETOOL", "True"))
    if DEFAULT_CHAPTARR_QUEUETOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-queue"])
        )

    DEFAULT_CHAPTARR_SEARCHTOOL = to_boolean(os.getenv("CHAPTARR_SEARCHTOOL", "True"))
    if DEFAULT_CHAPTARR_SEARCHTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-search"])
        )

    DEFAULT_CHAPTARR_SYSTEMTOOL = to_boolean(os.getenv("CHAPTARR_SYSTEMTOOL", "True"))
    if DEFAULT_CHAPTARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["chaptarr-system"])
        )

    DEFAULT_LIDARR_CATALOGTOOL = to_boolean(os.getenv("LIDARR_CATALOGTOOL", "True"))
    if DEFAULT_LIDARR_CATALOGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-catalog"])
        )

    DEFAULT_LIDARR_CONFIGTOOL = to_boolean(os.getenv("LIDARR_CONFIGTOOL", "True"))
    if DEFAULT_LIDARR_CONFIGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-config"])
        )

    DEFAULT_LIDARR_DOWNLOADSTOOL = to_boolean(os.getenv("LIDARR_DOWNLOADSTOOL", "True"))
    if DEFAULT_LIDARR_DOWNLOADSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-downloads"])
        )

    DEFAULT_LIDARR_HISTORYTOOL = to_boolean(os.getenv("LIDARR_HISTORYTOOL", "True"))
    if DEFAULT_LIDARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-history"])
        )

    DEFAULT_LIDARR_INDEXERTOOL = to_boolean(os.getenv("LIDARR_INDEXERTOOL", "True"))
    if DEFAULT_LIDARR_INDEXERTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-indexer"])
        )

    DEFAULT_LIDARR_OPERATIONSTOOL = to_boolean(
        os.getenv("LIDARR_OPERATIONSTOOL", "True")
    )
    if DEFAULT_LIDARR_OPERATIONSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-operations"])
        )

    DEFAULT_LIDARR_PROFILESTOOL = to_boolean(os.getenv("LIDARR_PROFILESTOOL", "True"))
    if DEFAULT_LIDARR_PROFILESTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-profiles"])
        )

    DEFAULT_LIDARR_QUEUETOOL = to_boolean(os.getenv("LIDARR_QUEUETOOL", "True"))
    if DEFAULT_LIDARR_QUEUETOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-queue"])
        )

    DEFAULT_LIDARR_SEARCHTOOL = to_boolean(os.getenv("LIDARR_SEARCHTOOL", "True"))
    if DEFAULT_LIDARR_SEARCHTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-search"])
        )

    DEFAULT_LIDARR_SYSTEMTOOL = to_boolean(os.getenv("LIDARR_SYSTEMTOOL", "True"))
    if DEFAULT_LIDARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["lidarr-system"])
        )

    DEFAULT_PROWLARR_CONFIGTOOL = to_boolean(os.getenv("PROWLARR_CONFIGTOOL", "True"))
    if DEFAULT_PROWLARR_CONFIGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-config"])
        )

    DEFAULT_PROWLARR_DOWNLOADSTOOL = to_boolean(
        os.getenv("PROWLARR_DOWNLOADSTOOL", "True")
    )
    if DEFAULT_PROWLARR_DOWNLOADSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-downloads"])
        )

    DEFAULT_PROWLARR_HISTORYTOOL = to_boolean(os.getenv("PROWLARR_HISTORYTOOL", "True"))
    if DEFAULT_PROWLARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-history"])
        )

    DEFAULT_PROWLARR_INDEXERTOOL = to_boolean(os.getenv("PROWLARR_INDEXERTOOL", "True"))
    if DEFAULT_PROWLARR_INDEXERTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-indexer"])
        )

    DEFAULT_PROWLARR_OPERATIONSTOOL = to_boolean(
        os.getenv("PROWLARR_OPERATIONSTOOL", "True")
    )
    if DEFAULT_PROWLARR_OPERATIONSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-operations"])
        )

    DEFAULT_PROWLARR_PROFILESTOOL = to_boolean(
        os.getenv("PROWLARR_PROFILESTOOL", "True")
    )
    if DEFAULT_PROWLARR_PROFILESTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-profiles"])
        )

    DEFAULT_PROWLARR_SEARCHTOOL = to_boolean(os.getenv("PROWLARR_SEARCHTOOL", "True"))
    if DEFAULT_PROWLARR_SEARCHTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-search"])
        )

    DEFAULT_PROWLARR_SYSTEMTOOL = to_boolean(os.getenv("PROWLARR_SYSTEMTOOL", "True"))
    if DEFAULT_PROWLARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["prowlarr-system"])
        )

    DEFAULT_RADARR_CATALOGTOOL = to_boolean(os.getenv("RADARR_CATALOGTOOL", "True"))
    if DEFAULT_RADARR_CATALOGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-catalog"])
        )

    DEFAULT_RADARR_CONFIGTOOL = to_boolean(os.getenv("RADARR_CONFIGTOOL", "True"))
    if DEFAULT_RADARR_CONFIGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-config"])
        )

    DEFAULT_RADARR_DOWNLOADSTOOL = to_boolean(os.getenv("RADARR_DOWNLOADSTOOL", "True"))
    if DEFAULT_RADARR_DOWNLOADSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-downloads"])
        )

    DEFAULT_RADARR_HISTORYTOOL = to_boolean(os.getenv("RADARR_HISTORYTOOL", "True"))
    if DEFAULT_RADARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-history"])
        )

    DEFAULT_RADARR_INDEXERTOOL = to_boolean(os.getenv("RADARR_INDEXERTOOL", "True"))
    if DEFAULT_RADARR_INDEXERTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-indexer"])
        )

    DEFAULT_RADARR_OPERATIONSTOOL = to_boolean(
        os.getenv("RADARR_OPERATIONSTOOL", "True")
    )
    if DEFAULT_RADARR_OPERATIONSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-operations"])
        )

    DEFAULT_RADARR_PROFILESTOOL = to_boolean(os.getenv("RADARR_PROFILESTOOL", "True"))
    if DEFAULT_RADARR_PROFILESTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-profiles"])
        )

    DEFAULT_RADARR_QUEUETOOL = to_boolean(os.getenv("RADARR_QUEUETOOL", "True"))
    if DEFAULT_RADARR_QUEUETOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-queue"])
        )

    DEFAULT_RADARR_SYSTEMTOOL = to_boolean(os.getenv("RADARR_SYSTEMTOOL", "True"))
    if DEFAULT_RADARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["radarr-system"])
        )

    DEFAULT_SEERR_CATALOGTOOL = to_boolean(os.getenv("SEERR_CATALOGTOOL", "True"))
    if DEFAULT_SEERR_CATALOGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["seerr-catalog"])
        )

    DEFAULT_SEERR_SEARCHTOOL = to_boolean(os.getenv("SEERR_SEARCHTOOL", "True"))
    if DEFAULT_SEERR_SEARCHTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["seerr-search"])
        )

    DEFAULT_SEERR_SYSTEMTOOL = to_boolean(os.getenv("SEERR_SYSTEMTOOL", "True"))
    if DEFAULT_SEERR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["seerr-system"])
        )

    DEFAULT_SONARR_CATALOGTOOL = to_boolean(os.getenv("SONARR_CATALOGTOOL", "True"))
    if DEFAULT_SONARR_CATALOGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-catalog"])
        )

    DEFAULT_SONARR_CONFIGTOOL = to_boolean(os.getenv("SONARR_CONFIGTOOL", "True"))
    if DEFAULT_SONARR_CONFIGTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-config"])
        )

    DEFAULT_SONARR_DOWNLOADSTOOL = to_boolean(os.getenv("SONARR_DOWNLOADSTOOL", "True"))
    if DEFAULT_SONARR_DOWNLOADSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-downloads"])
        )

    DEFAULT_SONARR_HISTORYTOOL = to_boolean(os.getenv("SONARR_HISTORYTOOL", "True"))
    if DEFAULT_SONARR_HISTORYTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-history"])
        )

    DEFAULT_SONARR_INDEXERTOOL = to_boolean(os.getenv("SONARR_INDEXERTOOL", "True"))
    if DEFAULT_SONARR_INDEXERTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-indexer"])
        )

    DEFAULT_SONARR_OPERATIONSTOOL = to_boolean(
        os.getenv("SONARR_OPERATIONSTOOL", "True")
    )
    if DEFAULT_SONARR_OPERATIONSTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-operations"])
        )

    DEFAULT_SONARR_PROFILESTOOL = to_boolean(os.getenv("SONARR_PROFILESTOOL", "True"))
    if DEFAULT_SONARR_PROFILESTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-profiles"])
        )

    DEFAULT_SONARR_QUEUETOOL = to_boolean(os.getenv("SONARR_QUEUETOOL", "True"))
    if DEFAULT_SONARR_QUEUETOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-queue"])
        )

    DEFAULT_SONARR_SYSTEMTOOL = to_boolean(os.getenv("SONARR_SYSTEMTOOL", "True"))
    if DEFAULT_SONARR_SYSTEMTOOL:
        registered_tags.extend(
            register_dynamic_tools(mcp, filter_tags=["sonarr-system"])
        )

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Arr MCP v{__version__}")
    print("\nStarting Arr MCP Server (Optimized Runtime Generation)")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Dynamic Tags Loaded: {len(registered_tags)}")

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
