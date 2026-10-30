---
name: arr-mcp-development
skill_type: skill
description: >-
  Develop, test, package, and release the arr-mcp connector. Use this skill when
  changing Arr API clients, MCP tool registration, connector content, ontology
  assets, documentation, or the repository delivery gates.
domain: development
license: MIT
tags: [arr-mcp, python, mcp, connector, sdk, development, delivery]
metadata:
  author: Repository Maintainers
  version: '0.1.0'
---

# arr-mcp development

`arr-mcp` is the connector for Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Seerr,
and Chaptarr. Keep external API calls, mappings, MCP tools, packaged content, and
connector-owned ontology assets here. Admission, durable graph storage, and
deployment identity remain owned by the SDK, Arbora, and the platform.

## Repository map and real entry points

- `arr_mcp/__init__.py` declares the SDK `Connector`, its instructions, and the
  seven concrete Arr API client targets.
- `arr_mcp/mcp/` contains the registered per-service MCP tools, including the
  consolidated action routers and `arr_ingest_library`.
- `arr_mcp/auth.py` constructs clients from the service-specific `*_BASE_URL`,
  token or API-key, and TLS-profile settings. Do not put credentials in source,
  fixtures, documentation, or skill content.
- `arr_mcp/connector_sources.py` declares the live source presets and mappings.
- `arr_mcp/ontology/` contains `arr.ttl`, source mappings, fixtures, and migration
  metadata for the Arr resource model.
- `arr_mcp/skills/` contains the packaged operations, movie-library,
  series-library, indexer-management, and this development skill.
- `arr_mcp/prompts/` contains the packaged media-curation prompt. `docs/` is the
  MkDocs source, and `tests/` contains client, security, ingestion, and startup
  contract checks.
- The only declared console entry point is `arr-mcp`, provided by
  `scion_sdk.cli:serve`; `arr_mcp/__main__.py` delegates to the SDK
  runner for local invocation.

## Route and inspect before editing

1. Read `AGENTS.md` and locate the owning row with `git grep -n "<term>" --
   specs` before changing behavior.
2. Reuse `scion-sdk` transport, TLS, configuration, and Connector
   registration helpers. Do not add an alternate MCP server or admission path.
3. Keep service-specific API details in the matching client and MCP module. Keep
   shared auth and TLS behavior in `arr_mcp/auth.py` and the SDK helpers.
4. When changing packaged content, check the package-data globs in `pyproject.toml`
   and run the existing content-discovery tests.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver one small, reviewable slice and tie every
claim to a real source path and command.

**Extend first**

- Find the owning requirement before changing behavior and cite its ID in the
  commit `Spec:` trailer. Never hand-edit generated `specs/*/status.json`.
- Bind behavior to an existing focused test or add a focused test under `tests/`
  with the literal spec marker. Keep tests credential-free and network-free.
- Keep one implementation of each capability; use the SDK's governed client and
  TLS profile rather than reintroducing ad-hoc requests or bypasses.

**Five-minute delivery**

- Work from an immutable `origin/main` commit in a private git worktree. Do not
  use `git stash`, force-push, broad staging, live provider calls, or native builds.
- Run the smallest relevant checks first, then the configured commit and push
  gates. A missing dependency or skipped check is an evidence gap, not a pass.
- Put `Spec:` and `Co-Authored-By:` on consecutive lines in the final paragraph of
  each commit message so the shared trailer gate can read both.

## Development and verification commands

Use the committed Python 3.12–3.14 environment and lockfile:

```bash
uv sync --locked
uv run arr-mcp --help
uv run pytest -q tests/test_auth_coverage.py tests/test_sdk_transport.py
uv run ruff check arr_mcp tests
uvx pre-commit run --all-files
uv run mkdocs build --strict
```

The focused tests cover the SDK transport boundary, TLS/auth configuration,
client request security, tool discovery, and packaged ontology/content. Do not
replace them with a live Arr service, real credentials, a package publication,
or a native build. The full hosted release and Pages workflows remain CI-owned.

## Connector content and Pages delivery

The canonical Pages caller is `.github/workflows/pages.yml`. It invokes
`Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main` with the
`docs` content source and `.config/spec-dashboard.json`; the trigger covers docs,
specs, the dashboard config, and the caller. Keep one Pages publisher and do not
add a competing `mkdocs gh-deploy` workflow.

The canonical pre-commit aggregate is supplied by `Knuckles-Team/pipelines` at
`rev: main`. Keep `connector-standard`, `secrets`, `spec`, `tests-fast`, and
`dependency-readiness` in `.pre-commit-config.yaml`; `spec` and `tests-fast` run
at pre-push.

## Runtime and release discipline

- Preserve the MCP transport's explicit auth requirement, loopback default, and
  fixed non-root/read-only deployment boundary. Provider endpoints and tokens are
  runtime configuration only.
- The central `[tool.pipelines.container]` table is the source for generated
  connector deployment files. `compose_host` and `publish_port` use validated
  literals or typed `{env, default}` bindings; do not use arbitrary Compose
  interpolation or reintroduce committed generated Docker files.
- There are no connector-owned persistent state volumes. Do not add one for
  provider credentials or caches; the connector remains stateless and read-only.
- When packaged skills or other package metadata change, advance the patch
  version and refresh `uv.lock` together. Verify the version and lock entry before
  review; never hand-edit generated status.
- Review the exact candidate head and hosted checks before merging. After merge,
  verify Pages uses that exact main SHA and that the public `/spec-delivery/`
  index and snapshot return HTTP 200 with the merged revision.
