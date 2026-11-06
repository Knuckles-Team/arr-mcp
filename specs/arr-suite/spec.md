# CONN-ARR-MCP-SUITE — The arr suite surface and its content

Owner: arr-mcp. Cross-repo IDs: none.

## Purpose and user stories

An operator runs the arr media suite through one connector. Each suite app must be reachable through typed tools for its whole API. An agent must know which tools to call, in which order, and where the data lives. Arbora builds agents from the connector's prompts, so each prompt must be a complete agent definition.

## Why a new spec

No local spec owns the per-app tool surface or the per-app content. `CONN-ARR-MCP-CONNECTOR-CONTENT` owns only how the SDK serves packaged content. This spec owns what the content says and the tool surface it names.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md) for Radarr, Sonarr, Lidarr, Prowlarr, Chaptarr, Bazarr and Seerr. Out of scope: the SDK tool registration and content serving (scion-sdk), the fleet gateway catalog (arbora), and the core ontology (medulla).

## User Scenarios & Testing

### User Story 1 - Every operation is a typed tool (Priority: P1)

An operator calls any upstream operation of any suite app as one typed tool, and a wrong route fails instead of returning a web page.

**Acceptance Scenarios**:

1. **Given** the connector is built, **When** the tools are listed, **Then** each census operation has one tool (`CONN-ARR-MCP-SUITE-R001`) and no tool routes by action (`CONN-ARR-MCP-SUITE-R002`).
2. **Given** an app answers with a web page, **When** a tool runs, **Then** it raises `NOT_AN_API_RESPONSE` (`CONN-ARR-MCP-SUITE-R003`).

### User Story 2 - Agents follow tool-use contracts (Priority: P1)

An agent built from a connector prompt runs a named workflow, such as add a movie and search, with the steps and parameters the contract gives.

**Acceptance Scenarios**:

1. **Given** the content is served, **When** an agent reads a skill, **Then** each workflow names served tools in order (`CONN-ARR-MCP-SUITE-R004`).
2. **Given** arbora reads the prompts, **When** it builds an agent, **Then** the prompt gives the role, goal, skills, tools, data locations, guardrails and outputs (`CONN-ARR-MCP-SUITE-R005`).

### User Story 3 - The graph knows where the data lives (Priority: P2)

A graph query answers which instance holds which library, where its files are, and how the apps federate, with every class under medulla core.

**Acceptance Scenarios**:

1. **Given** the ontology is loaded, **When** a query asks where films live, **Then** it gets the Radarr instance and `/movies` (`CONN-ARR-MCP-SUITE-R006`).
2. **Given** medulla core is loaded, **When** the arr classes are checked, **Then** each class reaches `bfo:Entity` without an import (`CONN-ARR-MCP-SUITE-R007`), and ingest emits core classes (`CONN-ARR-MCP-SUITE-R008`).

### Edge Cases

- An app with no root folder (Chaptarr today) must make its add contract stop at step 1 and report it.
- An upstream route that is only a web sign-in page is excluded from the census and listed in the fixture.

## Requirements

- **FR-001**: Every upstream operation is one tool. Rows: `CONN-ARR-MCP-SUITE-R001`.
- **FR-002**: Typed tools only. Rows: `CONN-ARR-MCP-SUITE-R002`.
- **FR-003**: The response boundary refuses web pages. Rows: `CONN-ARR-MCP-SUITE-R003`.
- **FR-004**: Skills carry the task workflows as tool-use contracts. Rows: `CONN-ARR-MCP-SUITE-R004`.
- **FR-005**: Prompts are agent definitions. Rows: `CONN-ARR-MCP-SUITE-R005`.
- **FR-006**: Data location, routing and federation. Rows: `CONN-ARR-MCP-SUITE-R006`.
- **FR-007**: Every class rolls up to medulla core. Rows: `CONN-ARR-MCP-SUITE-R007`.
- **FR-008**: Ingest uses core classes and served tools. Rows: `CONN-ARR-MCP-SUITE-R008`.
- **FR-009**: Bazarr's hidden operations are tools. Rows: `CONN-ARR-MCP-SUITE-R009`.
- **FR-010**: A failed call says why, and long calls get time. Rows: `CONN-ARR-MCP-SUITE-R010`.
- **FR-011**: Provisioning workflows proven live are contracts. Rows: `CONN-ARR-MCP-SUITE-R011`.
- **FR-012**: Settings reads never return secret values. Rows: `CONN-ARR-MCP-SUITE-R012`.
- **FR-013**: The whole surface is declared. Rows: `CONN-ARR-MCP-SUITE-R013`.

## Success Criteria

- **SC-001**: 1,373 of 1,373 census operations are served as typed tools. Rows: `CONN-ARR-MCP-SUITE-R001`.
- **SC-002**: 0 tools route by action or take `params_json`. Rows: `CONN-ARR-MCP-SUITE-R002`.
- **SC-003**: 100% of contract, skill and prompt tool names are served tools. Rows: `CONN-ARR-MCP-SUITE-R004`, `CONN-ARR-MCP-SUITE-R005`.
- **SC-004**: 100% of arr classes reach `BFO_0000001` through medulla core. Rows: `CONN-ARR-MCP-SUITE-R007`.

## Assumptions

- The upstream API descriptions in the census fixture match the deployed app versions it names.
- Chaptarr serves the Readarr v1 API.
- The SDK serves packaged skills, prompts and ontology files (`CONN-ARR-MCP-CONNECTOR-CONTENT-R001`).

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-ARR-MCP-SUITE-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-ARR-MCP-SUITE-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-ARR-MCP-SUITE-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
| FR-004 | `CONN-ARR-MCP-SUITE-R004` | [plan.md](plan.md) | T-004 | [test-spec.md](test-spec.md) |
| FR-005 | `CONN-ARR-MCP-SUITE-R005` | [plan.md](plan.md) | T-005 | [test-spec.md](test-spec.md) |
| FR-006 | `CONN-ARR-MCP-SUITE-R006` | [plan.md](plan.md) | T-006 | [test-spec.md](test-spec.md) |
| FR-007 | `CONN-ARR-MCP-SUITE-R007` | [plan.md](plan.md) | T-007 | [test-spec.md](test-spec.md) |
| FR-008 | `CONN-ARR-MCP-SUITE-R008` | [plan.md](plan.md) | T-008 | [test-spec.md](test-spec.md) |
| FR-009 | `CONN-ARR-MCP-SUITE-R009` | [plan.md](plan.md) | T-009 | [test-spec.md](test-spec.md) |
| FR-010 | `CONN-ARR-MCP-SUITE-R010` | [plan.md](plan.md) | T-010 | [test-spec.md](test-spec.md) |
| FR-011 | `CONN-ARR-MCP-SUITE-R011` | [plan.md](plan.md) | T-011 | [test-spec.md](test-spec.md) |
| FR-012 | `CONN-ARR-MCP-SUITE-R012` | [plan.md](plan.md) | T-012 | [test-spec.md](test-spec.md) |
| FR-013 | `CONN-ARR-MCP-SUITE-R013` | [plan.md](plan.md) | T-013 | [test-spec.md](test-spec.md) |
