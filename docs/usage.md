# Usage — API / CLI / MCP

`arr-mcp` exposes the same capability three ways: as **MCP tools** an agent calls, as
a **Python API** (the per-service clients) the operator import, and as a **CLI / agent**
entrypoint. The ecosystem role and configuration are summarized in
[Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one typed tool per upstream API
operation, named `<app>_<operation>`: 1,375 tools across Radarr, Sonarr, Lidarr, Chaptarr,
Prowlarr, Bazarr and Seerr, plus `arr_ingest_library`. No tool routes by `action`.

| Request | Tool |
|---|---|
| *"List the series Sonarr is tracking"* | `sonarr_get_series` |
| *"Search Prowlarr for 'nyaa'"* | `prowlarr_get_search` |
| *"Show pending requests in Seerr"* | `seerr_get_request` with `filter="pending"` |
| *"What is downloading?"* | `radarr_get_queue`, `sonarr_get_queue`, `lidarr_get_queue` |

The packaged skills (`skill://arr-*/SKILL.md`) hold the task workflows, and the packaged
prompts are agent definitions for the operator and each role (media librarian, request
manager, indexer maintainer, subtitle curator, download monitor). The ontology
(`ontology://arr-mcp/arr.ttl`, `ontology://arr-mcp/arr-contracts.ttl`) records the tool-use
contracts, where each library lives, and how the apps federate.

## As a Python API

Each service has its own client class (`Api`) under `arr_mcp.api`. The `arr_mcp.auth`
module builds a configured client straight from the environment:

```python
from arr_mcp.auth import get_sonarr_client, get_radarr_client

sonarr = get_sonarr_client()        # reads SONARR_BASE_URL / SONARR_TOKEN
series = sonarr.get("/api/v3/series")

radarr = get_radarr_client()        # reads RADARR_BASE_URL / RADARR_TOKEN
movies = radarr.get("/api/v3/movie")
health = radarr.get("/api/v3/health")
```

The operator can also build a client directly:

```python
from arr_mcp.api.api_client_sonarr import Api as SonarrApi
from scion_sdk.core.transport_security import resolve_tls_profile

sonarr = SonarrApi(
    base_url="http://your-sonarr:8989",
    token="your_sonarr_api_key",
    tls_profile=resolve_tls_profile("sonarr"),
)
queue = sonarr.request("GET", "/api/v3/queue")
```

The other services follow the same shape:
`get_lidarr_client`, `get_prowlarr_client`, `get_bazarr_client`,
`get_seerr_client`, and `get_chaptarr_client`. A factory raises a clear
`RuntimeError` when the required `*_BASE_URL` is unset, so missing configuration
fails loudly rather than silently.

## As a CLI / agent

The package installs two console scripts:

`arr-agent` connects to the MCP server over the Agent Control Protocol and drives the
for the agent environment variables and the combined Compose stack.
