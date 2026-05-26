# Code Enhancement: arr-mcp

> Automated code enhancement review for arr-mcp. Covers 17 analysis domains.

## User Stories

- As a **developer**, I want to **address Project Analysis findings (grade: C, score: 74)**, so that **improve project project analysis from C to at least B (80+)**.
- As a **developer**, I want to **address Codebase Optimization findings (grade: F, score: 49)**, so that **improve project codebase optimization from F to at least B (80+)**.
- As a **developer**, I want to **address Test Coverage findings (grade: C, score: 75)**, so that **improve project test coverage from C to at least B (80+)**.
- As a **developer**, I want to **address Architecture & Design Patterns findings (grade: C, score: 75)**, so that **improve project architecture & design patterns from C to at least B (80+)**.
- As a **developer**, I want to **address Concept Traceability findings (grade: F, score: 22)**, so that **improve project concept traceability from F to at least B (80+)**.
- As a **developer**, I want to **address Test Execution findings (grade: F, score: 25)**, so that **improve project test execution from F to at least B (80+)**.
- As a **developer**, I want to **address Version Sync Analysis findings (grade: D, score: 60)**, so that **improve project version sync analysis from D to at least B (80+)**.
- As a **developer**, I want to **address Changelog Audit findings (grade: C, score: 75)**, so that **improve project changelog audit from C to at least B (80+)**.
- As a **developer**, I want to **address analyze_xdg_kg findings (grade: F, score: 0)**, so that **improve project analyze_xdg_kg from F to at least B (80+)**.

## Functional Requirements

- **FR-001**: Minor update: pytest-xdist 3.6.0 (constraint — not installed) -> 3.8.0
- **FR-002**: Minor update: agent-utilities 0.2.40 (installed) -> 0.16.0
- **FR-003**: Minor update: urllib3 2.6.3 (installed) -> 2.7.0
- **FR-004**: Minor update: requests 2.32.5 (installed) -> 2.34.2
- **FR-005**: 1 functions exceed 200 lines (actionable refactoring targets): get_mcp_instance (320L)
- **FR-006**: Monolithic: api_client_prowlarr.py (1211L) — 2 functions with high complexity (worst: Api.get_indexer_id_newznab at 105L, CC=33); God class: Api (131 methods) — consider mixins/composition
- **FR-007**: Needs attention: api_client_sonarr.py (2002L) — God class: Api (238 methods) — consider mixins/composition
- **FR-008**: Needs attention: api_client_radarr.py (1919L) — God class: Api (241 methods) — consider mixins/composition
- **FR-009**: Needs attention: api_client_lidarr.py (1941L) — God class: Api (237 methods) — consider mixins/composition
- **FR-010**: High code duplication ratio: 24.6%
- **FR-011**: 8 functions with nesting depth >4
- **FR-012**: Test suite lacks intent diversity (only one type)
- **FR-013**: 13 potential doc-test drift items
- **FR-014**: SRP: 6 modules exceed 500 lines (god modules)
- **FR-015**: SRP: 7 classes have >15 methods
- **FR-016**: No discernible layer architecture (no domain/service/adapter separation)
- **FR-017**: Low traceability ratio: 17% concepts fully traced
- **FR-018**: 7 orphaned concepts (only in one source)
- **FR-019**: 29 test functions missing concept markers
- **FR-020**: 164 significant functions (>10 lines) missing concept markers in docstrings
- **FR-021**: Total lint findings: 1 (high/error: 0, medium/warning: 0, low: 1)
- **FR-022**: 2 hook(s) may be outdated: ruff-pre-commit, uv-pre-commit
- **FR-023**: 4 rogue/throwaway scripts detected (fix_*, validate_*, patch_*, etc.): patch_gen_script.py, fix_mcp_server.py, patch_gen.py, scripts/validate_a2a_agent.py
- **FR-024**: Found 2 file(s) with version '0.15.0' that are NOT tracked in .bumpversion.cfg:
- **FR-025**:   - .specify/reports/results.json
- **FR-026**:   - .specify/reports/code_enhancement_report.md
- **FR-027**: CHANGELOG.md exists but could not be parsed — check format compliance
- **FR-028**: No changelog entries within the last 30 days
- **FR-029**: keepachangelog not installed — pip install 'universal-skills[code-enhancer]'
- **FR-030**: 1 test files exceed 500 lines — split into focused modules
- **FR-031**: Test directory lacks subdirectory organization (consider unit/, integration/, e2e/)
- **FR-032**: 5 tests have no assertions
- **FR-033**: Undocumented env vars: CHAPTARR_API_KEY, EUNOMIA_REMOTE_URL, LIDARR_API_KEY, OAUTH_BASE_URL, OAUTH_UPSTREAM_AUTH_ENDPOINT, OAUTH_UPSTREAM_CLIENT_ID, OAUTH_UPSTREAM_CLIENT_SECRET, OAUTH_UPSTREAM_TOKEN_ENDPOINT, OIDC_BASE_URL, OIDC_CLIENT_ID
- **FR-034**: 27 Python env vars not in .env.example: BAZARR_API_KEY, BAZARR_BASE_URL, BAZARR_SSL_VERIFY, CHAPTARR_API_KEY, CHAPTARR_BASE_URL
- **FR-035**: Analysis error: No module named 'agent_utilities.knowledge_graph'

## Success Criteria

- Overall GPA: 2.12 → 3.0
- Domains at B or above: 8 → 17
- Actionable findings: 35 → 0
