---
name: arr-indexer-management
skill_type: skill
description: >-
  Manage Prowlarr search indexers via the arr-mcp MCP server — list configured
  indexers, inspect one, add/update/delete an indexer, and test connectivity. Use
  when the agent must audit which Torznab/Newznab indexers are enabled, add or
  fix an indexer, or ingest the indexer inventory into the knowledge graph. Do
  NOT use for curating movies (use arr-movie-library) or series (use
  arr-series-library); prefer those.
license: MIT
tags: [arr, prowlarr, indexers, media-automation, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Arr Indexer Management (Prowlarr)

Domain-typed access to the **Prowlarr** indexer inventory through the arr-mcp MCP
server. Prowlarr centralizes Torznab/Newznab search indexers and syncs them to
the *arr apps. Prefer the condensed `prowlarr_action` tool — it routes to the real
Prowlarr client methods and returns indexer-shaped records. (The same
`get_indexer` action exists on `radarr_action`/`sonarr_action` for per-app
indexers.)

## When to use
- Audit which indexers are configured and which are `enabled`.
- Inspect a single indexer by id (protocol, priority, implementation).
- Add, update, or delete an indexer; test one before saving.
- Ingest the indexer inventory into the knowledge graph as typed `:Indexer` nodes.

## When NOT to use
- Curating the movie library → `arr-movie-library` (Radarr).
- Curating the series library → `arr-series-library` (Sonarr).
- Download-client (not indexer) configuration → the `get_downloadclient` actions
  on the per-app tools.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`arr-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PROWLARR_BASE_URL` | ✅ | Prowlarr base URL (e.g. `http://prowlarr:9696`) |
| `PROWLARR_TOKEN` | ✅ | Prowlarr API key (sent as the API token) |
| `PROWLARR_SSL_VERIFY` | optional | TLS verification toggle (default off) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed
`prowlarr_action` tool (used below) vs. the 1:1 `prowlarr_<method>` verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the Prowlarr client method. Call
`action="list_actions"` to discover every valid action.

| Condensed tool | Key actions |
|----------------|-------------|
| `prowlarr_action` | `get_indexer`, `get_indexer_id`, `post_indexer`, `put_indexer_id`, `delete_indexer_id`, `post_indexer_test`, `get_indexerstats` |
| `arr_ingest_library` | `services="indexers"` → push `:Indexer` nodes into the KG |

### Key parameters
- `get_indexer` — no args; lists all configured indexers.
- `get_indexer_id` — `{"id": <indexer_id>}` for one indexer.
- `put_indexer_id` — `{"id": <id>, "data": {...}}` (e.g. toggle `enable`, set
  `priority`); pass `forceSave: true` to bypass validation on a known-good change.

## Recipes (`params_json`)
List all indexers:
```json
{}
```
Inspect one indexer:
```json
{"id": 3}
```
Disable an indexer (fetch its full body via `get_indexer_id` first, flip
`enable`, then):
```json
{"id": 3, "data": {"enable": false}, "forceSave": true}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `enable` (singular, no trailing `d`) is the raw Prowlarr field; the KG maps it
  to the `:enabled` property on `:Indexer`.
- `protocol` is `usenet` or `torrent` — a key discriminator when auditing coverage.
- Updates (`put_indexer_id`) usually require the **full** indexer body echoed
  back with your changes, not just the changed field; read it first.
- The KG keys `:Indexer` nodes by the instance-local Prowlarr `id`
  (`arr:Indexer:<id>`) — ids are not portable across instances.

## Related
- `arr_ingest_library` (tag `kg`) ingests indexers (and movies/series) as typed
  KG nodes — ingestion only, not part of the config surface.
- **Related skills:** `arr-movie-library` (Radarr), `arr-series-library` (Sonarr).
