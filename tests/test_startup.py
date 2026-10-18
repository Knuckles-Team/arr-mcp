import runpy
import sys
from unittest.mock import patch

from fastmcp import FastMCP




def test_mcp_server_main_startup():
    """Test the mcp_server.py direct execution entry point."""
    imported = sys.modules.pop("arr_mcp.mcp_server", None)
    try:
        with (
            patch("sys.argv", ["mcp_server.py"]),
            patch.object(FastMCP, "run") as mock_run,
        ):
            runpy.run_module("arr_mcp.mcp_server", run_name="__main__")
            assert mock_run.called
    finally:
        if imported is not None:
            sys.modules["arr_mcp.mcp_server"] = imported


