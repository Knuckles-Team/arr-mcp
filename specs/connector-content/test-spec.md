# CONN-ARR-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |

## Rows awaiting bound tests
- `CONN-ARR-MCP-CONNECTOR-CONTENT-R002`: planned proof `tests/test_ontology_parent_link.py::test_episode_has_no_duplicate_class_iri_with_core`. Expected: Loading arr.ttl with the core ontology yields one :Episode IRI and the connector class is a subclass of mv:TelevisionEpisode.. Refusal: A connector ontology that redeclares the core :Episode IRI fails the duplicate check..
