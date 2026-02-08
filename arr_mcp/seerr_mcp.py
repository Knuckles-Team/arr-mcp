#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import sys
import logging
from typing import Optional, List, Dict, Union

import requests
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger
from arr_mcp.seerr_api import Api
from arr_mcp.utils import to_boolean, to_integer

__version__ = "0.1.0"

logger = get_logger(name="SeerrMCP")
logger.setLevel(logging.DEBUG)

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(value=os.getenv("PORT", "8000"))


def register_prompts(mcp: FastMCP):
    @mcp.prompt(name="search_media", description="Search for media to request.")
    def search_media(query: str) -> str:
        """Search for media."""
        return f"Please search for '{query}' and show me the results."


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Status"},
    )
    async def get_status(
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get Seerr status"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_status()

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Status"},
    )
    async def get_status_appdata(
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get application data volume status"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_status_appdata()

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Authentication"},
    )
    async def get_auth_me(
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get logged-in user"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_auth_me()

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def post_request(
        media_type: str = Field(..., description="mediaType (movie or tv)"),
        media_id: int = Field(..., description="mediaId (TMDB ID)"),
        seasons: List[int] = Field(default=None, description="seasons (for TV)"),
        is4k: bool = Field(default=False, description="is4k"),
        server_id: int = Field(default=None, description="serverId"),
        profile_id: int = Field(default=None, description="profileId"),
        root_folder: str = Field(default=None, description="rootFolder"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Create a new request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.post_request(
            media_type=media_type,
            media_id=media_id,
            seasons=seasons,
            is4k=is4k,
            server_id=server_id,
            profile_id=profile_id,
            root_folder=root_folder,
        )

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def get_request(
        take: int = Field(default=20, description="take"),
        skip: int = Field(default=0, description="skip"),
        filter: str = Field(default=None, description="filter (available, approved, processing, pending, unavailable, failed)"),
        sort: str = Field(default='added', description="sort (added, modified)"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get all requests"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_request(take=take, skip=skip, filter=filter, sort=sort)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def get_request_id(
        request_id: int = Field(..., description="request_id"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_request_id(request_id=request_id)
    
    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def put_request_id(
        request_id: int = Field(..., description="request_id"),
        media_type: str = Field(..., description="mediaType"),
        seasons: List[int] = Field(default=None, description="seasons"),
        server_id: int = Field(default=None, description="serverId"),
        profile_id: int = Field(default=None, description="profileId"),
        root_folder: str = Field(default=None, description="rootFolder"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.put_request_id(
            request_id=request_id,
            media_type=media_type,
            seasons=seasons,
            server_id=server_id,
            profile_id=profile_id,
            root_folder=root_folder,
        )

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def delete_request_id(
        request_id: int = Field(..., description="request_id"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.delete_request_id(request_id=request_id)
        
    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def approve_request(
        request_id: int = Field(..., description="request_id"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Approve a request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.post_request_id_approve(request_id=request_id)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Request"},
    )
    async def decline_request(
        request_id: int = Field(..., description="request_id"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Decline a request"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.post_request_id_decline(request_id=request_id)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Movie"},
    )
    async def get_movie(
        movie_id: int = Field(..., description="movie_id (TMDB ID)"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get movie details"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_movie_id(movie_id=movie_id)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"TV"},
    )
    async def get_tv(
        tv_id: int = Field(..., description="tv_id (TMDB ID)"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get TV details"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_tv_id(tv_id=tv_id)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"Search"},
    )
    async def search(
        query: str = Field(..., description="query"),
        page: int = Field(default=1, description="page"),
        language: str = Field(default="en", description="language"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Search for content"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_search(query=query, page=page, language=language)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"User"},
    )
    async def get_users(
        take: int = Field(default=20, description="take"),
        skip: int = Field(default=0, description="skip"),
        sort: str = Field(default='created', description="sort"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get all users"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_user(take=take, skip=skip, sort=sort)

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"User"},
    )
    async def get_user_id(
        user_id: int = Field(..., description="user_id"),
        seerr_base_url: str = Field(
            default=os.environ.get("SEERR_BASE_URL", None), description="Base URL"
        ),
        seerr_api_key: Optional[str] = Field(
            default=os.environ.get("SEERR_API_KEY", None), description="API Key"
        ),
        seerr_verify: bool = Field(
            default=to_boolean(os.environ.get("SEERR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get user details"""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_user_id(user_id=user_id)


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(
        name="Seerr",
        dependencies=["requests", "fastmcp"],
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
    )

    register_prompts(mcp)
    register_tools(mcp)

    return mcp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seerr MCP Server")
    parser.add_argument(
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "sse"],
        help="Transport protocol to use",
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind to (for SSE)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port to bind to (for SSE)",
    )
    args = parser.parse_args()

    mcp = create_mcp_server()

    if args.transport == "sse":
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
