# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-11-06

### Changed
- Every upstream API operation of Radarr, Sonarr, Lidarr, Chaptarr, Prowlarr, Bazarr and Seerr is one typed tool (1,369 operations, 1,375 tools). The Bazarr client (84 operations, from the live API description) and the Seerr client (217 operations) are rewritten; their tool names follow the upstream operations.
- Knowledge-graph ingest emits the medulla core classes `Film`, `Series`, `MediaIndexer` and `QualityProfile`; the ingest presets name the typed tools.
- Require `scion-sdk>=0.8.2,<0.9`.

### Removed
- The `<app>_action` tools and the `<app>_request` raw-request tools.

### Fixed
- An HTML answer (a wrong route or a refused key) raises `NOT_AN_API_RESPONSE` instead of returning `status: success`. Fifteen Bazarr operations called routes Bazarr does not serve.
- Sonarr `GET /api/v3/rename/bulk` is served.

### Added
- Skills with task workflows for every app, the download queue and suite operations; agent-definition prompts for the operator and five roles; an ontology of apps, instances, libraries, data locations, routing, federation and 22 tool-use contracts, rolled up to medulla core.

## [2.3.8] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

## [0.15.0] - 2026-05-22

### Added
- Consolidated testing suite `conftest.py` with standard reusable fixtures for requests mocking and environment safety.
- Complete documentation of all 27 environment variables in `.env.example` and `README.md`.
- Inline concept markers (`CONCEPT:ECO-4.1`, `CONCEPT:OS-5.4`, `CONCEPT:OS-5.1`) to codebase functions and test docstrings for improved concept traceability.
- Top-level `Usage & Quick Start` guide with copy-pasteable execution examples in `README.md`.

### Fixed
- Fixed 2 broken internal references (`docs/mcp.md`, `docs/agent.md`) in `README.md`.
- Achieved 100% pytest test suite pass rate and 100% code coverage.

## [0.2.55] - 2026-04-29

### Added
- Initial release
