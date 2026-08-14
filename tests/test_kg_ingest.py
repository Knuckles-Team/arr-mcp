"""Native epistemic-graph typed-node ingestion — Wire-First coverage for arr-mcp.

Exercises the real ``ingest_entities`` / ``ingest_movies`` / ``ingest_series`` /
``ingest_indexers`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the *arr record → :Movie/:Series/:Indexer mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from arr_mcp.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_indexers,
    ingest_movies,
    ingest_series,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Movie", "title": "p"},
            {"id": "b", "node_type": "QualityProfile"},
        ],
        [{"source": "a", "target": "b", "relationship": "hasQualityProfile"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "arr-mcp"
    assert c.nodes.values["a"]["domain"] == "arr"
    assert c.changes.edges == [("a", "b", {"relationship": "hasQualityProfile"})]


def test_ingest_movies_maps_movie_quality_and_document():
    c = _FakeClient()
    res = ingest_movies(
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
        client=c,
    )
    # 1 movie + 1 quality profile + 1 overview document, 1 hasQualityProfile edge
    assert res == {"nodes": 3, "edges": 1}
    mv = c.nodes.values["arr:Movie:27205"]
    assert mv["node_type"] == "Movie"
    assert mv["title"] == "Inception"
    assert mv["tmdbId"] == "27205"
    assert mv["externalToolId"] == "27205"
    assert c.nodes.values["arr:QualityProfile:1"]["node_type"] == "QualityProfile"
    doc = c.nodes.values["arr:Document:movie:27205"]
    assert doc["node_type"] == "Document"
    assert "thief" in doc["text"]
    assert c.changes.edges == [
        ("arr:Movie:27205", "arr:QualityProfile:1", {"relationship": "hasQualityProfile"})
    ]


def test_ingest_series_maps_series_and_statistics_size():
    c = _FakeClient()
    res = ingest_series(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    sv = c.nodes.values["arr:Series:121361"]
    assert sv["node_type"] == "Series"
    assert sv["tvdbId"] == "121361"
    assert sv["sizeOnDisk"] == 1234
    assert sv["externalToolId"] == "121361"


def test_ingest_indexers_maps_indexer():
    c = _FakeClient()
    res = ingest_indexers(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    ix = c.nodes.values["arr:Indexer:3"]
    assert ix["node_type"] == "Indexer"
    assert ix["name"] == "MyIndexer"
    assert ix["enabled"] is True
    assert ix["protocol"] == "torrent"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "arr:Document:x", "text": "hello", "title": "X"}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.nodes.values["arr:Document:x"]["node_type"] == "Document"


def test_retired_node_type_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}],
            client=_FakeClient(),
        )


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
