# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`arr-mcp` exposes its MCP server (console script `arr-mcp`) four ways. Pick the row that
matches where the server runs relative to your MCP client, then copy the matching
`mcp_config.json` below. Replace the `<your-…>` placeholders with the values from the **Configuration / Environment Variables** section.

| # | Option | Transport | Where it runs | `mcp_config.json` key |
|---|--------|-----------|---------------|------------------------|
| 1 | stdio | `stdio` | client launches a subprocess | `command` |
| 2 | Streamable-HTTP (local) | `streamable-http` | a local network port | `command` or `url` |
| 3 | Local container / uv | `stdio` or `streamable-http` | Docker / Podman / uv on this host | `command` or `url` |
| 4 | Remote URL | `streamable-http` | a remote host behind Caddy | `url` |
| 5 | Open WebUI | `streamable-http` | any reachable HTTP endpoint | `url` |

### 1. stdio (local subprocess)

The client launches the server over stdio via `uvx` — best for local IDEs
(Cursor, Claude Desktop, VS Code):

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": ["--from", "arr-mcp", "arr-mcp"],
      "env": {
        "ARR_HOST": "<your-arr_host>"
      }
    }
  }
}
```

### 2. Streamable-HTTP (local process)

Run the server as a long-lived HTTP process:

```bash
uvx --from arr-mcp arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health        # {"status":"OK"}
```

Then either let the client launch it:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": ["--from", "arr-mcp", "arr-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "ARR_HOST": "<your-arr_host>"
      }
    }
  }
}
```

…or connect to the already-running process by URL:

```json
{
  "mcpServers": {
    "arr-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

### 3. Local container / uv

**(a) Launch a container directly from `mcp_config.json`** (stdio over the container —
no ports to manage). Swap `docker` for `podman` for a daemonless runtime:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "TRANSPORT=stdio",
        "-e", "ARR_HOST=<your-arr_host>",
        "knucklessg1/arr-mcp:latest"
      ]
    }
  }
}
```

**(b) Run a local streamable-http container, then connect by URL:**

```bash
docker run -d --name arr-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e ARR_HOST="<your-arr_host>" \
  knucklessg1/arr-mcp:latest
# or, from a clone of this repo:
docker compose -f docker/mcp.compose.yml up -d
```

```json
{
  "mcpServers": {
    "arr-mcp": { "url": "http://localhost:8000/mcp" }
  }
}
```

**(c) From a local checkout with `uv`:**

```bash
uv run arr-mcp --transport streamable-http --port 8000
```

### 4. Remote URL (deployed behind Caddy)

When the server is deployed remotely (e.g. as a Docker service) and published through
Caddy on the internal `*.arpa` zone, connect with the `"url"` key — no local process or
image required:

```json
{
  "mcpServers": {
    "arr-mcp": { "url": "http://arr-mcp.arpa/mcp" }
  }
}
```

Caddy reverse-proxies `http://arr-mcp.arpa` to the container's `:8000`
streamable-http listener; `http://arr-mcp.arpa/health` returns
`{"status":"OK"}` when the service is live.

### 5. Open WebUI

