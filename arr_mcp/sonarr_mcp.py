"""
Sonarr MCP Server.

This module implements an MCP server for Sonarr, providing tools to manage
TV series collections and lookups. It handles authentication, middleware,
and API interactions.
"""

import os
import sys
import logging
from typing import Optional, List, Dict, Union

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from arr_mcp.sonarr_api import Api
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_parser,
    config,
)
from agent_utilities.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.20"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="search_series", description="Search for a TV series to add or view."
    )
    def search_series(query: str) -> str:
        """Search for a TV series."""
        return f"Please search for the TV series '{query}'"

    @mcp.prompt(name="calendar", description="Check the upcoming TV schedule.")
    def calendar() -> str:
        """Check the upcoming TV schedule."""
        return "Please check the upcoming TV schedule."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def lookup_series(
        term: str = Field(default=..., description="Search term for the series"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> List[Dict]:
        """Search for a series using the lookup endpoint."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.lookup_series(term=term)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def add_series(
        term: str = Field(default=..., description="Search term for the series"),
        root_folder_path: str = Field(
            default=..., description="Root folder path for the series"
        ),
        quality_profile_id: int = Field(
            default=..., description="Quality profile ID for the series"
        ),
        monitored: bool = Field(default=True, description="Monitor the series"),
        search_for_missing_episodes: bool = Field(
            default=True, description="Search for missing episodes immediately"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Lookup a series by term, pick the first result, and add it to Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.add_series(
            term=term,
            root_folder_path=root_folder_path,
            quality_profile_id=quality_profile_id,
            monitored=monitored,
            search_for_missing_episodes=search_for_missing_episodes,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_api(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the base API information for Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_login(
        returnUrl: str = Field(default=None, description="returnUrl"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a login operation."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_login(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check the current login status."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_logout(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a logout operation."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def post_autotagging(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a logout operation."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_autotagging(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_autotagging(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new auto-tagging configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def put_autotagging_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all auto-tagging configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_autotagging_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def delete_autotagging_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing auto-tagging configuration by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_autotagging_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an auto-tagging configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_autotagging_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get details for an auto-tagging configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_backup(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the schema for auto-tagging configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def delete_system_backup_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the current system backup information."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_system_backup_restore_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a system backup by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_system_backup_restore_upload(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Restore Sonarr from a specific backup ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def get_blocklist(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        seriesIds: List = Field(default=None, description="seriesIds"),
        protocols: List = Field(default=None, description="protocols"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Upload and restore a Sonarr backup archive."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_blocklist(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            seriesIds=seriesIds,
            protocols=protocols,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def delete_blocklist_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a paginated list of items in the blocklist."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_blocklist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def delete_blocklist_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Remove an item from the blocklist by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_blocklist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_calendar(
        start: str = Field(default=None, description="start"),
        end: str = Field(default=None, description="end"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisodeFile: bool = Field(
            default=None, description="includeEpisodeFile"
        ),
        includeEpisodeImages: bool = Field(
            default=None, description="includeEpisodeImages"
        ),
        tags: str = Field(default=None, description="tags"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk removal of items from the blocklist."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_calendar(
            start=start,
            end=end,
            unmonitored=unmonitored,
            includeSeries=includeSeries,
            includeEpisodeFile=includeEpisodeFile,
            includeEpisodeImages=includeEpisodeImages,
            tags=tags,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_calendar_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve calendar events for a given time range."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_calendar_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_feed_v3_calendar_sonarrics(
        pastDays: int = Field(default=None, description="pastDays"),
        futureDays: int = Field(default=None, description="futureDays"),
        tags: str = Field(default=None, description="tags"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        premieresOnly: bool = Field(default=None, description="premieresOnly"),
        asAllDay: bool = Field(default=None, description="asAllDay"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a specific calendar event by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_feed_v3_calendar_sonarrics(
            pastDays=pastDays,
            futureDays=futureDays,
            tags=tags,
            unmonitored=unmonitored,
            premieresOnly=premieresOnly,
            asAllDay=asAllDay,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def post_command(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the calendar feed in iCal format."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_command(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check the current health status of Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def delete_command_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the schema for health status information."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_command_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve Sonarr activity history."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve activity history for a specific series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_customfilter(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a history item by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_customfilter_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Mark a history item as failed."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_customfilter_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a custom filter by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific custom filter by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined custom formats."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_customformat(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Create a new custom format."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_customformat(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_customformat_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing custom format by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customformat_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_customformat_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a custom format by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a specific custom format by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple custom formats."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple custom formats."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for custom formats."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_wanted_cutoff(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisodeFile: bool = Field(
            default=None, description="includeEpisodeFile"
        ),
        includeImages: bool = Field(default=None, description="includeImages"),
        monitored: bool = Field(default=None, description="monitored"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve episodes that have not reached their quality cutoff."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_cutoff(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeSeries=includeSeries,
            includeEpisodeFile=includeEpisodeFile,
            includeImages=includeImages,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_wanted_cutoff_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a specific wanted cutoff detailed info."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_cutoff_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_delayprofile(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new delay profile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_delayprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all delay profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_delayprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_delayprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific delay profile by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing delay profile configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_delayprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a delay profile from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_reorder_id(
        id: int = Field(default=..., description="id"),
        after: int = Field(default=None, description="after"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new delay profile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_delayprofile_reorder_id(id=id, after=after)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_diskspace(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured delay profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_diskspace()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about available disk space."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific download client by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing download client configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a download client from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured download clients."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new download client to Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple download clients."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple download clients."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for download clients."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_testall(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test a download client configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all configured download clients."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on a download client."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_config_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve download client configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update download client configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_episode(
        seriesId: int = Field(default=None, description="seriesId"),
        seasonNumber: int = Field(default=None, description="seasonNumber"),
        episodeIds: List = Field(default=None, description="episodeIds"),
        episodeFileId: int = Field(default=None, description="episodeFileId"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisodeFile: bool = Field(
            default=None, description="includeEpisodeFile"
        ),
        includeImages: bool = Field(default=None, description="includeImages"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all download client configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episode(
            seriesId=seriesId,
            seasonNumber=seasonNumber,
            episodeIds=episodeIds,
            episodeFileId=episodeFileId,
            includeSeries=includeSeries,
            includeEpisodeFile=includeEpisodeFile,
            includeImages=includeImages,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_episode_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific episode by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episode_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_episode_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing episode by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episode_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_episode_monitor(
        data: Dict = Field(default=..., description="data"),
        includeImages: bool = Field(default=None, description="includeImages"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all episodes for a specific series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episode_monitor(data=data, includeImages=includeImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_episodefile(
        seriesId: int = Field(default=None, description="seriesId"),
        episodeFileIds: List = Field(default=None, description="episodeFileIds"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update the monitoring status of multiple episodes."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episodefile(seriesId=seriesId, episodeFileIds=episodeFileIds)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_episodefile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Monitor multiple episodes."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def delete_episodefile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific episode file by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_episodefile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_episodefile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an episode file from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episodefile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_episodefile_editor(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update metadata for a specific episode file."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def delete_episodefile_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all episode files for a specific series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_episodefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_episodefile_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple episode files."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_filesystem(
        path: str = Field(default=None, description="path"),
        includeFiles: bool = Field(default=None, description="includeFiles"),
        allowFoldersWithoutTrailingSlashes: bool = Field(
            default=None, description="allowFoldersWithoutTrailingSlashes"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple episode files."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_filesystem(
            path=path,
            includeFiles=includeFiles,
            allowFoldersWithoutTrailingSlashes=allowFoldersWithoutTrailingSlashes,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_filesystem_type(
        path: str = Field(default=None, description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Browse the local filesystem."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_filesystem_mediafiles(
        path: str = Field(default=None, description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get information about a specific filesystem path."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_filesystem_mediafiles(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_health(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve media information for a specific file path."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"history"},
    )
    async def get_history(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisode: bool = Field(default=None, description="includeEpisode"),
        eventType: List = Field(default=None, description="eventType"),
        episodeId: int = Field(default=None, description="episodeId"),
        downloadId: str = Field(default=None, description="downloadId"),
        seriesIds: List = Field(default=None, description="seriesIds"),
        languages: List = Field(default=None, description="languages"),
        quality: List = Field(default=None, description="quality"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific import list by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_history(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeSeries=includeSeries,
            includeEpisode=includeEpisode,
            eventType=eventType,
            episodeId=episodeId,
            downloadId=downloadId,
            seriesIds=seriesIds,
            languages=languages,
            quality=quality,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"history"},
    )
    async def get_history_since(
        date: str = Field(default=None, description="date"),
        eventType: str = Field(default=None, description="eventType"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisode: bool = Field(default=None, description="includeEpisode"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing import list configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_history_since(
            date=date,
            eventType=eventType,
            includeSeries=includeSeries,
            includeEpisode=includeEpisode,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"history"},
    )
    async def get_history_series(
        seriesId: int = Field(default=None, description="seriesId"),
        seasonNumber: int = Field(default=None, description="seasonNumber"),
        eventType: str = Field(default=None, description="eventType"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisode: bool = Field(default=None, description="includeEpisode"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an import list from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_history_series(
            seriesId=seriesId,
            seasonNumber=seasonNumber,
            eventType=eventType,
            includeSeries=includeSeries,
            includeEpisode=includeEpisode,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"history"},
    )
    async def post_history_failed_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured import lists."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_history_failed_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_config_host(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new import list to Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def put_config_host_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for import lists."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_config_host_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test an import list configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all configured import lists."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on an import list."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve host configuration settings by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlist_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update host configuration settings by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all host configuration settings."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific indexer by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing indexer configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an indexer from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured indexers."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_testall(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer to Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple indexer configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_config_importlist(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple indexers."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_importlist()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_config_importlist_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for indexers."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_importlist_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_config_importlist_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test an indexer configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlistexclusion(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all configured indexers."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_importlistexclusion(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on an indexer."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlistexclusion(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlistexclusion_paged(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve indexer configuration details by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion_paged(
            page=page, pageSize=pageSize, sortKey=sortKey, sortDirection=sortDirection
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def put_importlistexclusion_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexer configuration details by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlistexclusion_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all indexer configuration settings."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific metadata profile by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlistexclusion_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing metadata profile configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlistexclusion_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a metadata profile from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined metadata profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Create a new metadata profile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for metadata profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve naming configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update naming configuration by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all naming configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific notification by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing notification configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_testall(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a notification from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured notifications."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test a notification configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_indexer()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def put_config_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all configured notifications."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_indexer_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on a notification."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerflag(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Parse series information from a string."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexerflag()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_language(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Parse episode information from a string."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_language()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_language_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific quality definition by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_language_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_languageprofile(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing quality definition configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_languageprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_languageprofile(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined quality definitions."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_languageprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple quality definitions."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_languageprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_languageprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for quality definitions."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_languageprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_languageprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific quality profile by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_languageprofile_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing quality profile configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_localization(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a quality profile from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_localization_language(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined quality profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization_language()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_localization_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Create a new quality profile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_log(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        level: str = Field(default=None, description="level"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for quality profiles."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            level=level,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_log_file(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the current download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_log_file_filename(
        filename: str = Field(default=..., description="filename"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed information about the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_manualimport(
        folder: str = Field(default=None, description="folder"),
        downloadId: str = Field(default=None, description="downloadId"),
        seriesId: int = Field(default=None, description="seriesId"),
        seasonNumber: int = Field(default=None, description="seasonNumber"),
        filterExistingFiles: bool = Field(
            default=None, description="filterExistingFiles"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the status of the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_manualimport(
            folder=folder,
            downloadId=downloadId,
            seriesId=seriesId,
            seasonNumber=seasonNumber,
            filterExistingFiles=filterExistingFiles,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_manualimport(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the schema for the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_manualimport(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_mediacover_series_id_filename(
        seriesId: int = Field(default=..., description="seriesId"),
        filename: str = Field(default=..., description="filename"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Manually grab an item from the queue by its ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_mediacover_series_id_filename(
            seriesId=seriesId, filename=filename
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Remove an item from the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_mediamanagement()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_config_mediamanagement_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk removal of items from the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_mediamanagement_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on the download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_mediamanagement_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_metadata(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve available releases."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_metadata(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Manually grab a specific release."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_metadata_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for pushed releases."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_metadata_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def delete_metadata_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Push a new release for processing."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_metadata_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve remote path mapping configurations."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_metadata_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve file rename information."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_metadata_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Execute a file rename operation."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_metadata_testall(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve rename information for a specific series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_metadata_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific restriction by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_wanted_missing(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeImages: bool = Field(default=None, description="includeImages"),
        monitored: bool = Field(default=None, description="monitored"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing restriction configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_missing(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeSeries=includeSeries,
            includeImages=includeImages,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_wanted_missing_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a restriction from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_missing_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined restrictions."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_naming()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_config_naming_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new restriction configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_naming_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific root folder by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_naming_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_examples(
        renameEpisodes: bool = Field(default=None, description="renameEpisodes"),
        replaceIllegalCharacters: bool = Field(
            default=None, description="replaceIllegalCharacters"
        ),
        colonReplacementFormat: int = Field(
            default=None, description="colonReplacementFormat"
        ),
        customColonReplacementFormat: str = Field(
            default=None, description="customColonReplacementFormat"
        ),
        multiEpisodeStyle: int = Field(default=None, description="multiEpisodeStyle"),
        standardEpisodeFormat: str = Field(
            default=None, description="standardEpisodeFormat"
        ),
        dailyEpisodeFormat: str = Field(default=None, description="dailyEpisodeFormat"),
        animeEpisodeFormat: str = Field(default=None, description="animeEpisodeFormat"),
        seriesFolderFormat: str = Field(default=None, description="seriesFolderFormat"),
        seasonFolderFormat: str = Field(default=None, description="seasonFolderFormat"),
        specialsFolderFormat: str = Field(
            default=None, description="specialsFolderFormat"
        ),
        id: int = Field(default=None, description="id"),
        resourceName: str = Field(default=None, description="resourceName"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a root folder from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_naming_examples(
            renameEpisodes=renameEpisodes,
            replaceIllegalCharacters=replaceIllegalCharacters,
            colonReplacementFormat=colonReplacementFormat,
            customColonReplacementFormat=customColonReplacementFormat,
            multiEpisodeStyle=multiEpisodeStyle,
            standardEpisodeFormat=standardEpisodeFormat,
            dailyEpisodeFormat=dailyEpisodeFormat,
            animeEpisodeFormat=animeEpisodeFormat,
            seriesFolderFormat=seriesFolderFormat,
            seasonFolderFormat=seasonFolderFormat,
            specialsFolderFormat=specialsFolderFormat,
            id=id,
            resourceName=resourceName,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_notification(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured root folders."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_notification(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific tag by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def put_notification_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing tag."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def delete_notification_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a tag from Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_notification_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined tags."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_notification_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new tag to Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_notification_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific tag by ID, including its usage."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_notification_testall(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for all tags, including their usage."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_notification_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve episodes that are missing from the collection."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "operations"},
    )
    async def get_parse(
        title: str = Field(default=None, description="title"),
        path: str = Field(default=None, description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve episodes that have not reached their quality cutoff."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_parse(title=title, path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_ping(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Search for series matching a specific term."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Import a series into Sonarr."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualitydefinition_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed info for a missing episode by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed info for a wanted cutoff episode by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_update(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about available manual imports."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualitydefinition_update(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition_limits(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve manual import details by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition_limits()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_qualityprofile(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed information about a specific manual import."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_qualityprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Execute a manual import operation."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve developer configuration settings by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_qualityprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update developer configuration settings by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualityprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all developer configuration settings."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_schema(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve available releases."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def delete_queue_id(
        id: int = Field(default=..., description="id"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about the system."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_queue_id(
            id=id,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def delete_queue_bulk(
        data: Dict = Field(default=..., description="data"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve system status information."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_queue_bulk(
            data=data,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def get_queue(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeUnknownSeriesItems: bool = Field(
            default=None, description="includeUnknownSeriesItems"
        ),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisode: bool = Field(default=None, description="includeEpisode"),
        seriesIds: List = Field(default=None, description="seriesIds"),
        protocol: str = Field(default=None, description="protocol"),
        languages: List = Field(default=None, description="languages"),
        quality: List = Field(default=None, description="quality"),
        status: List = Field(default=None, description="status"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific update by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_queue(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeUnknownSeriesItems=includeUnknownSeriesItems,
            includeSeries=includeSeries,
            includeEpisode=includeEpisode,
            seriesIds=seriesIds,
            protocol=protocol,
            languages=languages,
            quality=quality,
            status=status,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def post_queue_grab_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all available system updates."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_queue_grab_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def post_queue_grab_bulk(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Execute a system update."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_queue_grab_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def get_queue_details(
        seriesId: int = Field(default=None, description="seriesId"),
        episodeIds: List = Field(default=None, description="episodeIds"),
        includeSeries: bool = Field(default=None, description="includeSeries"),
        includeEpisode: bool = Field(default=None, description="includeEpisode"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve system logs."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_queue_details(
            seriesId=seriesId,
            episodeIds=episodeIds,
            includeSeries=includeSeries,
            includeEpisode=includeEpisode,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "queue"},
    )
    async def get_queue_status(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve list of log files."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_queue_status()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_release(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific log file by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_release(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def get_release(
        seriesId: int = Field(default=None, description="seriesId"),
        episodeId: int = Field(default=None, description="episodeId"),
        seasonNumber: int = Field(default=None, description="seasonNumber"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve contents of a specific log file."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_release(
            seriesId=seriesId, episodeId=episodeId, seasonNumber=seasonNumber
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def post_releaseprofile(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new releaseprofile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_releaseprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get releaseprofile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_releaseprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def delete_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete releaseprofile id."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def put_releaseprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update releaseprofile id."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_releaseprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific releaseprofile."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"downloads"},
    )
    async def post_release_push(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new release push."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_release_push(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_remotepathmapping(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new remotepathmapping."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_remotepathmapping(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_remotepathmapping(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed queue status."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_remotepathmapping()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def delete_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete remotepathmapping id."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def put_remotepathmapping_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve queue configuration schema."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_remotepathmapping_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the current download queue."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_rename(
        seriesId: int = Field(default=None, description="seriesId"),
        seasonNumber: int = Field(default=None, description="seasonNumber"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get rename."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rename(seriesId=seriesId, seasonNumber=seasonNumber)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def post_rootfolder(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new root folder."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_rootfolder(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_rootfolder(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get root folders."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rootfolder()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def delete_rootfolder_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a root folder."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"config"},
    )
    async def get_rootfolder_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific root folder."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_seasonpass(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Season Pass."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_seasonpass(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_series(
        tvdbId: int = Field(default=None, description="tvdbId"),
        includeSeasonImages: bool = Field(
            default=None, description="includeSeasonImages"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get series info."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series(tvdbId=tvdbId, includeSeasonImages=includeSeasonImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_series(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_series(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_series_id(
        id: int = Field(default=..., description="id"),
        includeSeasonImages: bool = Field(
            default=None, description="includeSeasonImages"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get series by ID."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_id(id=id, includeSeasonImages=includeSeasonImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_series_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        moveFiles: bool = Field(default=None, description="moveFiles"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_series_id(id=id, data=data, moveFiles=moveFiles)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def delete_series_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportListExclusion: bool = Field(
            default=None, description="addImportListExclusion"
        ),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_series_id(
            id=id,
            deleteFiles=deleteFiles,
            addImportListExclusion=addImportListExclusion,
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def put_series_editor(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update series editor."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_series_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def delete_series_editor(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete series editor."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_series_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_series_id_folder(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get series folder."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_id_folder(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def post_series_import(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Import series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_series_import(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "catalog"},
    )
    async def get_series_lookup(
        term: str = Field(default=None, description="term"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Lookup series."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_lookup(term=term)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_content_path(
        path: str = Field(default=..., description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get content path."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_(
        path: str = Field(default=..., description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get resource by path."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_path(
        path: str = Field(default=..., description="path"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system paths."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_status(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system status."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_routes(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system routes."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_routes_duplicate(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get duplicate system routes."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_system_shutdown(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Trigger system shutdown."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_system_restart(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Trigger system restart."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_tag(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get tags."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def post_tag(
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new tag."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def put_tag_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a tag."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def delete_tag_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a tag."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_tag_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific tag."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_tag_detail(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get tag usage details."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_tag_detail_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific tag usage details."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_task(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system tasks."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_system_task_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific system task."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def put_config_ui_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update UI configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_config_ui_id(
        id: int = Field(default=..., description="id"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific UI configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_config_ui(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get UI configuration."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_update(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get available updates."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_log_file_update(
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file update."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"sonarr", "system"},
    )
    async def get_log_file_update_filename(
        filename: str = Field(default=..., description="filename"),
        sonarr_base_url: str = Field(
            default=os.environ.get("SONARR_BASE_URL", None), description="Base URL"
        ),
        sonarr_api_key: Optional[str] = Field(
            default=os.environ.get("SONARR_API_KEY", None), description="API Key"
        ),
        sonarr_verify: bool = Field(
            default=to_boolean(os.environ.get("SONARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file update content."""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def sonarr_mcp():
    print(f"sonarr_mcp v{__version__}")
    parser = create_mcp_parser()

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        parser.print_help()

        sys.exit(0)

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key

        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("Sonarr", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Sonarr MCP v{__version__}")
    print("\nStarting Sonarr MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

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
    sonarr_mcp()
