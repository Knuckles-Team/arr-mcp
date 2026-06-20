"""
Authentication and client instantiation factory.

CONCEPT:OS-5.4 — OIDC & Credentials Governance
"""

import sys
from typing import TYPE_CHECKING

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting

if TYPE_CHECKING:
    from arr_mcp.api.api_client_bazarr import Api as BazarrApi
    from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
    from arr_mcp.api.api_client_lidarr import Api as LidarrApi
    from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
    from arr_mcp.api.api_client_radarr import Api as RadarrApi
    from arr_mcp.api.api_client_seerr import Api as SeerrApi
    from arr_mcp.api.api_client_sonarr import Api as SonarrApi

logger = get_logger(__name__)


def get_sonarr_client() -> "SonarrApi":
    """Get authenticated sonarr client."""
    api_cls = sys.modules[__name__].SonarrApi
    base_url = setting("SONARR_BASE_URL")
    token = setting("SONARR_TOKEN")
    verify = setting("SONARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("SONARR_BASE_URL not set")
    return api_cls(base_url=base_url, token=token, verify=verify)


def get_radarr_client() -> "RadarrApi":
    """Get authenticated radarr client."""
    api_cls = sys.modules[__name__].RadarrApi
    base_url = setting("RADARR_BASE_URL")
    token = setting("RADARR_TOKEN")
    verify = setting("RADARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("RADARR_BASE_URL not set")
    return api_cls(base_url=base_url, token=token, verify=verify)


def get_lidarr_client() -> "LidarrApi":
    """Get authenticated lidarr client."""
    api_cls = sys.modules[__name__].LidarrApi
    base_url = setting("LIDARR_BASE_URL")
    token = setting("LIDARR_TOKEN")
    verify = setting("LIDARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("LIDARR_BASE_URL not set")
    return api_cls(base_url=base_url, token=token, verify=verify)


def get_prowlarr_client() -> "ProwlarrApi":
    """Get authenticated prowlarr client."""
    api_cls = sys.modules[__name__].ProwlarrApi
    base_url = setting("PROWLARR_BASE_URL")
    token = setting("PROWLARR_TOKEN")
    verify = setting("PROWLARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("PROWLARR_BASE_URL not set")
    return api_cls(base_url=base_url, token=token, verify=verify)


def get_bazarr_client() -> "BazarrApi":
    """Get authenticated bazarr client."""
    api_cls = sys.modules[__name__].BazarrApi
    base_url = setting("BAZARR_BASE_URL")
    api_key = setting("BAZARR_API_KEY")
    verify = setting("BAZARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("BAZARR_BASE_URL not set")
    return api_cls(base_url=base_url, api_key=api_key, verify=verify)


def get_seerr_client() -> "SeerrApi":
    """Get authenticated seerr client."""
    api_cls = sys.modules[__name__].SeerrApi
    base_url = setting("SEERR_BASE_URL")
    api_key = setting("SEERR_API_KEY")
    verify = setting("SEERR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("SEERR_BASE_URL not set")
    return api_cls(base_url=base_url, api_key=api_key, verify=verify)


def get_chaptarr_client() -> "ChaptarrApi":
    """Get authenticated chaptarr client."""
    api_cls = sys.modules[__name__].ChaptarrApi
    base_url = setting("CHAPTARR_BASE_URL")
    token = setting("CHAPTARR_TOKEN")
    verify = setting("CHAPTARR_SSL_VERIFY", False)
    if not base_url:
        raise RuntimeError("CHAPTARR_BASE_URL not set")
    return api_cls(base_url=base_url, token=token, verify=verify)


def __getattr__(name: str):
    if name == "SonarrApi":
        from arr_mcp.api.api_client_sonarr import Api as SonarrClientApi

        return SonarrClientApi
    if name == "RadarrApi":
        from arr_mcp.api.api_client_radarr import Api as RadarrClientApi

        return RadarrClientApi
    if name == "LidarrApi":
        from arr_mcp.api.api_client_lidarr import Api as LidarrClientApi

        return LidarrClientApi
    if name == "ProwlarrApi":
        from arr_mcp.api.api_client_prowlarr import Api as ProwlarrClientApi

        return ProwlarrClientApi
    if name == "BazarrApi":
        from arr_mcp.api.api_client_bazarr import Api as BazarrClientApi

        return BazarrClientApi
    if name == "SeerrApi":
        from arr_mcp.api.api_client_seerr import Api as SeerrClientApi

        return SeerrClientApi
    if name == "ChaptarrApi":
        from arr_mcp.api.api_client_chaptarr import Api as ChaptarrClientApi

        return ChaptarrClientApi
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
