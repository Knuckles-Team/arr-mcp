"""Native epistemic-graph ingestion for *arr records (typed graph nodes + documents).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the arr-mcp connector natively pushes its library
into the epistemic-graph knowledge graph as **typed OWL nodes** (``:Movie``, ``:Series``,
``:Indexer``, …) + links, plus semantic **:Document** overviews, using the lightweight
engine client (``GraphComputeEngine()._client`` + ``txn``) — the same fast client the blob
``MediaStore`` uses, NOT the heavy in-process ingestion engine.

Entirely dependency-/engine-guarded: with no agent-utilities KG stack or no reachable
engine, every entry point **no-ops** (returns ``None``), so the connector keeps working
with zero KG infrastructure. Nodes carry the shared provenance (``domain``/``source``)
and match the classes federated by ``arr_mcp.ontology`` (``arr.ttl``). Node ids follow
``arr:<Class>:<externalId>``.

Thin mapper only: the txn write path lives once in
``agent_utilities.knowledge_graph.memory.native_ingest``. This module prefers that shared
primitive and falls back to a self-contained txn implementation when the primitive is not
present in the installed agent_utilities.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("arr_mcp.kg")

_SOURCE = "arr-mcp"
_DOMAIN = "arr"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------------------
# Shared-primitive bridge (guarded) + self-contained fallback.
# --------------------------------------------------------------------------------------
def _shared():
    """Return the shared native_ingest module, or ``None`` if unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest
    except Exception as e:  # noqa: BLE001 — primitive not installed yet
        logger.debug("shared native_ingest unavailable: %s", e)
        return None


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    shared = _shared()
    if shared is not None:
        try:
            return shared.native_client()
        except Exception as e:  # noqa: BLE001
            logger.debug("shared native_client failed: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed nodes (+ edges) into epistemic-graph via the fast engine client.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":rel}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    Delegates to the shared primitive when present; otherwise runs a self-contained txn.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None

    shared = _shared()
    if shared is not None and client is None:
        try:
            return shared.ingest_entities(
                entities, relationships, source=source, domain=domain
            )
        except Exception as e:  # noqa: BLE001 — fall through to local txn
            logger.debug("shared ingest_entities failed, using fallback: %s", e)

    if client is None:
        client, graph = _client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH

    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write ``:Document`` nodes (text worth semantic search) into the engine.

    ``docs``: ``[{"id":..., "text":..., "title":..., "source_uri":...}]``. Delegates to
    the shared primitive when present; otherwise ingests as ``:Document`` typed nodes.
    """
    docs = [d for d in (docs or []) if d.get("id") and d.get("text")]
    if not docs:
        return None

    shared = _shared()
    if shared is not None and client is None and hasattr(shared, "ingest_documents"):
        try:
            return shared.ingest_documents(docs, source=source, domain=domain)
        except Exception as e:  # noqa: BLE001 — fall through
            logger.debug("shared ingest_documents failed, using fallback: %s", e)

    entities = [
        {
            "id": d["id"],
            "type": "Document",
            "text": d.get("text"),
            "title": d.get("title"),
            "source_uri": d.get("source_uri"),
        }
        for d in docs
    ]
    return ingest_entities(
        entities, source=source, domain=domain, client=client, graph=graph
    )


# --------------------------------------------------------------------------------------
# Record → typed-node mappers (the thin, connector-specific layer).
# --------------------------------------------------------------------------------------
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
) -> dict[str, int] | None:
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
                "type": "Movie",
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
            entities.append({"id": qid, "type": "QualityProfile"})
            relationships.append(
                {"source": mid, "target": qid, "type": "hasQualityProfile"}
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
    doc_res = ingest_documents(docs, client=client, graph=graph)
    return _merge(res, doc_res)


def ingest_series(
    series: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                "type": "Series",
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
            entities.append({"id": qid, "type": "QualityProfile"})
            relationships.append(
                {"source": sid, "target": qid, "type": "hasQualityProfile"}
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
    doc_res = ingest_documents(docs, client=client, graph=graph)
    return _merge(res, doc_res)


def ingest_indexers(
    indexers: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Prowlarr/*arr indexer records → ``:Indexer`` nodes."""
    entities: list[dict[str, Any]] = []
    for ix in indexers or []:
        iid = ix.get("id")
        if iid is None:
            continue
        entities.append(
            {
                "id": f"arr:Indexer:{iid}",
                "type": "Indexer",
                "name": ix.get("name"),
                "protocol": ix.get("protocol"),
                "enabled": ix.get("enable"),
                "priority": ix.get("priority"),
                "implementation": ix.get("implementation"),
                "externalToolId": str(iid),
            }
        )
    return ingest_entities(entities, client=client, graph=graph)


def _merge(a: dict[str, int] | None, b: dict[str, int] | None) -> dict[str, int] | None:
    """Sum two ``{"nodes":..,"edges":..}`` results, tolerating ``None``."""
    if a is None and b is None:
        return None
    a = a or {}
    b = b or {}
    return {
        "nodes": a.get("nodes", 0) + b.get("nodes", 0),
        "edges": a.get("edges", 0) + b.get("edges", 0),
    }
