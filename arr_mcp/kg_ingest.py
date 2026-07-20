"""Native epistemic-graph ingestion for *arr records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The required agent-utilities
native-ingest primitive owns the transaction and raises NativeIngestError when the
authoritative engine cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "arr-mcp"
_DOMAIN = "arr"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through agent-utilities."""
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write searchable documents through the authoritative native-ingest path."""
    return _native_ingest_documents(
        documents,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def _ext_id(record: dict[str, Any], *keys: str) -> str | None:
    """First non-empty external id from ``keys``, coerced to string."""
    for k in keys:
        v = record.get(k)
        if v is not None and v != "" and v != 0:
            return str(v)
    # fall back to internal arr id
    v = record.get("id")
    return str(v) if v is not None else None


def ingest_movies(
    movies: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Radarr movie records → ``:Movie`` nodes (+ overview ``:Document`` links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    docs: list[dict[str, Any]] = []
    for m in movies or []:
        ext = _ext_id(m, "tmdbId", "imdbId")
        if ext is None:
            continue
        mid = f"arr:Movie:{ext}"
        entities.append(
            {
                "id": mid,
                "node_type": "Movie",
                "title": m.get("title"),
                "year": m.get("year"),
                "tmdbId": str(m["tmdbId"]) if m.get("tmdbId") else None,
                "imdbId": m.get("imdbId"),
                "mediaStatus": m.get("status"),
                "monitored": m.get("monitored"),
                "hasFile": m.get("hasFile"),
                "sizeOnDisk": m.get("sizeOnDisk"),
                "externalToolId": ext,
            }
        )
        qp = m.get("qualityProfileId")
        if qp is not None:
            qid = f"arr:QualityProfile:{qp}"
            entities.append({"id": qid, "node_type": "QualityProfile"})
            relationships.append(
                {"source": mid, "target": qid, "relationship": "hasQualityProfile"}
            )
        if m.get("overview"):
            did = f"arr:Document:movie:{ext}"
            docs.append(
                {
                    "id": did,
                    "text": m["overview"],
                    "title": m.get("title"),
                    "source_uri": f"tmdb:{m.get('tmdbId')}"
                    if m.get("tmdbId")
                    else None,
                }
            )
    res = ingest_entities(entities, relationships, client=client, graph=graph)
    doc_res = (
        ingest_documents(docs, client=client, graph=graph)
        if docs
        else {"nodes": 0, "edges": 0}
    )
    return _merge(res, doc_res)


def ingest_series(
    series: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Sonarr series records → ``:Series`` nodes (+ overview ``:Document`` links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    docs: list[dict[str, Any]] = []
    for s in series or []:
        ext = _ext_id(s, "tvdbId", "imdbId")
        if ext is None:
            continue
        sid = f"arr:Series:{ext}"
        entities.append(
            {
                "id": sid,
                "node_type": "Series",
                "title": s.get("title"),
                "year": s.get("year"),
                "tvdbId": str(s["tvdbId"]) if s.get("tvdbId") else None,
                "imdbId": s.get("imdbId"),
                "mediaStatus": s.get("status"),
                "monitored": s.get("monitored"),
                "sizeOnDisk": (s.get("statistics") or {}).get("sizeOnDisk"),
                "externalToolId": ext,
            }
        )
        qp = s.get("qualityProfileId")
        if qp is not None:
            qid = f"arr:QualityProfile:{qp}"
            entities.append({"id": qid, "node_type": "QualityProfile"})
            relationships.append(
                {"source": sid, "target": qid, "relationship": "hasQualityProfile"}
            )
        if s.get("overview"):
            did = f"arr:Document:series:{ext}"
            docs.append(
                {
                    "id": did,
                    "text": s["overview"],
                    "title": s.get("title"),
                    "source_uri": f"tvdb:{s.get('tvdbId')}"
                    if s.get("tvdbId")
                    else None,
                }
            )
    res = ingest_entities(entities, relationships, client=client, graph=graph)
    doc_res = (
        ingest_documents(docs, client=client, graph=graph)
        if docs
        else {"nodes": 0, "edges": 0}
    )
    return _merge(res, doc_res)


def ingest_indexers(
    indexers: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Prowlarr/*arr indexer records → ``:Indexer`` nodes."""
    entities: list[dict[str, Any]] = []
    for ix in indexers or []:
        iid = ix.get("id")
        if iid is None:
            continue
        entities.append(
            {
                "id": f"arr:Indexer:{iid}",
                "node_type": "Indexer",
                "name": ix.get("name"),
                "protocol": ix.get("protocol"),
                "enabled": ix.get("enable"),
                "priority": ix.get("priority"),
                "implementation": ix.get("implementation"),
                "externalToolId": str(iid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def _merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Sum two authoritative native-ingest results."""
    return {
        "nodes": a.get("nodes", 0) + b.get("nodes", 0),
        "edges": a.get("edges", 0) + b.get("edges", 0),
    }
