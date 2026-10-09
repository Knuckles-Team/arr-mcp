"""Native epistemic-graph ingestion for *arr records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The agent-connector-sdk knowledge-ingest
facade owns the transaction and raises IngestError when the authoritative engine cannot
commit.
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_BINDING = IngestBinding(connector="arr-mcp", stream="arr")


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={k: v for k, v in record.items() if k not in ("id", "node_type")},
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    props = {
        k: v for k, v in record.items() if k not in ("source", "target", "relationship")
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=props or None,
    )


def _to_document(record: dict[str, Any]) -> Document:
    return Document(
        id=record.get("id"),
        text=record.get("text"),
        title=record.get("title"),
        source_uri=record.get("source_uri"),
        properties={
            k: v
            for k, v in record.items()
            if k not in ("id", "text", "title", "source_uri")
        },
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through agent-connector-sdk."""
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships or ()),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write searchable documents through the authoritative knowledge-ingest path."""
    if not documents:
        raise IngestError("ingest_documents needs at least one document")
    change_set = ChangeSet(documents=tuple(_to_document(d) for d in documents))
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


def _ext_id(record: dict[str, Any], *keys: str) -> str | None:
    """First non-empty external id from ``keys``, coerced to string."""
    for k in keys:
        v = record.get(k)
        if v is not None and v != "" and v != 0:
            return str(v)
    # fall back to internal arr id
    v = record.get("id")
    return str(v) if v is not None else None


async def ingest_movies(
    movies: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
    res = await ingest_entities(entities, relationships, ingest=ingest)
    doc_res = (
        await ingest_documents(docs, ingest=ingest) if docs else {"nodes": 0, "edges": 0}
    )
    return _merge(res, doc_res)


async def ingest_series(
    series: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
    res = await ingest_entities(entities, relationships, ingest=ingest)
    doc_res = (
        await ingest_documents(docs, ingest=ingest) if docs else {"nodes": 0, "edges": 0}
    )
    return _merge(res, doc_res)


async def ingest_indexers(
    indexers: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
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
    return await ingest_entities(entities, ingest=ingest)


def _merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """Sum two authoritative knowledge-ingest results."""
    return {
        "nodes": a.get("nodes", 0) + b.get("nodes", 0),
        "edges": a.get("edges", 0) + b.get("edges", 0),
    }
