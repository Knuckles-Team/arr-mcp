---
name: arr-movie-library
skill_type: skill
description: >-
  Manage the Radarr movie library through arr-mcp: add a movie and search for it, search
  for missing movies, read the library, queue, history and wanted list, and tag movies.
  Use for any film in the movie library. Do NOT use for TV (arr-series-library), music
  (arr-music-library), books (arr-book-library), indexers (arr-indexer-management) or
  user requests (arr-media-requests).
license: MIT
tags: [arr, media-automation, mcp, radarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Movie Library (Radarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Radarr** (`radarr_*` tools, `RADARR_BASE_URL`): the movie library holding films; files under `/movies`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Add a movie and search for it (`radarr-add-and-search`)

Resolve the movie library location and quality profile, look the title up, add it monitored and start a search, then confirm it reached the download queue.

1. `radarr_get_rootfolder` — Pick the library root folder; use its `path`.
2. `radarr_get_qualityprofile` — Pick the quality profile the operator named (default the first); use its `id`.
3. `radarr_get_movie_lookup` (`term` = operator input: title or tmdb:/tvdb: id) — Confirm the right title and year before adding.
4. `radarr_get_movie` (`tmdbId` = step3.result[0].tmdbId) — Stop if the title is already in the library.
5. `radarr_add_movie` (`term` = operator input: title or tmdb:/tvdb: id, `root_folder_path` = step1.result[0].path, `quality_profile_id` = step2.result[0].id, `monitored` = true, `search_for_movie` = true) — Adds the title monitored and starts the search.
6. `radarr_get_queue` (`page` = 1, `pageSize` = 20) — A grabbed release shows here; an empty queue means no release matched yet.

### Search for missing movie items (`radarr-search-missing`)

List the monitored items that have no file and start one search command for them.

1. `radarr_get_wanted_missing` (`monitored` = true, `pageSize` = 50) — Collect the ids of the missing items.
2. `radarr_post_command` (`data` = {"name": "MoviesSearch", "movieIds": "<ids or id from step1>"}) — One command per batch; never one per item.
3. `radarr_get_queue` (`page` = 1) — Confirm grabs.

### Create and remove a label tag (reversible) (`radarr-tag-roundtrip`)

Create a tag to group items, verify it, and delete it again when it was only a test.

1. `radarr_get_tag` — Reuse an existing tag with the same label.
2. `radarr_post_tag` (`data` = {"label": "zz-validation-<date>"}) — Labels are lower case.
3. `radarr_delete_tag_id` (`id` = step2.id, `confirm` = true) — Only for tags this run created.

Needs approval: `radarr_delete_tag_id`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Change API keys, download client credentials or app connection settings only in an approval-required contract step, after the operator approves; read keys and passwords from the credential store and never print them.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
