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

*Version: 0.17.0*

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

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "arr-mcp",
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
        "arr-mcp",
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
  knucklessg1/arr-mcp:latest
```

---

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

The Arr MCP and Agent servers support extensive environment configuration. The full list of supported variables is documented below:

| Variable | Description | Default | Required for |
|:---|:---|:---|:---|
| `HOST` | The bind host for Streamable-HTTP or SSE transport. | `0.0.0.0` | Server Transport |
| `PORT` | The bind port for Streamable-HTTP or SSE transport. | `8000` | Server Transport |
| `TRANSPORT` | MCP communication transport layer (`stdio`, `streamable-http`, `sse`). | `stdio` | Server Transport |
| `ENABLE_OTEL` | Enable OpenTelemetry logging and tracing integration. | `True` | Observability |
| `EUNOMIA_TYPE` | Access control policy engine type (`none`, `embedded`, `remote`). | `none` | Access Governance |
| `EUNOMIA_POLICY_FILE` | Scoped embedded policy file location. | `mcp_policies.json` | Access Governance |
| `DEFAULT_AGENT_NAME` | Custom name identification for the Graph Agent. | `Arr Mcp` | Graph Agent |
| `ALLOWED_CLIENT_REDIRECT_URIS` | Permitted client redirect URIs for authentication flows. | None | Auth Flow |
| `AUTH_TYPE` | Type of authentication used for A2A endpoints. | None | Auth Flow |
| `SONARR_ENABLED` | Toggle to enable/disable Sonarr MCP tools and client. | `False` | Sonarr Service |
| `SONARR_BASE_URL` | Base API URL of your Sonarr service. | None | Sonarr Service |
| `SONARR_TOKEN` | Authentication API token for Sonarr. | None | Sonarr Service |
| `SONARR_SSL_VERIFY` | Verify SSL certificates for Sonarr requests. | `False` | Sonarr Service |
| `RADARR_ENABLED` | Toggle to enable/disable Radarr MCP tools and client. | `False` | Radarr Service |
| `RADARR_BASE_URL` | Base API URL of your Radarr service. | None | Radarr Service |
| `RADARR_TOKEN` | Authentication API token for Radarr. | None | Radarr Service |
| `RADARR_SSL_VERIFY` | Verify SSL certificates for Radarr requests. | `False` | Radarr Service |
| `LIDARR_ENABLED` | Toggle to enable/disable Lidarr MCP tools and client. | `False` | Lidarr Service |
| `LIDARR_BASE_URL` | Base API URL of your Lidarr service. | None | Lidarr Service |
| `LIDARR_TOKEN` | Authentication API token for Lidarr. | None | Lidarr Service |
| `LIDARR_SSL_VERIFY` | Verify SSL certificates for Lidarr requests. | `False` | Lidarr Service |
| `PROWLARR_ENABLED` | Toggle to enable/disable Prowlarr MCP tools and client. | `False` | Prowlarr Service |
| `PROWLARR_BASE_URL` | Base API URL of your Prowlarr service. | None | Prowlarr Service |
| `PROWLARR_TOKEN` | Authentication API token for Prowlarr. | None | Prowlarr Service |
| `PROWLARR_SSL_VERIFY` | Verify SSL certificates for Prowlarr requests. | `False` | Prowlarr Service |
| `BAZARR_ENABLED` | Toggle to enable/disable Bazarr MCP tools and client. | `False` | Bazarr Service |
| `BAZARR_BASE_URL` | Base API URL of your Bazarr service. | None | Bazarr Service |
| `BAZARR_API_KEY` | Authentication API key for Bazarr. | None | Bazarr Service |
| `BAZARR_SSL_VERIFY` | Verify SSL certificates for Bazarr requests. | `False` | Bazarr Service |
| `SEERR_ENABLED` | Toggle to enable/disable Seerr MCP tools and client. | `False` | Seerr Service |
| `SEERR_BASE_URL` | Base API URL of your Seerr service. | None | Seerr Service |
| `SEERR_API_KEY` | Authentication API key for Seerr. | None | Seerr Service |
| `SEERR_SSL_VERIFY` | Verify SSL certificates for Seerr requests. | `False` | Seerr Service |
| `CHAPTARR_ENABLED` | Toggle to enable/disable Chaptarr MCP tools and client. | `False` | Chaptarr Service |
| `CHAPTARR_BASE_URL` | Base API URL of your Chaptarr service. | None | Chaptarr Service |
| `CHAPTARR_TOKEN` | Authentication API token for Chaptarr. | None | Chaptarr Service |
| `CHAPTARR_SSL_VERIFY` | Verify SSL certificates for Chaptarr requests. | `False` | Chaptarr Service |

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

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install arr-mcp[all]

# Using standard pip
python -m pip install arr-mcp[all]
```

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

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
