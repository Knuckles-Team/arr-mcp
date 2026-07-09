---
name: arr-series-library
skill_type: skill
description: >-
  Manage the Sonarr TV series library via the arr-mcp MCP server — list series,
  look one up by TVDB id, add a series, inspect seasons/episodes, and check
  wanted/missing episodes. Use when the agent must inspect or curate the TV
  collection, add a new show for download, or reason about a series'
  monitored/continuing status. Do NOT use for movies (use arr-movie-library),
  music, books, or indexer setup (use arr-indexer-management); prefer those.
license: MIT
tags: [arr, sonarr, tv, series, media-automation, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Arr Series Library (Sonarr)

Domain-typed access to the **Sonarr** TV library through the arr-mcp MCP server.
Sonarr tracks series by their TVDB id, monitors seasons/episodes, and grabs
releases from configured indexers. Prefer the condensed `sonarr_action` tool — it
routes to the real Sonarr client methods and returns series-shaped records.

## When to use
- List the series library / triage monitored shows with missing episodes.
- Look up a single series by TVDB id or internal Sonarr id.
- Add a new series and choose which seasons to monitor.
- Ingest the series library into the knowledge graph as typed `:Series` nodes.

## When NOT to use
- Movies → `arr-movie-library` (Radarr).
- Music (artists/albums), books → the Lidarr / Chaptarr surfaces.
- Adding, enabling, or testing indexers → `arr-indexer-management` (Prowlarr).
- User-facing "please add this show" requests via Overseerr → the `seerr_action`
  tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`arr-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `SONARR_BASE_URL` | ✅ | Sonarr base URL (e.g. `http://sonarr:8989`) |
| `SONARR_TOKEN` | ✅ | Sonarr API key (sent as the API token) |
| `SONARR_SSL_VERIFY` | optional | TLS verification toggle (default off) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed
`sonarr_action` tool (used below) vs. the 1:1 `sonarr_<method>` verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the Sonarr client method. Call
`action="list_actions"` to discover every valid action.

| Condensed tool | Key actions |
|----------------|-------------|
| `sonarr_action` | `get_series`, `get_series_id`, `post_series`, `put_series_id`, `delete_series_id`, `get_episode`, `get_wanted_missing`, `get_series_lookup` |
| `arr_ingest_library` | `services="series"` → push `:Series` nodes into the KG |

### Key parameters
- `get_series` — no args lists all; pass `{"tvdbId": <id>}` to fetch one by TVDB.
- `get_series_id` — `{"id": <sonarr_id>}` for the internal id.
- `post_series` — `{"data": {...}}` with `tvdbId`, `qualityProfileId`,
  `rootFolderPath`, `languageProfileId`, `monitored`, and a `seasons` array /
  `addOptions.monitor`.

## Recipes (`params_json`)
List the whole library:
```json
{}
```
Look up one series by TVDB id:
```json
{"tvdbId": 121361}
```
Search for a show to add (by term), then add it monitoring all seasons:
```json
{"term": "The Expanse"}
```
```json
{"data": {"tvdbId": 121361, "qualityProfileId": 1, "rootFolderPath": "/tv", "monitored": true, "addOptions": {"monitor": "all", "searchForMissingEpisodes": true}}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `get_series` with no `tvdbId` returns the **entire** library; filter client-side.
- TVDB id (`tvdbId`) is the stable external key; the numeric Sonarr `id` is
  instance-local — the KG keys `:Series` nodes by `arr:Series:<tvdbId>`.
- Series size lives under `statistics.sizeOnDisk`, not a top-level field.
- Adding a series needs a valid `qualityProfileId` **and** `rootFolderPath`;
  use `get_series_lookup` (term search) to resolve the `tvdbId` first.

## Related
- `arr_ingest_library` (tag `kg`) ingests series (and movies/indexers) as typed
  KG nodes — ingestion only, not part of the curation surface.
- **Related skills:** `arr-movie-library` (Radarr), `arr-indexer-management`
  (Prowlarr).