[Open WebUI](https://openwebui.com/) connects to MCP servers via their
Streamable-HTTP endpoint. Run arr-mcp with the `streamable-http` transport so
Open WebUI can reach it by URL:

```bash
arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

Or with Docker, ensuring the port is published:

```bash
docker run -d --name arr-mcp -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e ARR_HOST="<your-arr_host>" \
  knucklessg1/arr-mcp:latest
```

In Open WebUI, navigate to **Workspace → MCP Servers → Add Server** and enter:

| Field | Value |
|-------|-------|
| **Name** | `arr-mcp` |
| **Server URL** | `http://<host>:8000/mcp` |

Replace `<host>` with the address where arr-mcp is reachable from Open WebUI.
When running on the same Docker network or host, `http://localhost:8000/mcp`
or `http://arr-mcp:8000/mcp` (Docker service name) work as the URL.

No additional headers are required. Open WebUI discovers the full tool set
(`radarr_action`, `sonarr_action`, `lidarr_action`, etc.) automatically via
the MCP protocol's `tools/list` handshake.

To test the connection, use Open WebUI's built-in tool call editor or send a
simple query like *"Show me movies in Radarr"* — the LLM will call
`radarr_action` with action `get_movie` to list the catalog.

**Action naming:** All actions follow the API client method names. Use
`action='list_actions'` to discover every valid action for a service. Common
plurals like `get_movies` are aliased automatically to `get_movie` by the
dispatch resolver. A `did-you-mean` suggestion is returned for any action name
that can't be resolved.

<!-- END GENERATED: deployment-options -->

This page covers running `arr-mcp` as long-lived servers: the MCP transports, the
companion A2A agent, a Docker Compose stack, putting it behind a Caddy reverse proxy,
and giving it a DNS name with Technitium. To provision the **Arr Suite services** it
connects to, see [Backing Platform](platform.md).

> `arr-mcp` ships **two** console scripts: an **MCP server** (`arr-mcp`) and an
> **A2A agent server** (`arr-agent`). The MCP server is a typed, deterministic tool
> surface; the agent server is a Pydantic-AI agent that calls those tools over the
> Agent Control Protocol.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    arr-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    arr-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`arr-mcp` is configured entirely from the environment. The server-level settings:

| Var | Default | Meaning |
|---|---|---|
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Listen port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `ENABLE_OTEL` | `True` | OpenTelemetry / Langfuse export |
| `EUNOMIA_TYPE` | `none` | Authorization mode: `none`, `embedded`, `remote` |

Each Arr service is connected with its own block; a connector **remains inactive
when its credentials are absent**:

| Var | Example | Meaning |
|---|---|---|
| `SONARR_BASE_URL` | `http://localhost:8989` | Sonarr base URL |
| `SONARR_TOKEN` | `your_sonarr_api_key` | Sonarr API key |
| `RADARR_BASE_URL` | `http://localhost:7878` | Radarr base URL |
| `RADARR_TOKEN` | `your_radarr_api_key` | Radarr API key |
| `LIDARR_BASE_URL` | `http://localhost:8686` | Lidarr base URL |
| `LIDARR_TOKEN` | `your_lidarr_api_key` | Lidarr API key |
| `PROWLARR_BASE_URL` | `http://localhost:9696` | Prowlarr base URL |
| `PROWLARR_TOKEN` | `your_prowlarr_api_key` | Prowlarr API key |
| `BAZARR_BASE_URL` | `http://localhost:6767` | Bazarr base URL |
| `BAZARR_API_KEY` | `your_bazarr_api_key` | Bazarr API key |
| `SEERR_BASE_URL` | `http://localhost:5055` | Seerr base URL |
| `SEERR_API_KEY` | `your_seerr_api_key` | Seerr API key |
| `CHAPTARR_BASE_URL` | `http://localhost:8006` | Chaptarr base URL |
| `CHAPTARR_TOKEN` | `your_chaptarr_api_key` | Chaptarr API key |

Each service also accepts a `*_SSL_VERIFY` flag (default `False` for self-signed
homelab certificates). The full set, grouped by service, is documented in
[`.env.example`](https://github.com/Knuckles-Team/arr-mcp/blob/main/.env.example).
Copy it to `.env` and populate only the services you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/arr-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  arr-mcp-mcp:
    image: knucklessg1/arr-mcp:latest
    container_name: arr-mcp-mcp
    hostname: arr-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit the SONARR_* / RADARR_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Run the A2A agent server

`arr-mcp` ships a second console script, `arr-agent`, a Pydantic-AI agent that calls
the MCP tools over the Agent Control Protocol and exposes an optional web interface.
It connects to the MCP server via `MCP_URL` and listens on `:9099` by default. The
repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/arr-mcp/blob/main/docker/agent.compose.yml),
which runs both servers together:

```yaml
services:
  arr-mcp-mcp:
    image: knucklessg1/arr-mcp:latest
    container_name: arr-mcp-mcp
    hostname: arr-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"

  arr-mcp-agent:
    image: knucklessg1/arr-mcp:latest
    container_name: arr-mcp-agent
    hostname: arr-mcp-agent
    restart: always
    depends_on:
      - arr-mcp-mcp
    env_file:
      - ../.env
    command: ["arr-agent"]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9099
      - MCP_URL=http://arr-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports:
      - "9099:9099"
```

```bash
docker compose -f docker/agent.compose.yml up -d
curl -s http://localhost:9099/health         # agent health
```

| Var | Default | Meaning |
|---|---|---|
| `MCP_URL` | `http://arr-mcp-mcp:8000/mcp` | MCP server the agent calls |
| `PROVIDER` | `openai` | LLM provider |
| `MODEL_ID` | `gpt-4o` | Model identifier |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
arr-mcp.arpa {
    tls internal
    reverse_proxy arr-mcp-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
arr-mcp.example.com {
    reverse_proxy arr-mcp-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=arr-mcp.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `arr-mcp.arpa → <caddy-host-ip>` in the Technitium web
console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uv",
      "args": ["run", "arr-mcp"],
      "env": {
        "SONARR_BASE_URL": "http://your-sonarr:8989",
        "SONARR_TOKEN": "your_sonarr_api_key",
        "RADARR_BASE_URL": "http://your-radarr:7878",
        "RADARR_TOKEN": "your_radarr_api_key"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://arr-mcp.arpa/mcp` instead.
