# CONN-ARR-MCP-COMPETENCY-OPERATIONS — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ARR-MCP-COMPETENCY-OPERATIONS-R001` | The connector must serve a `prowlarr_action` history-by-title projection that returns the last searched indexer for a title. Radarr and Sonarr keep no per-title search log, and Prowlarr history is keyed by query, so the projection joins them by title. Proving test: `tests/test_prowlarr_history_by_title.py`. | The operation returns the documented fields. |
