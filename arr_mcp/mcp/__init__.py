"""Tool registrars beyond the API operations.

Every upstream API operation is served as one typed tool from the client
methods (``verbose_targets`` in ``arr_mcp/__init__.py``,
CONN-ARR-MCP-SUITE-R001). This package registers only the tools that are not
API operations: the knowledge-graph ingest tool.
"""

from arr_mcp.mcp.mcp_kg import register_kg_tools

__all__ = ["register_kg_tools"]
