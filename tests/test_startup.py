import runpy
import sys
from unittest.mock import patch

from fastmcp import FastMCP


def test_main_startup():
    """Test the __main__.py entry point."""
    with patch("sys.argv", ["agent_server.py"]):
        with patch("agent_utilities.create_agent_server") as mock_agent_server:
            runpy.run_module("arr_mcp.__main__", run_name="__main__")
            assert mock_agent_server.called


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


def test_agent_server_main_startup():
    """Test the agent_server.py direct execution entry point."""
    imported = sys.modules.pop("arr_mcp.agent_server", None)
    try:
        with (
            patch("sys.argv", ["agent_server.py"]),
            patch("agent_utilities.create_agent_server") as mock_agent_server,
        ):
            runpy.run_module("arr_mcp.agent_server", run_name="__main__")
            assert mock_agent_server.called
    finally:
        if imported is not None:
            sys.modules["arr_mcp.agent_server"] = imported
