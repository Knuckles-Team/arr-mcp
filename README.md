# Arr Mcp
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/arr-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/arr-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/arr-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/arr-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/arr-mcp)
![PyPI - License](https://img.shields.io/pypi/l/arr-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/arr-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/arr-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/arr-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/arr-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/arr-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/arr-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/arr-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/arr-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/arr-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/arr-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/arr-mcp)

*Version: 0.46.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, MCP, and
> A2A agent interfaces, and guidance for provisioning the Arr Suite services are
> maintained in the [official documentation](https://knuckles-team.github.io/arr-mcp/).

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [CLI or API](#cli-or-api)
- [MCP](#mcp)
  - [Dynamic Tool Selection & Visibility](#dynamic-tool-selection--visibility)
- [Agent](#agent)
- [Environment Variables](#environment-variables)
- [Security & Governance](#security--governance)
- [Contribute](#contribute)

---

## Overview

**Arr Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Arr Suite MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Arr Suite MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

The table below is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `bazarr_action` | `BAZARRTOOL` | Execute any Bazarr API action. |
| `chaptarr_action` | `CHAPTARRTOOL` | Execute any Chaptarr API action. |
| `lidarr_action` | `LIDARRTOOL` | Execute any Lidarr API action. |
| `prowlarr_action` | `PROWLARRTOOL` | Execute any Prowlarr API action. |
| `radarr_action` | `RADARRTOOL` | Execute any Radarr API action. |
| `seerr_action` | `SEERRTOOL` | Execute any Seerr API action. |
| `sonarr_action` | `SONARRTOOL` | Execute any Sonarr API action. |

_7 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md#mcp-tools](docs/index.md#mcp-tools).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

> **Install the slim `[mcp]` extra.** All examples below install
> `arr-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "arr-mcp[mcp]",
        "arr-mcp"
      ],
      "env": {
        "ARR_HOST": "your_arr_host_here",
        "ARR_API_KEY": "your_arr_api_key_here",
        "PVR_API_KEY": "your_pvr_api_key_here",
        "PLEX_TOKEN": "your_plex_token_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "arr-mcp[mcp]",
        "arr-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "ARR_HOST": "your_arr_host_here",
        "ARR_API_KEY": "your_arr_api_key_here",
        "PVR_API_KEY": "your_pvr_api_key_here",
        "PLEX_TOKEN": "your_plex_token_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "url": "http://localhost:8000/arr-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name arr-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e ARR_HOST="your_value" \
  -e ARR_API_KEY="your_value" \
  -e PVR_API_KEY="your_value" \
  -e PLEX_TOKEN="your_value" \
  knucklessg1/arr-mcp:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `arr-mcp[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `arr-mcp[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `arr-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`arr-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/arr-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://arr-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export ARR_HOST="your_value"
export ARR_API_KEY="your_value"
export PVR_API_KEY="your_value"
export PLEX_TOKEN="your_value"

# Run the agent server
arr-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  arr-mcp-mcp:
    image: knucklessg1/arr-mcp:mcp
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
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  arr-mcp-agent:
    image: knucklessg1/arr-mcp:latest
    container_name: arr-mcp-agent
    hostname: arr-mcp-agent
    restart: always
    depends_on:
      - arr-mcp-mcp
    env_file:
      - ../.env
    command: [ "arr-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9099
      - MCP_URL=http://arr-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9099:9099"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9099/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/index.md#a2a-agent](docs/index.md#a2a-agent).

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `ARR_HOST` | `your_arr_host` |  |
| `ARR_API_KEY` | `your_arr_api_key_here` |  |
| `PVR_API_KEY` | `your_pvr_api_key_here` |  |
| `PLEX_TOKEN` | `your_plex_token_here` |  |
| `SONARR_ENABLED` | `True` | Sonarr Client |
| `SONARR_BASE_URL` | `http://localhost:8989` |  |
| `SONARR_TOKEN` | `your_sonarr_token_here` |  |
| `SONARR_SSL_VERIFY` | `False` |  |
| `RADARR_ENABLED` | `True` | Radarr Client |
| `RADARR_BASE_URL` | `http://localhost:7878` |  |
| `RADARR_TOKEN` | `your_radarr_token_here` |  |
| `RADARR_SSL_VERIFY` | `False` |  |
| `LIDARR_ENABLED` | `True` | Lidarr Client |
| `LIDARR_BASE_URL` | `http://localhost:8686` |  |
| `LIDARR_TOKEN` | `your_lidarr_token_here` |  |
| `LIDARR_SSL_VERIFY` | `False` |  |
| `PROWLARR_ENABLED` | `True` | Prowlarr Client |
| `PROWLARR_BASE_URL` | `http://localhost:9696` |  |
| `PROWLARR_TOKEN` | `your_prowlarr_token_here` |  |
| `PROWLARR_SSL_VERIFY` | `False` |  |
| `BAZARR_ENABLED` | `True` | Bazarr Client |
| `BAZARR_BASE_URL` | `http://localhost:6767` |  |
| `BAZARR_API_KEY` | `your_bazarr_api_key_here` |  |
| `BAZARR_SSL_VERIFY` | `False` |  |
| `SEERR_ENABLED` | `True` | Seerr Client |
| `SEERR_BASE_URL` | `http://localhost:5055` |  |
| `SEERR_API_KEY` | `your_seerr_api_key_here` |  |
| `SEERR_SSL_VERIFY` | `False` |  |
| `CHAPTARR_ENABLED` | `True` | Chaptarr Client |
| `CHAPTARR_BASE_URL` | `http://localhost:8006` |  |
| `CHAPTARR_TOKEN` | `your_chaptarr_token_here` |  |
| `CHAPTARR_SSL_VERIFY` | `False` |  |
| `SONARRTOOL` | `True` | MCP tools table (condensed action-routed surface). |
| `RADARRTOOL` | `True` |  |
| `LIDARRTOOL` | `True` |  |
| `PROWLARRTOOL` | `True` |  |
| `BAZARRTOOL` | `True` |  |
| `SEERRTOOL` | `True` |  |
| `CHAPTARRTOOL` | `True` |  |
| `DEFAULT_AGENT_NAME` | `Arr Mcp` |  |
| `ALLOWED_CLIENT_REDIRECT_URIS` | — |  |
| `AUTH_TYPE` | — |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_53 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by concern. arr-mcp fronts seven independent
*arr services — each is wired by setting its own `<SVC>_ENABLED` plus that service's
`_BASE_URL` and `_TOKEN`/`_API_KEY`. The shared `ARR_HOST` / `ARR_API_KEY` / `PVR_API_KEY` /
`PLEX_TOKEN` values are convenience defaults consumed by the clients.

### Connection & Credentials — shared
| Variable | Description | Default |
|----------|-------------|---------|
| `ARR_HOST` | Shared base host for the Arr services | — |
| `ARR_API_KEY` | Shared Arr API key | — |
| `PVR_API_KEY` | Shared PVR (Sonarr/Radarr/Lidarr) API key | — |
| `PLEX_TOKEN` | Plex authentication token (Seerr/overseerr flows) | — |

### Connection & Credentials — per service
Each service accepts an `_ENABLED` toggle, a `_BASE_URL`, an auth token (`_TOKEN` for
Sonarr/Radarr/Lidarr/Prowlarr/Chaptarr; `_API_KEY` for Bazarr/Seerr), and a `_SSL_VERIFY` flag.

| Variable | Description | Default |
|----------|-------------|---------|
| `SONARR_ENABLED` / `SONARR_BASE_URL` / `SONARR_TOKEN` / `SONARR_SSL_VERIFY` | Sonarr service enable + connection + API token + TLS verify | `False` / — / — / `False` |
| `RADARR_ENABLED` / `RADARR_BASE_URL` / `RADARR_TOKEN` / `RADARR_SSL_VERIFY` | Radarr service enable + connection + API token + TLS verify | `False` / — / — / `False` |
| `LIDARR_ENABLED` / `LIDARR_BASE_URL` / `LIDARR_TOKEN` / `LIDARR_SSL_VERIFY` | Lidarr service enable + connection + API token + TLS verify | `False` / — / — / `False` |
| `PROWLARR_ENABLED` / `PROWLARR_BASE_URL` / `PROWLARR_TOKEN` / `PROWLARR_SSL_VERIFY` | Prowlarr service enable + connection + API token + TLS verify | `False` / — / — / `False` |
| `BAZARR_ENABLED` / `BAZARR_BASE_URL` / `BAZARR_API_KEY` / `BAZARR_SSL_VERIFY` | Bazarr service enable + connection + API key + TLS verify | `False` / — / — / `False` |
| `SEERR_ENABLED` / `SEERR_BASE_URL` / `SEERR_API_KEY` / `SEERR_SSL_VERIFY` | Seerr service enable + connection + API key + TLS verify | `False` / — / — / `False` |
| `CHAPTARR_ENABLED` / `CHAPTARR_BASE_URL` / `CHAPTARR_TOKEN` / `CHAPTARR_SSL_VERIFY` | Chaptarr service enable + connection + API token + TLS verify | `False` / — / — / `False` |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above
(e.g. `SONARRTOOL`, `RADARRTOOL`, `PROWLARRTOOL`, `BAZARRTOOL`, `SEERRTOOL`, `CHAPTARRTOOL`,
`LIDARRTOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |
| `DEFAULT_AGENT_NAME` | Custom name for the Graph Agent | `Arr Mcp` |
| `ALLOWED_CLIENT_REDIRECT_URIS` | Permitted client redirect URIs for auth flows | — |
| `AUTH_TYPE` | Authentication type for A2A endpoints | — |

See [`.env.example`](.env.example) for a copy-paste starting point.

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `arr-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `arr-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `arr-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "arr-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "arr-mcp[agent]"

# Everything (development)
uv pip install "arr-mcp[all]"      # or: python -m pip install "arr-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/arr-mcp:mcp` | `--target mcp` | `arr-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `arr-mcp` |
| `knucklessg1/arr-mcp:latest` | `--target agent` (default) | `arr-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `arr-agent` |

```bash
docker build --target mcp   -t knucklessg1/arr-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/arr-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Usage & Quick Start

To launch and run `arr-mcp` services:

### 1. Launching the MCP Server
Launch the MCP server in standard I/O mode (ideal for IDEs):
```bash
arr-mcp
```

Or launch it as a Streamable-HTTP server on port `8000`:
```bash
arr-mcp --transport streamable-http --port 8000
```

### 2. Running the Graph Agent Server
Start the interactive Pydantic AI Graph Agent CLI with OIDC token delegation and Eunomia policies:
```bash
arr-agent --provider openai --model-id gpt-4o
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/arr-mcp/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/arr-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/arr-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/arr-mcp/usage/) | the MCP tools, the Python API clients, the CLI |
| [Backing Platform](https://knuckles-team.github.io/arr-mcp/platform/) | provision the Arr Suite services with Docker |
| [Overview](https://knuckles-team.github.io/arr-mcp/overview/) | ecosystem role, enterprise readiness, configuration |
| [Concepts](https://knuckles-team.github.io/arr-mcp/concepts/) | concept registry (`CONCEPT:ARR-*`) |

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `arr-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx arr-mcp` · or `uv tool install arr-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/arr-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
