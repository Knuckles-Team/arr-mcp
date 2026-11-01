# CONN-ARR-MCP-COMPETENCY-OPERATIONS — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ARR-MCP-COMPETENCY-OPERATIONS-R001` | The connector must serve a `prowlarr_action` history-by-title projection that returns the last searched indexer for a title. Radarr and Sonarr keep no per-title search log, and Prowlarr history is keyed by query, so the projection joins them by title. Proving test: `tests/test_prowlarr_history_by_title.py`. Caller chain: (planned) the `prowlarr_action` MCP tool (`arr_mcp/mcp/mcp_prowlarr.py:17`, registered by `register_prowlarr_tools`) -> `dispatch_async` -> a new history-by-title method on `ProwlarrApi` (`arr_mcp/api/api_client_prowlarr.py`), beside the existing `get_history_indexer` at line 495. Shape: (planned) add one `ProwlarrApi` method that reads `get_history` and joins records to the Radarr `get_movie` or Sonarr `get_series` title, reusing the `request` helper and `dispatch_async` action lookup; no new tool, only a new action. | The operation returns the documented fields. Planned test: `tests/test_prowlarr_history_by_title.py::test_history_by_title_returns_last_indexer`. |
