"""
Arr MCP Server — Consolidated & Optimized.

This module implements a dynamic unified MCP server for the entire Arr stack.
It collapses hundreds of individual tools into 7 high-level, service-specific
action-routed tools.

MCP & Universal Skills
Action Execution Pipeline
"""

import importlib
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.mcp.action_dispatch import dispatch, parse_json_object
from agent_connector_sdk.tls.resolve import resolve_tls_profile


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
