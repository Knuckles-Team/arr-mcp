"""Native knowledge-graph ingestion tool for the *arr stack (Wire-First).

CONCEPT:AU-KG.ingest.enterprise-source-extractor — lists the live library via the real
Radarr/Sonarr/Prowlarr clients and pushes it into epistemic-graph as typed :Movie /
:Series / :Indexer nodes (+ :Document overviews). Native-ingest failures propagate to
the caller. Auto-discovered by ``register_tool_surface`` (gated by ``KGTOOL``, default on).
"""

from typing import Any

from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import FastMCP
from pydantic import Field

from arr_mcp.auth import (
    get_prowlarr_client,
    get_radarr_client,
    get_sonarr_client,
)
from arr_mcp.kg_ingest import ingest_indexers, ingest_movies, ingest_series


def _records(resp: Any) -> list[dict[str, Any]]:
    """Normalize an *arr client response into a list of plain dict records."""
    data = getattr(resp, "data", resp)
    records = data if isinstance(data, list) else [data]
    out: list[dict[str, Any]] = []
    for r in records:
        if r is None:
            continue
        out.append(r.model_dump() if hasattr(r, "model_dump") else r)
    return out


def register_kg_tools(mcp: FastMCP) -> None:
    @mcp.tool(tags={"kg"})
    async def arr_ingest_library(
        services: str = Field(
            default="movies,series,indexers",
            description=(
                "Comma-separated selection of what to ingest: any of "
                "'movies' (Radarr), 'series' (Sonarr), 'indexers' (Prowlarr)."
            ),
        ),
    ) -> Any:
        """Ingest the live *arr library into epistemic-graph as typed nodes.

        Lists movies/series/indexers via the real clients and pushes them (with their
        :QualityProfile links + :Document overviews) into the knowledge graph via the
        authoritative native-ingest transaction.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        wanted = {s.strip().lower() for s in services.split(",") if s.strip()}
        result: dict[str, Any] = {}

        if "movies" in wanted:
            movies = _records(await run_blocking(get_radarr_client().get_movie))
            result["movies"] = {
                "listed": len(movies),
                "ingested": ingest_movies(movies),
            }
        if "series" in wanted:
            series = _records(await run_blocking(get_sonarr_client().get_series))
            result["series"] = {
                "listed": len(series),
                "ingested": ingest_series(series),
            }
        if "indexers" in wanted:
            indexers = _records(await run_blocking(get_prowlarr_client().get_indexer))
            result["indexers"] = {
                "listed": len(indexers),
                "ingested": ingest_indexers(indexers),
            }
        return result
