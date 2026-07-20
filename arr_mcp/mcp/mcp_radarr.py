"""Radarr condensed action-routed MCP tool.

CONCEPT:AU-ECO.mcp.tool-mode-standardization — gitlab-style organized per-service tool surface.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from fastmcp import Context, FastMCP
from pydantic import Field

from arr_mcp.auth import get_radarr_client


def register_radarr_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"radarr"})
    async def radarr_action(
        action: str = Field(
            description="The action/method name to execute on Radarr (e.g. get_movie to list all movies, add_movie, get_system_status). Use action='list_actions' to discover every valid action."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters to pass to the action.",
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Execute any Radarr API action."""
        client = get_radarr_client()
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            client, action, kwargs, service="arr-radarr", ctx=ctx
        )
