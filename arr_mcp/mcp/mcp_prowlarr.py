"""Prowlarr condensed action-routed MCP tool.

CONCEPT:AU-ECO.mcp.tool-mode-standardization — gitlab-style organized per-service tool surface.
"""

from typing import Any, Literal

from agent_utilities.mcp.action_dispatch import dispatch_async, parse_json_object
from fastmcp import Context, FastMCP
from pydantic import Field

from arr_mcp.auth import get_prowlarr_client

_PROWLARR_ACTIONS = Literal[
    "delete_applications_bulk",
    "delete_applications_id",
    "delete_appprofile_id",
    "delete_command_id",
    "delete_customfilter_id",
    "delete_downloadclient_bulk",
    "delete_downloadclient_id",
    "delete_indexer_bulk",
    "delete_indexer_id",
    "delete_indexerproxy_id",
    "delete_notification_id",
    "delete_system_backup_id",
    "delete_tag_id",
    "get_",
    "get_api",
    "get_applications",
    "get_applications_id",
    "get_applications_schema",
    "get_appprofile",
    "get_appprofile_id",
    "get_appprofile_schema",
    "get_command",
    "get_command_id",
    "get_config_development",
    "get_config_development_id",
    "get_config_downloadclient",
    "get_config_downloadclient_id",
    "get_config_host",
    "get_config_host_id",
    "get_config_ui",
    "get_config_ui_id",
    "get_content_path",
    "get_customfilter",
    "get_customfilter_id",
    "get_downloadclient",
    "get_downloadclient_id",
    "get_downloadclient_schema",
    "get_filesystem",
    "get_filesystem_type",
    "get_health",
    "get_history",
    "get_history_indexer",
    "get_history_since",
    "get_id_api",
    "get_id_download",
    "get_indexer",
    "get_indexer_categories",
    "get_indexer_id",
    "get_indexer_id_download",
    "get_indexer_id_newznab",
    "get_indexer_schema",
    "get_indexerproxy",
    "get_indexerproxy_id",
    "get_indexerproxy_schema",
    "get_indexerstats",
    "get_indexerstatus",
    "get_localization",
    "get_localization_options",
    "get_log",
    "get_log_file",
    "get_log_file_filename",
    "get_log_file_update",
    "get_log_file_update_filename",
    "get_login",
    "get_logout",
    "get_notification",
    "get_notification_id",
    "get_notification_schema",
    "get_path",
    "get_ping",
    "get_search",
    "get_system_backup",
    "get_system_routes",
    "get_system_routes_duplicate",
    "get_system_status",
    "get_system_task",
    "get_system_task_id",
    "get_tag",
    "get_tag_detail",
    "get_tag_detail_id",
    "get_tag_id",
    "get_update",
    "post_applications",
    "post_applications_action_name",
    "post_applications_test",
    "post_applications_testall",
    "post_appprofile",
    "post_command",
    "post_customfilter",
    "post_downloadclient",
    "post_downloadclient_action_name",
    "post_downloadclient_test",
    "post_downloadclient_testall",
    "post_indexer",
    "post_indexer_action_name",
    "post_indexer_test",
    "post_indexer_testall",
    "post_indexerproxy",
    "post_indexerproxy_action_name",
    "post_indexerproxy_test",
    "post_indexerproxy_testall",
    "post_login",
    "post_notification",
    "post_notification_action_name",
    "post_notification_test",
    "post_notification_testall",
    "post_search",
    "post_search_bulk",
    "post_system_backup_restore_id",
    "post_system_backup_restore_upload",
    "post_system_restart",
    "post_system_shutdown",
    "post_tag",
    "put_applications_bulk",
    "put_applications_id",
    "put_appprofile_id",
    "put_config_development_id",
    "put_config_downloadclient_id",
    "put_config_host_id",
    "put_config_ui_id",
    "put_customfilter_id",
    "put_downloadclient_bulk",
    "put_downloadclient_id",
    "put_indexer_bulk",
    "put_indexer_id",
    "put_indexerproxy_id",
    "put_notification_id",
    "put_tag_id",
    "search",
]


def register_prowlarr_tools(mcp: FastMCP) -> None:
    @mcp.tool(
        tags={"prowlarr"},
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": True,
        },
        meta={
            "eg.annotations": {"modalities_in": ["text"], "modalities_out": ["text"]}
        },
    )
    async def prowlarr_action(
        action: _PROWLARR_ACTIONS = Field(
            description="The action/method name to execute on Prowlarr (get_indexer to list all indexers, get_system_status). One of 129 real Prowlarr API methods; use action='list_actions' to list them all at runtime."
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
