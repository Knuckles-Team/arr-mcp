"""
Arr MCP Server — Consolidated & Optimized.

This module implements a dynamic unified MCP server for the entire Arr stack.
It uses metaprogramming to dynamically generate FastMCP tool wrappers at runtime
by reading the API method signatures and `tool_tags.json`.

Environment Variables:
    <SERVICE>_<CATEGORY>TOOL (e.g. SONARR_CATALOGTOOL)
"""

import os
import sys
import logging
import json
import inspect
from pathlib import Path
from typing import Optional, List, Dict, Union, Any

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
from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_parser, config
from agent_utilities.middlewares import UserTokenMiddleware, JWTClaimsLoggingMiddleware

from arr_mcp.sonarr_api import Api as SonarrApi
from arr_mcp.radarr_api import Api as RadarrApi
from arr_mcp.lidarr_api import Api as LidarrApi
from arr_mcp.prowlarr_api import Api as ProwlarrApi
from arr_mcp.bazarr_api import Api as BazarrApi
from arr_mcp.seerr_api import Api as SeerrApi
from arr_mcp.chaptarr_api import Api as ChaptarrApi

__version__ = "0.2.26"

logger = get_logger(name="ArrMCP")
logger.setLevel(logging.INFO)

API_CLASSES = {
    "sonarr": SonarrApi,
    "radarr": RadarrApi,
    "lidarr": LidarrApi,
    "prowlarr": ProwlarrApi,
    "bazarr": BazarrApi,
    "seerr": SeerrApi,
    "chaptarr": ChaptarrApi,
}


def load_tool_config() -> Dict[str, Dict[str, str]]:
    """Load the tool methods to tag mapping."""
    config_path = Path(__file__).parent / "tool_tags.json"
    if not config_path.exists():
        logger.error(f"Missing {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_dynamic_tool(
    service: str, method_name: str, tag: str, api_class: type
) -> Optional[Any]:
    """
    Dynamically compile a wrapper function for an API method using exec().
    This allows FastMCP/Pydantic to perfectly parse standard python signatures.
    """
    method = getattr(api_class, method_name)
    sig = inspect.signature(method)
    docstring = method.__doc__ or f"Call {service} {method_name}"

    # Analyze parameters (skip `self`)
    params_code = []
    call_args = []

    for name, param in list(sig.parameters.items())[1:]:
        # Get type annotation string safely
        if param.annotation is inspect.Parameter.empty:
            type_str = "Any"
        else:
            try:
                # Basic representation of common types (Dict, List, int, str, bool, Optional, Any)
                type_str = str(param.annotation).replace("typing.", "")
                # Clean up <class 'int'> -> int
                if "class" in type_str:
                    type_str = param.annotation.__name__
            except Exception:
                type_str = "Any"

        # Handle defaults via pydantic Field
        if param.default is inspect.Parameter.empty:
            field_def = f"Field(..., description='{name}')"
        else:
            # We must repr the default so strings get quotes, None gets None, etc.
            field_def = f"Field(default={repr(param.default)}, description='{name}')"

        params_code.append(f"    {name}: {type_str} = {field_def}")
        call_args.append(f"{name}={name}")

    params_str = ",\n".join(params_code)
    call_args_str = ", ".join(call_args)
    if params_str:
        params_str += ",\n"

    svc_upper = service.upper()

    # Prefix tool names to ensure global uniqueness (e.g. lidarr_get_series)
    tool_name = f"{service}_{method_name}"

    # We compile the function exactly as if a human wrote it
    # We add the required base_url, api_key, and verify fields
    func_source = f'''
async def {tool_name}(
{params_str}
    {service}_base_url: str = Field(default=os.environ.get("{svc_upper}_BASE_URL", None), description="Base URL"),
    {service}_api_key: Optional[str] = Field(default=os.environ.get("{svc_upper}_API_KEY", None), description="API Key"),
    {service}_verify: bool = Field(default=to_boolean(os.environ.get("{svc_upper}_VERIFY", "False")), description="Verify SSL")
) -> Dict:
    """{docstring}"""
    # Initialize the specific API client
    client = api_class(
        base_url={service}_base_url,
        token={service}_api_key,
        verify={service}_verify
    )
    # Execute the underlying method
    return client.{method_name}({call_args_str})
'''

    # Required globals for the exec environment
    local_env = {}
    global_env = {
        "os": os,
        "Field": Field,
        "Optional": Optional,
        "Dict": Dict,
        "List": List,
        "Any": Any,
        "to_boolean": to_boolean,
        "api_class": api_class,
    }

    try:
        exec(func_source, global_env, local_env)
        wrapper_func = local_env[tool_name]
        return wrapper_func
    except Exception as e:
        logger.error(f"Failed to compile dynamic tool {service}.{method_name}: {e}")
        return None


def register_dynamic_tools(mcp: FastMCP) -> List[str]:
    """Read configuration, evaluate env vars, and dynamically register allowed tools."""
    tool_config = load_tool_config()
    registered_tags = set()

    for service, methods in tool_config.items():
        if service not in API_CLASSES:
            continue

        api_class = API_CLASSES[service]

        for method_name, tag in methods.items():
            # e.g., tag="sonarr-catalog" -> env_var="SONARR_CATALOGTOOL"
            parts = tag.split("-", 1)
            cat = parts[1] if len(parts) > 1 else "system"
            env_var = f"{service.upper()}_{cat.upper()}TOOL"

            # Check gating flag
            if not to_boolean(str(os.environ.get(env_var, "True"))):
                continue

            wrapper_func = _generate_dynamic_tool(service, method_name, tag, api_class)
            if wrapper_func:
                mcp.add_tool(wrapper_func)
                registered_tags.add(tag)

    return sorted(list(registered_tags))


mcp = FastMCP("Arr")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "OK"})


def mcp_server():
    print(f"arr-mcp v{__version__}")
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
            logger.error("Delegation requires complete OIDC configuration")
            sys.exit(1)

        try:
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                raise ValueError("No token_endpoint found in OIDC configuration")
        except Exception as e:
            logger.error(f"Failed to fetch OIDC configuration: {e}")
            sys.exit(1)

    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    # Set auth dynamically here if args specify it
    if args.auth_type == "static":
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

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        public_key = secret_or_key
        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key = f.read()
            except Exception as e:
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)

        required_scopes = (
            [s.strip() for s in args.required_scopes.split(",") if s.strip()]
            if args.required_scopes
            else None
        )

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
        except Exception as e:
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
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
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
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
            middlewares.append(
                create_eunomia_middleware(
                    policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
                )
            )
        except Exception as e:
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    if auth:
        mcp._local_provider.auth = auth

    # Dynamic Registration of API Tools
    registered_tags = register_dynamic_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Arr MCP v{__version__}")
    print("\\nStarting Arr MCP Server (Optimized Runtime Generation)")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Dynamic Tags Loaded: {len(registered_tags)}")

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
    mcp_server()
