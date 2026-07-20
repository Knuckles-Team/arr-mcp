"""Bazarr condensed action-routed MCP tool.

CONCEPT:AU-ECO.mcp.tool-mode-standardization — gitlab-style organized per-service tool surface.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from fastmcp import Context, FastMCP
from pydantic import Field

from arr_mcp.auth import get_bazarr_client


def register_bazarr_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"bazarr"})
    async def bazarr_action(
        action: str = Field(
            description="The action/method name to execute on Bazarr (e.g. get_series, get_movies, get_system_status). Use action='list_actions' to discover every valid action."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters to pass to the action.",
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Execute any Bazarr API action."""
        client = get_bazarr_client()
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            client, action, kwargs, service="arr-bazarr", ctx=ctx
        )
