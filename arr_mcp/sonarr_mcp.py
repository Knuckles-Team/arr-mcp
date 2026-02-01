#!/usr/bin/env python
# coding: utf-8
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
from arr_mcp.sonarr_api import Api
from arr_mcp.utils import to_boolean, to_integer
from arr_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.1.1"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,  # Will be fetched dynamically from OIDC config
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


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ApiInfo"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Authentication"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"StaticResource"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Authentication"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_autotagging(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_autotagging_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"AutoTagging"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_autotagging_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Backup"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Backup"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Backup"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Backup"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Blocklist"},
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
        """No description"""
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
        tags={"Blocklist"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_blocklist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Blocklist"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_blocklist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Calendar"},
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
        """No description"""
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
        tags={"Calendar"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_calendar_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CalendarFeed"},
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
        """No description"""
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
        tags={"Command"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Command"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Command"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Command"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFilter"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFilter"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFilter"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFilter"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFilter"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_customformat(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customformat_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"CustomFormat"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_customformat_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Cutoff"},
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
        """No description"""
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
        tags={"Cutoff"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_cutoff_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_delayprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_delayprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_delayprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DelayProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_delayprofile_reorder_id(id=id, after=after)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DiskSpace"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_diskspace()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClient"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClientConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClientConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"DownloadClientConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Episode"},
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
        """No description"""
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
        tags={"Episode"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episode_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Episode"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episode_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Episode"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episode_monitor(data=data, includeImages=includeImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episodefile(seriesId=seriesId, episodeFileIds=episodeFileIds)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_episodefile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_episodefile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_episodefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"EpisodeFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_episodefile_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"FileSystem"},
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
        """No description"""
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
        tags={"FileSystem"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"FileSystem"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_filesystem_mediafiles(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Health"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"History"},
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
        """No description"""
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
        tags={"History"},
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
        """No description"""
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
        tags={"History"},
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
        """No description"""
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
        tags={"History"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_history_failed_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"HostConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"HostConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"HostConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlist_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlist_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportList"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlist_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_importlist()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_importlist_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_importlistexclusion(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion_paged(
            page=page, pageSize=pageSize, sortKey=sortKey, sortDirection=sortDirection
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_importlistexclusion_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ImportListExclusion"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_importlistexclusion_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Indexer"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"IndexerConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_indexer()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"IndexerConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_indexer_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"IndexerConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"IndexerFlag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_indexerflag()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Language"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_language()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Language"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_language_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_languageprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_languageprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_languageprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LanguageProfileSchema"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_languageprofile_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Localization"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Localization"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization_language()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Localization"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_localization_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Log"},
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
        """No description"""
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
        tags={"LogFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"LogFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ManualImport"},
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
        """No description"""
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
        tags={"ManualImport"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_manualimport(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"MediaCover"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_mediacover_series_id_filename(
            seriesId=seriesId, filename=filename
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"MediaManagementConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_mediamanagement()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"MediaManagementConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_mediamanagement_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"MediaManagementConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_mediamanagement_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_metadata_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_metadata_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Metadata"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_metadata_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Missing"},
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
        """No description"""
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
        tags={"Missing"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_wanted_missing_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"NamingConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_naming()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"NamingConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_naming_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"NamingConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_naming_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"NamingConfig"},
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
        """No description"""
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
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Notification"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Parse"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_parse(title=title, path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Ping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityDefinition"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualitydefinition_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityDefinition"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityDefinition"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityDefinition"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualitydefinition_update(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityDefinition"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualitydefinition_limits()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_qualityprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_qualityprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QualityProfileSchema"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_qualityprofile_schema()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Queue"},
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
        """No description"""
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
        tags={"Queue"},
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
        """No description"""
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
        tags={"Queue"},
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
        """No description"""
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
        tags={"QueueAction"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_queue_grab_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QueueAction"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_queue_grab_bulk(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"QueueDetails"},
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
        """No description"""
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
        tags={"QueueStatus"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_queue_status()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Release"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_release(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Release"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_release(
            seriesId=seriesId, episodeId=episodeId, seasonNumber=seasonNumber
        )

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleaseProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_releaseprofile(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleaseProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_releaseprofile()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleaseProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleaseProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_releaseprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleaseProfile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"ReleasePush"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_release_push(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RemotePathMapping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_remotepathmapping(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RemotePathMapping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_remotepathmapping()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RemotePathMapping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RemotePathMapping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_remotepathmapping_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RemotePathMapping"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RenameEpisode"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rename(seriesId=seriesId, seasonNumber=seasonNumber)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RootFolder"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_rootfolder(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RootFolder"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rootfolder()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RootFolder"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"RootFolder"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"SeasonPass"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_seasonpass(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Series"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series(tvdbId=tvdbId, includeSeasonImages=includeSeasonImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Series"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_series(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Series"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_id(id=id, includeSeasonImages=includeSeasonImages)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Series"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_series_id(id=id, data=data, moveFiles=moveFiles)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Series"},
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
        """No description"""
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
        tags={"SeriesEditor"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_series_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"SeriesEditor"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_series_editor(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"SeriesFolder"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_id_folder(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"SeriesImport"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_series_import(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"SeriesLookup"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_series_lookup(term=term)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"StaticResource"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"StaticResource"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"StaticResource"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"System"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"System"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"System"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"System"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"System"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Tag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Tag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Tag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Tag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Tag"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"TagDetails"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"TagDetails"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Task"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Task"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"UiConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"UiConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"UiConfig"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"Update"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"UpdateLogFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["sonarr_base_url", "sonarr_api_key", "sonarr_verify"],
        tags={"UpdateLogFile"},
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
        """No description"""
        client = Api(
            base_url=sonarr_base_url, token=sonarr_api_key, verify=sonarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def sonarr_mcp():
    print(f"sonarr_mcp v{__version__}")
    parser = argparse.ArgumentParser(description="Sonarr MCP")

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
    # JWT/Token params
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
    # OAuth Proxy params
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
    # OIDC Proxy params
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    # Remote OAuth params
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    # Common
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    # Eunomia params
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
    # Delegation params
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

    args = parser.parse_args()

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    # Update config with CLI arguments
    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    # Configure delegation if enabled
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

        # Fetch OIDC configuration to get token_endpoint
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

    # Set auth based on type
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
        # Fallback to env vars if not provided via CLI
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

        # Load static public key from file if path is given
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
            public_key_pem = args.token_public_key  # Inline PEM

        # Validation: Conflicting options
        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        # HMAC mode
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

        # Required scopes
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

    # === 2. Build Middleware List ===
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
