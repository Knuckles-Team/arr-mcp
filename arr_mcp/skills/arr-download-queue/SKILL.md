---
name: arr-download-queue
skill_type: skill
description: >-
  Check and repair the download queue across Radarr, Sonarr, Lidarr and Chaptarr through
  arr-mcp: read every queue, find stalled or failed downloads, and remove a stalled
  download with blocklisting so another release is found. Use when a user asks where a
  download is or downloads are stuck.
license: MIT
tags: [arr, media-automation, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Download Queue

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Radarr** (`radarr_*` tools, `RADARR_BASE_URL`): the movie library holding films; files under `/movies`.
- **Sonarr** (`sonarr_*` tools, `SONARR_BASE_URL`): the TV library holding TV series, seasons and episodes; files under `/tv`.
- **Lidarr** (`lidarr_*` tools, `LIDARR_BASE_URL`): the music library holding music artists, albums and tracks; files under `/music`.
- **Chaptarr** (`chaptarr_*` tools, `CHAPTARR_BASE_URL`): the book library holding authors, e-books and audiobooks; no file root folder.
- **Prowlarr** (`prowlarr_*` tools, `PROWLARR_BASE_URL`): the indexer pool holding search indexers, synced to Radarr, Sonarr and Lidarr; no file root folder.
- **Bazarr** (`bazarr_*` tools, `BAZARR_BASE_URL`): the subtitle store holding subtitle files beside the Sonarr and Radarr media; no file root folder.
- **Seerr** (`seerr_*` tools, `SEERR_BASE_URL`): the request queue holding user media requests, forwarded to Radarr and Sonarr; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Check the download queue (`arr-check-download-queue`)

Read every app's queue summary and items to find stalled, failed or warning downloads.

1. `radarr_get_queue_status` — Totals, errors and warnings for movies.
2. `radarr_get_queue` (`page` = 1, `pageSize` = 50) — Items with `status`, `trackedDownloadState`, `statusMessages`.
3. `sonarr_get_queue_status` — Series totals.
4. `sonarr_get_queue` (`page` = 1, `pageSize` = 50) — Series items.
5. `lidarr_get_queue_status` — Music totals.
6. `lidarr_get_queue` (`page` = 1, `pageSize` = 50) — Music items.
7. `chaptarr_get_queue_status` — Book totals.
8. `chaptarr_get_queue` (`page` = 1) — Book items.

### Remove a stalled download and find another (`arr-remove-stalled-download`)

Remove one stalled or failed queue item, blocklist the release so it is not grabbed again, and search again.

1. `radarr_get_queue` (`status` = ["warning", "failed"], `includeMovie` = true) — Pick the stalled item (`id`, `movieId`).
2. `radarr_delete_queue_id` (`id` = step1.records[].id, `removeFromClient` = true, `blocklist` = true, `confirm` = true) — Approval required: deletes the download from qBittorrent.
3. `radarr_post_command` (`data` = {"name": "MoviesSearch", "movieIds": [<step1.movieId>]}) — Search for another release.

Needs approval: `radarr_delete_queue_id`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Never change API keys, download client credentials, or app connection settings.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
