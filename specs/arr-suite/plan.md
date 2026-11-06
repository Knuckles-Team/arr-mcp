# CONN-ARR-MCP-SUITE — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

Each app client holds one method per upstream operation, and the SDK serves each method as one typed tool. The Bazarr and Seerr clients come from their API descriptions through `scripts/generate_api_client.py`. The content tier is plain files in the package: skills, prompts and two Turtle files. The tests check that the files agree with the served tools and with medulla core.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp; tests add rdflib and medulla (for the core ontology)
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest, in-process server and mocked HTTP transports
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; no `owl:imports` of core
- **Scale/Scope**: 8 rows, 7 apps, 1,369 operations

## Constitution Check

- One owner per concept: pass. Core classes stay in medulla; the connector only subclasses them.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
arr_mcp/api/api_client_bazarr.py      written from the Bazarr API description
arr_mcp/api/api_client_seerr.py       written from the Seerr API description
arr_mcp/skills/<skill>/SKILL.md       one skill per app plus queue and operations
arr_mcp/prompts/<role>.json           operator and role agent definitions
arr_mcp/ontology/arr.ttl              classes, apps, instances, libraries, routing, federation
arr_mcp/ontology/arr-contracts.ttl    tool-use contracts, skills, prompts, tools
scripts/generate_api_client.py        client writer
tests/fixtures/upstream_operations.json  census fixture
tests/test_suite_surface.py           bound tests
```

## Phase 0: Research

See [research.md](research.md). The census read the upstream API descriptions of each app and the live instances: Radarr 6.4.4, Sonarr 4.0.20, Lidarr 3.1.0, Prowlarr 2.5.1, Chaptarr 0.9.879 (Readarr v1 API), Bazarr 1.6.2 and Seerr 3.5.0. The Servarr clients already covered their APIs. Bazarr covered 10 of 84 operations, with 15 calls to routes Bazarr does not serve. Seerr covered 17 of 217.

## Phase 1: Design

The entities are in [data-model.md](data-model.md). The shortest proof is in [quickstart.md](quickstart.md).

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `spec`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

Each row's `Caller chain:` sentence in [requirements.md](requirements.md) traces the entry point to the code.

## Cross-repo seams

none. The connector calls scion-sdk in process, and reads the medulla core ontology only in tests.
