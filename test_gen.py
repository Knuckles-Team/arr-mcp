import json
from collections import defaultdict

from arr_mcp.api.api_client_bazarr import Api as BazarrApi
from arr_mcp.api.api_client_chaptarr import Api as ChaptarrApi
from arr_mcp.api.api_client_lidarr import Api as LidarrApi
from arr_mcp.api.api_client_prowlarr import Api as ProwlarrApi
from arr_mcp.api.api_client_radarr import Api as RadarrApi
from arr_mcp.api.api_client_seerr import Api as SeerrApi
from arr_mcp.api.api_client_sonarr import Api as SonarrApi

API_CLASSES = {
    "sonarr": SonarrApi,
    "radarr": RadarrApi,
    "lidarr": LidarrApi,
    "prowlarr": ProwlarrApi,
    "bazarr": BazarrApi,
    "seerr": SeerrApi,
    "chaptarr": ChaptarrApi,
}

with open("arr_mcp/tool_tags.json") as f:
    config = json.load(f)

# Group methods by tag
tags = defaultdict(list)
for service, methods in config.items():
    api_class = API_CLASSES[service]
    for method_name, tag in methods.items():
        if hasattr(api_class, method_name):
            tags[tag].append((service, method_name, getattr(api_class, method_name)))

print(f"Total tags: {len(tags)}")
for tag, funcs in tags.items():
    print(f"{tag}: {len(funcs)} methods")
