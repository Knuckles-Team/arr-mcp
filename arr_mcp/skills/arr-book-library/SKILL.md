---
name: arr-book-library
skill_type: skill
description: >-
  Manage the Chaptarr book and audiobook library through arr-mcp: add an author and
  search for their books, search for missing books, read authors, books and the queue.
  Use for books and audiobooks. Do NOT use for movies, TV or music.
license: MIT
tags: [arr, media-automation, mcp, chaptarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Book Library (Chaptarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Chaptarr** (`chaptarr_*` tools, `CHAPTARR_BASE_URL`): the book library holding authors, e-books and audiobooks; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Add an author and search for their books (`chaptarr-add-author-and-search`)

Resolve the book library location and profiles, look the author up and add them with a missing-book search. Stops when no root folder is configured.

1. `chaptarr_get_rootfolder` — An empty list means the book library is not provisioned: stop and report it.
2. `chaptarr_get_qualityprofile` — E-Book or Audiobook profile; use its `id`.
3. `chaptarr_get_metadataprofile` — Use its `id`.
4. `chaptarr_get_author_lookup` (`term` = operator input: author name) — Pick the right author.
5. `chaptarr_post_author` (`data` = {"foreignAuthorId": "<step4>", "authorName": "<step4>", "rootFolderPath": "<step1.path>", "qualityProfileId": "<step2.id>", "metadataProfileId": "<step3.id>", "monitored": true, "addOptions": {"searchForMissingBooks": true}}) — Adds and searches.
6. `chaptarr_get_queue` (`page` = 1) — Confirm grabs.

### Search for missing books (`chaptarr-search-missing`)

List monitored books with no file and start one book search.

1. `chaptarr_get_wanted_missing` (`monitored` = true) — Collect book ids.
2. `chaptarr_post_command` (`data` = {"name": "BookSearch", "bookIds": [<ids from step1>]}) — One command per batch.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Never change API keys, download client credentials, or app connection settings.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
