# CONN-ARR-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `arr-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `arr_mcp` from it.
