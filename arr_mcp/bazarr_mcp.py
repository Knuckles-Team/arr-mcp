#!/usr/bin/python
# coding: utf-8
import os
import argparse
import sys
import logging
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import Field

from arr_mcp.bazarr_api import Api
from arr_mcp.utils import to_integer, to_boolean

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration
BAZARR_BASE_URL = os.getenv("BAZARR_BASE_URL", "http://localhost:6767")
BAZARR_API_KEY = os.getenv("BAZARR_API_KEY", "")
BAZARR_VERIFY_SSL = to_boolean(os.getenv("BAZARR_VERIFY_SSL", "False"))

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(value=os.getenv("PORT", "8000"))


def register_prompts(mcp: FastMCP):
    @mcp.prompt("search_subtitles")
    def search_subtitles_prompt(query: str) -> str:
        """Search for subtitles for a movie or series."""
        return f"Search for subtitles matching '{query}'"


def register_tools(mcp: FastMCP):
    api = Api(BAZARR_BASE_URL, BAZARR_API_KEY, BAZARR_VERIFY_SSL)

    # Series Subtitles
    @mcp.tool()
    def get_series(
        page: int = Field(1, description="Page number"),
        page_size: int = Field(20, description="Page size"),
    ) -> str:
        """Get all series managed by Bazarr."""
        return str(api.get_series(page, page_size))

    @mcp.tool()
    def get_series_subtitles(
        series_id: int = Field(..., description="Series ID"),
    ) -> str:
        """Get subtitle information for a specific series."""
        return str(api.get_series_subtitles(series_id))

    @mcp.tool()
    def get_episode_subtitles(
        episode_id: int = Field(..., description="Episode ID"),
    ) -> str:
        """Get subtitle information for a specific episode."""
        return str(api.get_episode_subtitles(episode_id))

    @mcp.tool()
    def search_series_subtitles(
        series_id: int = Field(..., description="Series ID"),
        episode_id: Optional[int] = Field(None, description="Episode ID (optional)"),
    ) -> str:
        """Search for subtitles for a series or episode. Note: This triggers a search, it doesn't just list them."""
        return str(api.search_series_subtitles(series_id, episode_id))

    @mcp.tool()
    def download_series_subtitle(
        episode_id: int = Field(..., description="Episode ID"),
        language: str = Field(..., description="Language code (e.g., 'en')"),
        forced: bool = Field(False, description="Is forced subtitle"),
        hi: bool = Field(False, description="Is hearing impaired subtitle"),
    ) -> str:
        """Download a subtitle for an episode."""
        return str(api.download_series_subtitle(episode_id, language, forced, hi))

    # Movie Subtitles
    @mcp.tool()
    def get_movies(
        page: int = Field(1, description="Page number"),
        page_size: int = Field(20, description="Page size"),
    ) -> str:
        """Get all movies managed by Bazarr."""
        return str(api.get_movies(page, page_size))

    @mcp.tool()
    def get_movie_subtitles(
        movie_id: int = Field(..., description="Movie ID"),
    ) -> str:
        """Get subtitle information for a specific movie."""
        return str(api.get_movie_subtitles(movie_id))

    @mcp.tool()
    def search_movie_subtitles(
        movie_id: int = Field(..., description="Movie ID"),
    ) -> str:
        """Search for subtitles for a movie. Note: This triggers a search, it doesn't just list them."""
        return str(api.search_movie_subtitles(movie_id))

    @mcp.tool()
    def download_movie_subtitle(
        movie_id: int = Field(..., description="Movie ID"),
        language: str = Field(..., description="Language code (e.g., 'en')"),
        forced: bool = Field(False, description="Is forced subtitle"),
        hi: bool = Field(False, description="Is hearing impaired subtitle"),
    ) -> str:
        """Download a subtitle for a movie."""
        return str(api.download_movie_subtitle(movie_id, language, forced, hi))

    # History
    @mcp.tool()
    def get_history(
        page: int = Field(1, description="Page number"),
        page_size: int = Field(20, description="Page size"),
    ) -> str:
        """Get subtitle download history."""
        return str(api.get_history(page, page_size))

    # System & Config
    @mcp.tool()
    def get_system_status() -> str:
        """Get Bazarr system status."""
        return str(api.get_system_status())

    @mcp.tool()
    def get_system_health() -> str:
        """Get system health issues."""
        return str(api.get_system_health())

    # Wanted
    @mcp.tool()
    def get_wanted_series(
        page: int = Field(1, description="Page number"),
        page_size: int = Field(20, description="Page size"),
    ) -> str:
        """Get series episodes with wanted/missing subtitles."""
        return str(api.get_wanted_series(page, page_size))

    @mcp.tool()
    def get_wanted_movies(
        page: int = Field(1, description="Page number"),
        page_size: int = Field(20, description="Page size"),
    ) -> str:
        """Get movies with wanted/missing subtitles."""
        return str(api.get_wanted_movies(page, page_size))


def bazarr_mcp():
    print("Bazarr MCP Server")
    parser = argparse.ArgumentParser(description="Bazarr MCP Server")
    parser.add_argument(
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "sse"],
        help="Transport protocol to use",
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind to (for SSE)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port to bind to (for SSE)",
    )
    args = parser.parse_args()

    mcp = FastMCP("Bazarr")
    register_prompts(mcp)
    register_tools(mcp)

    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    bazarr_mcp()
