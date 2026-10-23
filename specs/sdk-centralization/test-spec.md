# CONN-ARR-MCP-SDK-CENTRALIZATION — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Level | Setup and input | Expected observation | Evidence |
|---|---|---|---|---|---|
| T-001 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001` | Unit | Every child row. | See each child. |  |
| T-002 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.1` | Unit | `tests/test_sdk_transport.py::test_clients_are_governed_and_send_the_api_key` | Each client holds an SDK client, sends the key header and imports no `requests`. |  |
| T-003 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.2` | Unit | `tests/test_auth_coverage.py::test_session_uses_resolved_tls_profile` | The client is built with the resolved profile. |  |
| T-004 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.3` | Unit | `tests/test_sdk_transport.py::test_request_shapes_are_unchanged` | A request keeps its path, query and JSON body, and each status maps as before. |  |
| T-005 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001.4` | Unit | `tests/test_sdk_transport.py::test_dependencies_come_from_the_sdk` | `pyproject.toml` has no `requests` or `urllib3` pin and the SDK floor is `0.3.11` or later. |  |
