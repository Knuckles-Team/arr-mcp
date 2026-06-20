"""MCP tool registration modules — one organized module per *arr service.

Mirrors the gitlab-api / servicenow-api layout: each service exposes a
``register_<svc>_tools(mcp)`` that registers one condensed action-routed tool.
``mcp_server.get_mcp_instance`` discovers these via ``register_tool_surface``.

CONCEPT:ECO-4.82 — gitlab-style organized per-service tool surface.
"""

from arr_mcp.mcp.mcp_bazarr import register_bazarr_tools
from arr_mcp.mcp.mcp_chaptarr import register_chaptarr_tools
from arr_mcp.mcp.mcp_lidarr import register_lidarr_tools
from arr_mcp.mcp.mcp_prowlarr import register_prowlarr_tools
from arr_mcp.mcp.mcp_radarr import register_radarr_tools
from arr_mcp.mcp.mcp_seerr import register_seerr_tools
from arr_mcp.mcp.mcp_sonarr import register_sonarr_tools

__all__ = [
    "register_bazarr_tools",
    "register_chaptarr_tools",
    "register_lidarr_tools",
    "register_prowlarr_tools",
    "register_radarr_tools",
    "register_seerr_tools",
    "register_sonarr_tools",
]
