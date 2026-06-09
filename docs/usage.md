# Usage — API / CLI / MCP

`arr-mcp` exposes the same capability three ways: as **MCP tools** an agent calls, as
a **Python API** (the per-service clients) you import, and as a **CLI / agent**
entrypoint. The ecosystem role and configuration are summarized in
[Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one consolidated, action-routed
tool per Arr service. A service's tool registers only when its credentials are
configured, so the tool surface stays compact.

| Tool | Service |
|---|---|
| `sonarr_action` | Sonarr (TV) |
| `radarr_action` | Radarr (movies) |
| `lidarr_action` | Lidarr (music) |
| `prowlarr_action` | Prowlarr (indexers) |
| `bazarr_action` | Bazarr (subtitles) |
| `seerr_action` | Seerr (requests) |
| `chaptarr_action` | Chaptarr (audiobooks / ebooks) |

Each tool takes an `action` plus parameters and dispatches to the corresponding API
method. Example agent prompts that map onto these tools:

- *"List the series Sonarr is tracking"* → `sonarr_action`
- *"Search Prowlarr for an indexer named 'nyaa'"* → `prowlarr_action`
- *"Show pending requests in Seerr"* → `seerr_action`

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

You can also construct a client directly:

```python
from arr_mcp.api.api_client_sonarr import Api as SonarrApi

sonarr = SonarrApi(
    base_url="http://your-sonarr:8989",
    token="your_sonarr_api_key",
    verify=False,
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

```bash
# The MCP server (see Deployment for transports)
arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# The Pydantic-AI A2A agent (serves the AG-UI web interface)
MCP_URL=http://localhost:8000/mcp arr-agent
```

`arr-agent` connects to the MCP server over the Agent Control Protocol and drives the
Arr tools on your behalf. See [Deployment](deployment.md#run-the-a2a-agent-server)
for the agent environment variables and the combined Compose stack.
