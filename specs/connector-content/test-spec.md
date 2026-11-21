# CONN-ARR-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R003` | `tests/test_pack_extends_core.py` | No core term is redeclared and no retired IRI base remains. |

## Rows awaiting bound tests
- `CONN-ARR-MCP-CONNECTOR-CONTENT-R002`: proof `tests/test_ontology_parent_link.py::test_episode_has_no_duplicate_class_iri_with_core`. Expected: The packaged ontology declares no `:Episode` class and no class outside the arr namespace. Refusal: A connector ontology that redeclares the core :Episode IRI fails the duplicate check..
