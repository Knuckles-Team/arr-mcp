"""Prowlarr condensed action-routed MCP tool.

CONCEPT:AU-ECO.mcp.tool-mode-standardization — gitlab-style organized per-service tool surface.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from fastmcp import Context, FastMCP
from pydantic import Field

from arr_mcp.auth import get_prowlarr_client


def register_prowlarr_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"prowlarr"})
    async def prowlarr_action(
        action: str = Field(
            description="The action/method name to execute on Prowlarr. Use action='list_actions' to discover every valid action."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters to pass to the action.",
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Execute any Prowlarr API action."""
        client = get_prowlarr_client()
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            client, action, kwargs, service="arr-prowlarr", ctx=ctx
        )
