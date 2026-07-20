"""Native epistemic-graph typed-node ingestion — Wire-First coverage for arr-mcp.

Exercises the real ``ingest_entities`` / ``ingest_movies`` / ``ingest_series`` /
``ingest_indexers`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the *arr record → :Movie/:Series/:Indexer mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from arr_mcp.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_indexers,
    ingest_movies,
    ingest_series,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Movie", "title": "p"},
            {"id": "b", "node_type": "QualityProfile"},
        ],
        [{"source": "a", "target": "b", "relationship": "hasQualityProfile"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "arr-mcp"
    assert c.txn.nodes["a"]["domain"] == "arr"
    assert c.txn.edges == [("a", "b", {"relationship": "hasQualityProfile"})]


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
        graph="__commons__",
    )
    # 1 movie + 1 quality profile + 1 overview document, 1 hasQualityProfile edge
    assert res == {"nodes": 3, "edges": 1}
    mv = c.txn.nodes["arr:Movie:27205"]
    assert mv["node_type"] == "Movie"
    assert mv["title"] == "Inception"
    assert mv["tmdbId"] == "27205"
    assert mv["externalToolId"] == "27205"
    assert c.txn.nodes["arr:QualityProfile:1"]["node_type"] == "QualityProfile"
    doc = c.txn.nodes["arr:Document:movie:27205"]
    assert doc["node_type"] == "Document"
    assert "thief" in doc["text"]
    assert c.txn.edges == [
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    sv = c.txn.nodes["arr:Series:121361"]
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    ix = c.txn.nodes["arr:Indexer:3"]
    assert ix["node_type"] == "Indexer"
    assert ix["name"] == "MyIndexer"
    assert ix["enabled"] is True
    assert ix["protocol"] == "torrent"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "arr:Document:x", "text": "hello", "title": "X"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["arr:Document:x"]["node_type"] == "Document"


def test_retired_node_type_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}],
            client=_FakeClient(),
        )


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
