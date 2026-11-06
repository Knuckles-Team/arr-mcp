---
name: arr-music-library
skill_type: skill
description: >-
  Manage the Lidarr music library through arr-mcp: add an artist and search for their
  albums, search for missing albums, read artists, albums and the queue. Use for music.
  Do NOT use for movies, TV, books or indexers.
license: MIT
tags: [arr, media-automation, mcp, lidarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Music Library (Lidarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Lidarr** (`lidarr_*` tools, `LIDARR_BASE_URL`): the music library holding music artists, albums and tracks; files under `/music`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Add an artist and search for their albums (`lidarr-add-artist-and-search`)

Resolve the music library location, quality and metadata profiles, look the artist up and add them with a missing-album search.

1. `lidarr_get_rootfolder` — Use its `path`.
2. `lidarr_get_qualityprofile` — Use its `id`.
3. `lidarr_get_metadataprofile` — Use its `id` (which release types to track).
4. `lidarr_get_artist_lookup` (`term` = operator input: artist name or lidarr:<mbid>) — Pick the right artist (MusicBrainz id).
5. `lidarr_get_artist` (`mbId` = step4.result[0].foreignArtistId) — Stop if already in the library.
6. `lidarr_post_artist` (`data` = {"foreignArtistId": "<step4>", "artistName": "<step4>", "rootFolderPath": "<step1.path>", "qualityProfileId": "<step2.id>", "metadataProfileId": "<step3.id>", "monitored": true, "addOptions": {"searchForMissingAlbums": true}}) — Adds and searches.
7. `lidarr_get_queue` (`page` = 1) — Confirm grabs.

### Search for missing albums (`lidarr-search-missing`)

List monitored albums with no files and start one album search.

1. `lidarr_get_wanted_missing` (`monitored` = true, `pageSize` = 50) — Collect album ids.
2. `lidarr_post_command` (`data` = {"name": "AlbumSearch", "albumIds": [<ids from step1>]}) — One command per batch.
3. `lidarr_get_queue` (`page` = 1) — Confirm grabs.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Never change API keys, download client credentials, or app connection settings.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
