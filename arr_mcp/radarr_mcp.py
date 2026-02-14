"""
Radarr MCP Server.

This module implements an MCP server for Radarr, providing tools to manage
movie collections and lookups. It handles authentication, middleware,
and API interactions.
"""

import os
import argparse
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
from arr_mcp.radarr_api import Api
from arr_mcp.utils import to_boolean, to_integer
from arr_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.8"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="search_movies", description="Search for a movie to add or view.")
    def search_movies(query: str) -> str:
        """Search for a movie."""
        return f"Please search for the movie '{query}'"

    @mcp.prompt(name="calendar", description="Check the upcoming movie schedule.")
    def calendar() -> str:
        """Check the upcoming movie schedule."""
        return "Please check the upcoming movie schedule."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def lookup_movie(
        term: str = Field(default=..., description="Search term for the movie"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> List[Dict]:
        """Search for a movie using the lookup endpoint."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.lookup_movie(term=term)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def add_movie(
        term: str = Field(default=..., description="Search term for the movie"),
        root_folder_path: str = Field(
            default=..., description="Root folder path for the movie"
        ),
        quality_profile_id: int = Field(
            default=..., description="Quality profile ID for the movie"
        ),
        monitored: bool = Field(default=True, description="Monitor the movie"),
        search_for_movie: bool = Field(
            default=True, description="Search for movie immediately"
        ),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Lookup a movie by term, pick the first result, and add it to Radarr."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.add_movie(
            term=term,
            root_folder_path=root_folder_path,
            quality_profile_id=quality_profile_id,
            monitored=monitored,
            search_for_movie=search_for_movie,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_alttitle(
        movieId: int = Field(default=None, description="movieId"),
        movieMetadataId: int = Field(default=None, description="movieMetadataId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get alternative titles for a movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_alttitle(movieId=movieId, movieMetadataId=movieMetadataId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_alttitle_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get details for a specific alternative title by ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_alttitle_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_api(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the base API information for Radarr."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_login(
        returnUrl: str = Field(default=None, description="returnUrl"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a login operation."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_login(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check the current login status."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_logout(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a logout operation."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def post_autotagging(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new auto-tagging configuration."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_autotagging(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_autotagging(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all auto-tagging configurations."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_autotagging()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def put_autotagging_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing auto-tagging configuration by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_autotagging_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def delete_autotagging_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get details for an auto-tagging configuration by ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_autotagging_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the schema for auto-tagging configurations."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_autotagging_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the current system backup information."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_autotagging_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_backup(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a system backup by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def delete_system_backup_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Restore Radarr from a specific backup ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Upload and restore a Radarr backup archive."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_upload(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a paginated list of items in the blocklist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def get_blocklist(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        movieIds: List = Field(default=None, description="movieIds"),
        protocols: List = Field(default=None, description="protocols"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Remove an item from the blocklist by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_blocklist(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            movieIds=movieIds,
            protocols=protocols,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def get_blocklist_movie(
        movieId: int = Field(default=None, description="movieId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk removal of items from the blocklist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_blocklist_movie(movieId=movieId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def delete_blocklist_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve calendar events for a given time range."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_blocklist_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def delete_blocklist_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a specific calendar event by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_blocklist_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_calendar(
        start: str = Field(default=None, description="start"),
        end: str = Field(default=None, description="end"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        tags: str = Field(default=None, description="tags"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the calendar feed in iCal format."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_calendar(
            start=start, end=end, unmonitored=unmonitored, tags=tags
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_feed_v3_calendar_radarrics(
        pastDays: int = Field(default=None, description="pastDays"),
        futureDays: int = Field(default=None, description="futureDays"),
        tags: str = Field(default=None, description="tags"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        releaseTypes: List = Field(default=None, description="releaseTypes"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the status of a specific command by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_feed_v3_calendar_radarrics(
            pastDays=pastDays,
            futureDays=futureDays,
            tags=tags,
            unmonitored=unmonitored,
            releaseTypes=releaseTypes,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_collection(
        tmdbId: int = Field(default=None, description="tmdbId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get information for a movie collection."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_collection(tmdbId=tmdbId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_collection(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Cancel a specific command by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_collection(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_collection_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Execute a command in Radarr."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_collection_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_collection_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all currently running or recently finished commands."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_collection_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def post_command(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific custom filter by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_command(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing custom filter by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def delete_command_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a custom filter by its ID."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_command_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined custom filters."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_credit(
        movieId: int = Field(default=None, description="movieId"),
        movieMetadataId: int = Field(default=None, description="movieMetadataId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get credit."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_credit(movieId=movieId, movieMetadataId=movieMetadataId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_credit_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific credit."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_credit_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get customfilter."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def post_customfilter(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new customfilter."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_customfilter_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update customfilter id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_customfilter_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete customfilter id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific customfilter."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get customformat."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_customformat()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def post_customformat(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new customformat."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_customformat(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_customformat_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update customformat id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_customformat_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_customformat_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete customformat id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific customformat."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update customformat bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete customformat bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get customformat schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_customformat_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_wanted_cutoff(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        monitored: bool = Field(default=None, description="monitored"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get wanted cutoff."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_wanted_cutoff(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def post_delayprofile(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new delayprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_delayprofile(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get delayprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_delayprofile()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_delayprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete delayprofile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update delayprofile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_delayprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific delayprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_reorder_id(
        id: int = Field(default=..., description="id"),
        after: int = Field(default=None, description="after"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update delayprofile reorder id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_delayprofile_reorder_id(id=id, after=after)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_diskspace(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get diskspace."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_diskspace()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update downloadclient id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete downloadclient id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update downloadclient bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete downloadclient bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get downloadclient schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_testall(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new downloadclient testall."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new downloadclient action name."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_config_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config downloadclient id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config downloadclient."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_extrafile(
        movieId: int = Field(default=None, description="movieId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get extrafile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_extrafile(movieId=movieId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_filesystem(
        path: str = Field(default=None, description="path"),
        includeFiles: bool = Field(default=None, description="includeFiles"),
        allowFoldersWithoutTrailingSlashes: bool = Field(
            default=None, description="allowFoldersWithoutTrailingSlashes"
        ),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get filesystem."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_filesystem(
            path=path,
            includeFiles=includeFiles,
            allowFoldersWithoutTrailingSlashes=allowFoldersWithoutTrailingSlashes,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_filesystem_type(
        path: str = Field(default=None, description="path"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get filesystem type."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_filesystem_mediafiles(
        path: str = Field(default=None, description="path"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get filesystem mediafiles."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_filesystem_mediafiles(path=path)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_health(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get health."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"history"},
    )
    async def get_history(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeMovie: bool = Field(default=None, description="includeMovie"),
        eventType: List = Field(default=None, description="eventType"),
        downloadId: str = Field(default=None, description="downloadId"),
        movieIds: List = Field(default=None, description="movieIds"),
        languages: List = Field(default=None, description="languages"),
        quality: List = Field(default=None, description="quality"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_history(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeMovie=includeMovie,
            eventType=eventType,
            downloadId=downloadId,
            movieIds=movieIds,
            languages=languages,
            quality=quality,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"history"},
    )
    async def get_history_since(
        date: str = Field(default=None, description="date"),
        eventType: str = Field(default=None, description="eventType"),
        includeMovie: bool = Field(default=None, description="includeMovie"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history since."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_history_since(
            date=date, eventType=eventType, includeMovie=includeMovie
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"history"},
    )
    async def get_history_movie(
        movieId: int = Field(default=None, description="movieId"),
        eventType: str = Field(default=None, description="eventType"),
        includeMovie: bool = Field(default=None, description="includeMovie"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_history_movie(
            movieId=movieId, eventType=eventType, includeMovie=includeMovie
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"history"},
    )
    async def post_history_failed_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new history failed id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_history_failed_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_config_host(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config host."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def put_config_host_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config host id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_config_host_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config host."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_importlist()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_importlist(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update importlist id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_importlist_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete importlist id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update importlist bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete importlist bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get importlist schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_importlist_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_importlist_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_testall(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new importlist testall."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_importlist_testall()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new importlist action name."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_importlist_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_config_importlist(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_importlist()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_config_importlist_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config importlist id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_importlist_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_config_importlist_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config importlist."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_exclusions(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get exclusions."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_exclusions()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_exclusions(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new exclusions."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_exclusions(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_exclusions_paged(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get exclusions paged."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_exclusions_paged(
            page=page, pageSize=pageSize, sortKey=sortKey, sortDirection=sortDirection
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def put_exclusions_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update exclusions id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_exclusions_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_exclusions_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete exclusions id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_exclusions_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_exclusions_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific exclusions."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_exclusions_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_exclusions_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new exclusions bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_exclusions_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def delete_exclusions_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete exclusions bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_exclusions_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_importlist_movie(
        includeRecommendations: bool = Field(
            default=None, description="includeRecommendations"
        ),
        includeTrending: bool = Field(default=None, description="includeTrending"),
        includePopular: bool = Field(default=None, description="includePopular"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get importlist movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_importlist_movie(
            includeRecommendations=includeRecommendations,
            includeTrending=includeTrending,
            includePopular=includePopular,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_importlist_movie(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new importlist movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_importlist_movie(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexer id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete indexer id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexer bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete indexer bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_testall(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer testall."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer action name."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_indexer()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def put_config_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config indexer id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_indexer_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config indexer."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerflag(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexerflag."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_indexerflag()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_language(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get language."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_language()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_language_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific language."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_language_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_localization(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_localization_language(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization language."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_localization_language()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_log(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        level: str = Field(default=None, description="level"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_log(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            level=level,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_log_file(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_log_file_filename(
        filename: str = Field(default=..., description="filename"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file filename."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_manualimport(
        folder: str = Field(default=None, description="folder"),
        downloadId: str = Field(default=None, description="downloadId"),
        movieId: int = Field(default=None, description="movieId"),
        filterExistingFiles: bool = Field(
            default=None, description="filterExistingFiles"
        ),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get manualimport."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_manualimport(
            folder=folder,
            downloadId=downloadId,
            movieId=movieId,
            filterExistingFiles=filterExistingFiles,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_manualimport(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new manualimport."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_manualimport(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_mediacover_movie_id_filename(
        movieId: int = Field(default=..., description="movieId"),
        filename: str = Field(default=..., description="filename"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific mediacover movie filename."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_mediacover_movie_id_filename(
            movieId=movieId, filename=filename
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config mediamanagement."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_mediamanagement()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_config_mediamanagement_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config mediamanagement id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_mediamanagement_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config mediamanagement."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_mediamanagement_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_metadata(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_metadata()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_metadata(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_metadata(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_metadata_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update metadata id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_metadata_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def delete_metadata_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete metadata id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_metadata_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_metadata_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_metadata_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_metadata_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_metadata_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_metadata_testall(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new metadata testall."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_metadata_testall()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_metadata_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new metadata action name."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_metadata_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_metadata(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_metadata()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_config_metadata_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config metadata id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_metadata_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_metadata_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config metadata."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_wanted_missing(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        monitored: bool = Field(default=None, description="monitored"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get wanted missing."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_wanted_missing(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie(
        tmdbId: int = Field(default=None, description="tmdbId"),
        excludeLocalCovers: bool = Field(
            default=None, description="excludeLocalCovers"
        ),
        languageId: int = Field(default=None, description="languageId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie(
            tmdbId=tmdbId, excludeLocalCovers=excludeLocalCovers, languageId=languageId
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_movie(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_movie(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_movie_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        moveFiles: bool = Field(default=None, description="moveFiles"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update movie id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_movie_id(id=id, data=data, moveFiles=moveFiles)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def delete_movie_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportExclusion: bool = Field(
            default=None, description="addImportExclusion"
        ),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete movie id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_movie_id(
            id=id, deleteFiles=deleteFiles, addImportExclusion=addImportExclusion
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_movie_editor(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update movie editor."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_movie_editor(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def delete_movie_editor(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete movie editor."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_movie_editor(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_moviefile(
        movieId: List = Field(default=None, description="movieId"),
        movieFileIds: List = Field(default=None, description="movieFileIds"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get moviefile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_moviefile(movieId=movieId, movieFileIds=movieFileIds)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_moviefile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update moviefile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_moviefile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def delete_moviefile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete moviefile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_moviefile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_moviefile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific moviefile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_moviefile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_moviefile_editor(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update moviefile editor."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_moviefile_editor(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def delete_moviefile_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete moviefile bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_moviefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def put_moviefile_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update moviefile bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_moviefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie_id_folder(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific movie folder."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie_id_folder(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def post_movie_import(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new movie import."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_movie_import(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie_lookup_tmdb(
        tmdbId: int = Field(default=None, description="tmdbId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get movie lookup tmdb."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie_lookup_tmdb(tmdbId=tmdbId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie_lookup_imdb(
        imdbId: str = Field(default=None, description="imdbId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get movie lookup imdb."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie_lookup_imdb(imdbId=imdbId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_movie_lookup(
        term: str = Field(default=None, description="term"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get movie lookup."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_movie_lookup(term=term)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config naming."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_naming()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_config_naming_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config naming id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_naming_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config naming."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_naming_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_examples(
        renameMovies: bool = Field(default=None, description="renameMovies"),
        replaceIllegalCharacters: bool = Field(
            default=None, description="replaceIllegalCharacters"
        ),
        colonReplacementFormat: str = Field(
            default=None, description="colonReplacementFormat"
        ),
        standardMovieFormat: str = Field(
            default=None, description="standardMovieFormat"
        ),
        movieFolderFormat: str = Field(default=None, description="movieFolderFormat"),
        id: int = Field(default=None, description="id"),
        resourceName: str = Field(default=None, description="resourceName"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config naming examples."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_naming_examples(
            renameMovies=renameMovies,
            replaceIllegalCharacters=replaceIllegalCharacters,
            colonReplacementFormat=colonReplacementFormat,
            standardMovieFormat=standardMovieFormat,
            movieFolderFormat=movieFolderFormat,
            id=id,
            resourceName=resourceName,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_notification(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notification."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_notification(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def put_notification_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update notification id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def delete_notification_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete notification id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_notification_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific notification."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_notification_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notification schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_notification_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test notification."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_notification_testall(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification testall."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_notification_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification action name."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"operations"},
    )
    async def get_parse(
        title: str = Field(default=None, description="title"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get parse."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_parse(title=title)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_ping(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get ping."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update qualitydefinition id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_qualitydefinition_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific qualitydefinition."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualitydefinition_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get qualitydefinition."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualitydefinition()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_update(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update qualitydefinition update."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_qualitydefinition_update(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition_limits(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get qualitydefinition limits."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualitydefinition_limits()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def post_qualityprofile(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new qualityprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_qualityprofile(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get qualityprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualityprofile()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete qualityprofile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_qualityprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update qualityprofile id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_qualityprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific qualityprofile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_schema(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get qualityprofile schema."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_qualityprofile_schema()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def delete_queue_id(
        id: int = Field(default=..., description="id"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete queue id."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_queue_id(
            id=id,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def delete_queue_bulk(
        data: Dict = Field(default=..., description="data"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete queue bulk."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_queue_bulk(
            data=data,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def get_queue(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeUnknownMovieItems: bool = Field(
            default=None, description="includeUnknownMovieItems"
        ),
        includeMovie: bool = Field(default=None, description="includeMovie"),
        movieIds: List = Field(default=None, description="movieIds"),
        protocol: str = Field(default=None, description="protocol"),
        languages: List = Field(default=None, description="languages"),
        quality: List = Field(default=None, description="quality"),
        status: List = Field(default=None, description="status"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_queue(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeUnknownMovieItems=includeUnknownMovieItems,
            includeMovie=includeMovie,
            movieIds=movieIds,
            protocol=protocol,
            languages=languages,
            quality=quality,
            status=status,
        )

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def post_queue_grab_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_queue_grab_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def post_queue_grab_bulk(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Grab queue item."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_queue_grab_bulk(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def get_queue_details(
        movieId: int = Field(default=None, description="movieId"),
        includeMovie: bool = Field(default=None, description="includeMovie"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk grab queue items."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_queue_details(movieId=movieId, includeMovie=includeMovie)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"queue"},
    )
    async def get_queue_status(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue details."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_queue_status()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_release(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue status."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_release(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def get_release(
        movieId: int = Field(default=None, description="movieId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a release."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_release(movieId=movieId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def post_releaseprofile(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get releases."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_releaseprofile(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a release profile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_releaseprofile()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def delete_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get release profiles."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def put_releaseprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a release profile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_releaseprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a release profile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"downloads"},
    )
    async def post_release_push(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific release profile."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_release_push(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_remotepathmapping(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Push release."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_remotepathmapping(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_remotepathmapping(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add remote path mapping."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_remotepathmapping()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def delete_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get remote path mappings."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def put_remotepathmapping_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete remote path mapping."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_remotepathmapping_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update remote path mapping."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"catalog"},
    )
    async def get_rename(
        movieId: List = Field(default=None, description="movieId"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific remote path mapping."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_rename(movieId=movieId)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def post_rootfolder(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get rename suggestions."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_rootfolder(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_rootfolder(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new root folder."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_rootfolder()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def delete_rootfolder_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get root folders."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"config"},
    )
    async def get_rootfolder_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a root folder."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_content_path(
        path: str = Field(default=..., description="path"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific root folder."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_(
        path: str = Field(default=..., description="path"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get content path."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_path(
        path: str = Field(default=..., description="path"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get resource by path."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_status(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system paths."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_routes(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system routes."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_routes_duplicate(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get duplicate system routes."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_system_shutdown(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Trigger system shutdown."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_system_restart(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Trigger system restart."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_tag(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific system task."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def post_tag(
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve logs for system tasks."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def put_tag_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve logs for a specific system task."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def delete_tag_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detail logs for a specific system task."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_tag_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all movies in the collection."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Check if a movie exists in the collection."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about a movie file."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_task(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all movie files for a specific movie."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_system_task_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a movie file from Radarr."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def put_config_ui_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update metadata for multiple movie files."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_config_ui_id(
        id: int = Field(default=..., description="id"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple movie files."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_config_ui(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about movie import lists."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_update(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific import list."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update(
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined import lists."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["radarr_base_url", "radarr_api_key", "radarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update_filename(
        filename: str = Field(default=..., description="filename"),
        radarr_base_url: str = Field(
            default=os.environ.get("RADARR_BASE_URL", None), description="Base URL"
        ),
        radarr_api_key: Optional[str] = Field(
            default=os.environ.get("RADARR_API_KEY", None), description="API Key"
        ),
        radarr_verify: bool = Field(
            default=to_boolean(os.environ.get("RADARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Create a new import list."""
        client = Api(
            base_url=radarr_base_url, token=radarr_api_key, verify=radarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def radarr_mcp():
    print(f"radarr_mcp v{__version__}")
    parser = argparse.ArgumentParser(add_help=False, description="Radarr MCP")

    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., ansible.read,ansible.write).",
    )
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        usage()

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

    mcp = FastMCP("Radarr", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Radarr MCP v{__version__}")
    print("\nStarting Radarr MCP Server")
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


def usage():
    print(
        f"Arr Mcp ({__version__}): Radarr MCP Server\n\n"
        "Usage:\n"
        "-t | --transport                   [ Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio) ]\n"
        "-s | --host                        [ Host address for HTTP transport (default: 0.0.0.0) ]\n"
        "-p | --port                        [ Port number for HTTP transport (default: 8000) ]\n"
        "--auth-type                        [ Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none) ]\n"
        "--token-jwks-uri                   [ JWKS URI for JWT verification ]\n"
        "--token-issuer                     [ Issuer for JWT verification ]\n"
        "--token-audience                   [ Audience for JWT verification ]\n"
        "--token-algorithm                  [ JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS. ]\n"
        "--token-secret                     [ Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification. ]\n"
        "--token-public-key                 [ Path to PEM public key file or inline PEM string (for static asymmetric keys). ]\n"
        "--required-scopes                  [ Comma-separated list of required scopes (e.g., ansible.read,ansible.write). ]\n"
        "--oauth-upstream-auth-endpoint     [ Upstream authorization endpoint for OAuth Proxy ]\n"
        "--oauth-upstream-token-endpoint    [ Upstream token endpoint for OAuth Proxy ]\n"
        "--oauth-upstream-client-id         [ Upstream client ID for OAuth Proxy ]\n"
        "--oauth-upstream-client-secret     [ Upstream client secret for OAuth Proxy ]\n"
        "--oauth-base-url                   [ Base URL for OAuth Proxy ]\n"
        "--oidc-config-url                  [ OIDC configuration URL ]\n"
        "--oidc-client-id                   [ OIDC client ID ]\n"
        "--oidc-client-secret               [ OIDC client secret ]\n"
        "--oidc-base-url                    [ Base URL for OIDC Proxy ]\n"
        "--remote-auth-servers              [ Comma-separated list of authorization servers for Remote OAuth ]\n"
        "--remote-base-url                  [ Base URL for Remote OAuth ]\n"
        "--allowed-client-redirect-uris     [ Comma-separated list of allowed client redirect URIs ]\n"
        "--eunomia-type                     [ Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none) ]\n"
        "--eunomia-policy-file              [ Policy file for embedded Eunomia (default: mcp_policies.json) ]\n"
        "--eunomia-remote-url               [ URL for remote Eunomia server ]\n"
        "--enable-delegation                [ Enable OIDC token delegation ]\n"
        "--audience                         [ Audience for the delegated token ]\n"
        "--delegated-scopes                 [ Scopes for the delegated token (space-separated) ]\n"
        "--openapi-file                     [ Path to the OpenAPI JSON file to import additional tools from ]\n"
        "--openapi-base-url                 [ Base URL for the OpenAPI client (overrides instance URL) ]\n"
        "--openapi-use-token                [ Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import ]\n"
        "--openapi-username                 [ Username for basic auth during OpenAPI import ]\n"
        "--openapi-password                 [ Password for basic auth during OpenAPI import ]\n"
        "--openapi-client-id                [ OAuth client ID for OpenAPI import ]\n"
        "--openapi-client-secret            [ OAuth client secret for OpenAPI import ]\n"
        "\n"
        "Examples:\n"
        "  [Simple]  radarr-mcp \n"
        '  [Complex] radarr-mcp --transport "value" --host "value" --port "value" --auth-type "value" --token-jwks-uri "value" --token-issuer "value" --token-audience "value" --token-algorithm "value" --token-secret "value" --token-public-key "value" --required-scopes "value" --oauth-upstream-auth-endpoint "value" --oauth-upstream-token-endpoint "value" --oauth-upstream-client-id "value" --oauth-upstream-client-secret "value" --oauth-base-url "value" --oidc-config-url "value" --oidc-client-id "value" --oidc-client-secret "value" --oidc-base-url "value" --remote-auth-servers "value" --remote-base-url "value" --allowed-client-redirect-uris "value" --eunomia-type "value" --eunomia-policy-file "value" --eunomia-remote-url "value" --enable-delegation --audience "value" --delegated-scopes "value" --openapi-file "value" --openapi-base-url "value" --openapi-use-token --openapi-username "value" --openapi-password "value" --openapi-client-id "value" --openapi-client-secret "value"\n'
    )


if __name__ == "__main__":
    radarr_mcp()
