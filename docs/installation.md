# Installation

`arr-mcp` is a standard Python package and a prebuilt container image. Pick the path
that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- One or more reachable **Arr Suite services** (Sonarr, Radarr, Lidarr, Prowlarr,
  Bazarr, Seerr, Chaptarr) — see [Backing Platform](platform.md) to provision them
  locally.

## From PyPI (recommended)

```bash
pip install arr-mcp
```

### Optional extras

The base install is intentionally minimal. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "arr-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "arr-mcp[agent]"` | Pydantic-AI agent + Logfire tracing (`agent-utilities[agent,logfire]`) |
| `all` | `pip install "arr-mcp[all]"` | Everything above |
| `test` | `pip install "arr-mcp[test]"` | The pytest suite (`pytest`, `pytest-xdist`, `pytest-asyncio`) |

```bash
# Typical: run the MCP server and the A2A agent
pip install "arr-mcp[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/arr-mcp.git
cd arr-mcp
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run arr-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `arr-mcp`):

```bash
docker pull knucklessg1/arr-mcp:latest

docker run --rm -i \
  -e SONARR_BASE_URL=http://your-sonarr:8989 \
  -e SONARR_TOKEN=your_sonarr_api_key \
  knucklessg1/arr-mcp:latest            # stdio transport (default)
```

For an HTTP server with a published port — and the A2A agent — see
[Deployment](deployment.md).

## Verify the install

```bash
arr-mcp --help
python -c "import arr_mcp; print(arr_mcp.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP and agent server behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API clients, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
