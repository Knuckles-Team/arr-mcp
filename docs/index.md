# arr-mcp

typed, deterministic control surface over Sonarr, Radarr, Lidarr, Prowlarr, Bazarr,
Seerr, and Chaptarr.

!!! info "Official documentation"
    This site is the canonical reference for `arr-mcp`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/arr-mcp)](https://pypi.org/project/arr-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/arr-mcp)](https://github.com/Knuckles-Team/arr-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/arr-mcp)

## Overview

`arr-mcp` wraps the REST surface of the **Arr Suite** of media-automation services
provides:

- **Per-service API clients** — request-session facades over Sonarr, Radarr, Lidarr,
  Prowlarr, Bazarr, Seerr, and Chaptarr, each constructed from the environment.
- **Action-dispatch MCP tools** — one consolidated tool per service
  (`sonarr_action`, `radarr_action`, …) that keeps the LLM tool surface compact and
  togglable.
  Agent Control Protocol with an optional web interface.

Each service connector remains inactive when its credentials are absent, so the
server runs cleanly with only the integrations the operator configure.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-start: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-console: **[Usage](usage.md)** — the MCP tools, the Python API clients, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — provision the Arr Suite services with Docker.
- :material-sitemap: **[Overview](overview.md)** — ecosystem role, enterprise readiness, and configuration.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:ARR-*` registry.

</div>

## Quick start

```bash
pip install "arr-mcp[mcp]"
arr-mcp                          # stdio MCP server (default transport)
```

Connect it to the operator's Arr Suite services:

```bash
export SONARR_BASE_URL=http://localhost:8989
export SONARR_TOKEN=your_sonarr_api_key
arr-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
proxy, DNS).
