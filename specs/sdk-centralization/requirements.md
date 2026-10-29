# CONN-ARR-MCP-SDK-CENTRALIZATION — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A child row `.n` is one five-minute unit of work. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ARR-MCP-SDK-CENTRALIZATION-R001` | **Capabilities come from the SDK (rollup).** The connector must use the SDK for HTTP, retry, TLS and optional dependencies. Children `.1` to `.4` deliver it. | See each child. |
| `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.1` | **Governed client.** Every arr API client must send HTTP through the SDK governed client and must not import `requests` or `urllib3` (`SCION-CENTRALIZED-CAPABILITIES-R001`, `SCION-CENTRALIZED-CAPABILITIES-R003`). The service key must travel as SDK API-key auth in the `X-Api-Key` header. The generator must emit the same client. Proving test: `tests/test_sdk_transport.py::test_clients_are_governed_and_send_the_api_key`. | Each client holds an SDK client, sends the key header and imports no `requests`. |
| `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.2` | **TLS profile only.** Each client must take transport trust from `resolve_tls_profile` for its service prefix (`SCION-CENTRALIZED-CAPABILITIES-R008`). The connector must not read a verification flag. Proving test: `tests/test_auth_coverage.py::test_session_uses_resolved_tls_profile`. | The client is built with the resolved profile. |
| `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.3` | **Same behaviour.** Each client must keep the origin check, the response size and time limits, and the redirect refusal. A status of 400 or more must raise `API error: HTTP <status>`. A 204 must return a success marker. Proving test: `tests/test_sdk_transport.py::test_request_shapes_are_unchanged`. | A request keeps its path, query and JSON body, and each status maps as before. |
| `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.4` | **SDK floor.** The package must depend on `agent-connector-sdk[mcp]` at the latest release floor and must not pin `requests` or `urllib3` (`SCION-CENTRALIZED-CAPABILITIES-R040`). Proving test: `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk`. | `pyproject.toml` has no `requests` or `urllib3` pin and the SDK floor is `0.3.11` or later. |
