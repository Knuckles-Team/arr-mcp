from scion_sdk.connector import Connector

from arr_mcp.api.api_client_bazarr import Api as BazarrApi
from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
from arr_mcp.api.api_client_lidarr import Api as LidarrApi
from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
from arr_mcp.api.api_client_radarr import Api as RadarrApi
from arr_mcp.api.api_client_seerr import Api as SeerrApi
from arr_mcp.api.api_client_sonarr import Api as SonarrApi
from arr_mcp.auth import (
    get_bazarr_client,
    get_chaptarr_client,
    get_lidarr_client,
    get_prowlarr_client,
    get_radarr_client,
    get_seerr_client,
    get_sonarr_client,
)

connector = Connector(
    tools="arr_mcp.mcp",
    instructions="Arr Stack MCP Server — Dynamic unified server for Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Seerr, and Chaptarr.",
    verbose_targets=(
        {"client_cls": SonarrApi, "get_client": get_sonarr_client, "prefix": "sonarr"},
        {"client_cls": RadarrApi, "get_client": get_radarr_client, "prefix": "radarr"},
        {"client_cls": LidarrApi, "get_client": get_lidarr_client, "prefix": "lidarr"},
        {
            "client_cls": ProwlarrApi,
            "get_client": get_prowlarr_client,
            "prefix": "prowlarr",
        },
        {"client_cls": BazarrApi, "get_client": get_bazarr_client, "prefix": "bazarr"},
        {"client_cls": SeerrApi, "get_client": get_seerr_client, "prefix": "seerr"},
        {
            "client_cls": ChaptarrApi,
            "get_client": get_chaptarr_client,
            "prefix": "chaptarr",
        },
    ),
)
