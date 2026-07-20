# Arr Movie Library

Manage the Radarr movie library via the arr-mcp MCP server — list monitored movies, look up a movie by TMDB id, add a movie, trigger searches, and check wanted/missing. Use when the agent must inspect or curate the film collection, add a new movie for download, or reason about a movie's monitored/hasFile status. Do NOT use for TV series (use arr-series-library), music, books, or indexer configuration (use arr-indexer-management); prefer those.

# Arr Movie Library (Radarr)

Domain-typed access to the **Radarr** movie library through the arr-mcp MCP
server. Radarr tracks films by their TMDB id, monitors them, and grabs releases
from configured indexers. Prefer the condensed `radarr_action` tool — it routes
to the real Radarr client methods and returns movie-shaped records.

## When to use
- List the movie library / triage monitored but not-yet-downloaded films.
- Look up a single movie by TMDB id or internal Radarr id.
- Add a new movie and kick off a search.
- Ingest the movie library into the knowledge graph as typed `:Movie` nodes.

## When NOT to use
- TV series / episodes → `arr-series-library` (Sonarr).
- Music (artists/albums), books → the Lidarr / Chaptarr surfaces.
- Adding, enabling, or testing indexers → `arr-indexer-management` (Prowlarr).
- User-facing "please add this" requests routed through Overseerr → the
  `seerr_action` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`arr-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `RADARR_BASE_URL` | ✅ | Radarr base URL (e.g. `[configured-endpoint]`) |
| `RADARR_TOKEN` | ✅ | Radarr API key (sent as the API token) |
| `RADARR_TLS_PROFILE` | optional | Runtime trust, mTLS, and proxy profile |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed
`radarr_action` tool (used below) vs. the 1:1 `radarr_<method>` verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the Radarr client method. Call
`action="list_actions"` to discover every valid action.

| Condensed tool | Key actions |
|----------------|-------------|
| `radarr_action` | `get_movie`, `get_movie_id`, `post_movie`, `put_movie_id`, `delete_movie_id`, `get_wanted_missing`, `get_qualityprofile` |
| `arr_ingest_library` | `services="movies"` → push `:Movie` nodes into the KG |

### Key parameters
- `get_movie` — no args lists all; pass `{"tmdbId": <id>}` to fetch one by TMDB.
- `get_movie_id` — `{"id": <radarr_id>}` for the internal id.
- `post_movie` — `{"data": {...}}` with `tmdbId`, `qualityProfileId`,
  `rootFolderPath`, `monitored`, and `addOptions.searchForMovie`.

## Recipes (`params_json`)
List the whole library:
```json
{}
```
Look up one movie by TMDB id:
```json
{"tmdbId": 27205}
```
Add a movie and search for it immediately:
```json
{"data": {"tmdbId": 27205, "qualityProfileId": 1, "rootFolderPath": "/movies", "monitored": true, "addOptions": {"searchForMovie": true}}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `get_movie` with no `tmdbId` returns the **entire** library; page/filter client-side.
- TMDB id (`tmdbId`) is the stable external key; the numeric Radarr `id` is
  instance-local — the KG keys `:Movie` nodes by `arr:Movie:<tmdbId>`.
- Adding a movie needs a valid `qualityProfileId` **and** `rootFolderPath`;
  fetch them via `get_qualityprofile` / `get_rootfolder` first.
- Plural guesses like `get_movies` are alias-resolved to `get_movie`, but prefer
  the real singular action name.

## Related
- `arr_ingest_library` (tag `kg`) ingests movies (and series/indexers) as typed
  KG nodes — ingestion only, not part of the curation surface.
- **Related skills:** `arr-series-library` (Sonarr), `arr-indexer-management`
  (Prowlarr).
