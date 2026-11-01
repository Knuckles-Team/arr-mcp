# CONN-ARR-MCP-SDK-CENTRALIZATION — Capabilities through the SDK

Owner: .. Cross-repo IDs: `SCION-CENTRALIZED-CAPABILITIES-R001`, `SCION-CENTRALIZED-CAPABILITIES-R003`, `SCION-CENTRALIZED-CAPABILITIES-R008`, `SCION-CENTRALIZED-CAPABILITIES-R040`.

Extends: [SCION-CENTRALIZED-CAPABILITIES](https://github.com/Knuckles-Team/scion-sdk/blob/main/specs/centralized-capabilities/spec.md)

## Purpose and user stories

The connector must reach the arr media services through the SDK. The SDK owns the governed HTTP client, retry, TLS profiles and optional dependencies.

An operator points the connector at the arr media services. Transport security and retries come from the SDK, not from connector code.

## Why a new spec

The search covered `specs/` of this repository and the SDK centralized-capabilities spec. This repository had no spec for these capabilities. The SDK owns them. This spec states how this connector uses them.

## Scope and interfaces

In scope: the connector's HTTP client, retry handling, TLS handling and dependency pins.

Out of scope: the tool surface, which stays one tool per API operation, and the SDK modules themselves.

## User Scenarios & Testing

### User Story 1 - Capabilities through the SDK (Priority: P1)

The connector must reach the arr media services through the SDK. The SDK owns the governed HTTP client, retry, TLS profiles and optional dependencies.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-ARR-MCP-SDK-CENTRALIZATION-R001` (capabilities come from the sdk (rollup)) is exercised, **Then** see each child.

### Edge Cases

- If `CONN-ARR-MCP-SDK-CENTRALIZATION-R001` is not met, its proving test fails: capabilities come from the sdk (rollup).

## Requirements

- **FR-001**: Capabilities come from the SDK (rollup). Rows: `CONN-ARR-MCP-SDK-CENTRALIZATION-R001`.

## Success Criteria

- **SC-001**: See each child. Rows: `CONN-ARR-MCP-SDK-CENTRALIZATION-R001`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-ARR-MCP-SDK-CENTRALIZATION-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
