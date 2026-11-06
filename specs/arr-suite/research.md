# CONN-ARR-MCP-SUITE — Research

Governing spec: [spec.md](spec.md).

## Census (2026-11-06)

| App | Live version | Upstream operations | Client methods before | After |
|---|---|---|---|---|
| Radarr | 6.4.4 | 237 (+2 web sign-in routes) | 237 | 237 |
| Sonarr | 4.0.20 | 235 (+4 web sign-in routes) | 234 | 235 |
| Lidarr | 3.1.0 | 235 | 235 | 235 |
| Prowlarr | 2.5.1 | 128 | 128 | 128 |
| Chaptarr | 0.9.879 | 233 (Readarr v1 API) | 233 | 233 |
| Bazarr | 1.6.2 | 84 (live API description) | 10 correct, 15 wrong routes | 84 |
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
- Bazarr has no Sonarr or Radarr connection and no enabled subtitle provider.
- Chaptarr has no root folder and no download client.
