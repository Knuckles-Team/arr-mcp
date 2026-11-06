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

### Provision the book library (`chaptarr-provision-book-library`)

Give Chaptarr its book root folder, qBittorrent as download client, and a Prowlarr link for book indexers.

1. `chaptarr_get_rootfolder` — An empty result means no library.
2. `chaptarr_get_qualityprofile` — The ebook and audiobook quality profiles (`profileType`).
3. `chaptarr_get_metadataprofile` — The ebook and audiobook metadata profiles.
4. `chaptarr_post_rootfolder` (`data` = {name: "Books", path: "/ebooks", folderType: 2, ebookQualityProfileId: step2 ebook id, ebookMetadataProfileId: step3 ebook id, defaultMonitorOption: "all", defaultNewItemMonitorOption: "all"}) — Approval required: adds the folder. Chaptarr needs `folderType` (1 audiobook, 2 ebook, 0 mixed) and the matching `ebookQualityProfileId` / `ebookMetadataProfileId` (or the audiobook pair).
5. `chaptarr_get_downloadclient_schema` — The `QBittorrent` entry with its fields; categories default to `chaptarr`.
6. `chaptarr_post_downloadclient_test` (`data` = step5 QBittorrent entry with host, port and credentials) — Tests the client with the stored qBittorrent credentials.
7. `chaptarr_post_downloadclient` (`data` = step6 data) — Approval required: saves the client.
8. `prowlarr_get_applications_schema` — Chaptarr speaks the Readarr API: use the `Readarr` entry.
9. `prowlarr_post_applications_test` (`data` = step8 Readarr entry with baseUrl and apiKey) — Tests the link with Chaptarr's base URL and API key (CHAPTARR_API_KEY).
10. `prowlarr_post_applications` (`data` = step9 data) — Approval required: adds the link with `syncLevel` fullSync, so Prowlarr pushes its book indexers.

Needs approval: `chaptarr_post_rootfolder`, `chaptarr_post_downloadclient`, `prowlarr_post_applications`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Change API keys, download client credentials or app connection settings only in an approval-required contract step, after the operator approves; read keys and passwords from the credential store and never print them.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
