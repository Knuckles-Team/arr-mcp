# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
