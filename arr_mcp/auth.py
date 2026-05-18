"""Authentication module for arr-mcp."""

import os

from agent_utilities.base_utilities import get_logger, to_boolean

from arr_mcp.api.api_client_bazarr import Api as BazarrApi
from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
from arr_mcp.api.api_client_lidarr import Api as LidarrApi
from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
from arr_mcp.api.api_client_radarr import Api as RadarrApi
from arr_mcp.api.api_client_seerr import Api as SeerrApi
from arr_mcp.api.api_client_sonarr import Api as SonarrApi

logger = get_logger(__name__)


def get_sonarr_client() -> SonarrApi:
    """Get authenticated sonarr client."""
    base_url = os.getenv("SONARR_BASE_URL")
    token = os.getenv("SONARR_TOKEN")
    verify = to_boolean(os.getenv("SONARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("SONARR_BASE_URL not set")
    return SonarrApi(base_url=base_url, token=token, verify=verify)


def get_radarr_client() -> RadarrApi:
    """Get authenticated radarr client."""
    base_url = os.getenv("RADARR_BASE_URL")
    token = os.getenv("RADARR_TOKEN")
    verify = to_boolean(os.getenv("RADARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("RADARR_BASE_URL not set")
    return RadarrApi(base_url=base_url, token=token, verify=verify)


def get_lidarr_client() -> LidarrApi:
    """Get authenticated lidarr client."""
    base_url = os.getenv("LIDARR_BASE_URL")
    token = os.getenv("LIDARR_TOKEN")
    verify = to_boolean(os.getenv("LIDARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("LIDARR_BASE_URL not set")
    return LidarrApi(base_url=base_url, token=token, verify=verify)


def get_prowlarr_client() -> ProwlarrApi:
    """Get authenticated prowlarr client."""
    base_url = os.getenv("PROWLARR_BASE_URL")
    token = os.getenv("PROWLARR_TOKEN")
    verify = to_boolean(os.getenv("PROWLARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("PROWLARR_BASE_URL not set")
    return ProwlarrApi(base_url=base_url, token=token, verify=verify)


def get_bazarr_client() -> BazarrApi:
    """Get authenticated bazarr client."""
    base_url = os.getenv("BAZARR_BASE_URL")
    api_key = os.getenv("BAZARR_API_KEY")
    verify = to_boolean(os.getenv("BAZARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("BAZARR_BASE_URL not set")
    return BazarrApi(base_url=base_url, api_key=api_key, verify=verify)


def get_seerr_client() -> SeerrApi:
    """Get authenticated seerr client."""
    base_url = os.getenv("SEERR_BASE_URL")
    api_key = os.getenv("SEERR_API_KEY")
    verify = to_boolean(os.getenv("SEERR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("SEERR_BASE_URL not set")
    return SeerrApi(base_url=base_url, api_key=api_key, verify=verify)


def get_chaptarr_client() -> ChaptarrApi:
    """Get authenticated chaptarr client."""
    base_url = os.getenv("CHAPTARR_BASE_URL")
    token = os.getenv("CHAPTARR_TOKEN")
    verify = to_boolean(os.getenv("CHAPTARR_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("CHAPTARR_BASE_URL not set")
    return ChaptarrApi(base_url=base_url, token=token, verify=verify)
