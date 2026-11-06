---
name: arr-subtitle-management
skill_type: skill
description: >-
  Manage subtitles through Bazarr and arr-mcp: download wanted subtitles for episodes
  and movies, check and reset subtitle providers, and read subtitle history. Use when
  media is missing subtitles. Do NOT use for downloading media itself.
license: MIT
tags: [arr, media-automation, mcp, bazarr]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Arr Subtitle Management (Bazarr)

Use the typed tools of the `arr-mcp` connector: one tool per upstream API operation, named `<app>_<operation>` (for example `radarr_get_queue`). Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **Bazarr** (`bazarr_*` tools, `BAZARR_BASE_URL`): the subtitle store holding subtitle files beside the Sonarr and Radarr media; no file root folder.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology (`ontology://arr-mcp/arr-contracts.ttl`, `arr:ToolUseContract`). Run the steps in order; a parameter written `stepN.field` comes from step N's result.

### Download wanted subtitles (`bazarr-download-wanted-subtitles`)

Check that Bazarr is connected to Sonarr and Radarr, list the episodes and movies missing subtitles, and download one for each.

1. `bazarr_get_system_status` — Empty `sonarr_version` or `radarr_version` means Bazarr is not connected to that app: stop and report it.
2. `bazarr_get_providers` — No enabled provider means no subtitle can be found: stop and report it.
3. `bazarr_get_episodes_wanted` (`length` = 50) — Episodes missing subtitles (`sonarrSeriesId`, `sonarrEpisodeId`, `missing_subtitles`).
4. `bazarr_patch_episodes_subtitles` (`seriesid` = step3.data[].sonarrSeriesId, `episodeid` = step3.data[].sonarrEpisodeId, `language` = step3.data[].missing_subtitles[].code2, `forced` = false, `hi` = false) — Searches the providers and downloads the best match.
5. `bazarr_get_movies_wanted` (`length` = 50) — Movies missing subtitles (`radarrId`).
6. `bazarr_patch_movies_subtitles` (`radarrid` = step5.data[].radarrId, `language` = step5.data[].missing_subtitles[].code2, `forced` = false, `hi` = false) — Downloads the best match.

### Reset throttled subtitle providers (`bazarr-reset-providers`)

Read the provider status and reset throttled providers with approval.

1. `bazarr_get_providers` (`history` = false) — Throttled providers carry a status and retry time.
2. `bazarr_post_providers_reset` — Approval required: clears every provider's throttle.

Needs approval: `bazarr_post_providers_reset`.

### Connect Bazarr to Sonarr and Radarr (`bazarr-connect-sonarr-radarr`)

Point Bazarr at the Sonarr and Radarr instances, sync their series and movies, and confirm both links are live.

1. `bazarr_get_system_settings` — `general.use_sonarr` / `general.use_radarr` false, or an empty `sonarr.apikey`, means the link is missing.
2. `sonarr_get_system_status` — Sonarr answers; Bazarr reaches it at the same host and port.
3. `radarr_get_system_status` — Radarr answers; Bazarr reaches it at the same host and port.
4. `bazarr_post_system_settings` (`settings` = {settings-general-use_sonarr: true, settings-sonarr-ip, settings-sonarr-port, settings-sonarr-base_url: "/", settings-sonarr-apikey: secret SONARR_API_KEY, settings-general-use_radarr: true, settings-radarr-ip, settings-radarr-port, settings-radarr-base_url: "/", settings-radarr-apikey: secret RADARR_API_KEY}) — Approval required: saves the connection. Keys come from the credential store (SONARR_API_KEY, RADARR_API_KEY), never from chat.
5. `bazarr_post_system_tasks` (`taskid` = "update_series") — Sync series from Sonarr now instead of waiting for the hourly job.
6. `bazarr_get_badges` — `sonarr_signalr` and `radarr_signalr` read `LIVE` once both links work; `episodes` / `movies` count what is missing subtitles.

Needs approval: `bazarr_post_system_settings`.

### Enable free subtitle providers and the default language profile (`bazarr-enable-free-providers`)

Enable the subtitle providers that need no account, create the default language profile, and prove a search returns subtitles for one movie and one episode.

1. `bazarr_get_system_settings` — `general.enabled_providers` lists the enabled providers; the provider sections show which need credentials.
2. `bazarr_get_languages_profiles` — An empty list means no language profile: nothing is wanted.
3. `bazarr_post_system_settings` (`settings` = {settings-general-enabled_providers: [...], languages-enabled: ["en"], languages-profiles: JSON [{profileId: 1, name: "English", items: [{id: 1, language: "en", hi: "False", forced: "False", audio_exclude: "False", audio_only_include: "False"}], cutoff: null, mustContain: [], mustNotContain: [], originalFormat: false}], settings-general-serie_default_enabled: true, settings-general-serie_default_profile: 1, settings-general-movie_default_enabled: true, settings-general-movie_default_profile: 1}) — Approval required: enables the no-account providers (Bazarr 1.6.2: embeddedsubtitles, gestdown, subtitlecat, supersubtitles, tvsubtitles, yifysubtitles), enables the language, saves the profile and makes it the series and movie default.
4. `bazarr_get_providers` — Each enabled provider reads `Good`; a throttled one names its retry time.
5. `bazarr_get_movies_wanted` (`length` = 5) — Pick one movie missing subtitles (`radarrId`).
6. `bazarr_get_provider_movies` (`radarrid` = step5.data[0].radarrId) — Manual search across the providers; results name provider, language and score. Can take minutes.
7. `bazarr_get_episodes_wanted` (`length` = 5) — Pick one episode missing subtitles (`sonarrEpisodeId`).
8. `bazarr_get_provider_episodes` (`episodeid` = step7.data[0].sonarrEpisodeId) — Manual search for the episode; results name provider, language and score.

Needs approval: `bazarr_post_system_settings`.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Writes that delete, approve, or change shared settings need the operator's approval first; pass `confirm=true` only after it.
- Never delete media files, series, movies, artists, authors or real tags; only remove test objects named `zz-validation-<date>` that this run created.
- Change API keys, download client credentials or app connection settings only in an approval-required contract step, after the operator approves; read keys and passwords from the credential store and never print them.
- Identify media by its stable external id (TMDB, TVDB, MusicBrainz), not the app-local numeric id.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
