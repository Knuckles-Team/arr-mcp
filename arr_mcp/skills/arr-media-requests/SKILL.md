---
name: arr-media-requests
skill_type: skill
description: >-
  Handle user media requests through Seerr and arr-mcp: triage pending requests, request
  a title for a user, retry failed requests, and check where requests route (Radarr or
  Sonarr). Use for anything users asked for. Do NOT use to add media directly to a
  library (arr-movie-library, arr-series-library).
license: MIT
tags: [arr, media-automation, mcp, seerr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Media Requests (Seerr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Seerr** (`seerr_*` tools, `SEERR_BASE_URL`): the request queue holding user media requests, forwarded to Radarr and Sonarr; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Triage pending requests (`seerr-triage-requests`)

Count and list pending requests, read each one, check where it will route, and approve or decline it with approval.

1. `seerr_get_request_count` — Pending, approved, processing and failed counts.
2. `seerr_get_request` (`filter` = "pending", `take` = 20) — Pending requests with media and requester.
3. `seerr_get_request_id` (`request_id` = step2.results[].id) — One request in full.
4. `seerr_get_service_radarr` — Radarr servers a movie request routes to (4K flag, default).
5. `seerr_get_service_sonarr` — Sonarr servers a series request routes to.
6. `seerr_post_request_id_status` (`request_id` = step3.id, `status` = operator input: approve or decline) — Approval required: approving forwards the request to Radarr or Sonarr.

Needs approval: `seerr_post_request_id_status`.

### Request a title for a user (`seerr-request-title`)

Search the catalogue and file a request that Seerr routes to Radarr or Sonarr.

1. `seerr_get_search` (`query` = operator input: title) — Pick the result (`id` is the TMDB id, `mediaType`).
2. `seerr_get_movie_id` (`movie_id` = step1.results[0].id) — For a movie: `mediaInfo` shows whether it is already available or requested.
3. `seerr_post_request` (`media_type` = step1.results[0].mediaType, `media_id` = step1.results[0].id, `is4k` = false) — Creates the request; set `seasons` for a series.
4. `seerr_get_request` (`filter` = "all", `take` = 5) — Confirm the request exists.

### Retry failed requests (`seerr-retry-failed`)

List failed requests and retry each one after the routing problem is fixed.

1. `seerr_get_request` (`filter` = "failed") — Failed requests.
2. `seerr_get_settings_radarr` — Check the Radarr server the request routes to.
3. `seerr_post_request_id_retry` (`request_id` = step1.results[].id) — Resends the request.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Never change API keys, download client credentials, or app connection settings.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
