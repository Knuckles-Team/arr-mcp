"""CONN-ARR-MCP-CONNECTOR-CONTENT-R002: the connector ontology redeclares no core class."""

from pathlib import Path

import pytest

rdflib = pytest.importorskip("rdflib")
from rdflib.namespace import OWL, RDF  # noqa: E402

ONTOLOGY = Path(__file__).resolve().parents[1] / "arr_mcp" / "ontology"


@pytest.mark.spec("CONN-ARR-MCP-CONNECTOR-CONTENT-R002")
def test_episode_has_no_duplicate_class_iri_with_core():
    graph = rdflib.Graph()
    for path in ONTOLOGY.glob("*.ttl"):
        graph.parse(path, format="turtle")
    declared = {str(c) for c in graph.subjects(RDF.type, OWL.Class)}
    assert "https://knuckles-team.github.io/ontology/core#Episode" not in declared
    assert all(c.startswith("https://knuckles-team.github.io/ontology/connector/arr#") for c in declared)
