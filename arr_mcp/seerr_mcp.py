"""
Seerr MCP Server.

This module implements an MCP server for Seerr (Overseerr/Jellyseerr),
providing tools to manage media requests and discover content. It handles
authentication, middleware, and API interactions.
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
from arr_mcp.seerr_api import Api
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_parser,
    config,
)
from agent_utilities.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "0.2.16"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)


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
        tags={"system"},
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
        tags={"system"},
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
        """Get information about the application data volumes."""
        client = Api(
            base_url=seerr_base_url, api_key=seerr_api_key, verify=seerr_verify
        )
        return client.get_status_appdata()

    @mcp.tool(
        exclude_args=["seerr_base_url", "seerr_api_key", "seerr_verify"],
        tags={"system"},
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
        tags={"search"},
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
        tags={"search"},
    )
    async def get_request(
        take: int = Field(default=20, description="take"),
        skip: int = Field(default=0, description="skip"),
        filter: str = Field(
            default=None,
            description="filter (available, approved, processing, pending, unavailable, failed)",
        ),
        sort: str = Field(default="added", description="sort (added, modified)"),
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
        tags={"search"},
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
        tags={"search"},
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
        tags={"search"},
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
        tags={"search"},
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
        tags={"search"},
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
        tags={"catalog"},
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
        tags={"catalog"},
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
        tags={"search"},
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
        tags={"system"},
    )
    async def get_users(
        take: int = Field(default=20, description="take"),
        skip: int = Field(default=0, description="skip"),
        sort: str = Field(default="created", description="sort"),
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
        tags={"system"},
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


def seerr_mcp():
    print(f"Seerr MCP v{__version__}")
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


if __name__ == "__main__":
    seerr_mcp()
