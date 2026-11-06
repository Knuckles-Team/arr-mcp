---
name: arr-indexer-management
skill_type: skill
description: >-
  Keep the Prowlarr indexer pool healthy through arr-mcp: fix a failing indexer, sync
  indexers to Radarr, Sonarr and Lidarr, and search releases across indexers. Use when
  searches find nothing, health shows indexer failures, or an indexer must be added or
  fixed. Do NOT use for library curation or user requests.
license: MIT
tags: [arr, media-automation, mcp, prowlarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Indexer Management (Prowlarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Prowlarr** (`prowlarr_*` tools, `PROWLARR_BASE_URL`): the indexer pool holding search indexers, synced to Radarr, Sonarr and Lidarr; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Fix a failing indexer (`prowlarr-fix-failing-indexer`)

Find indexers Prowlarr has disabled after failures, read the failure, retest, and change the indexer settings only with approval.

1. `prowlarr_get_indexerstatus` — Each entry is a failing indexer (`indexerId`, `disabledTill`, `mostRecentFailure`).
2. `prowlarr_get_health` — Health messages name the failing indexers and the reason.
3. `prowlarr_get_indexer_id` (`id` = step1.indexerId) — Read the full indexer definition.
4. `prowlarr_post_indexer_test` (`data` = step3, `forceTest` = true) — A pass clears the failure; a Cloudflare error needs the FlareSolverr proxy tag.
5. `prowlarr_get_indexerproxy` — The proxy (FlareSolverr) and its tag.
6. `prowlarr_put_indexer_id` (`id` = step3.id, `data` = step3 with the fix (tags, baseUrl, enable)) — Approval required: changes a shared indexer.
7. `prowlarr_post_indexer_test` (`data` = step6, `forceTest` = true) — Confirm the fix.

Needs approval: `prowlarr_put_indexer_id`.

### Sync indexers to the apps (`prowlarr-sync-indexers`)

Push the Prowlarr indexer pool to every connected app (Radarr, Sonarr, Lidarr).

1. `prowlarr_get_applications` — Each application and its sync level (fullSync).
2. `prowlarr_post_command` (`data` = {"name": "ApplicationIndexerSync"}) — Starts the sync.
3. `radarr_get_indexer` — The synced indexers appear in the app.

### Search releases across indexers (`prowlarr-search-releases`)

Run one manual search across the enabled indexers.

1. `prowlarr_get_indexer` — Pick indexer ids, or omit to search all.
2. `prowlarr_get_search` (`query` = operator input: search text, `type` = "search", `limit` = 50) — Read-only: lists releases, grabs nothing.

### Replace a permanently dead indexer (`prowlarr-replace-dead-indexer`)

After the fix-a-failing-indexer workflow shows an indexer cannot work (domain gone, TLS broken on every mirror, Cloudflare the proxy cannot solve), add a tested public replacement, remove the dead one and sync the apps.

1. `prowlarr_get_indexer_schema` — Every definition with its `indexerUrls` mirrors; pick a replacement that covers the same categories.
2. `prowlarr_post_indexer_test` (`data` = step1 definition with baseUrl set, `forceTest` = true) — Test the candidate before adding it; try each mirror in `indexerUrls`.
3. `prowlarr_post_indexer` (`data` = step2 data) — Approval required: adds the replacement.
4. `prowlarr_delete_indexer_id` (`id` = the dead indexer id) — Approval required: removes the dead indexer (destructive; pass `confirm=true` after approval).
5. `prowlarr_post_command` (`data` = {"name": "ApplicationIndexerSync"}) — Push the indexer change to every linked app.

Needs approval: `prowlarr_post_indexer`, `prowlarr_delete_indexer_id`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Change API keys, download client credentials or app connection settings only in an approval-required contract step, after the operator approves; read keys and passwords from the credential store and never print them.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
