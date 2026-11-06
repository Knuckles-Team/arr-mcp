# CONN-ARR-MCP-SUITE — Research

Governing spec: [spec.md](spec.md).

## Census (2026-11-06)

| App | Live version | Upstream operations | Client methods before | After |
|---|---|---|---|---|
| Radarr | 6.4.4 | 237 (+2 web sign-in routes) | 237 | 237 |
| Sonarr | 4.0.20 | 235 (+4 web sign-in routes) | 234 | 235 |
| Lidarr | 3.1.0 | 235 | 235 | 235 |
| Prowlarr | 2.5.1 | 128 | 128 | 128 |
| Chaptarr | 0.9.879, then 0.9.965 | 233 (Readarr v1 API) | 233 | 233 |
| Bazarr | 1.6.2 | 88 (84 in the live API description, 4 hidden with `Namespace.hide`) | 10 correct, 15 wrong routes | 88 |
| Seerr | 3.5.0 | 217 | 17 correct, 2 wrong routes | 217 |

## Findings

- A wrong Bazarr route answers with the web page and status 200. The client returned it as `status: success`. Row `CONN-ARR-MCP-SUITE-R003` makes it a refusal.
- Each client exposed its HTTP helper as an `<app>_request` tool that bypassed the typed surface and the delete confirmation. Row `CONN-ARR-MCP-SUITE-R002` removes it.
- The ingest presets named `*_action` tools that the SDK no longer lists. Row `CONN-ARR-MCP-SUITE-R008` repoints them.
- The ontology redeclared core classes (`:Series`, `:Book`, `:Indexer`, `:QualityProfile`, `:Episode`). Row `CONN-ARR-MCP-SUITE-R007` removes the declarations and subclasses core.
- Released medulla 3.1.0 leaves `:Workflow` and `:AgentRole` without a `bfo:Entity` ancestor. The skill and role classes use `:Procedure` and `:Role`, which reach `bfo:Entity` in 3.1.0 and on main.

## Live topology

- Prowlarr syncs its indexers to Radarr, Sonarr and Lidarr (full sync).
- Seerr routes movie requests to Radarr (`/movies`) and series requests to Sonarr (`/tv`).
- Radarr, Sonarr and Lidarr send releases to one torrent download client.
- Bazarr is connected to Sonarr and Radarr in the same pod (`127.0.0.1`), with the no-account providers enabled and an English default profile (2026-11-06).
- Seerr has a default non-4K Radarr and Sonarr server with the 1080p profile, and a 4K server of each with the 4K profile.

## Findings from the provisioning run (2026-11-06)

- Bazarr's settings, notification test and restart routes are hidden from its swagger, so the generated client could not connect Bazarr or enable a provider. Row R009 adds them.
- Every failure read `API error: HTTP 400` with no reason. The live reasons were a qBittorrent login ban (`Host: Unable to connect to qBittorrent`), a stale download-client password (`Username: Authentication failure`), a Chaptarr root folder missing `folderType`, Cloudflare blocks and dead indexer domains. Row R010 carries the reason.
- Indexer tests through FlareSolverr and Bazarr provider searches take 60 to 212 seconds; the 30-second read timeout reported them as `Upstream timed out`. Row R010 allows 300 seconds.
- Bazarr 1.6.2 no longer ships the Podnapisi provider. The providers that need no account are embeddedsubtitles, gestdown, subtitlecat, supersubtitles, tvsubtitles and yifysubtitles.
- Chaptarr root folders need `folderType` (1 audiobook, 2 ebook, 0 mixed) and the matching profile pair, which the generic body schema does not show. Row R011's contract records the shape.
- Chaptarr has no root folder and no download client.
