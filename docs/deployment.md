# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`arr-mcp` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "arr": {
      "command": "arr-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
arr-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/arr-mcp@sha256:<digest> arr-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "arr": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
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

Each service also accepts a `*_TLS_PROFILE` selector. For a private CA, inject a
complete PEM trust chain through the shared runtime transport-security environment.
Certificate and hostname verification are mandatory. The full set, grouped by service, is documented in
[`.env.example`](https://github.com/Knuckles-Team/arr-mcp/blob/main/.env.example).
Copy it to `.env` and populate only the services you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/arr-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  arr-mcp-mcp:
    image: example/arr-mcp@sha256:<digest>
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
    image: example/arr-mcp@sha256:<digest>
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
    image: example/arr-mcp@sha256:<digest>
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
# Internal (self-signed) — homelab .example.invalid zone
arr-mcp.example.invalid {
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
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=arr-mcp.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `arr-mcp.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
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

For a remote HTTP server, point the client at `http://arr-mcp.example.invalid/mcp` instead.
