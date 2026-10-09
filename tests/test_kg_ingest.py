"""Knowledge-ingest typed-node ingestion — Wire-First coverage for arr-mcp.

Exercises the real ``ingest_entities`` / ``ingest_movies`` / ``ingest_series`` /
``ingest_indexers`` seam against a fake epistemic-graph transport (no engine required),
letting the agent-connector-sdk's own request builder run on top of it so the test
exercises the SDK's validation contract rather than re-deriving it.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from arr_mcp.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_indexers,
    ingest_movies,
    ingest_series,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Movie", "title": "p"},
            {"id": "b", "node_type": "QualityProfile"},
        ],
        [{"source": "a", "target": "b", "relationship": "hasQualityProfile"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert {r.record_id for r in request.records} == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["title"] == "p"
    assert request.relationships[0].source.record_id == "a"
    assert request.relationships[0].target.record_id == "b"
    assert request.relationships[0].relation_reference.endswith(
        "/relations/hasQualityProfile"
    )


@pytest.mark.asyncio
async def test_ingest_movies_maps_movie_quality_and_document(ingest):
    service, transport = ingest
    res = await ingest_movies(
        [
            {
                "id": 5,
                "tmdbId": 27205,
                "title": "Inception",
                "year": 2010,
                "status": "released",
                "monitored": True,
                "hasFile": True,
                "qualityProfileId": 1,
                "overview": "A thief who steals corporate secrets.",
            }
        ],
        ingest=service,
    )
    # 1 movie + 1 quality profile + 1 overview document, 1 hasQualityProfile edge
    assert res == {"nodes": 3, "edges": 1}
    # two submits: entities+relationships, then the overview document
    assert len(transport.requests) == 2
    entity_request, doc_request = transport.requests
    mv = next(r for r in entity_request.records if r.record_id == "arr:Movie:27205")
    assert mv.payload["title"] == "Inception"
    assert mv.payload["tmdbId"] == "27205"
    assert mv.payload["externalToolId"] == "27205"
    assert any(
        r.record_id == "arr:QualityProfile:1" for r in entity_request.records
    )
    assert entity_request.relationships[0].source.record_id == "arr:Movie:27205"
    assert entity_request.relationships[0].target.record_id == "arr:QualityProfile:1"
    doc = doc_request.records[0]
    assert doc.record_id == "arr:Document:movie:27205"
    assert "thief" in doc.payload["text"]


@pytest.mark.asyncio
async def test_ingest_series_maps_series_and_statistics_size(ingest):
    service, transport = ingest
    res = await ingest_series(
        [
            {
                "id": 9,
                "tvdbId": 121361,
                "title": "The Expanse",
                "year": 2015,
                "status": "ended",
                "monitored": True,
                "statistics": {"sizeOnDisk": 1234},
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    sv = transport.requests[0].records[0]
    assert sv.record_id == "arr:Series:121361"
    assert sv.payload["tvdbId"] == "121361"
    assert sv.payload["sizeOnDisk"] == 1234
    assert sv.payload["externalToolId"] == "121361"


@pytest.mark.asyncio
async def test_ingest_indexers_maps_indexer(ingest):
    service, transport = ingest
    res = await ingest_indexers(
        [
            {
                "id": 3,
                "name": "MyIndexer",
                "protocol": "torrent",
                "enable": True,
                "priority": 25,
                "implementation": "Torznab",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    ix = transport.requests[0].records[0]
    assert ix.record_id == "arr:Indexer:3"
    assert ix.payload["name"] == "MyIndexer"
    assert ix.payload["enabled"] is True
    assert ix.payload["protocol"] == "torrent"


@pytest.mark.asyncio
async def test_ingest_documents_writes_document_nodes(ingest):
    service, transport = ingest
    res = await ingest_documents(
        [{"id": "arr:Document:x", "text": "hello", "title": "X"}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert transport.requests[0].records[0].record_id == "arr:Document:x"


@pytest.mark.asyncio
async def test_missing_node_type_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}],
            ingest=service,
        )


@pytest.mark.asyncio
async def test_empty_entities_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
