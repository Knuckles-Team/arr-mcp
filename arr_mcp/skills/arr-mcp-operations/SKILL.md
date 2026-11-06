---
name: arr-mcp-operations
skill_type: skill
description: >-
  Operate the whole arr suite through arr-mcp: check every app's status and health, know
  which app holds which library and where its files live, follow how the apps federate
  (Prowlarr indexers, Seerr routing, Bazarr subtitles, one download client), and mirror
  the library into the knowledge graph. Use as the entry point for any arr-suite
  request; it routes to the per-app skills.
license: MIT
tags: [arr, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Suite Operations

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Radarr** (`radarr_*` tools, `RADARR_BASE_URL`): the movie library holding films; files under `/movies`.
- **Sonarr** (`sonarr_*` tools, `SONARR_BASE_URL`): the TV library holding TV series, seasons and episodes; files under `/tv`.
- **Lidarr** (`lidarr_*` tools, `LIDARR_BASE_URL`): the music library holding music artists, albums and tracks; files under `/music`.
- **Chaptarr** (`chaptarr_*` tools, `CHAPTARR_BASE_URL`): the book library holding authors, e-books and audiobooks; no file root folder.
- **Prowlarr** (`prowlarr_*` tools, `PROWLARR_BASE_URL`): the indexer pool holding search indexers, synced to Radarr, Sonarr and Lidarr; no file root folder.
- **Bazarr** (`bazarr_*` tools, `BAZARR_BASE_URL`): the subtitle store holding subtitle files beside the Sonarr and Radarr media; no file root folder.
- **Seerr** (`seerr_*` tools, `SEERR_BASE_URL`): the request queue holding user media requests, forwarded to Radarr and Sonarr; no file root folder.

## How the apps federate

- Prowlarr pushes its indexer pool to Radarr (full sync).
- Prowlarr pushes its indexer pool to Sonarr (full sync).
- Prowlarr pushes its indexer pool to Lidarr (full sync).
- Seerr sends approved movie requests to Radarr (root folder /movies).
- Seerr sends approved series requests to Sonarr (root folder /tv).
- Bazarr reads episodes from Sonarr and writes subtitles beside them.
- Bazarr reads movies from Radarr and writes subtitles beside them.
- Radarr, Sonarr and Lidarr download through one qBittorrent download client.

## Which skill to use

- `arr-movie-library` — Manage the Radarr movie library through arr-mcp.
- `arr-series-library` — Manage the Sonarr TV library through arr-mcp.
- `arr-music-library` — Manage the Lidarr music library through arr-mcp.
- `arr-book-library` — Manage the Chaptarr book and audiobook library through arr-mcp.
- `arr-indexer-management` — Keep the Prowlarr indexer pool healthy through arr-mcp.
- `arr-subtitle-management` — Manage subtitles through Bazarr and arr-mcp.
- `arr-media-requests` — Handle user media requests through Seerr and arr-mcp.
- `arr-download-queue` — Check and repair the download queue across Radarr, Sonarr, Lidarr and Chaptarr through arr-mcp.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Check suite health (`arr-suite-health-check`)

Read every app's status and health, and report versions, connectivity and open health issues.

1. `radarr_get_system_status` — Version and instance name.
2. `radarr_get_health` — Open health issues.
3. `sonarr_get_system_status`
4. `sonarr_get_health`
5. `lidarr_get_system_status`
6. `lidarr_get_health`
7. `chaptarr_get_system_status`
8. `chaptarr_get_health`
9. `prowlarr_get_system_status`
10. `prowlarr_get_health` — Failing indexers show here.
11. `bazarr_get_system_status` — Empty Sonarr or Radarr version means not connected.
12. `bazarr_get_system_health`
13. `seerr_get_status` — Version and pending update.

### Mirror the library into the knowledge graph (`arr-ingest-library`)

Ingest movies, series and indexers as typed graph nodes (Film, Series, MediaIndexer, QualityProfile).

1. `arr_ingest_library` (`services` = ["radarr", "sonarr", "prowlarr"]) — Writes typed nodes through the governed ingest path.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Change API keys, download client credentials or app connection settings only in an approval-required contract step, after the operator approves; read keys and passwords from the credential store and never print them.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
