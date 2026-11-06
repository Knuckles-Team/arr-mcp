---
name: arr-subtitle-management
skill_type: skill
description: >-
  Manage subtitles through Bazarr and arr-mcp: download wanted subtitles for episodes
  and movies, check and reset subtitle providers, and read subtitle history. Use when
  media is missing subtitles. Do NOT use for downloading media itself.
license: MIT
tags: [arr, media-automation, mcp, bazarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Subtitle Management (Bazarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Bazarr** (`bazarr_*` tools, `BAZARR_BASE_URL`): the subtitle store holding subtitle files beside the Sonarr and Radarr media; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Download wanted subtitles (`bazarr-download-wanted-subtitles`)

Check that Bazarr is connected to Sonarr and Radarr, list the episodes and movies missing subtitles, and download one for each.

1. `bazarr_get_system_status` — Empty `sonarr_version` or `radarr_version` means Bazarr is not connected to that app: stop and report it.
2. `bazarr_get_providers` — No enabled provider means no subtitle can be found: stop and report it.
3. `bazarr_get_episodes_wanted` (`length` = 50) — Episodes missing subtitles (`sonarrSeriesId`, `sonarrEpisodeId`, `missing_subtitles`).
4. `bazarr_patch_episodes_subtitles` (`seriesid` = step3.data[].sonarrSeriesId, `episodeid` = step3.data[].sonarrEpisodeId, `language` = step3.data[].missing_subtitles[].code2, `forced` = false, `hi` = false) — Searches the providers and downloads the best match.
5. `bazarr_get_movies_wanted` (`length` = 50) — Movies missing subtitles (`radarrId`).
6. `bazarr_patch_movies_subtitles` (`radarrid` = step5.data[].radarrId, `language` = step5.data[].missing_subtitles[].code2, `forced` = false, `hi` = false) — Downloads the best match.

### Reset throttled subtitle providers (`bazarr-reset-providers`)

Read the provider status and reset throttled providers with approval.

1. `bazarr_get_providers` (`history` = false) — Throttled providers carry a status and retry time.
2. `bazarr_post_providers` (`action` = "reset") — Approval required: clears every provider's throttle.

Needs approval: `bazarr_post_providers`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Never change API keys, download client credentials, or app connection settings.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
