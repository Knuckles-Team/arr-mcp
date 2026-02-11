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
from arr_mcp.lidarr_api import Api
from arr_mcp.utils import to_boolean, to_integer
from arr_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.3"

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


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="search_artist", description="Search for an artist.")
    def search_artist() -> str:
        """Search for an artist."""
        return "Please search for an artist."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def get_album(
        artistId: int = Field(default=None, description="artistId"),
        albumIds: List = Field(default=None, description="albumIds"),
        foreignAlbumId: str = Field(default=None, description="foreignAlbumId"),
        includeAllArtistAlbums: bool = Field(
            default=None, description="includeAllArtistAlbums"
        ),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_album(
            artistId=artistId,
            albumIds=albumIds,
            foreignAlbumId=foreignAlbumId,
            includeAllArtistAlbums=includeAllArtistAlbums,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def post_album(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_album(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def put_album_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_album_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def delete_album_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportListExclusion: bool = Field(
            default=None, description="addImportListExclusion"
        ),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_album_id(
            id=id,
            deleteFiles=deleteFiles,
            addImportListExclusion=addImportListExclusion,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def get_album_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_album_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Album"},
    )
    async def put_album_monitor(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_album_monitor(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AlbumLookup"},
    )
    async def get_album_lookup(
        term: str = Field(default=None, description="term"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_album_lookup(term=term)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AlbumStudio"},
    )
    async def post_albumstudio(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_albumstudio(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ApiInfo"},
    )
    async def get_api(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Artist"},
    )
    async def get_artist_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_artist_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Artist"},
    )
    async def put_artist_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        moveFiles: bool = Field(default=None, description="moveFiles"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_artist_id(id=id, data=data, moveFiles=moveFiles)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Artist"},
    )
    async def delete_artist_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportListExclusion: bool = Field(
            default=None, description="addImportListExclusion"
        ),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_artist_id(
            id=id,
            deleteFiles=deleteFiles,
            addImportListExclusion=addImportListExclusion,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Artist"},
    )
    async def get_artist(
        mbId: str = Field(default=None, description="mbId"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_artist(mbId=mbId)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Artist"},
    )
    async def post_artist(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_artist(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ArtistEditor"},
    )
    async def put_artist_editor(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_artist_editor(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ArtistEditor"},
    )
    async def delete_artist_editor(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_artist_editor(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ArtistLookup"},
    )
    async def get_artist_lookup(
        term: str = Field(default=None, description="term"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_artist_lookup(term=term)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Authentication"},
    )
    async def post_login(
        returnUrl: str = Field(default=None, description="returnUrl"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"StaticResource"},
    )
    async def get_login(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Authentication"},
    )
    async def get_logout(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def get_autotagging_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def put_autotagging_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_autotagging_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def delete_autotagging_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_autotagging_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def post_autotagging(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_autotagging(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def get_autotagging(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_autotagging()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"AutoTagging"},
    )
    async def get_autotagging_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_autotagging_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Backup"},
    )
    async def get_system_backup(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Backup"},
    )
    async def delete_system_backup_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Backup"},
    )
    async def post_system_backup_restore_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Backup"},
    )
    async def post_system_backup_restore_upload(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Blocklist"},
    )
    async def get_blocklist(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_blocklist(
            page=page, pageSize=pageSize, sortKey=sortKey, sortDirection=sortDirection
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Blocklist"},
    )
    async def delete_blocklist_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_blocklist_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Blocklist"},
    )
    async def delete_blocklist_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_blocklist_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Calendar"},
    )
    async def get_calendar(
        start: str = Field(default=None, description="start"),
        end: str = Field(default=None, description="end"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        tags: str = Field(default=None, description="tags"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_calendar(
            start=start,
            end=end,
            unmonitored=unmonitored,
            includeArtist=includeArtist,
            tags=tags,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Calendar"},
    )
    async def get_calendar_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_calendar_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CalendarFeed"},
    )
    async def get_feed_v1_calendar_lidarrics(
        pastDays: int = Field(default=None, description="pastDays"),
        futureDays: int = Field(default=None, description="futureDays"),
        tags: str = Field(default=None, description="tags"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_feed_v1_calendar_lidarrics(
            pastDays=pastDays, futureDays=futureDays, tags=tags, unmonitored=unmonitored
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Command"},
    )
    async def get_command_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Command"},
    )
    async def delete_command_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Command"},
    )
    async def post_command(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Command"},
    )
    async def get_command(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFilter"},
    )
    async def get_customfilter_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFilter"},
    )
    async def put_customfilter_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFilter"},
    )
    async def delete_customfilter_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFilter"},
    )
    async def get_customfilter(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFilter"},
    )
    async def post_customfilter(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def get_customformat_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def put_customformat_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_customformat_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def delete_customformat_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def get_customformat(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_customformat()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def post_customformat(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_customformat(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def put_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def delete_customformat_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_customformat_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"CustomFormat"},
    )
    async def get_customformat_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_customformat_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Cutoff"},
    )
    async def get_wanted_cutoff(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        monitored: bool = Field(default=None, description="monitored"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_wanted_cutoff(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeArtist=includeArtist,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Cutoff"},
    )
    async def get_wanted_cutoff_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_wanted_cutoff_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def post_delayprofile(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_delayprofile(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def get_delayprofile(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_delayprofile()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def delete_delayprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def put_delayprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_delayprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def get_delayprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DelayProfile"},
    )
    async def put_delayprofile_reorder_id(
        id: int = Field(default=..., description="id"),
        afterId: int = Field(default=None, description="afterId"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_delayprofile_reorder_id(id=id, afterId=afterId)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DiskSpace"},
    )
    async def get_diskspace(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_diskspace()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def get_downloadclient_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def put_downloadclient_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def delete_downloadclient_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def get_downloadclient(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def post_downloadclient(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def put_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def delete_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def get_downloadclient_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def post_downloadclient_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def post_downloadclient_testall(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClient"},
    )
    async def post_downloadclient_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClientConfig"},
    )
    async def get_config_downloadclient_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClientConfig"},
    )
    async def put_config_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"DownloadClientConfig"},
    )
    async def get_config_downloadclient(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"FileSystem"},
    )
    async def get_filesystem(
        path: str = Field(default=None, description="path"),
        includeFiles: bool = Field(default=None, description="includeFiles"),
        allowFoldersWithoutTrailingSlashes: bool = Field(
            default=None, description="allowFoldersWithoutTrailingSlashes"
        ),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_filesystem(
            path=path,
            includeFiles=includeFiles,
            allowFoldersWithoutTrailingSlashes=allowFoldersWithoutTrailingSlashes,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"FileSystem"},
    )
    async def get_filesystem_type(
        path: str = Field(default=None, description="path"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"FileSystem"},
    )
    async def get_filesystem_mediafiles(
        path: str = Field(default=None, description="path"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_filesystem_mediafiles(path=path)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Health"},
    )
    async def get_health(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"History"},
    )
    async def get_history(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        includeAlbum: bool = Field(default=None, description="includeAlbum"),
        includeTrack: bool = Field(default=None, description="includeTrack"),
        eventType: List = Field(default=None, description="eventType"),
        albumId: int = Field(default=None, description="albumId"),
        downloadId: str = Field(default=None, description="downloadId"),
        artistIds: List = Field(default=None, description="artistIds"),
        quality: List = Field(default=None, description="quality"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_history(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeArtist=includeArtist,
            includeAlbum=includeAlbum,
            includeTrack=includeTrack,
            eventType=eventType,
            albumId=albumId,
            downloadId=downloadId,
            artistIds=artistIds,
            quality=quality,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"History"},
    )
    async def get_history_since(
        date: str = Field(default=None, description="date"),
        eventType: str = Field(default=None, description="eventType"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        includeAlbum: bool = Field(default=None, description="includeAlbum"),
        includeTrack: bool = Field(default=None, description="includeTrack"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_history_since(
            date=date,
            eventType=eventType,
            includeArtist=includeArtist,
            includeAlbum=includeAlbum,
            includeTrack=includeTrack,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"History"},
    )
    async def get_history_artist(
        artistId: int = Field(default=None, description="artistId"),
        albumId: int = Field(default=None, description="albumId"),
        eventType: str = Field(default=None, description="eventType"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        includeAlbum: bool = Field(default=None, description="includeAlbum"),
        includeTrack: bool = Field(default=None, description="includeTrack"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_history_artist(
            artistId=artistId,
            albumId=albumId,
            eventType=eventType,
            includeArtist=includeArtist,
            includeAlbum=includeAlbum,
            includeTrack=includeTrack,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"History"},
    )
    async def post_history_failed_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_history_failed_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"HostConfig"},
    )
    async def get_config_host_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"HostConfig"},
    )
    async def put_config_host_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"HostConfig"},
    )
    async def get_config_host(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def get_importlist_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def put_importlist_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_importlist_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def delete_importlist_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def get_importlist(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_importlist()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def post_importlist(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_importlist(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def put_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def delete_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def get_importlist_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_importlist_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def post_importlist_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_importlist_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def post_importlist_testall(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_importlist_testall()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportList"},
    )
    async def post_importlist_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_importlist_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportListExclusion"},
    )
    async def get_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportListExclusion"},
    )
    async def put_importlistexclusion_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_importlistexclusion_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportListExclusion"},
    )
    async def delete_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportListExclusion"},
    )
    async def get_importlistexclusion(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_importlistexclusion()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ImportListExclusion"},
    )
    async def post_importlistexclusion(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_importlistexclusion(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def get_indexer_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def put_indexer_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def delete_indexer_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def get_indexer(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def post_indexer(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def put_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def delete_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def get_indexer_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def post_indexer_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def post_indexer_testall(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Indexer"},
    )
    async def post_indexer_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"IndexerConfig"},
    )
    async def get_config_indexer_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"IndexerConfig"},
    )
    async def put_config_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_indexer_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"IndexerConfig"},
    )
    async def get_config_indexer(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_indexer()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"IndexerFlag"},
    )
    async def get_indexerflag(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_indexerflag()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Language"},
    )
    async def get_language_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_language_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Language"},
    )
    async def get_language(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_language()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Localization"},
    )
    async def get_localization(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Log"},
    )
    async def get_log(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        level: str = Field(default=None, description="level"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_log(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            level=level,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"LogFile"},
    )
    async def get_log_file(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"LogFile"},
    )
    async def get_log_file_filename(
        filename: str = Field(default=..., description="filename"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ManualImport"},
    )
    async def post_manualimport(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_manualimport(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ManualImport"},
    )
    async def get_manualimport(
        folder: str = Field(default=None, description="folder"),
        downloadId: str = Field(default=None, description="downloadId"),
        artistId: int = Field(default=None, description="artistId"),
        filterExistingFiles: bool = Field(
            default=None, description="filterExistingFiles"
        ),
        replaceExistingFiles: bool = Field(
            default=None, description="replaceExistingFiles"
        ),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_manualimport(
            folder=folder,
            downloadId=downloadId,
            artistId=artistId,
            filterExistingFiles=filterExistingFiles,
            replaceExistingFiles=replaceExistingFiles,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MediaCover"},
    )
    async def get_mediacover_artist_artist_id_filename(
        artistId: int = Field(default=..., description="artistId"),
        filename: str = Field(default=..., description="filename"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_mediacover_artist_artist_id_filename(
            artistId=artistId, filename=filename
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MediaCover"},
    )
    async def get_mediacover_album_album_id_filename(
        albumId: int = Field(default=..., description="albumId"),
        filename: str = Field(default=..., description="filename"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_mediacover_album_album_id_filename(
            albumId=albumId, filename=filename
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MediaManagementConfig"},
    )
    async def get_config_mediamanagement_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_mediamanagement_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MediaManagementConfig"},
    )
    async def put_config_mediamanagement_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_mediamanagement_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MediaManagementConfig"},
    )
    async def get_config_mediamanagement(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_mediamanagement()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def get_metadata_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def put_metadata_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_metadata_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def delete_metadata_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def get_metadata(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadata()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def post_metadata(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_metadata(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def get_metadata_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadata_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def post_metadata_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_metadata_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def post_metadata_testall(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_metadata_testall()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Metadata"},
    )
    async def post_metadata_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_metadata_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfile"},
    )
    async def post_metadataprofile(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_metadataprofile(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfile"},
    )
    async def get_metadataprofile(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadataprofile()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfile"},
    )
    async def delete_metadataprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_metadataprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfile"},
    )
    async def put_metadataprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_metadataprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfile"},
    )
    async def get_metadataprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadataprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProfileSchema"},
    )
    async def get_metadataprofile_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_metadataprofile_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProviderConfig"},
    )
    async def get_config_metadataprovider_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_metadataprovider_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProviderConfig"},
    )
    async def put_config_metadataprovider_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_metadataprovider_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"MetadataProviderConfig"},
    )
    async def get_config_metadataprovider(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_metadataprovider()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Missing"},
    )
    async def get_wanted_missing(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        monitored: bool = Field(default=None, description="monitored"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_wanted_missing(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeArtist=includeArtist,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Missing"},
    )
    async def get_wanted_missing_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_wanted_missing_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"NamingConfig"},
    )
    async def get_config_naming_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_naming_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"NamingConfig"},
    )
    async def put_config_naming_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_naming_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"NamingConfig"},
    )
    async def get_config_naming(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_naming()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"NamingConfig"},
    )
    async def get_config_naming_examples(
        renameTracks: bool = Field(default=None, description="renameTracks"),
        replaceIllegalCharacters: bool = Field(
            default=None, description="replaceIllegalCharacters"
        ),
        colonReplacementFormat: int = Field(
            default=None, description="colonReplacementFormat"
        ),
        standardTrackFormat: str = Field(
            default=None, description="standardTrackFormat"
        ),
        multiDiscTrackFormat: str = Field(
            default=None, description="multiDiscTrackFormat"
        ),
        artistFolderFormat: str = Field(default=None, description="artistFolderFormat"),
        includeArtistName: bool = Field(default=None, description="includeArtistName"),
        includeAlbumTitle: bool = Field(default=None, description="includeAlbumTitle"),
        includeQuality: bool = Field(default=None, description="includeQuality"),
        replaceSpaces: bool = Field(default=None, description="replaceSpaces"),
        separator: str = Field(default=None, description="separator"),
        numberStyle: str = Field(default=None, description="numberStyle"),
        id: int = Field(default=None, description="id"),
        resourceName: str = Field(default=None, description="resourceName"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_naming_examples(
            renameTracks=renameTracks,
            replaceIllegalCharacters=replaceIllegalCharacters,
            colonReplacementFormat=colonReplacementFormat,
            standardTrackFormat=standardTrackFormat,
            multiDiscTrackFormat=multiDiscTrackFormat,
            artistFolderFormat=artistFolderFormat,
            includeArtistName=includeArtistName,
            includeAlbumTitle=includeAlbumTitle,
            includeQuality=includeQuality,
            replaceSpaces=replaceSpaces,
            separator=separator,
            numberStyle=numberStyle,
            id=id,
            resourceName=resourceName,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def get_notification_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def put_notification_id(
        id: int = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def delete_notification_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def get_notification(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def post_notification(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def get_notification_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def post_notification_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def post_notification_testall(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Notification"},
    )
    async def post_notification_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Parse"},
    )
    async def get_parse(
        title: str = Field(default=None, description="title"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_parse(title=title)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Ping"},
    )
    async def get_ping(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityDefinition"},
    )
    async def put_qualitydefinition_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_qualitydefinition_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityDefinition"},
    )
    async def get_qualitydefinition_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_qualitydefinition_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityDefinition"},
    )
    async def get_qualitydefinition(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_qualitydefinition()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityDefinition"},
    )
    async def put_qualitydefinition_update(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_qualitydefinition_update(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfile"},
    )
    async def post_qualityprofile(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_qualityprofile(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfile"},
    )
    async def get_qualityprofile(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_qualityprofile()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfile"},
    )
    async def delete_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfile"},
    )
    async def put_qualityprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_qualityprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfile"},
    )
    async def get_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QualityProfileSchema"},
    )
    async def get_qualityprofile_schema(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_qualityprofile_schema()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Queue"},
    )
    async def delete_queue_id(
        id: int = Field(default=..., description="id"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_queue_id(
            id=id,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Queue"},
    )
    async def delete_queue_bulk(
        data: Dict = Field(default=..., description="data"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_queue_bulk(
            data=data,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Queue"},
    )
    async def get_queue(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeUnknownArtistItems: bool = Field(
            default=None, description="includeUnknownArtistItems"
        ),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        includeAlbum: bool = Field(default=None, description="includeAlbum"),
        artistIds: List = Field(default=None, description="artistIds"),
        protocol: str = Field(default=None, description="protocol"),
        quality: List = Field(default=None, description="quality"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_queue(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeUnknownArtistItems=includeUnknownArtistItems,
            includeArtist=includeArtist,
            includeAlbum=includeAlbum,
            artistIds=artistIds,
            protocol=protocol,
            quality=quality,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QueueAction"},
    )
    async def post_queue_grab_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_queue_grab_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QueueAction"},
    )
    async def post_queue_grab_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_queue_grab_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QueueDetails"},
    )
    async def get_queue_details(
        artistId: int = Field(default=None, description="artistId"),
        albumIds: List = Field(default=None, description="albumIds"),
        includeArtist: bool = Field(default=None, description="includeArtist"),
        includeAlbum: bool = Field(default=None, description="includeAlbum"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_queue_details(
            artistId=artistId,
            albumIds=albumIds,
            includeArtist=includeArtist,
            includeAlbum=includeAlbum,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"QueueStatus"},
    )
    async def get_queue_status(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_queue_status()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Release"},
    )
    async def post_release(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_release(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Release"},
    )
    async def get_release(
        albumId: int = Field(default=None, description="albumId"),
        artistId: int = Field(default=None, description="artistId"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_release(albumId=albumId, artistId=artistId)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleaseProfile"},
    )
    async def get_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleaseProfile"},
    )
    async def put_releaseprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_releaseprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleaseProfile"},
    )
    async def delete_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleaseProfile"},
    )
    async def get_releaseprofile(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_releaseprofile()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleaseProfile"},
    )
    async def post_releaseprofile(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_releaseprofile(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"ReleasePush"},
    )
    async def post_release_push(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_release_push(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RemotePathMapping"},
    )
    async def get_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RemotePathMapping"},
    )
    async def delete_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RemotePathMapping"},
    )
    async def put_remotepathmapping_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_remotepathmapping_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RemotePathMapping"},
    )
    async def post_remotepathmapping(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_remotepathmapping(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RemotePathMapping"},
    )
    async def get_remotepathmapping(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_remotepathmapping()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RenameTrack"},
    )
    async def get_rename(
        artistId: int = Field(default=None, description="artistId"),
        albumId: int = Field(default=None, description="albumId"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_rename(artistId=artistId, albumId=albumId)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RetagTrack"},
    )
    async def get_retag(
        artistId: int = Field(default=None, description="artistId"),
        albumId: int = Field(default=None, description="albumId"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_retag(artistId=artistId, albumId=albumId)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RootFolder"},
    )
    async def get_rootfolder_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RootFolder"},
    )
    async def put_rootfolder_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_rootfolder_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RootFolder"},
    )
    async def delete_rootfolder_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RootFolder"},
    )
    async def post_rootfolder(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_rootfolder(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"RootFolder"},
    )
    async def get_rootfolder(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_rootfolder()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Search"},
    )
    async def get_search(
        term: str = Field(default=None, description="term"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_search(term=term)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"StaticResource"},
    )
    async def get_content_path(
        path: str = Field(default=..., description="path"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"StaticResource"},
    )
    async def get_(
        path: str = Field(default=..., description="path"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"StaticResource"},
    )
    async def get_path(
        path: str = Field(default=..., description="path"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"System"},
    )
    async def get_system_status(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"System"},
    )
    async def get_system_routes(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"System"},
    )
    async def get_system_routes_duplicate(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"System"},
    )
    async def post_system_shutdown(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"System"},
    )
    async def post_system_restart(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Tag"},
    )
    async def get_tag_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Tag"},
    )
    async def put_tag_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Tag"},
    )
    async def delete_tag_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Tag"},
    )
    async def get_tag(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Tag"},
    )
    async def post_tag(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TagDetails"},
    )
    async def get_tag_detail_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TagDetails"},
    )
    async def get_tag_detail(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Task"},
    )
    async def get_system_task(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Task"},
    )
    async def get_system_task_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Track"},
    )
    async def get_track(
        artistId: int = Field(default=None, description="artistId"),
        albumId: int = Field(default=None, description="albumId"),
        albumReleaseId: int = Field(default=None, description="albumReleaseId"),
        trackIds: List = Field(default=None, description="trackIds"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_track(
            artistId=artistId,
            albumId=albumId,
            albumReleaseId=albumReleaseId,
            trackIds=trackIds,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Track"},
    )
    async def get_track_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_track_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def get_trackfile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_trackfile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def put_trackfile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_trackfile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def delete_trackfile_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_trackfile_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def get_trackfile(
        artistId: int = Field(default=None, description="artistId"),
        trackFileIds: List = Field(default=None, description="trackFileIds"),
        albumId: List = Field(default=None, description="albumId"),
        unmapped: bool = Field(default=None, description="unmapped"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_trackfile(
            artistId=artistId,
            trackFileIds=trackFileIds,
            albumId=albumId,
            unmapped=unmapped,
        )

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def put_trackfile_editor(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_trackfile_editor(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"TrackFile"},
    )
    async def delete_trackfile_bulk(
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.delete_trackfile_bulk(data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"UiConfig"},
    )
    async def put_config_ui_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"UiConfig"},
    )
    async def get_config_ui_id(
        id: int = Field(default=..., description="id"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"UiConfig"},
    )
    async def get_config_ui(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"Update"},
    )
    async def get_update(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"UpdateLogFile"},
    )
    async def get_log_file_update(
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["lidarr_base_url", "lidarr_api_key", "lidarr_verify"],
        tags={"UpdateLogFile"},
    )
    async def get_log_file_update_filename(
        filename: str = Field(default=..., description="filename"),
        lidarr_base_url: str = Field(
            default=os.environ.get("LIDARR_BASE_URL", None), description="Base URL"
        ),
        lidarr_api_key: Optional[str] = Field(
            default=os.environ.get("LIDARR_API_KEY", None), description="API Key"
        ),
        lidarr_verify: bool = Field(
            default=to_boolean(os.environ.get("LIDARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """No description"""
        client = Api(
            base_url=lidarr_base_url, token=lidarr_api_key, verify=lidarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def lidarr_mcp():
    print(f"Lidarr MCP v{__version__}")
    parser = argparse.ArgumentParser(add_help=False, description="Lidarr MCP")

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

    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        usage()

        sys.exit(0)

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

    mcp = FastMCP("Lidarr", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Lidarr MCP v{__version__}")
    print("\nStarting Lidarr MCP Server")
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
        f"Arr Mcp ({__version__}): Lidarr MCP Server\n\n"
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
        "  [Simple]  lidarr-mcp \n"
        '  [Complex] lidarr-mcp --transport "value" --host "value" --port "value" --auth-type "value" --token-jwks-uri "value" --token-issuer "value" --token-audience "value" --token-algorithm "value" --token-secret "value" --token-public-key "value" --required-scopes "value" --oauth-upstream-auth-endpoint "value" --oauth-upstream-token-endpoint "value" --oauth-upstream-client-id "value" --oauth-upstream-client-secret "value" --oauth-base-url "value" --oidc-config-url "value" --oidc-client-id "value" --oidc-client-secret "value" --oidc-base-url "value" --remote-auth-servers "value" --remote-base-url "value" --allowed-client-redirect-uris "value" --eunomia-type "value" --eunomia-policy-file "value" --eunomia-remote-url "value" --enable-delegation --audience "value" --delegated-scopes "value" --openapi-file "value" --openapi-base-url "value" --openapi-use-token --openapi-username "value" --openapi-password "value" --openapi-client-id "value" --openapi-client-secret "value"\n'
    )


if __name__ == "__main__":
    lidarr_mcp()
