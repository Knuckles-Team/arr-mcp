# CONN-ARR-MCP-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: arr-mcp. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `arr-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - The connector serves its packaged content (Priority: P1)

The `arr-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-ARR-MCP-CONNECTOR-CONTENT-R002` (the connector ontology redeclares no core class) is exercised, **Then** the ontology declares classes only in the arr namespace.
3. **Given** the connector is configured, **When** the behaviour of row `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.
4. **Given** the connector is configured, **When** the behaviour of row `CONN-ARR-MCP-CONNECTOR-CONTENT-R003` (pack extends only the core ontology) is exercised, **Then** no core class or property is redeclared and no retired IRI base remains. Test: `tests/test_pack_extends_core.py::test_pack_declares_no_core_term`.

### Edge Cases

- If `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.
- If `CONN-ARR-MCP-CONNECTOR-CONTENT-R002` is not met, its proving test fails: the connector ontology redeclares no core class.
- If `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.
- If `CONN-ARR-MCP-CONNECTOR-CONTENT-R003` is not met, its proving test fails: pack extends only the core ontology.

## Requirements

- **FR-001**: Default content. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R001`.
- **FR-002**: The connector ontology redeclares no core class. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R002`.
- **FR-003**: Default content. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R001`.
- **FR-004**: Pack extends only the core ontology. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R003`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R001`.
- **SC-002**: The connector ontology redeclares no core class. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R002`.
- **SC-003**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R001`.
- **SC-004**: No pack term redeclares a core term and no retired IRI base remains. Rows: `CONN-ARR-MCP-CONNECTOR-CONTENT-R003`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-ARR-MCP-CONNECTOR-CONTENT-R003` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
