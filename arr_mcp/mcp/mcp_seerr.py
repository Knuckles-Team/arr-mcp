"""Seerr condensed action-routed MCP tool.

CONCEPT:ECO-4.82 — gitlab-style organized per-service tool surface.
"""

import json
from typing import Any

from agent_utilities.mcp_utilities import dispatch, run_blocking
from fastmcp import FastMCP
from pydantic import Field

from arr_mcp.auth import get_seerr_client


def register_seerr_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"seerr"})
    async def seerr_action(
        action: str = Field(
            description="The action/method name to execute on Seerr. Use action='list_actions' to discover every valid action."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters to pass to the action.",
        ),
    ) -> Any:
        """Execute any Seerr API action."""
        client = get_seerr_client()
        kwargs = {k: v for k, v in json.loads(params_json).items() if v is not None}
        return await run_blocking(dispatch, client, action, kwargs, service="arr-seerr")
