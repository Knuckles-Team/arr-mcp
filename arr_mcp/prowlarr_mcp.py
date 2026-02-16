"""
Prowlarr MCP Server.

This module implements an MCP server for Prowlarr, providing tools to manage
indexers and search across multiple indexers. It handles authentication,
middleware, and API interactions.
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
from arr_mcp.prowlarr_api import Api
from arr_mcp.utils import to_boolean, to_integer
from arr_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.10"

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
    @mcp.prompt(name="search_indexers", description="Search for indexers.")
    def search_indexers() -> str:
        """Search for indexers."""
        return "Please search for indexers."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"search"},
    )
    async def search(
        query: str = Field(default=..., description="Search query"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> List[Dict]:
        """Search for indexers using the search endpoint."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.search(query=query)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_api(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the base API information for Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_applications_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get information for a specific application by ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_applications_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_applications_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an application configuration by ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_applications_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def delete_applications_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an application configuration by ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_applications_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_applications(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get all applications managed by Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_applications()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_applications(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new application to Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_applications(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_applications_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update application configurations."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_applications_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def delete_applications_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete application configurations."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_applications_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_applications_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the configuration schema for applications."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_applications_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_applications_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing custom filter by its ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_applications_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_applications_testall(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific custom filter by its ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_applications_testall()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_applications_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new download client to Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_applications_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_appprofile(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing download client configuration."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_appprofile(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_appprofile(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a download client from Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_appprofile()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def delete_appprofile_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all configured download clients."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_appprofile_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_appprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple download clients."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_appprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_appprofile_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete multiple download clients."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_appprofile_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_appprofile_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the configuration schema for download clients."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_appprofile_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_login(
        returnUrl: str = Field(default=None, description="returnUrl"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test a download client configuration."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_login(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all configured download clients."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_logout(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform an action on a download client."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_backup(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve download client configuration by ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def delete_system_backup_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update download client configuration by ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all download client configurations."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_upload(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Browse the local filesystem."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"operations"},
    )
    async def get_command_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get information about a specific filesystem path."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"operations"},
    )
    async def delete_command_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the current health status of Prowlarr."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"operations"},
    )
    async def post_command(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve Prowlarr activity history."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"operations"},
    )
    async def get_command(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve activity history since a specific date."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific custom filter by its ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"profiles"},
    )
    async def put_customfilter_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a custom filter by its ID."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"profiles"},
    )
    async def delete_customfilter_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get application info."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get custom filters."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"profiles"},
    )
    async def post_customfilter(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an application."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_config_development_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific application."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_config_development_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_development_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get application schema."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_development_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_development(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system backups."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_development()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a system backup."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update download client."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete download client."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get downloadclient."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new downloadclient."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update downloadclient bulk."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete downloadclient bulk."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update general configuration."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test downloadclient."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_testall(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new downloadclient testall."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new download client."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config downloadclient."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def put_config_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a download client."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config downloadclient."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_filesystem(
        path: str = Field(default=None, description="path"),
        includeFiles: bool = Field(default=None, description="includeFiles"),
        allowFoldersWithoutTrailingSlashes: bool = Field(
            default=None, description="allowFoldersWithoutTrailingSlashes"
        ),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get filesystem."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_filesystem(
            path=path,
            includeFiles=includeFiles,
            allowFoldersWithoutTrailingSlashes=allowFoldersWithoutTrailingSlashes,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_filesystem_type(
        path: str = Field(default=None, description="path"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get filesystem type."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_health(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system health."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"history"},
    )
    async def get_history(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        eventType: List = Field(default=None, description="eventType"),
        successful: bool = Field(default=None, description="successful"),
        downloadId: str = Field(default=None, description="downloadId"),
        indexerIds: List = Field(default=None, description="indexerIds"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_history(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            eventType=eventType,
            successful=successful,
            downloadId=downloadId,
            indexerIds=indexerIds,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"history"},
    )
    async def get_history_since(
        date: str = Field(default=None, description="date"),
        eventType: str = Field(default=None, description="eventType"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history since date."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_history_since(date=date, eventType=eventType)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"history"},
    )
    async def get_history_indexer(
        indexerId: int = Field(default=None, description="indexerId"),
        eventType: str = Field(default=None, description="eventType"),
        limit: int = Field(default=None, description="limit"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer history."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_history_indexer(
            indexerId=indexerId, eventType=eventType, limit=limit
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_host_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific host config."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_config_host_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update host config."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_host(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get host config."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an indexer."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an indexer."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexers."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update indexers."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete indexers."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer schema."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test an indexer."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_testall(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all indexers."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer action name."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_categories(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer categories."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer_categories()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerproxy_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexerproxy."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexerproxy_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def put_indexerproxy_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexerproxy id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_indexerproxy_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexerproxy_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete indexerproxy id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_indexerproxy_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerproxy(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexerproxy."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexerproxy()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexerproxy(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexerproxy."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexerproxy(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerproxy_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexerproxy schema."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexerproxy_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexerproxy_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test indexerproxy."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexerproxy_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexerproxy_testall(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexerproxy testall."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexerproxy_testall()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def post_indexerproxy_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexerproxy action name."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_indexerproxy_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerstats(
        startDate: str = Field(default=None, description="startDate"),
        endDate: str = Field(default=None, description="endDate"),
        indexers: str = Field(default=None, description="indexers"),
        protocols: str = Field(default=None, description="protocols"),
        tags: str = Field(default=None, description="tags"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexerstats."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexerstats(
            startDate=startDate,
            endDate=endDate,
            indexers=indexers,
            protocols=protocols,
            tags=tags,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerstatus(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexerstatus."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexerstatus()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_localization(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_localization_options(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization options."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_localization_options()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_log(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        level: str = Field(default=None, description="level"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_log(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            level=level,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_log_file(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_log_file_filename(
        filename: str = Field(default=..., description="filename"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file filename."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id_newznab(
        id: int = Field(default=..., description="id"),
        t: str = Field(default=None, description="t"),
        q: str = Field(default=None, description="q"),
        cat: str = Field(default=None, description="cat"),
        imdbid: str = Field(default=None, description="imdbid"),
        tmdbid: int = Field(default=None, description="tmdbid"),
        extended: str = Field(default=None, description="extended"),
        limit: int = Field(default=None, description="limit"),
        offset: int = Field(default=None, description="offset"),
        minage: int = Field(default=None, description="minage"),
        maxage: int = Field(default=None, description="maxage"),
        minsize: int = Field(default=None, description="minsize"),
        maxsize: int = Field(default=None, description="maxsize"),
        rid: int = Field(default=None, description="rid"),
        tvmazeid: int = Field(default=None, description="tvmazeid"),
        traktid: int = Field(default=None, description="traktid"),
        tvdbid: int = Field(default=None, description="tvdbid"),
        doubanid: int = Field(default=None, description="doubanid"),
        season: int = Field(default=None, description="season"),
        ep: str = Field(default=None, description="ep"),
        album: str = Field(default=None, description="album"),
        artist: str = Field(default=None, description="artist"),
        label: str = Field(default=None, description="label"),
        track: str = Field(default=None, description="track"),
        year: int = Field(default=None, description="year"),
        genre: str = Field(default=None, description="genre"),
        author: str = Field(default=None, description="author"),
        title: str = Field(default=None, description="title"),
        publisher: str = Field(default=None, description="publisher"),
        configured: str = Field(default=None, description="configured"),
        source: str = Field(default=None, description="source"),
        host: str = Field(default=None, description="host"),
        server: str = Field(default=None, description="server"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer newznab."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer_id_newznab(
            id=id,
            t=t,
            q=q,
            cat=cat,
            imdbid=imdbid,
            tmdbid=tmdbid,
            extended=extended,
            limit=limit,
            offset=offset,
            minage=minage,
            maxage=maxage,
            minsize=minsize,
            maxsize=maxsize,
            rid=rid,
            tvmazeid=tvmazeid,
            traktid=traktid,
            tvdbid=tvdbid,
            doubanid=doubanid,
            season=season,
            ep=ep,
            album=album,
            artist=artist,
            label=label,
            track=track,
            year=year,
            genre=genre,
            author=author,
            title=title,
            publisher=publisher,
            configured=configured,
            source=source,
            host=host,
            server=server,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_id_api(
        id: int = Field(default=..., description="id"),
        t: str = Field(default=None, description="t"),
        q: str = Field(default=None, description="q"),
        cat: str = Field(default=None, description="cat"),
        imdbid: str = Field(default=None, description="imdbid"),
        tmdbid: int = Field(default=None, description="tmdbid"),
        extended: str = Field(default=None, description="extended"),
        limit: int = Field(default=None, description="limit"),
        offset: int = Field(default=None, description="offset"),
        minage: int = Field(default=None, description="minage"),
        maxage: int = Field(default=None, description="maxage"),
        minsize: int = Field(default=None, description="minsize"),
        maxsize: int = Field(default=None, description="maxsize"),
        rid: int = Field(default=None, description="rid"),
        tvmazeid: int = Field(default=None, description="tvmazeid"),
        traktid: int = Field(default=None, description="traktid"),
        tvdbid: int = Field(default=None, description="tvdbid"),
        doubanid: int = Field(default=None, description="doubanid"),
        season: int = Field(default=None, description="season"),
        ep: str = Field(default=None, description="ep"),
        album: str = Field(default=None, description="album"),
        artist: str = Field(default=None, description="artist"),
        label: str = Field(default=None, description="label"),
        track: str = Field(default=None, description="track"),
        year: int = Field(default=None, description="year"),
        genre: str = Field(default=None, description="genre"),
        author: str = Field(default=None, description="author"),
        title: str = Field(default=None, description="title"),
        publisher: str = Field(default=None, description="publisher"),
        configured: str = Field(default=None, description="configured"),
        source: str = Field(default=None, description="source"),
        host: str = Field(default=None, description="host"),
        server: str = Field(default=None, description="server"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific id api."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_id_api(
            id=id,
            t=t,
            q=q,
            cat=cat,
            imdbid=imdbid,
            tmdbid=tmdbid,
            extended=extended,
            limit=limit,
            offset=offset,
            minage=minage,
            maxage=maxage,
            minsize=minsize,
            maxsize=maxsize,
            rid=rid,
            tvmazeid=tvmazeid,
            traktid=traktid,
            tvdbid=tvdbid,
            doubanid=doubanid,
            season=season,
            ep=ep,
            album=album,
            artist=artist,
            label=label,
            track=track,
            year=year,
            genre=genre,
            author=author,
            title=title,
            publisher=publisher,
            configured=configured,
            source=source,
            host=host,
            server=server,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id_download(
        id: int = Field(default=..., description="id"),
        link: str = Field(default=None, description="link"),
        file: str = Field(default=None, description="file"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer download."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_indexer_id_download(id=id, link=link, file=file)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"indexer"},
    )
    async def get_id_download(
        id: int = Field(default=..., description="id"),
        link: str = Field(default=None, description="link"),
        file: str = Field(default=None, description="file"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific id download."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_id_download(id=id, link=link, file=file)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def get_notification_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific notification."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def put_notification_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update notification id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def delete_notification_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete notification id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def get_notification(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notification."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def post_notification(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def get_notification_schema(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notification schema."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def post_notification_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test notification."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def post_notification_testall(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification testall."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"config"},
    )
    async def post_notification_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification action name."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_ping(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get ping."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"search"},
    )
    async def post_search(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new search."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_search(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"search"},
    )
    async def get_search(
        query: str = Field(default=None, description="query"),
        type: str = Field(default=None, description="type"),
        indexerIds: List = Field(default=None, description="indexerIds"),
        categories: List = Field(default=None, description="categories"),
        limit: int = Field(default=None, description="limit"),
        offset: int = Field(default=None, description="offset"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get search."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_search(
            query=query,
            type=type,
            indexerIds=indexerIds,
            categories=categories,
            limit=limit,
            offset=offset,
        )

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"search"},
    )
    async def post_search_bulk(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new search bulk."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_search_bulk(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_content_path(
        path: str = Field(default=..., description="path"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get content path."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_(
        path: str = Field(default=..., description="path"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get ."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_path(
        path: str = Field(default=..., description="path"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get path."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_status(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system status."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_routes(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system routes."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_routes_duplicate(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system routes duplicate."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_system_shutdown(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new system shutdown."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_system_restart(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new system restart."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_tag_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific tag."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_tag_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update tag id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def delete_tag_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete tag id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_tag(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get tag."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def post_tag(
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new tag."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific tag detail."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get tag detail."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_task(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system task."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_system_task_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific system task."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def put_config_ui_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config ui id."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_ui_id(
        id: int = Field(default=..., description="id"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific config ui."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_config_ui(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config ui."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_update(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get update."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update(
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file update."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["prowlarr_base_url", "prowlarr_api_key", "prowlarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update_filename(
        filename: str = Field(default=..., description="filename"),
        prowlarr_base_url: str = Field(
            default=os.environ.get("PROWLARR_BASE_URL", None), description="Base URL"
        ),
        prowlarr_api_key: Optional[str] = Field(
            default=os.environ.get("PROWLARR_API_KEY", None), description="API Key"
        ),
        prowlarr_verify: bool = Field(
            default=to_boolean(os.environ.get("PROWLARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file update filename."""
        client = Api(
            base_url=prowlarr_base_url, token=prowlarr_api_key, verify=prowlarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def prowlarr_mcp():
    print(f"Prowlarr MCP v{__version__}")
    parser = argparse.ArgumentParser(add_help=False, description="Prowlarr MCP")

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

    mcp = FastMCP("Prowlarr", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Prowlarr MCP v{__version__}")
    print("\nStarting Prowlarr MCP Server")
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
        f"Arr Mcp ({__version__}): Prowlarr MCP Server\n\n"
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
        "  [Simple]  prowlarr-mcp \n"
        '  [Complex] prowlarr-mcp --transport "value" --host "value" --port "value" --auth-type "value" --token-jwks-uri "value" --token-issuer "value" --token-audience "value" --token-algorithm "value" --token-secret "value" --token-public-key "value" --required-scopes "value" --oauth-upstream-auth-endpoint "value" --oauth-upstream-token-endpoint "value" --oauth-upstream-client-id "value" --oauth-upstream-client-secret "value" --oauth-base-url "value" --oidc-config-url "value" --oidc-client-id "value" --oidc-client-secret "value" --oidc-base-url "value" --remote-auth-servers "value" --remote-base-url "value" --allowed-client-redirect-uris "value" --eunomia-type "value" --eunomia-policy-file "value" --eunomia-remote-url "value" --enable-delegation --audience "value" --delegated-scopes "value" --openapi-file "value" --openapi-base-url "value" --openapi-use-token --openapi-username "value" --openapi-password "value" --openapi-client-id "value" --openapi-client-secret "value"\n'
    )


if __name__ == "__main__":
    prowlarr_mcp()
