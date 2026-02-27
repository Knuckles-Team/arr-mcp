"""
Chaptarr MCP Server.

This module implements an MCP server for Chaptarr, providing tools to manage
books and authors. It handles authentication, middleware, and API interactions.
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
from arr_mcp.chaptarr_api import Api
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_parser,
    config,
)
from agent_utilities.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.21"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_api(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the base API information for Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_api()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_login(
        returnUrl: str = Field(default=None, description="returnUrl"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a login operation to the Chaptarr instance."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_login(returnUrl=returnUrl)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_login(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get the current login status for the Chaptarr instance."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_login()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_logout(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform a logout operation from the Chaptarr instance."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_logout()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_author(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get all authors managed by Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_author()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_author(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new author to Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_author(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_author_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        moveFiles: bool = Field(default=None, description="moveFiles"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an author's information by ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_author_id(id=id, data=data, moveFiles=moveFiles)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_author_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportListExclusion: bool = Field(
            default=None, description="addImportListExclusion"
        ),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an author from Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_author_id(
            id=id,
            deleteFiles=deleteFiles,
            addImportListExclusion=addImportListExclusion,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_author_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get information for a specific author by ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_author_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_author_editor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update author parameters."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_author_editor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_author_editor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete authors."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_author_editor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_author_lookup(
        term: str = Field(default=None, description="term"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Search for authors matching a term."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_author_lookup(term=term)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_backup(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all system backups."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_backup()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def delete_system_backup_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a specific system backup."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_system_backup_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Restore a system backup."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_system_backup_restore_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_system_backup_restore_upload(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Upload and restore a system backup."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_system_backup_restore_upload()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def get_blocklist(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the blocklist."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_blocklist(
            page=page, pageSize=pageSize, sortKey=sortKey, sortDirection=sortDirection
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def delete_blocklist_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an item from the blocklist."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_blocklist_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def delete_blocklist_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete items from the blocklist."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_blocklist_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_book(
        authorId: int = Field(default=None, description="authorId"),
        bookIds: List = Field(default=None, description="bookIds"),
        titleSlug: str = Field(default=None, description="titleSlug"),
        includeAllAuthorBooks: bool = Field(
            default=None, description="includeAllAuthorBooks"
        ),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_book(
            authorId=authorId,
            bookIds=bookIds,
            titleSlug=titleSlug,
            includeAllAuthorBooks=includeAllAuthorBooks,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_book(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new book."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_book(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_book_id_overview(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve overview for a specific book."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_book_id_overview(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_book_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve a paginated list of items in the blocklist."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_book_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_book_id(
        id: int = Field(default=..., description="id"),
        deleteFiles: bool = Field(default=None, description="deleteFiles"),
        addImportListExclusion: bool = Field(
            default=None, description="addImportListExclusion"
        ),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Remove an item from the blocklist by its ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_book_id(
            id=id,
            deleteFiles=deleteFiles,
            addImportListExclusion=addImportListExclusion,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_book_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk removal of items from the blocklist."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_book_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_book_monitor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific book by its ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_book_monitor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_book_editor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an existing book configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_book_editor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_book_editor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the schema for book configurations."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_book_editor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_bookfile(
        authorId: int = Field(default=None, description="authorId"),
        bookFileIds: List = Field(default=None, description="bookFileIds"),
        bookId: List = Field(default=None, description="bookId"),
        unmapped: bool = Field(default=None, description="unmapped"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all book files for a specific book."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_bookfile(
            authorId=authorId, bookFileIds=bookFileIds, bookId=bookId, unmapped=unmapped
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_bookfile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a specific book file."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_bookfile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_bookfile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific book file by its ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_bookfile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_bookfile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update multiple book files."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_bookfile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_bookfile_editor(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update book file editor."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_bookfile_editor(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_bookfile_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete book files."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_bookfile_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_book_lookup(
        term: str = Field(default=None, description="term"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Search for books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_book_lookup(term=term)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_bookshelf(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add book to bookshelf."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_bookshelf(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_calendar(
        start: str = Field(default=None, description="start"),
        end: str = Field(default=None, description="end"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get calendar events."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_calendar(
            start=start, end=end, unmonitored=unmonitored, includeAuthor=includeAuthor
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_calendar_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific calendar event."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_calendar_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_feed_v1_calendar_readarrics(
        pastDays: int = Field(default=None, description="pastDays"),
        futureDays: int = Field(default=None, description="futureDays"),
        tagList: str = Field(default=None, description="tagList"),
        unmonitored: bool = Field(default=None, description="unmonitored"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get calendar feed."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_feed_v1_calendar_readarrics(
            pastDays=pastDays,
            futureDays=futureDays,
            tagList=tagList,
            unmonitored=unmonitored,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def post_command(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Execute a command."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_command(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_command(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get all commands."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_command()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def delete_command_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a specific command."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_command_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_command_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific command by ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_command_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get custom filters."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_customfilter()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_customfilter(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new custom filter."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_customfilter(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_customfilter_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a custom filter."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_customfilter_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_customfilter_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a custom filter."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_customfilter_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific custom filter."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_customfilter_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_customformat(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new custom format."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_customformat(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a custom format."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_customformat()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_customformat_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a custom format."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_customformat_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_customformat_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific custom format."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update custom formats."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_customformat_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_customformat_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete custom formats."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_customformat_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_wanted_cutoff(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        monitored: bool = Field(default=None, description="monitored"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get custom format schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_wanted_cutoff(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeAuthor=includeAuthor,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_wanted_cutoff_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new delay profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_wanted_cutoff_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_delayprofile(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get delay profiles."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_delayprofile(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a delay profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_delayprofile()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_delayprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a delay profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific delay profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_delayprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_delayprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Reorder delay profiles."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_delayprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_delayprofile_reorder_id(
        id: int = Field(default=..., description="id"),
        afterId: int = Field(default=None, description="afterId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get disk space information."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_delayprofile_reorder_id(id=id, afterId=afterId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_development(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get download clients."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_development()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def put_config_development_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new download client."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_development_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_development_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a download client."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_development_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_diskspace(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a download client."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_diskspace()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific download client."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_downloadclient()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get download client configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_downloadclient(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update download client configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_downloadclient_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific download client configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get missing books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get books missing cutoff."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def delete_downloadclient_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_downloadclient_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_downloadclient_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Mark history item as failed."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_downloadclient_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific history item."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_downloadclient_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_testall(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get history for a book."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_downloadclient_testall()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_downloadclient_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system health."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_downloadclient_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get import lists."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_downloadclient()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_config_downloadclient_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_downloadclient_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_config_downloadclient_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_downloadclient_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_edition(
        bookId: List = Field(default=None, description="bookId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_edition(bookId=bookId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_filesystem(
        path: str = Field(default=None, description="path"),
        includeFiles: bool = Field(default=None, description="includeFiles"),
        allowFoldersWithoutTrailingSlashes: bool = Field(
            default=None, description="allowFoldersWithoutTrailingSlashes"
        ),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_filesystem(
            path=path,
            includeFiles=includeFiles,
            allowFoldersWithoutTrailingSlashes=allowFoldersWithoutTrailingSlashes,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_filesystem_type(
        path: str = Field(default=None, description="path"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update import lists."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_filesystem_type(path=path)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_filesystem_mediafiles(
        path: str = Field(default=None, description="path"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete import lists."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_filesystem_mediafiles(path=path)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_health(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get import list schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_health()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"history"},
    )
    async def get_history(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        includeBook: bool = Field(default=None, description="includeBook"),
        eventType: List = Field(default=None, description="eventType"),
        bookId: int = Field(default=None, description="bookId"),
        downloadId: str = Field(default=None, description="downloadId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test an import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_history(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeAuthor=includeAuthor,
            includeBook=includeBook,
            eventType=eventType,
            bookId=bookId,
            downloadId=downloadId,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"history"},
    )
    async def get_history_since(
        date: str = Field(default=None, description="date"),
        eventType: str = Field(default=None, description="eventType"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        includeBook: bool = Field(default=None, description="includeBook"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all import lists."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_history_since(
            date=date,
            eventType=eventType,
            includeAuthor=includeAuthor,
            includeBook=includeBook,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"history"},
    )
    async def get_history_author(
        authorId: int = Field(default=None, description="authorId"),
        bookId: int = Field(default=None, description="bookId"),
        eventType: str = Field(default=None, description="eventType"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        includeBook: bool = Field(default=None, description="includeBook"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform action on import list."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_history_author(
            authorId=authorId,
            bookId=bookId,
            eventType=eventType,
            includeAuthor=includeAuthor,
            includeBook=includeBook,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"history"},
    )
    async def post_history_failed_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get import list configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_history_failed_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_host(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update import list configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_host()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def put_config_host_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific import list configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_host_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_host_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get import list exclusions."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_host_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add import list exclusion."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_importlist()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update import list exclusion."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_importlist(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete import list exclusion."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_importlist_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific import list exclusion."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_importlist_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlist_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update an indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_importlist_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_importlist_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_importlist_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_importlist_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_testall(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk update indexers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_importlist_testall()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_importlist_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete indexers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_importlist_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_importlistexclusion(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_importlistexclusion()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_importlistexclusion(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test an indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_importlistexclusion(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def put_importlistexclusion_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all indexers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_importlistexclusion_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def delete_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform action on indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_importlistexclusion_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_importlistexclusion_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_indexer()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_indexer(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer flags."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_indexer_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get available languages."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific language."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def put_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def delete_indexer_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system logs."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_indexer_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_indexer_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log files."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_indexer_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file content."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_indexer_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_testall(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new indexer testall."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_indexer_testall()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def post_indexer_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform action on indexer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_indexer_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_indexer()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def put_config_indexer_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_indexer_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_config_indexer_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific indexer configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_indexer_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"indexer"},
    )
    async def get_indexerflag(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get indexer flags."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_indexerflag()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_language(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get available languages."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_language()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_language_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific language."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_language_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_localization(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get localization."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_localization()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_log(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        level: str = Field(default=None, description="level"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system logs."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_log(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            level=level,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_log_file(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log files."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_log_file()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_log_file_filename(
        filename: str = Field(default=..., description="filename"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get log file content."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_log_file_filename(filename=filename)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_manualimport(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new manualimport."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_manualimport(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_manualimport(
        folder: str = Field(default=None, description="folder"),
        downloadId: str = Field(default=None, description="downloadId"),
        authorId: int = Field(default=None, description="authorId"),
        filterExistingFiles: bool = Field(
            default=None, description="filterExistingFiles"
        ),
        replaceExistingFiles: bool = Field(
            default=None, description="replaceExistingFiles"
        ),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get manualimport."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_manualimport(
            folder=folder,
            downloadId=downloadId,
            authorId=authorId,
            filterExistingFiles=filterExistingFiles,
            replaceExistingFiles=replaceExistingFiles,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_mediacover_author_author_id_filename(
        authorId: int = Field(default=..., description="authorId"),
        filename: str = Field(default=..., description="filename"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific mediacover author author filename."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_mediacover_author_author_id_filename(
            authorId=authorId, filename=filename
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_mediacover_book_book_id_filename(
        bookId: int = Field(default=..., description="bookId"),
        filename: str = Field(default=..., description="filename"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific mediacover book book filename."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_mediacover_book_book_id_filename(
            bookId=bookId, filename=filename
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get config mediamanagement."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_mediamanagement()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_config_mediamanagement_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update config mediamanagement id."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_mediamanagement_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_mediamanagement_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific media management configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_mediamanagement_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_metadata(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata consumers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadata()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_metadata(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_metadata(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def put_metadata_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_metadata_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def delete_metadata_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_metadata_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadata_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_metadata_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadata_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_metadata_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_metadata_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_metadata_testall(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all metadata consumers."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_metadata_testall()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def post_metadata_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform action on metadata consumer."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_metadata_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_metadataprofile(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new metadata profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_metadataprofile(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_metadataprofile(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata profiles."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadataprofile()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_metadataprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a metadata profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_metadataprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_metadataprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a metadata profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_metadataprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_metadataprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific metadata profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadataprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_metadataprofile_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata profile schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_metadataprofile_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_metadataprovider(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get metadata provider configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_metadataprovider()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_config_metadataprovider_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update metadata provider configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_metadataprovider_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_metadataprovider_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific metadata provider configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_metadataprovider_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_wanted_missing(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        monitored: bool = Field(default=None, description="monitored"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get missing books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_wanted_missing(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeAuthor=includeAuthor,
            monitored=monitored,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_wanted_missing_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get missing books (paged)."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_wanted_missing_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get naming configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_naming()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_config_naming_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update naming configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_naming_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific naming configuration."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_naming_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_config_naming_examples(
        renameBooks: bool = Field(default=None, description="renameBooks"),
        replaceIllegalCharacters: bool = Field(
            default=None, description="replaceIllegalCharacters"
        ),
        colonReplacementFormat: int = Field(
            default=None, description="colonReplacementFormat"
        ),
        standardBookFormat: str = Field(default=None, description="standardBookFormat"),
        authorFolderFormat: str = Field(default=None, description="authorFolderFormat"),
        includeAuthorName: bool = Field(default=None, description="includeAuthorName"),
        includeBookTitle: bool = Field(default=None, description="includeBookTitle"),
        includeQuality: bool = Field(default=None, description="includeQuality"),
        replaceSpaces: bool = Field(default=None, description="replaceSpaces"),
        separator: str = Field(default=None, description="separator"),
        numberStyle: str = Field(default=None, description="numberStyle"),
        id: int = Field(default=None, description="id"),
        resourceName: str = Field(default=None, description="resourceName"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get naming configuration examples."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_naming_examples(
            renameBooks=renameBooks,
            replaceIllegalCharacters=replaceIllegalCharacters,
            colonReplacementFormat=colonReplacementFormat,
            standardBookFormat=standardBookFormat,
            authorFolderFormat=authorFolderFormat,
            includeAuthorName=includeAuthorName,
            includeBookTitle=includeBookTitle,
            includeQuality=includeQuality,
            replaceSpaces=replaceSpaces,
            separator=separator,
            numberStyle=numberStyle,
            id=id,
            resourceName=resourceName,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_notification(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notifications."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_notification()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_notification(
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_notification(data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def put_notification_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        forceSave: bool = Field(default=None, description="forceSave"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_notification_id(id=id, data=data, forceSave=forceSave)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def delete_notification_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_notification_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_notification_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_notification_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_notification_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get notification schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_notification_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_notification_test(
        data: Dict = Field(default=..., description="data"),
        forceTest: bool = Field(default=None, description="forceTest"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_notification_test(data=data, forceTest=forceTest)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_notification_testall(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Test all notifications."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_notification_testall()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_notification_action_name(
        name: str = Field(default=..., description="name"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Perform action on notification."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_notification_action_name(name=name, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"operations"},
    )
    async def get_parse(
        title: str = Field(default=None, description="title"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Parse book information."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_parse(title=title)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_ping(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get quality definitions."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_ping()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update quality definition."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_qualitydefinition_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific quality definition."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_qualitydefinition_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_qualitydefinition(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get quality profiles."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_qualitydefinition()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_qualitydefinition_update(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new quality profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_qualitydefinition_update(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_qualityprofile(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a quality profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_qualityprofile(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a quality profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_qualityprofile()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific quality profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_qualityprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get quality profile schema."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_qualityprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_qualityprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_qualityprofile_schema(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue details."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_qualityprofile_schema()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def delete_queue_id(
        id: int = Field(default=..., description="id"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue status."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_queue_id(
            id=id,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def delete_queue_bulk(
        data: Dict = Field(default=..., description="data"),
        removeFromClient: bool = Field(default=None, description="removeFromClient"),
        blocklist: bool = Field(default=None, description="blocklist"),
        skipRedownload: bool = Field(default=None, description="skipRedownload"),
        changeCategory: bool = Field(default=None, description="changeCategory"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk delete queue items."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_queue_bulk(
            data=data,
            removeFromClient=removeFromClient,
            blocklist=blocklist,
            skipRedownload=skipRedownload,
            changeCategory=changeCategory,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def get_queue(
        page: int = Field(default=None, description="page"),
        pageSize: int = Field(default=None, description="pageSize"),
        sortKey: str = Field(default=None, description="sortKey"),
        sortDirection: str = Field(default=None, description="sortDirection"),
        includeUnknownAuthorItems: bool = Field(
            default=None, description="includeUnknownAuthorItems"
        ),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        includeBook: bool = Field(default=None, description="includeBook"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_queue(
            page=page,
            pageSize=pageSize,
            sortKey=sortKey,
            sortDirection=sortDirection,
            includeUnknownAuthorItems=includeUnknownAuthorItems,
            includeAuthor=includeAuthor,
            includeBook=includeBook,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def post_queue_grab_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Grab queue item."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_queue_grab_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def post_queue_grab_bulk(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Bulk grab queue items."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_queue_grab_bulk(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def get_queue_details(
        authorId: int = Field(default=None, description="authorId"),
        bookIds: List = Field(default=None, description="bookIds"),
        includeAuthor: bool = Field(default=None, description="includeAuthor"),
        includeBook: bool = Field(default=None, description="includeBook"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue details."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_queue_details(
            authorId=authorId,
            bookIds=bookIds,
            includeAuthor=includeAuthor,
            includeBook=includeBook,
        )

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"queue"},
    )
    async def get_queue_status(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get queue status."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_queue_status()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_release(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a release."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_release(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def get_release(
        bookId: int = Field(default=None, description="bookId"),
        authorId: int = Field(default=None, description="authorId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get releases."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_release(bookId=bookId, authorId=authorId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get release profiles."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_releaseprofile()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def post_releaseprofile(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a release profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_releaseprofile(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def put_releaseprofile_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a release profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_releaseprofile_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def delete_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a release profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"profiles"},
    )
    async def get_releaseprofile_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get a specific release profile."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_releaseprofile_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"downloads"},
    )
    async def post_release_push(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Push release."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_release_push(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_remotepathmapping(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add remote path mapping."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_remotepathmapping(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_remotepathmapping(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get remote path mappings."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_remotepathmapping()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def delete_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete remote path mapping."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def put_remotepathmapping_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update remote path mapping."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_remotepathmapping_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_remotepathmapping_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific remote path mapping."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_remotepathmapping_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_rename(
        authorId: int = Field(default=None, description="authorId"),
        bookId: int = Field(default=None, description="bookId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get rename suggestions."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_rename(authorId=authorId, bookId=bookId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_retag(
        authorId: int = Field(default=None, description="authorId"),
        bookId: int = Field(default=None, description="bookId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retag books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_retag(authorId=authorId, bookId=bookId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def post_rootfolder(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new root folder."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_rootfolder(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_rootfolder(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get root folders."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_rootfolder()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def put_rootfolder_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Update a root folder."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_rootfolder_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def delete_rootfolder_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a root folder."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "config"},
    )
    async def get_rootfolder_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get specific root folder."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_rootfolder_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"search"},
    )
    async def get_search(
        term: str = Field(default=None, description="term"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Search for books."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_search(term=term)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"chaptarr", "catalog"},
    )
    async def get_series(
        authorId: int = Field(default=None, description="authorId"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get series info."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_series(authorId=authorId)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_content_path(
        path: str = Field(default=..., description="path"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get content path."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_content_path(path=path)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_(
        path: str = Field(default=..., description="path"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get resource by path."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_(path=path)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_path(
        path: str = Field(default=..., description="path"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Get system paths."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_path(path=path)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_status(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the current download queue."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_status()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_routes(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed entries in the download queue."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_routes()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_routes_duplicate(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve status information for the download queue."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_routes_duplicate()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_system_shutdown(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve the current system status of Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_system_shutdown()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_system_restart(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve available system routes."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_system_restart()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_tag(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve duplicate system routes."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_tag()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def post_tag(
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all system backups."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.post_tag(data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def put_tag_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete a system backup by its ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_tag_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def delete_tag_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve all defined tags."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.delete_tag_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_tag_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Add a new tag to Chaptarr."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_tag_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Delete an existing tag."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_tag_detail()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_tag_detail_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific tag by its ID."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_tag_detail_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_task(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed usage information for all tags."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_task()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_system_task_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve detailed usage information for a specific tag."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_system_task_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def put_config_ui_id(
        id: str = Field(default=..., description="id"),
        data: Dict = Field(default=..., description="data"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve information about system tasks."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.put_config_ui_id(id=id, data=data)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_ui_id(
        id: int = Field(default=..., description="id"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve details for a specific system task."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_ui_id(id=id)

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_config_ui(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve logs for system tasks."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_config_ui()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_update(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve logs for a specific system task."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_update()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update(
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve available log file updates."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_log_file_update()

    @mcp.tool(
        exclude_args=["chaptarr_base_url", "chaptarr_api_key", "chaptarr_verify"],
        tags={"system"},
    )
    async def get_log_file_update_filename(
        filename: str = Field(default=..., description="filename"),
        chaptarr_base_url: str = Field(
            default=os.environ.get("CHAPTARR_BASE_URL", None), description="Base URL"
        ),
        chaptarr_api_key: Optional[str] = Field(
            default=os.environ.get("CHAPTARR_API_KEY", None), description="API Key"
        ),
        chaptarr_verify: bool = Field(
            default=to_boolean(os.environ.get("CHAPTARR_VERIFY", "False")),
            description="Verify SSL",
        ),
    ) -> Dict:
        """Retrieve content of a specific log file update."""
        client = Api(
            base_url=chaptarr_base_url, token=chaptarr_api_key, verify=chaptarr_verify
        )
        return client.get_log_file_update_filename(filename=filename)


def chaptarr_mcp():
    print(f"chaptarr_mcp v{__version__}")
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

    mcp = FastMCP("Chaptarr", auth=auth)
    register_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Chaptarr MCP v{__version__}")
    print("\nStarting Chaptarr MCP Server")
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
    chaptarr_mcp()
