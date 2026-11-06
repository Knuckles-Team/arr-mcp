# Arr Mcp
## CLI or API | MCP

![PyPI - Version](https://img.shields.io/pypi/v/arr-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/arr-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/arr-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/arr-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/arr-mcp)
![PyPI - License](https://img.shields.io/pypi/l/arr-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/arr-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/arr-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/arr-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/arr-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/arr-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/arr-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/arr-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/arr-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/arr-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/arr-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/arr-mcp)

> **Documentation** — Installation, deployment, usage across the API, CLI, MCP, and
> maintained in the [official documentation](https://knuckles-team.github.io/arr-mcp/).

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [CLI or API](#cli-or-api)
- [MCP](#mcp)
  - [Dynamic Tool Selection & Visibility](#dynamic-tool-selection--visibility)
- [Environment Variables](#environment-variables)
- [Security & Governance](#security--governance)
- [Contribute](#contribute)

---

## Overview

**Arr Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Arr Suite MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Complete support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Arr Suite MCP Server for Agentic AI! API. The operator can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server use dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

The table below is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

Every upstream API operation is one typed tool named `<app>_<operation>`. No tool routes by `action`; there is no `params_json`. Every tool is tagged `gated`, so a fleet gateway loads it on demand.

| App | Tools |
|---|---|
| Radarr (movies) | 239 |
| Sonarr (TV) | 237 |
| Lidarr (music) | 235 |
| Chaptarr (books, audiobooks) | 233 |
| Prowlarr (indexers) | 129 |
| Bazarr (subtitles) | 84 |
| Seerr (requests) | 217 |
| Knowledge graph | 1 (`arr_ingest_library`) |

<details>
<summary>Radarr (movies): 239 tools</summary>

| MCP Tool | Description |
|---|---|
| `radarr_add_movie` | Lookup a movie by term, pick the first result, and add it to Radarr. |
| `radarr_delete_autotagging_id` | Delete autotagging id. |
| `radarr_delete_blocklist_bulk` | Delete blocklist bulk. |
| `radarr_delete_blocklist_id` | Delete blocklist id. |
| `radarr_delete_command_id` | Delete command id. |
| `radarr_delete_customfilter_id` | Delete customfilter id. |
| `radarr_delete_customformat_bulk` | Delete customformat bulk. |
| `radarr_delete_customformat_id` | Delete customformat id. |
| `radarr_delete_delayprofile_id` | Delete delayprofile id. |
| `radarr_delete_downloadclient_bulk` | Delete downloadclient bulk. |
| `radarr_delete_downloadclient_id` | Delete downloadclient id. |
| `radarr_delete_exclusions_bulk` | Delete exclusions bulk. |
| `radarr_delete_exclusions_id` | Delete exclusions id. |
| `radarr_delete_importlist_bulk` | Delete importlist bulk. |
| `radarr_delete_importlist_id` | Delete importlist id. |
| `radarr_delete_indexer_bulk` | Delete indexer bulk. |
| `radarr_delete_indexer_id` | Delete indexer id. |
| `radarr_delete_metadata_id` | Delete metadata id. |
| `radarr_delete_movie_editor` | Delete movie editor. |
| `radarr_delete_movie_id` | Delete movie id. |
| `radarr_delete_moviefile_bulk` | Delete moviefile bulk. |
| `radarr_delete_moviefile_id` | Delete moviefile id. |
| `radarr_delete_notification_id` | Delete notification id. |
| `radarr_delete_qualityprofile_id` | Delete qualityprofile id. |
| `radarr_delete_queue_bulk` | Delete queue bulk. |
| `radarr_delete_queue_id` | Delete an item from the download queue. |
| `radarr_delete_releaseprofile_id` | Delete releaseprofile id. |
| `radarr_delete_remotepathmapping_id` | Delete remotepathmapping id. |
| `radarr_delete_rootfolder_id` | Delete rootfolder id. |
| `radarr_delete_system_backup_id` | Delete system backup id. |
| `radarr_delete_tag_id` | Delete tag id. |
| `radarr_get_` | Get . |
| `radarr_get_alttitle` | Get alternative titles for movies. |
| `radarr_get_alttitle_id` | Get a specific alternative title by ID. |
| `radarr_get_api` | Get the base API information. |
| `radarr_get_autotagging` | Get autotagging. |
| `radarr_get_autotagging_id` | Get specific autotagging. |
| `radarr_get_autotagging_schema` | Get autotagging schema. |
| `radarr_get_blocklist` | Get blocklist. |
| `radarr_get_blocklist_movie` | Get blocklisted items for a specific movie. |
| `radarr_get_calendar` | Get calendar. |
| `radarr_get_collection` | Get collection. |
| `radarr_get_collection_id` | Get specific collection. |
| `radarr_get_command` | Get command. |
| `radarr_get_command_id` | Get specific command. |
| `radarr_get_config_downloadclient` | Get config downloadclient. |
| `radarr_get_config_downloadclient_id` | Get specific config downloadclient. |
| `radarr_get_config_host` | Get config host. |
| `radarr_get_config_host_id` | Get specific config host. |
| `radarr_get_config_importlist` | Get config importlist. |
| `radarr_get_config_importlist_id` | Get specific config importlist. |
| `radarr_get_config_indexer` | Get config indexer. |
| `radarr_get_config_indexer_id` | Get specific config indexer. |
| `radarr_get_config_mediamanagement` | Get config mediamanagement. |
| `radarr_get_config_mediamanagement_id` | Get specific config mediamanagement. |
| `radarr_get_config_metadata` | Get config metadata. |
| `radarr_get_config_metadata_id` | Get specific config metadata. |
| `radarr_get_config_naming` | Get config naming. |
| `radarr_get_config_naming_examples` | Get config naming examples. |
| `radarr_get_config_naming_id` | Get specific config naming. |
| `radarr_get_config_ui` | Get config ui. |
| `radarr_get_config_ui_id` | Get specific config ui. |
| `radarr_get_content_path` | Get content path. |
| `radarr_get_credit` | Get credit. |
| `radarr_get_credit_id` | Get specific credit. |
| `radarr_get_customfilter` | Get customfilter. |
| `radarr_get_customfilter_id` | Get specific customfilter. |
| `radarr_get_customformat` | Get customformat. |
| `radarr_get_customformat_id` | Get specific customformat. |
| `radarr_get_customformat_schema` | Get customformat schema. |
| `radarr_get_delayprofile` | Get delayprofile. |
| `radarr_get_delayprofile_id` | Get specific delayprofile. |
| `radarr_get_diskspace` | Get diskspace. |
| `radarr_get_downloadclient` | Get downloadclient. |
| `radarr_get_downloadclient_id` | Get specific downloadclient. |
| `radarr_get_downloadclient_schema` | Get downloadclient schema. |
| `radarr_get_exclusions` | Get all movie import exclusions. |
| `radarr_get_exclusions_id` | Get specific exclusions. |
| `radarr_get_exclusions_paged` | Get exclusions paged. |
| `radarr_get_extrafile` | Get extrafile. |
| `radarr_get_feed_v3_calendar_radarrics` | Get feed v3 calendar radarrics. |
| `radarr_get_filesystem` | Get filesystem. |
| `radarr_get_filesystem_mediafiles` | Get filesystem mediafiles. |
| `radarr_get_filesystem_type` | Get filesystem type. |
| `radarr_get_health` | Get health. |
| `radarr_get_history` | Get history. |
| `radarr_get_history_movie` | Get history movie. |
| `radarr_get_history_since` | Get history since. |
| `radarr_get_importlist` | Get importlist. |
| `radarr_get_importlist_id` | Get specific importlist. |
| `radarr_get_importlist_movie` | Get importlist movie. |
| `radarr_get_importlist_schema` | Get importlist schema. |
| `radarr_get_indexer` | Get indexer. |
| `radarr_get_indexer_id` | Get specific indexer. |
| `radarr_get_indexer_schema` | Get indexer schema. |
| `radarr_get_indexerflag` | Get indexerflag. |
| `radarr_get_language` | Get language. |
| `radarr_get_language_id` | Get specific language. |
| `radarr_get_localization` | Get localization. |
| `radarr_get_localization_language` | Get localization language. |
| `radarr_get_log` | Get log. |
| `radarr_get_log_file` | Get log file. |
| `radarr_get_log_file_filename` | Get log file filename. |
| `radarr_get_log_file_update` | Get log file update. |
| `radarr_get_log_file_update_filename` | Get log file update filename. |
| `radarr_get_login` | Get login. |
| `radarr_get_logout` | Get logout. |
| `radarr_get_manualimport` | Get manualimport. |
| `radarr_get_mediacover_movie_id_filename` | Get specific mediacover movie filename. |
| `radarr_get_metadata` | Get metadata. |
| `radarr_get_metadata_id` | Get specific metadata. |
| `radarr_get_metadata_schema` | Get metadata schema. |
| `radarr_get_movie` | Get movie. |
| `radarr_get_movie_id` | Get specific movie. |
| `radarr_get_movie_id_folder` | Get specific movie folder. |
| `radarr_get_movie_lookup` | Get movie lookup. |
| `radarr_get_movie_lookup_imdb` | Get movie lookup imdb. |
| `radarr_get_movie_lookup_tmdb` | Get movie lookup tmdb. |
| `radarr_get_moviefile` | Get moviefile. |
| `radarr_get_moviefile_id` | Get specific moviefile. |
| `radarr_get_notification` | Get notification. |
| `radarr_get_notification_id` | Get specific notification. |
| `radarr_get_notification_schema` | Get notification schema. |
| `radarr_get_parse` | Get parse. |
| `radarr_get_path` | Get path. |
| `radarr_get_ping` | Get ping. |
| `radarr_get_qualitydefinition` | Get qualitydefinition. |
| `radarr_get_qualitydefinition_id` | Get specific qualitydefinition. |
| `radarr_get_qualitydefinition_limits` | Get qualitydefinition limits. |
| `radarr_get_qualityprofile` | Get qualityprofile. |
| `radarr_get_qualityprofile_id` | Get specific qualityprofile. |
| `radarr_get_qualityprofile_schema` | Get qualityprofile schema. |
| `radarr_get_queue` | Get queue. |
| `radarr_get_queue_details` | Get queue details. |
| `radarr_get_queue_status` | Get queue status. |
| `radarr_get_release` | Get release. |
| `radarr_get_releaseprofile` | Get releaseprofile. |
| `radarr_get_releaseprofile_id` | Get specific releaseprofile. |
| `radarr_get_remotepathmapping` | Get remotepathmapping. |
| `radarr_get_remotepathmapping_id` | Get specific remotepathmapping. |
| `radarr_get_rename` | Get rename. |
| `radarr_get_rootfolder` | Get rootfolder. |
| `radarr_get_rootfolder_id` | Get specific rootfolder. |
| `radarr_get_system_backup` | Get system backup. |
| `radarr_get_system_routes` | Get system routes. |
| `radarr_get_system_routes_duplicate` | Get system routes duplicate. |
| `radarr_get_system_status` | Get system status. |
| `radarr_get_system_task` | Get system task. |
| `radarr_get_system_task_id` | Get specific system task. |
| `radarr_get_tag` | Get tag. |
| `radarr_get_tag_detail` | Get tag detail. |
| `radarr_get_tag_detail_id` | Get specific tag detail. |
| `radarr_get_tag_id` | Get specific tag. |
| `radarr_get_update` | Get update. |
| `radarr_get_wanted_cutoff` | Get wanted cutoff. |
| `radarr_get_wanted_missing` | Get wanted missing. |
| `radarr_lookup_movie` | Search for a movie using the lookup endpoint. |
| `radarr_post_autotagging` | Add a new autotagging. |
| `radarr_post_command` | Add a new command. |
| `radarr_post_customfilter` | Add a new customfilter. |
| `radarr_post_customformat` | Add a new customformat. |
| `radarr_post_delayprofile` | Add a new delayprofile. |
| `radarr_post_downloadclient` | Add a new downloadclient. |
| `radarr_post_downloadclient_action_name` | Add a new downloadclient action name. |
| `radarr_post_downloadclient_test` | Test downloadclient. |
| `radarr_post_downloadclient_testall` | Add a new downloadclient testall. |
| `radarr_post_exclusions` | Add a new exclusions. |
| `radarr_post_exclusions_bulk` | Add a new exclusions bulk. |
| `radarr_post_history_failed_id` | Add a new history failed id. |
| `radarr_post_importlist` | Add a new importlist. |
| `radarr_post_importlist_action_name` | Add a new importlist action name. |
| `radarr_post_importlist_movie` | Add a new importlist movie. |
| `radarr_post_importlist_test` | Test importlist. |
| `radarr_post_importlist_testall` | Add a new importlist testall. |
| `radarr_post_indexer` | Add a new indexer configuration. |
| `radarr_post_indexer_action_name` | Add a new indexer action name. |
| `radarr_post_indexer_test` | Test indexer. |
| `radarr_post_indexer_testall` | Add a new indexer testall. |
| `radarr_post_login` | Log in to the Radarr web interface. |
| `radarr_post_manualimport` | Add a new manualimport. |
| `radarr_post_metadata` | Add a new metadata. |
| `radarr_post_metadata_action_name` | Add a new metadata action name. |
| `radarr_post_metadata_test` | Test metadata. |
| `radarr_post_metadata_testall` | Add a new metadata testall. |
| `radarr_post_movie` | Add a new movie to Radarr. |
| `radarr_post_movie_import` | Add a new movie import. |
| `radarr_post_notification` | Add a new notification. |
| `radarr_post_notification_action_name` | Add a new notification action name. |
| `radarr_post_notification_test` | Test notification. |
| `radarr_post_notification_testall` | Add a new notification testall. |
| `radarr_post_qualityprofile` | Add a new qualityprofile. |
| `radarr_post_queue_grab_bulk` | Add a new queue grab bulk. |
| `radarr_post_queue_grab_id` | Add a new queue grab id. |
| `radarr_post_release` | Add a new release. |
| `radarr_post_release_push` | Add a new release push. |
| `radarr_post_releaseprofile` | Add a new releaseprofile. |
| `radarr_post_remotepathmapping` | Add a new remotepathmapping. |
| `radarr_post_rootfolder` | Add a new rootfolder. |
| `radarr_post_system_backup_restore_id` | Add a new system backup restore id. |
| `radarr_post_system_backup_restore_upload` | Add a new system backup restore upload. |
| `radarr_post_system_restart` | Add a new system restart. |
| `radarr_post_system_shutdown` | Add a new system shutdown. |
| `radarr_post_tag` | Add a new tag. |
| `radarr_put_autotagging_id` | Update autotagging id. |
| `radarr_put_collection` | Update collection. |
| `radarr_put_collection_id` | Update collection id. |
| `radarr_put_config_downloadclient_id` | Update config downloadclient id. |
| `radarr_put_config_host_id` | Update config host id. |
| `radarr_put_config_importlist_id` | Update config importlist id. |
| `radarr_put_config_indexer_id` | Update config indexer id. |
| `radarr_put_config_mediamanagement_id` | Update config mediamanagement id. |
| `radarr_put_config_metadata_id` | Update config metadata id. |
| `radarr_put_config_naming_id` | Update config naming id. |
| `radarr_put_config_ui_id` | Update config ui id. |
| `radarr_put_customfilter_id` | Update customfilter id. |
| `radarr_put_customformat_bulk` | Update customformat bulk. |
| `radarr_put_customformat_id` | Update customformat id. |
| `radarr_put_delayprofile_id` | Update delayprofile id. |
| `radarr_put_delayprofile_reorder_id` | Update delayprofile reorder id. |
| `radarr_put_downloadclient_bulk` | Update downloadclient bulk. |
| `radarr_put_downloadclient_id` | Update downloadclient id. |
| `radarr_put_exclusions_id` | Update exclusions id. |
| `radarr_put_importlist_bulk` | Update importlist bulk. |
| `radarr_put_importlist_id` | Update importlist id. |
| `radarr_put_indexer_bulk` | Update indexer bulk. |
| `radarr_put_indexer_id` | Update an existing indexer configuration by ID. |
| `radarr_put_metadata_id` | Update metadata id. |
| `radarr_put_movie_editor` | Update movie editor. |
| `radarr_put_movie_id` | Update an existing movie configuration. |
| `radarr_put_moviefile_bulk` | Update moviefile bulk. |
| `radarr_put_moviefile_editor` | Update moviefile editor. |
| `radarr_put_moviefile_id` | Update moviefile id. |
| `radarr_put_notification_id` | Update notification id. |
| `radarr_put_qualitydefinition_id` | Update qualitydefinition id. |
| `radarr_put_qualitydefinition_update` | Update qualitydefinition update. |
| `radarr_put_qualityprofile_id` | Update qualityprofile id. |
| `radarr_put_releaseprofile_id` | Update releaseprofile id. |
| `radarr_put_remotepathmapping_id` | Update remotepathmapping id. |
| `radarr_put_tag_id` | Update tag id. |

</details>

<details>
<summary>Sonarr (TV): 237 tools</summary>

| MCP Tool | Description |
|---|---|
| `sonarr_add_series` | Lookup a series by term, pick the first result, and add it to Sonarr. |
| `sonarr_delete_autotagging_id` | Delete an auto-tagging rule by ID. |
| `sonarr_delete_blocklist_bulk` | Delete blocklist bulk. |
| `sonarr_delete_blocklist_id` | Delete a blocklisted item by ID. |
| `sonarr_delete_command_id` | Delete command id. |
| `sonarr_delete_customfilter_id` | Delete customfilter id. |
| `sonarr_delete_customformat_bulk` | Delete customformat bulk. |
| `sonarr_delete_customformat_id` | Delete customformat id. |
| `sonarr_delete_delayprofile_id` | Delete delayprofile id. |
| `sonarr_delete_downloadclient_bulk` | Delete downloadclient bulk. |
| `sonarr_delete_downloadclient_id` | Delete downloadclient id. |
| `sonarr_delete_episodefile_bulk` | Delete episodefile bulk. |
| `sonarr_delete_episodefile_id` | Delete episodefile id. |
| `sonarr_delete_importlist_bulk` | Delete importlist bulk. |
| `sonarr_delete_importlist_id` | Delete an import list configuration by ID. |
| `sonarr_delete_importlistexclusion_bulk` | Delete importlistexclusion bulk. |
| `sonarr_delete_importlistexclusion_id` | Delete importlistexclusion id. |
| `sonarr_delete_indexer_bulk` | Delete indexer bulk. |
| `sonarr_delete_indexer_id` | Delete an indexer configuration by ID. |
| `sonarr_delete_languageprofile_id` | Delete languageprofile id. |
| `sonarr_delete_metadata_id` | Delete metadata id. |
| `sonarr_delete_notification_id` | Delete notification id. |
| `sonarr_delete_qualityprofile_id` | Delete qualityprofile id. |
| `sonarr_delete_queue_bulk` | Delete queue bulk. |
| `sonarr_delete_queue_id` | Delete queue id. |
| `sonarr_delete_releaseprofile_id` | Delete releaseprofile id. |
| `sonarr_delete_remotepathmapping_id` | Delete remotepathmapping id. |
| `sonarr_delete_rootfolder_id` | Delete rootfolder id. |
| `sonarr_delete_series_editor` | Delete series editor. |
| `sonarr_delete_series_id` | Delete series. |
| `sonarr_delete_system_backup_id` | Delete a system backup file by ID. |
| `sonarr_delete_tag_id` | Delete a tag. |
| `sonarr_get_` | Get resource by path. |
| `sonarr_get_api` | Get the base API information. |
| `sonarr_get_autotagging` | Get all auto-tagging rules. |
| `sonarr_get_autotagging_id` | Get details for a specific auto-tagging rule by ID. |
| `sonarr_get_autotagging_schema` | Get the schema for auto-tagging rules. |
| `sonarr_get_blocklist` | Get blocklist. |
| `sonarr_get_calendar` | Get calendar. |
| `sonarr_get_calendar_id` | Get specific calendar. |
| `sonarr_get_command` | Get command. |
| `sonarr_get_command_id` | Get specific command. |
| `sonarr_get_config_downloadclient` | Get config downloadclient. |
| `sonarr_get_config_downloadclient_id` | Get specific config downloadclient. |
| `sonarr_get_config_host` | Get config host. |
| `sonarr_get_config_host_id` | Get specific config host. |
| `sonarr_get_config_importlist` | Get config importlist. |
| `sonarr_get_config_importlist_id` | Get specific config importlist. |
| `sonarr_get_config_indexer` | Get config indexer. |
| `sonarr_get_config_indexer_id` | Get specific config indexer. |
| `sonarr_get_config_mediamanagement` | Get config mediamanagement. |
| `sonarr_get_config_mediamanagement_id` | Get specific config mediamanagement. |
| `sonarr_get_config_naming` | Get config naming. |
| `sonarr_get_config_naming_examples` | Get config naming examples. |
| `sonarr_get_config_naming_id` | Get specific config naming. |
| `sonarr_get_config_ui` | Get UI configuration. |
| `sonarr_get_config_ui_id` | Get specific UI configuration. |
| `sonarr_get_content_path` | Get content path. |
| `sonarr_get_customfilter` | Get customfilter. |
| `sonarr_get_customfilter_id` | Get specific customfilter. |
| `sonarr_get_customformat` | Get customformat. |
| `sonarr_get_customformat_id` | Get specific customformat. |
| `sonarr_get_customformat_schema` | Get customformat schema. |
| `sonarr_get_delayprofile` | Get delayprofile. |
| `sonarr_get_delayprofile_id` | Get specific delayprofile. |
| `sonarr_get_diskspace` | Get diskspace. |
| `sonarr_get_downloadclient` | Get downloadclient. |
| `sonarr_get_downloadclient_id` | Get specific downloadclient. |
| `sonarr_get_downloadclient_schema` | Get downloadclient schema. |
| `sonarr_get_episode` | Get episode. |
| `sonarr_get_episode_id` | Get specific episode. |
| `sonarr_get_episodefile` | Get episodefile. |
| `sonarr_get_episodefile_id` | Get specific episodefile. |
| `sonarr_get_feed_v3_calendar_sonarrics` | Get feed v3 calendar sonarrics. |
| `sonarr_get_filesystem` | Get filesystem. |
| `sonarr_get_filesystem_mediafiles` | Get filesystem mediafiles. |
| `sonarr_get_filesystem_type` | Get filesystem type. |
| `sonarr_get_health` | Get health. |
| `sonarr_get_history` | Get history. |
| `sonarr_get_history_series` | Get history series. |
| `sonarr_get_history_since` | Get history since. |
| `sonarr_get_importlist` | Get importlist. |
| `sonarr_get_importlist_id` | Get details for a specific import list by ID. |
| `sonarr_get_importlist_schema` | Get importlist schema. |
| `sonarr_get_importlistexclusion` | Get importlistexclusion. |
| `sonarr_get_importlistexclusion_id` | Get specific importlistexclusion. |
| `sonarr_get_importlistexclusion_paged` | Get importlistexclusion paged. |
| `sonarr_get_indexer` | Get indexer. |
| `sonarr_get_indexer_id` | Get specific indexer. |
| `sonarr_get_indexer_schema` | Get indexer schema. |
| `sonarr_get_indexerflag` | Get indexerflag. |
| `sonarr_get_language` | Get language. |
| `sonarr_get_language_id` | Get specific language. |
| `sonarr_get_languageprofile` | Get languageprofile. |
| `sonarr_get_languageprofile_id` | Get specific languageprofile. |
| `sonarr_get_languageprofile_schema` | Get languageprofile schema. |
| `sonarr_get_localization` | Get localization. |
| `sonarr_get_localization_id` | Get specific localization. |
| `sonarr_get_localization_language` | Get localization language. |
| `sonarr_get_log` | Get log. |
| `sonarr_get_log_file` | Get log file. |
| `sonarr_get_log_file_filename` | Get log file filename. |
| `sonarr_get_log_file_update` | Get log file update. |
| `sonarr_get_log_file_update_filename` | Get log file update content. |
| `sonarr_get_login` | Get the login status and information. |
| `sonarr_get_logout` | Log out from the Sonarr web interface. |
| `sonarr_get_manualimport` | Get manualimport. |
| `sonarr_get_mediacover_series_id_filename` | Get specific mediacover series filename. |
| `sonarr_get_metadata` | Get metadata. |
| `sonarr_get_metadata_id` | Get specific metadata. |
| `sonarr_get_metadata_schema` | Get metadata schema. |
| `sonarr_get_notification` | Get notification. |
| `sonarr_get_notification_id` | Get specific notification. |
| `sonarr_get_notification_schema` | Get notification schema. |
| `sonarr_get_parse` | Get parse. |
| `sonarr_get_path` | Get system routes. |
| `sonarr_get_ping` | Ping the Sonarr API to check connectivity. |
| `sonarr_get_qualitydefinition` | Get all quality definitions. |
| `sonarr_get_qualitydefinition_id` | Get a specific quality definition by ID. |
| `sonarr_get_qualitydefinition_limits` | Get qualitydefinition limits. |
| `sonarr_get_qualityprofile` | Get qualityprofile. |
| `sonarr_get_qualityprofile_id` | Get specific qualityprofile. |
| `sonarr_get_qualityprofile_schema` | Get qualityprofile schema. |
| `sonarr_get_queue` | Get queue. |
| `sonarr_get_queue_details` | Get queue details. |
| `sonarr_get_queue_status` | Get queue status. |
| `sonarr_get_release` | Get release. |
| `sonarr_get_releaseprofile` | Get releaseprofile. |
| `sonarr_get_releaseprofile_id` | Get specific releaseprofile. |
| `sonarr_get_remotepathmapping` | Get remotepathmapping. |
| `sonarr_get_remotepathmapping_id` | Get specific remotepathmapping. |
| `sonarr_get_rename` | Get rename. |
| `sonarr_get_rename_bulk` | Preview the episode file renames of several series at once. |
| `sonarr_get_rootfolder` | Get rootfolder. |
| `sonarr_get_rootfolder_id` | Get specific rootfolder. |
| `sonarr_get_series` | Get series. |
| `sonarr_get_series_id` | Get specific series. |
| `sonarr_get_series_id_folder` | Get series folder. |
| `sonarr_get_series_lookup` | Lookup series. |
| `sonarr_get_system_backup` | Get information about available system backups. |
| `sonarr_get_system_routes` | Get system routes. |
| `sonarr_get_system_routes_duplicate` | Get duplicate system routes. |
| `sonarr_get_system_status` | Get system status. |
| `sonarr_get_system_task` | Get system tasks. |
| `sonarr_get_system_task_id` | Get specific system task. |
| `sonarr_get_tag` | Get tags. |
| `sonarr_get_tag_detail` | Get tag usage details. |
| `sonarr_get_tag_detail_id` | Get specific tag usage details. |
| `sonarr_get_tag_id` | Get specific tag. |
| `sonarr_get_update` | Get available updates. |
| `sonarr_get_wanted_cutoff` | Get wanted cutoff. |
| `sonarr_get_wanted_cutoff_id` | Get specific wanted cutoff. |
| `sonarr_get_wanted_missing` | Get wanted missing. |
| `sonarr_get_wanted_missing_id` | Get specific wanted missing. |
| `sonarr_lookup_series` | Search for a series using the lookup endpoint. |
| `sonarr_post_autotagging` | Add a new auto-tagging rule. |
| `sonarr_post_command` | Add a new command. |
| `sonarr_post_customfilter` | Add a new customfilter. |
| `sonarr_post_customformat` | Add a new customformat. |
| `sonarr_post_delayprofile` | Add a new delayprofile. |
| `sonarr_post_downloadclient` | Add a new downloadclient. |
| `sonarr_post_downloadclient_action_name` | Add a new downloadclient action name. |
| `sonarr_post_downloadclient_test` | Test downloadclient. |
| `sonarr_post_downloadclient_testall` | Add a new downloadclient testall. |
| `sonarr_post_history_failed_id` | Add a new history failed id. |
| `sonarr_post_importlist` | Add a new import list configuration. |
| `sonarr_post_importlist_action_name` | Add a new importlist action name. |
| `sonarr_post_importlist_test` | Test importlist. |
| `sonarr_post_importlist_testall` | Add a new importlist testall. |
| `sonarr_post_importlistexclusion` | Add a new importlistexclusion. |
| `sonarr_post_indexer` | Add a new indexer configuration. |
| `sonarr_post_indexer_action_name` | Add a new indexer action name. |
| `sonarr_post_indexer_test` | Test indexer. |
| `sonarr_post_indexer_testall` | Add a new indexer testall. |
| `sonarr_post_languageprofile` | Add a new languageprofile. |
| `sonarr_post_login` | Log in to the Sonarr web interface. |
| `sonarr_post_manualimport` | Add a new manualimport. |
| `sonarr_post_metadata` | Add a new metadata. |
| `sonarr_post_metadata_action_name` | Add a new metadata action name. |
| `sonarr_post_metadata_test` | Test metadata. |
| `sonarr_post_metadata_testall` | Add a new metadata testall. |
| `sonarr_post_notification` | Add a new notification. |
| `sonarr_post_notification_action_name` | Add a new notification action name. |
| `sonarr_post_notification_test` | Test notification. |
| `sonarr_post_notification_testall` | Add a new notification testall. |
| `sonarr_post_qualityprofile` | Add a new qualityprofile. |
| `sonarr_post_queue_grab_bulk` | Add a new queue grab bulk. |
| `sonarr_post_queue_grab_id` | Add a new queue grab id. |
| `sonarr_post_release` | Add a new release. |
| `sonarr_post_release_push` | Add a new release push. |
| `sonarr_post_releaseprofile` | Add a new releaseprofile. |
| `sonarr_post_remotepathmapping` | Add a new remotepathmapping. |
| `sonarr_post_rootfolder` | Add a new rootfolder. |
| `sonarr_post_seasonpass` | Add a new seasonpass. |
| `sonarr_post_series` | Add a new series. |
| `sonarr_post_series_import` | Import series. |
| `sonarr_post_system_backup_restore_id` | Add a new system backup restore id. |
| `sonarr_post_system_backup_restore_upload` | Add a new system backup restore upload. |
| `sonarr_post_system_restart` | Trigger system restart. |
| `sonarr_post_system_shutdown` | Trigger system shutdown. |
| `sonarr_post_tag` | Add a new tag. |
| `sonarr_put_autotagging_id` | Update an existing auto-tagging rule by ID. |
| `sonarr_put_config_downloadclient_id` | Update config downloadclient id. |
| `sonarr_put_config_host_id` | Update config host id. |
| `sonarr_put_config_importlist_id` | Update config importlist id. |
| `sonarr_put_config_indexer_id` | Update config indexer id. |
| `sonarr_put_config_mediamanagement_id` | Update config mediamanagement id. |
| `sonarr_put_config_naming_id` | Update config naming id. |
| `sonarr_put_config_ui_id` | Update UI configuration. |
| `sonarr_put_customfilter_id` | Update customfilter id. |
| `sonarr_put_customformat_bulk` | Update customformat bulk. |
| `sonarr_put_customformat_id` | Update customformat id. |
| `sonarr_put_delayprofile_id` | Update delayprofile id. |
| `sonarr_put_delayprofile_reorder_id` | Update delayprofile reorder id. |
| `sonarr_put_downloadclient_bulk` | Update downloadclient bulk. |
| `sonarr_put_downloadclient_id` | Update downloadclient id. |
| `sonarr_put_episode_id` | Update episode id. |
| `sonarr_put_episode_monitor` | Update episode monitor. |
| `sonarr_put_episodefile_bulk` | Update episodefile bulk. |
| `sonarr_put_episodefile_editor` | Update episodefile editor. |
| `sonarr_put_episodefile_id` | Update episodefile id. |
| `sonarr_put_importlist_bulk` | Update importlist bulk. |
| `sonarr_put_importlist_id` | Update an existing import list configuration. |
| `sonarr_put_importlistexclusion_id` | Update importlistexclusion id. |
| `sonarr_put_indexer_bulk` | Update indexer bulk. |
| `sonarr_put_indexer_id` | Update an existing indexer configuration by ID. |
| `sonarr_put_languageprofile_id` | Update languageprofile id. |
| `sonarr_put_metadata_id` | Update metadata id. |
| `sonarr_put_notification_id` | Update notification id. |
| `sonarr_put_qualitydefinition_id` | Update qualitydefinition id. |
| `sonarr_put_qualitydefinition_update` | Update qualitydefinition update. |
| `sonarr_put_qualityprofile_id` | Update qualityprofile id. |
| `sonarr_put_releaseprofile_id` | Update releaseprofile id. |
| `sonarr_put_remotepathmapping_id` | Update remotepathmapping id. |
| `sonarr_put_series_editor` | Update series editor. |
| `sonarr_put_series_id` | Update series id. |
| `sonarr_put_tag_id` | Update a tag. |

</details>

<details>
<summary>Lidarr (music): 235 tools</summary>

| MCP Tool | Description |
|---|---|
| `lidarr_delete_album_id` | Delete an album and optionally its files and add exclusion. |
| `lidarr_delete_artist_editor` | Delete multiple artists using the artist editor. |
| `lidarr_delete_artist_id` | Delete artist id. |
| `lidarr_delete_autotagging_id` | Delete autotagging id. |
| `lidarr_delete_blocklist_bulk` | Delete blocklist bulk. |
| `lidarr_delete_blocklist_id` | Delete blocklist id. |
| `lidarr_delete_command_id` | Delete command id. |
| `lidarr_delete_customfilter_id` | Delete customfilter id. |
| `lidarr_delete_customformat_bulk` | Delete customformat bulk. |
| `lidarr_delete_customformat_id` | Delete customformat id. |
| `lidarr_delete_delayprofile_id` | Delete delayprofile id. |
| `lidarr_delete_downloadclient_bulk` | Delete downloadclient bulk. |
| `lidarr_delete_downloadclient_id` | Delete downloadclient id. |
| `lidarr_delete_importlist_bulk` | Delete multiple import lists in bulk. |
| `lidarr_delete_importlist_id` | Delete an import list configuration. |
| `lidarr_delete_importlistexclusion_id` | Delete importlistexclusion id. |
| `lidarr_delete_indexer_bulk` | Delete indexer bulk. |
| `lidarr_delete_indexer_id` | Delete an indexer configuration by ID. |
| `lidarr_delete_metadata_id` | Delete metadata id. |
| `lidarr_delete_metadataprofile_id` | Delete metadataprofile id. |
| `lidarr_delete_notification_id` | Delete notification id. |
| `lidarr_delete_qualityprofile_id` | Delete qualityprofile id. |
| `lidarr_delete_queue_bulk` | Delete queue bulk. |
| `lidarr_delete_queue_id` | Delete queue id. |
| `lidarr_delete_releaseprofile_id` | Delete releaseprofile id. |
| `lidarr_delete_remotepathmapping_id` | Delete remotepathmapping id. |
| `lidarr_delete_rootfolder_id` | Delete rootfolder id. |
| `lidarr_delete_system_backup_id` | Delete system backup id. |
| `lidarr_delete_tag_id` | Delete tag id. |
| `lidarr_delete_trackfile_bulk` | Delete trackfile bulk. |
| `lidarr_delete_trackfile_id` | Delete trackfile id. |
| `lidarr_get_` | Get . |
| `lidarr_get_album` | Get albums managed by Lidarr. |
| `lidarr_get_album_id` | Get details for a specific album by ID. |
| `lidarr_get_album_lookup` | Search for new albums to add to Lidarr. |
| `lidarr_get_api` | Get the base API information. |
| `lidarr_get_artist` | Get all artists managed by Lidarr. |
| `lidarr_get_artist_id` | Get details for a specific artist by ID. |
| `lidarr_get_artist_lookup` | Search for new artists to add to Lidarr. |
| `lidarr_get_autotagging` | Get autotagging. |
| `lidarr_get_autotagging_id` | Get specific autotagging. |
| `lidarr_get_autotagging_schema` | Get autotagging schema. |
| `lidarr_get_blocklist` | Get blocklist. |
| `lidarr_get_calendar` | Get calendar. |
| `lidarr_get_calendar_id` | Get specific calendar. |
| `lidarr_get_command` | Get command. |
| `lidarr_get_command_id` | Get specific command. |
| `lidarr_get_config_downloadclient` | Get config downloadclient. |
| `lidarr_get_config_downloadclient_id` | Get specific config downloadclient. |
| `lidarr_get_config_host` | Get config host. |
| `lidarr_get_config_host_id` | Get specific config host. |
| `lidarr_get_config_indexer` | Get config indexer. |
| `lidarr_get_config_indexer_id` | Get specific config indexer. |
| `lidarr_get_config_mediamanagement` | Get config mediamanagement. |
| `lidarr_get_config_mediamanagement_id` | Get specific config mediamanagement. |
| `lidarr_get_config_metadataprovider` | Get config metadataprovider. |
| `lidarr_get_config_metadataprovider_id` | Get specific config metadataprovider. |
| `lidarr_get_config_naming` | Get config naming. |
| `lidarr_get_config_naming_examples` | Get config naming examples. |
| `lidarr_get_config_naming_id` | Get specific config naming. |
| `lidarr_get_config_ui` | Get config ui. |
| `lidarr_get_config_ui_id` | Get specific config ui. |
| `lidarr_get_content_path` | Get content path. |
| `lidarr_get_customfilter` | Get customfilter. |
| `lidarr_get_customfilter_id` | Get specific customfilter. |
| `lidarr_get_customformat` | Get customformat. |
| `lidarr_get_customformat_id` | Get specific customformat. |
| `lidarr_get_customformat_schema` | Get customformat schema. |
| `lidarr_get_delayprofile` | Get delayprofile. |
| `lidarr_get_delayprofile_id` | Get specific delayprofile. |
| `lidarr_get_diskspace` | Get diskspace. |
| `lidarr_get_downloadclient` | Get downloadclient. |
| `lidarr_get_downloadclient_id` | Get specific downloadclient. |
| `lidarr_get_downloadclient_schema` | Get downloadclient schema. |
| `lidarr_get_feed_v1_calendar_lidarrics` | Get feed v1 calendar lidarrics. |
| `lidarr_get_filesystem` | Get filesystem. |
| `lidarr_get_filesystem_mediafiles` | Get filesystem mediafiles. |
| `lidarr_get_filesystem_type` | Get filesystem type. |
| `lidarr_get_health` | Get health. |
| `lidarr_get_history` | Get history. |
| `lidarr_get_history_artist` | Get history artist. |
| `lidarr_get_history_since` | Get history since. |
| `lidarr_get_importlist` | Get all import lists. |
| `lidarr_get_importlist_id` | Get details for a specific import list by ID. |
| `lidarr_get_importlist_schema` | Get the schema for import list configurations. |
| `lidarr_get_importlistexclusion` | Get importlistexclusion. |
| `lidarr_get_importlistexclusion_id` | Get specific importlistexclusion. |
| `lidarr_get_indexer` | Get all configured indexers. |
| `lidarr_get_indexer_id` | Get details for a specific indexer by ID. |
| `lidarr_get_indexer_schema` | Get indexer schema. |
| `lidarr_get_indexerflag` | Get indexerflag. |
| `lidarr_get_language` | Get language. |
| `lidarr_get_language_id` | Get specific language. |
| `lidarr_get_localization` | Get localization. |
| `lidarr_get_log` | Get log. |
| `lidarr_get_log_file` | Get log file. |
| `lidarr_get_log_file_filename` | Get log file filename. |
| `lidarr_get_log_file_update` | Get log file update. |
| `lidarr_get_log_file_update_filename` | Get log file update filename. |
| `lidarr_get_login` | Get login. |
| `lidarr_get_logout` | Get logout. |
| `lidarr_get_manualimport` | Get manualimport. |
| `lidarr_get_mediacover_album_album_id_filename` | Get specific mediacover album album filename. |
| `lidarr_get_mediacover_artist_artist_id_filename` | Get specific mediacover artist artist filename. |
| `lidarr_get_metadata` | Get metadata. |
| `lidarr_get_metadata_id` | Get specific metadata. |
| `lidarr_get_metadata_schema` | Get metadata schema. |
| `lidarr_get_metadataprofile` | Get metadataprofile. |
| `lidarr_get_metadataprofile_id` | Get specific metadataprofile. |
| `lidarr_get_metadataprofile_schema` | Get metadataprofile schema. |
| `lidarr_get_notification` | Get notification. |
| `lidarr_get_notification_id` | Get specific notification. |
| `lidarr_get_notification_schema` | Get notification schema. |
| `lidarr_get_parse` | Get parse. |
| `lidarr_get_path` | Get path. |
| `lidarr_get_ping` | Get ping. |
| `lidarr_get_qualitydefinition` | Get qualitydefinition. |
| `lidarr_get_qualitydefinition_id` | Get specific qualitydefinition. |
| `lidarr_get_qualityprofile` | Get qualityprofile. |
| `lidarr_get_qualityprofile_id` | Get specific qualityprofile. |
| `lidarr_get_qualityprofile_schema` | Get qualityprofile schema. |
| `lidarr_get_queue` | Get queue. |
| `lidarr_get_queue_details` | Get queue details. |
| `lidarr_get_queue_status` | Get queue status. |
| `lidarr_get_release` | Get release. |
| `lidarr_get_releaseprofile` | Get all configured release profiles. |
| `lidarr_get_releaseprofile_id` | Get specific releaseprofile. |
| `lidarr_get_remotepathmapping` | Get remotepathmapping. |
| `lidarr_get_remotepathmapping_id` | Get specific remotepathmapping. |
| `lidarr_get_rename` | Get rename. |
| `lidarr_get_retag` | Get retag. |
| `lidarr_get_rootfolder` | Get all configured root folders. |
| `lidarr_get_rootfolder_id` | Get specific rootfolder. |
| `lidarr_get_search` | Get search. |
| `lidarr_get_system_backup` | Get system backup. |
| `lidarr_get_system_routes` | Get system routes. |
| `lidarr_get_system_routes_duplicate` | Get system routes duplicate. |
| `lidarr_get_system_status` | Get the current system status for Lidarr. |
| `lidarr_get_system_task` | Get system task. |
| `lidarr_get_system_task_id` | Get specific system task. |
| `lidarr_get_tag` | Get all configured tags. |
| `lidarr_get_tag_detail` | Get tag detail. |
| `lidarr_get_tag_detail_id` | Get specific tag detail. |
| `lidarr_get_tag_id` | Get specific tag. |
| `lidarr_get_track` | Get track. |
| `lidarr_get_track_id` | Get specific track. |
| `lidarr_get_trackfile` | Get trackfile. |
| `lidarr_get_trackfile_id` | Get specific trackfile. |
| `lidarr_get_update` | Get update. |
| `lidarr_get_wanted_cutoff` | Get wanted cutoff. |
| `lidarr_get_wanted_cutoff_id` | Get specific wanted cutoff. |
| `lidarr_get_wanted_missing` | Get wanted missing. |
| `lidarr_get_wanted_missing_id` | Get specific wanted missing. |
| `lidarr_post_album` | Add a new album to Lidarr. |
| `lidarr_post_albumstudio` | Perform studio operations on albums. |
| `lidarr_post_artist` | Add a new artist to Lidarr. |
| `lidarr_post_autotagging` | Add a new autotagging. |
| `lidarr_post_command` | Add a new command. |
| `lidarr_post_customfilter` | Add a new customfilter. |
| `lidarr_post_customformat` | Add a new customformat. |
| `lidarr_post_delayprofile` | Add a new delayprofile. |
| `lidarr_post_downloadclient` | Add a new downloadclient. |
| `lidarr_post_downloadclient_action_name` | Add a new downloadclient action name. |
| `lidarr_post_downloadclient_test` | Test downloadclient. |
| `lidarr_post_downloadclient_testall` | Add a new downloadclient testall. |
| `lidarr_post_history_failed_id` | Add a new history failed id. |
| `lidarr_post_importlist` | Add a new import list. |
| `lidarr_post_importlist_action_name` | Perform a specific action on import lists. |
| `lidarr_post_importlist_test` | Test an import list configuration. |
| `lidarr_post_importlist_testall` | Test all configured import lists. |
| `lidarr_post_importlistexclusion` | Add a new importlistexclusion. |
| `lidarr_post_indexer` | Add a new indexer configuration. |
| `lidarr_post_indexer_action_name` | Add a new indexer action name. |
| `lidarr_post_indexer_test` | Test indexer. |
| `lidarr_post_indexer_testall` | Add a new indexer testall. |
| `lidarr_post_login` | Add a new login. |
| `lidarr_post_manualimport` | Add a new manualimport. |
| `lidarr_post_metadata` | Add a new metadata. |
| `lidarr_post_metadata_action_name` | Add a new metadata action name. |
| `lidarr_post_metadata_test` | Test metadata. |
| `lidarr_post_metadata_testall` | Add a new metadata testall. |
| `lidarr_post_metadataprofile` | Add a new metadataprofile. |
| `lidarr_post_notification` | Add a new notification. |
| `lidarr_post_notification_action_name` | Add a new notification action name. |
| `lidarr_post_notification_test` | Test notification. |
| `lidarr_post_notification_testall` | Add a new notification testall. |
| `lidarr_post_qualityprofile` | Add a new qualityprofile. |
| `lidarr_post_queue_grab_bulk` | Add a new queue grab bulk. |
| `lidarr_post_queue_grab_id` | Add a new queue grab id. |
| `lidarr_post_release` | Add a new release. |
| `lidarr_post_release_push` | Add a new release push. |
| `lidarr_post_releaseprofile` | Add a new release profile configuration. |
| `lidarr_post_remotepathmapping` | Add a new remotepathmapping. |
| `lidarr_post_rootfolder` | Add a new root folder. |
| `lidarr_post_system_backup_restore_id` | Add a new system backup restore id. |
| `lidarr_post_system_backup_restore_upload` | Add a new system backup restore upload. |
| `lidarr_post_system_restart` | Add a new system restart. |
| `lidarr_post_system_shutdown` | Add a new system shutdown. |
| `lidarr_post_tag` | Add a new tag. |
| `lidarr_put_album_id` | Update an existing album by ID. |
| `lidarr_put_album_monitor` | Update monitoring status for multiple albums. |
| `lidarr_put_artist_editor` | Update monitoring or tagging for multiple artists. |
| `lidarr_put_artist_id` | Update an existing artist configuration. |
| `lidarr_put_autotagging_id` | Update autotagging id. |
| `lidarr_put_config_downloadclient_id` | Update config downloadclient id. |
| `lidarr_put_config_host_id` | Update config host id. |
| `lidarr_put_config_indexer_id` | Update config indexer id. |
| `lidarr_put_config_mediamanagement_id` | Update config mediamanagement id. |
| `lidarr_put_config_metadataprovider_id` | Update config metadataprovider id. |
| `lidarr_put_config_naming_id` | Update config naming id. |
| `lidarr_put_config_ui_id` | Update config ui id. |
| `lidarr_put_customfilter_id` | Update customfilter id. |
| `lidarr_put_customformat_bulk` | Update customformat bulk. |
| `lidarr_put_customformat_id` | Update customformat id. |
| `lidarr_put_delayprofile_id` | Update delayprofile id. |
| `lidarr_put_delayprofile_reorder_id` | Update delayprofile reorder id. |
| `lidarr_put_downloadclient_bulk` | Update downloadclient bulk. |
| `lidarr_put_downloadclient_id` | Update downloadclient id. |
| `lidarr_put_importlist_bulk` | Update multiple import lists in bulk. |
| `lidarr_put_importlist_id` | Update an existing import list configuration. |
| `lidarr_put_importlistexclusion_id` | Update importlistexclusion id. |
| `lidarr_put_indexer_bulk` | Update indexer bulk. |
| `lidarr_put_indexer_id` | Update an existing indexer configuration. |
| `lidarr_put_metadata_id` | Update metadata id. |
| `lidarr_put_metadataprofile_id` | Update metadataprofile id. |
| `lidarr_put_notification_id` | Update notification id. |
| `lidarr_put_qualitydefinition_id` | Update qualitydefinition id. |
| `lidarr_put_qualitydefinition_update` | Update qualitydefinition update. |
| `lidarr_put_qualityprofile_id` | Update qualityprofile id. |
| `lidarr_put_releaseprofile_id` | Update releaseprofile id. |
| `lidarr_put_remotepathmapping_id` | Update remotepathmapping id. |
| `lidarr_put_rootfolder_id` | Update rootfolder id. |
| `lidarr_put_tag_id` | Update tag id. |
| `lidarr_put_trackfile_editor` | Update trackfile editor. |
| `lidarr_put_trackfile_id` | Update trackfile id. |

</details>

<details>
<summary>Chaptarr (books, audiobooks): 233 tools</summary>

| MCP Tool | Description |
|---|---|
| `chaptarr_delete_author_editor` | Delete author editor. |
| `chaptarr_delete_author_id` | Delete an author by ID. |
| `chaptarr_delete_blocklist_bulk` | Delete blocklist bulk. |
| `chaptarr_delete_blocklist_id` | Delete blocklist id. |
| `chaptarr_delete_book_editor` | Delete book editor. |
| `chaptarr_delete_book_id` | Delete book id. |
| `chaptarr_delete_bookfile_bulk` | Delete bookfile bulk. |
| `chaptarr_delete_bookfile_id` | Delete bookfile id. |
| `chaptarr_delete_command_id` | Delete command id. |
| `chaptarr_delete_customfilter_id` | Delete customfilter id. |
| `chaptarr_delete_customformat_id` | Delete customformat id. |
| `chaptarr_delete_delayprofile_id` | Delete delayprofile id. |
| `chaptarr_delete_downloadclient_bulk` | Delete downloadclient bulk. |
| `chaptarr_delete_downloadclient_id` | Delete downloadclient id. |
| `chaptarr_delete_importlist_bulk` | Delete importlist bulk. |
| `chaptarr_delete_importlist_id` | Delete importlist id. |
| `chaptarr_delete_importlistexclusion_id` | Delete importlistexclusion id. |
| `chaptarr_delete_indexer_bulk` | Delete indexer bulk. |
| `chaptarr_delete_indexer_id` | Delete indexer id. |
| `chaptarr_delete_metadata_id` | Delete metadata id. |
| `chaptarr_delete_metadataprofile_id` | Delete metadataprofile id. |
| `chaptarr_delete_notification_id` | Delete notification id. |
| `chaptarr_delete_qualityprofile_id` | Delete qualityprofile id. |
| `chaptarr_delete_queue_bulk` | Delete queue bulk. |
| `chaptarr_delete_queue_id` | Delete queue id. |
| `chaptarr_delete_releaseprofile_id` | Delete releaseprofile id. |
| `chaptarr_delete_remotepathmapping_id` | Delete remotepathmapping id. |
| `chaptarr_delete_rootfolder_id` | Delete rootfolder id. |
| `chaptarr_delete_system_backup_id` | Delete system backup id. |
| `chaptarr_delete_tag_id` | Delete tag id. |
| `chaptarr_get_` | Get . |
| `chaptarr_get_api` | Get the base API information. |
| `chaptarr_get_author` | Get all authors managed by Chaptarr. |
| `chaptarr_get_author_id` | Get specific author. |
| `chaptarr_get_author_lookup` | Get author lookup. |
| `chaptarr_get_blocklist` | Get blocklist. |
| `chaptarr_get_book` | Get book. |
| `chaptarr_get_book_id` | Get specific book. |
| `chaptarr_get_book_id_overview` | Get specific book overview. |
| `chaptarr_get_book_lookup` | Get book lookup. |
| `chaptarr_get_bookfile` | Get bookfile. |
| `chaptarr_get_bookfile_id` | Get specific bookfile. |
| `chaptarr_get_calendar` | Get calendar. |
| `chaptarr_get_calendar_id` | Get specific calendar. |
| `chaptarr_get_command` | Get command. |
| `chaptarr_get_command_id` | Get specific command. |
| `chaptarr_get_config_development` | Get config development. |
| `chaptarr_get_config_development_id` | Get specific config development. |
| `chaptarr_get_config_downloadclient` | Get config downloadclient. |
| `chaptarr_get_config_downloadclient_id` | Get specific config downloadclient. |
| `chaptarr_get_config_host` | Get config host. |
| `chaptarr_get_config_host_id` | Get specific config host. |
| `chaptarr_get_config_indexer` | Get config indexer. |
| `chaptarr_get_config_indexer_id` | Get specific config indexer. |
| `chaptarr_get_config_mediamanagement` | Get config mediamanagement. |
| `chaptarr_get_config_mediamanagement_id` | Get specific config mediamanagement. |
| `chaptarr_get_config_metadataprovider` | Get config metadataprovider. |
| `chaptarr_get_config_metadataprovider_id` | Get specific config metadataprovider. |
| `chaptarr_get_config_naming` | Get config naming. |
| `chaptarr_get_config_naming_examples` | Get config naming examples. |
| `chaptarr_get_config_naming_id` | Get specific config naming. |
| `chaptarr_get_config_ui` | Get config ui. |
| `chaptarr_get_config_ui_id` | Get specific config ui. |
| `chaptarr_get_content_path` | Get content path. |
| `chaptarr_get_customfilter` | Get customfilter. |
| `chaptarr_get_customfilter_id` | Get specific customfilter. |
| `chaptarr_get_customformat` | Get customformat. |
| `chaptarr_get_customformat_id` | Get specific customformat. |
| `chaptarr_get_customformat_schema` | Get customformat schema. |
| `chaptarr_get_delayprofile` | Get delayprofile. |
| `chaptarr_get_delayprofile_id` | Get specific delayprofile. |
| `chaptarr_get_diskspace` | Get diskspace. |
| `chaptarr_get_downloadclient` | Get downloadclient. |
| `chaptarr_get_downloadclient_id` | Get specific downloadclient. |
| `chaptarr_get_downloadclient_schema` | Get downloadclient schema. |
| `chaptarr_get_edition` | Get edition. |
| `chaptarr_get_feed_v1_calendar_readarrics` | Get feed v1 calendar readarrics. |
| `chaptarr_get_filesystem` | Get filesystem. |
| `chaptarr_get_filesystem_mediafiles` | Get filesystem mediafiles. |
| `chaptarr_get_filesystem_type` | Get filesystem type. |
| `chaptarr_get_health` | Get health. |
| `chaptarr_get_history` | Get history. |
| `chaptarr_get_history_author` | Get history author. |
| `chaptarr_get_history_since` | Get history since. |
| `chaptarr_get_importlist` | Get importlist. |
| `chaptarr_get_importlist_id` | Get specific importlist. |
| `chaptarr_get_importlist_schema` | Get importlist schema. |
| `chaptarr_get_importlistexclusion` | Get importlistexclusion. |
| `chaptarr_get_importlistexclusion_id` | Get specific importlistexclusion. |
| `chaptarr_get_indexer` | Get indexer. |
| `chaptarr_get_indexer_id` | Get specific indexer. |
| `chaptarr_get_indexer_schema` | Get indexer schema. |
| `chaptarr_get_indexerflag` | Get indexerflag. |
| `chaptarr_get_language` | Get language. |
| `chaptarr_get_language_id` | Get specific language. |
| `chaptarr_get_localization` | Get localization. |
| `chaptarr_get_log` | Get log. |
| `chaptarr_get_log_file` | Get log file. |
| `chaptarr_get_log_file_filename` | Get log file filename. |
| `chaptarr_get_log_file_update` | Get log file update. |
| `chaptarr_get_log_file_update_filename` | Get log file update filename. |
| `chaptarr_get_login` | Get the login status or page. |
| `chaptarr_get_logout` | Log out from the Chaptarr instance. |
| `chaptarr_get_manualimport` | Get manualimport. |
| `chaptarr_get_mediacover_author_author_id_filename` | Get specific mediacover author author filename. |
| `chaptarr_get_mediacover_book_book_id_filename` | Get specific mediacover book book filename. |
| `chaptarr_get_metadata` | Get metadata. |
| `chaptarr_get_metadata_id` | Get specific metadata. |
| `chaptarr_get_metadata_schema` | Get metadata schema. |
| `chaptarr_get_metadataprofile` | Get metadataprofile. |
| `chaptarr_get_metadataprofile_id` | Get specific metadataprofile. |
| `chaptarr_get_metadataprofile_schema` | Get metadataprofile schema. |
| `chaptarr_get_notification` | Get notification. |
| `chaptarr_get_notification_id` | Get specific notification. |
| `chaptarr_get_notification_schema` | Get notification schema. |
| `chaptarr_get_parse` | Get parse. |
| `chaptarr_get_path` | Get path. |
| `chaptarr_get_ping` | Get ping. |
| `chaptarr_get_qualitydefinition` | Get qualitydefinition. |
| `chaptarr_get_qualitydefinition_id` | Get specific qualitydefinition. |
| `chaptarr_get_qualityprofile` | Get qualityprofile. |
| `chaptarr_get_qualityprofile_id` | Get specific qualityprofile. |
| `chaptarr_get_qualityprofile_schema` | Get qualityprofile schema. |
| `chaptarr_get_queue` | Get queue. |
| `chaptarr_get_queue_details` | Get queue details. |
| `chaptarr_get_queue_status` | Get queue status. |
| `chaptarr_get_release` | Get release. |
| `chaptarr_get_releaseprofile` | Get releaseprofile. |
| `chaptarr_get_releaseprofile_id` | Get specific releaseprofile. |
| `chaptarr_get_remotepathmapping` | Get remotepathmapping. |
| `chaptarr_get_remotepathmapping_id` | Get specific remotepathmapping. |
| `chaptarr_get_rename` | Get rename. |
| `chaptarr_get_retag` | Get retag. |
| `chaptarr_get_rootfolder` | Get rootfolder. |
| `chaptarr_get_rootfolder_id` | Get specific rootfolder. |
| `chaptarr_get_search` | Get search. |
| `chaptarr_get_series` | Get series. |
| `chaptarr_get_system_backup` | Get system backup. |
| `chaptarr_get_system_routes` | Get system routes. |
| `chaptarr_get_system_routes_duplicate` | Get system routes duplicate. |
| `chaptarr_get_system_status` | Get system status. |
| `chaptarr_get_system_task` | Get system task. |
| `chaptarr_get_system_task_id` | Get specific system task. |
| `chaptarr_get_tag` | Get tag. |
| `chaptarr_get_tag_detail` | Get tag detail. |
| `chaptarr_get_tag_detail_id` | Get specific tag detail. |
| `chaptarr_get_tag_id` | Get specific tag. |
| `chaptarr_get_update` | Get update. |
| `chaptarr_get_wanted_cutoff` | Get wanted cutoff. |
| `chaptarr_get_wanted_cutoff_id` | Get specific wanted cutoff. |
| `chaptarr_get_wanted_missing` | Get wanted missing. |
| `chaptarr_get_wanted_missing_id` | Get specific wanted missing. |
| `chaptarr_post_author` | Add a new author. |
| `chaptarr_post_book` | Add a new book. |
| `chaptarr_post_bookshelf` | Add a new bookshelf. |
| `chaptarr_post_command` | Add a new command. |
| `chaptarr_post_customfilter` | Add a new customfilter. |
| `chaptarr_post_customformat` | Add a new customformat. |
| `chaptarr_post_delayprofile` | Add a new delayprofile. |
| `chaptarr_post_downloadclient` | Add a new downloadclient. |
| `chaptarr_post_downloadclient_action_name` | Add a new downloadclient action name. |
| `chaptarr_post_downloadclient_test` | Test downloadclient. |
| `chaptarr_post_downloadclient_testall` | Add a new downloadclient testall. |
| `chaptarr_post_history_failed_id` | Add a new history failed id. |
| `chaptarr_post_importlist` | Add a new importlist. |
| `chaptarr_post_importlist_action_name` | Add a new importlist action name. |
| `chaptarr_post_importlist_test` | Test importlist. |
| `chaptarr_post_importlist_testall` | Add a new importlist testall. |
| `chaptarr_post_importlistexclusion` | Add a new importlistexclusion. |
| `chaptarr_post_indexer` | Add a new indexer. |
| `chaptarr_post_indexer_action_name` | Add a new indexer action name. |
| `chaptarr_post_indexer_test` | Test indexer. |
| `chaptarr_post_indexer_testall` | Add a new indexer testall. |
| `chaptarr_post_login` | Log in to the Chaptarr instance. |
| `chaptarr_post_manualimport` | Add a new manualimport. |
| `chaptarr_post_metadata` | Add a new metadata. |
| `chaptarr_post_metadata_action_name` | Add a new metadata action name. |
| `chaptarr_post_metadata_test` | Test metadata. |
| `chaptarr_post_metadata_testall` | Add a new metadata testall. |
| `chaptarr_post_metadataprofile` | Add a new metadataprofile. |
| `chaptarr_post_notification` | Add a new notification. |
| `chaptarr_post_notification_action_name` | Add a new notification action name. |
| `chaptarr_post_notification_test` | Test notification. |
| `chaptarr_post_notification_testall` | Add a new notification testall. |
| `chaptarr_post_qualityprofile` | Add a new qualityprofile. |
| `chaptarr_post_queue_grab_bulk` | Add a new queue grab bulk. |
| `chaptarr_post_queue_grab_id` | Add a new queue grab id. |
| `chaptarr_post_release` | Add a new release. |
| `chaptarr_post_release_push` | Add a new release push. |
| `chaptarr_post_releaseprofile` | Add a new releaseprofile. |
| `chaptarr_post_remotepathmapping` | Add a new remotepathmapping. |
| `chaptarr_post_rootfolder` | Add a new rootfolder. |
| `chaptarr_post_system_backup_restore_id` | Add a new system backup restore id. |
| `chaptarr_post_system_backup_restore_upload` | Add a new system backup restore upload. |
| `chaptarr_post_system_restart` | Add a new system restart. |
| `chaptarr_post_system_shutdown` | Add a new system shutdown. |
| `chaptarr_post_tag` | Add a new tag. |
| `chaptarr_put_author_editor` | Update author editor. |
| `chaptarr_put_author_id` | Update an existing author by ID. |
| `chaptarr_put_book_editor` | Update book editor. |
| `chaptarr_put_book_id` | Update book id. |
| `chaptarr_put_book_monitor` | Update book monitor. |
| `chaptarr_put_bookfile_editor` | Update bookfile editor. |
| `chaptarr_put_bookfile_id` | Update bookfile id. |
| `chaptarr_put_config_development_id` | Update config development id. |
| `chaptarr_put_config_downloadclient_id` | Update config downloadclient id. |
| `chaptarr_put_config_host_id` | Update config host id. |
| `chaptarr_put_config_indexer_id` | Update config indexer id. |
| `chaptarr_put_config_mediamanagement_id` | Update config mediamanagement id. |
| `chaptarr_put_config_metadataprovider_id` | Update config metadataprovider id. |
| `chaptarr_put_config_naming_id` | Update config naming id. |
| `chaptarr_put_config_ui_id` | Update config ui id. |
| `chaptarr_put_customfilter_id` | Update customfilter id. |
| `chaptarr_put_customformat_id` | Update customformat id. |
| `chaptarr_put_delayprofile_id` | Update delayprofile id. |
| `chaptarr_put_delayprofile_reorder_id` | Update delayprofile reorder id. |
| `chaptarr_put_downloadclient_bulk` | Update downloadclient bulk. |
| `chaptarr_put_downloadclient_id` | Update downloadclient id. |
| `chaptarr_put_importlist_bulk` | Update importlist bulk. |
| `chaptarr_put_importlist_id` | Update importlist id. |
| `chaptarr_put_importlistexclusion_id` | Update importlistexclusion id. |
| `chaptarr_put_indexer_bulk` | Update indexer bulk. |
| `chaptarr_put_indexer_id` | Update indexer id. |
| `chaptarr_put_metadata_id` | Update metadata id. |
| `chaptarr_put_metadataprofile_id` | Update metadataprofile id. |
| `chaptarr_put_notification_id` | Update notification id. |
| `chaptarr_put_qualitydefinition_id` | Update qualitydefinition id. |
| `chaptarr_put_qualitydefinition_update` | Update qualitydefinition update. |
| `chaptarr_put_qualityprofile_id` | Update qualityprofile id. |
| `chaptarr_put_releaseprofile_id` | Update releaseprofile id. |
| `chaptarr_put_remotepathmapping_id` | Update remotepathmapping id. |
| `chaptarr_put_rootfolder_id` | Update rootfolder id. |
| `chaptarr_put_tag_id` | Update tag id. |

</details>

<details>
<summary>Prowlarr (indexers): 129 tools</summary>

| MCP Tool | Description |
|---|---|
| `prowlarr_delete_applications_bulk` | Delete applications bulk. |
| `prowlarr_delete_applications_id` | Delete an application configuration. |
| `prowlarr_delete_appprofile_id` | Delete appprofile id. |
| `prowlarr_delete_command_id` | Delete command id. |
| `prowlarr_delete_customfilter_id` | Delete customfilter id. |
| `prowlarr_delete_downloadclient_bulk` | Delete downloadclient bulk. |
| `prowlarr_delete_downloadclient_id` | Delete downloadclient id. |
| `prowlarr_delete_indexer_bulk` | Delete indexer bulk. |
| `prowlarr_delete_indexer_id` | Delete indexer id. |
| `prowlarr_delete_indexerproxy_id` | Delete indexerproxy id. |
| `prowlarr_delete_notification_id` | Delete notification id. |
| `prowlarr_delete_system_backup_id` | Delete system backup id. |
| `prowlarr_delete_tag_id` | Delete tag id. |
| `prowlarr_get_` | Get . |
| `prowlarr_get_api` | Get the base API information. |
| `prowlarr_get_applications` | Get all applications managed by Prowlarr. |
| `prowlarr_get_applications_id` | Get details for a specific application by ID. |
| `prowlarr_get_applications_schema` | Get applications schema. |
| `prowlarr_get_appprofile` | Get appprofile. |
| `prowlarr_get_appprofile_id` | Get specific appprofile. |
| `prowlarr_get_appprofile_schema` | Get appprofile schema. |
| `prowlarr_get_command` | Get command. |
| `prowlarr_get_command_id` | Get specific command. |
| `prowlarr_get_config_development` | Get config development. |
| `prowlarr_get_config_development_id` | Get specific config development. |
| `prowlarr_get_config_downloadclient` | Get config downloadclient. |
| `prowlarr_get_config_downloadclient_id` | Get specific config downloadclient. |
| `prowlarr_get_config_host` | Get config host. |
| `prowlarr_get_config_host_id` | Get specific config host. |
| `prowlarr_get_config_ui` | Get config ui. |
| `prowlarr_get_config_ui_id` | Get specific config ui. |
| `prowlarr_get_content_path` | Get content path. |
| `prowlarr_get_customfilter` | Get customfilter. |
| `prowlarr_get_customfilter_id` | Get specific customfilter. |
| `prowlarr_get_downloadclient` | Get downloadclient. |
| `prowlarr_get_downloadclient_id` | Get specific downloadclient. |
| `prowlarr_get_downloadclient_schema` | Get downloadclient schema. |
| `prowlarr_get_filesystem` | Get filesystem. |
| `prowlarr_get_filesystem_type` | Get filesystem type. |
| `prowlarr_get_health` | Get health. |
| `prowlarr_get_history` | Get history. |
| `prowlarr_get_history_indexer` | Get history indexer. |
| `prowlarr_get_history_since` | Get history since. |
| `prowlarr_get_id_api` | Get results for a specific indexer endpoint in Newznab format. |
| `prowlarr_get_id_download` | Get specific id download. |
| `prowlarr_get_indexer` | Get indexer. |
| `prowlarr_get_indexer_categories` | Get indexer categories. |
| `prowlarr_get_indexer_id` | Get specific indexer. |
| `prowlarr_get_indexer_id_download` | Download a release from a specific indexer. |
| `prowlarr_get_indexer_id_newznab` | Get specific indexer newznab. |
| `prowlarr_get_indexer_schema` | Get indexer schema. |
| `prowlarr_get_indexerproxy` | Get indexerproxy. |
| `prowlarr_get_indexerproxy_id` | Get specific indexerproxy. |
| `prowlarr_get_indexerproxy_schema` | Get indexerproxy schema. |
| `prowlarr_get_indexerstats` | Get indexerstats. |
| `prowlarr_get_indexerstatus` | Get indexerstatus. |
| `prowlarr_get_localization` | Get localization. |
| `prowlarr_get_localization_options` | Get localization options. |
| `prowlarr_get_log` | Get log. |
| `prowlarr_get_log_file` | Get log file. |
| `prowlarr_get_log_file_filename` | Get log file filename. |
| `prowlarr_get_log_file_update` | Get log file update. |
| `prowlarr_get_log_file_update_filename` | Get log file update filename. |
| `prowlarr_get_login` | Get login. |
| `prowlarr_get_logout` | Get logout. |
| `prowlarr_get_notification` | Get all configured notifications. |
| `prowlarr_get_notification_id` | Get specific notification. |
| `prowlarr_get_notification_schema` | Get notification schema. |
| `prowlarr_get_path` | Get path. |
| `prowlarr_get_ping` | Ping the Prowlarr API to check connectivity. |
| `prowlarr_get_search` | Get search. |
| `prowlarr_get_system_backup` | Get system backup. |
| `prowlarr_get_system_routes` | Get system routes. |
| `prowlarr_get_system_routes_duplicate` | Get system routes duplicate. |
| `prowlarr_get_system_status` | Get system status. |
| `prowlarr_get_system_task` | Get system task. |
| `prowlarr_get_system_task_id` | Get specific system task. |
| `prowlarr_get_tag` | Get tag. |
| `prowlarr_get_tag_detail` | Get tag detail. |
| `prowlarr_get_tag_detail_id` | Get specific tag detail. |
| `prowlarr_get_tag_id` | Get specific tag. |
| `prowlarr_get_update` | Get update. |
| `prowlarr_post_applications` | Add a new applications. |
| `prowlarr_post_applications_action_name` | Add a new applications action name. |
| `prowlarr_post_applications_test` | Test applications. |
| `prowlarr_post_applications_testall` | Add a new applications testall. |
| `prowlarr_post_appprofile` | Add a new appprofile. |
| `prowlarr_post_command` | Add a new command. |
| `prowlarr_post_customfilter` | Add a new customfilter. |
| `prowlarr_post_downloadclient` | Add a new downloadclient. |
| `prowlarr_post_downloadclient_action_name` | Add a new downloadclient action name. |
| `prowlarr_post_downloadclient_test` | Test downloadclient. |
| `prowlarr_post_downloadclient_testall` | Add a new downloadclient testall. |
| `prowlarr_post_indexer` | Add a new indexer. |
| `prowlarr_post_indexer_action_name` | Add a new indexer action name. |
| `prowlarr_post_indexer_test` | Test indexer. |
| `prowlarr_post_indexer_testall` | Add a new indexer testall. |
| `prowlarr_post_indexerproxy` | Add a new indexerproxy. |
| `prowlarr_post_indexerproxy_action_name` | Add a new indexerproxy action name. |
| `prowlarr_post_indexerproxy_test` | Test indexerproxy. |
| `prowlarr_post_indexerproxy_testall` | Add a new indexerproxy testall. |
| `prowlarr_post_login` | Add a new login. |
| `prowlarr_post_notification` | Add a new notification. |
| `prowlarr_post_notification_action_name` | Add a new notification action name. |
| `prowlarr_post_notification_test` | Test notification. |
| `prowlarr_post_notification_testall` | Add a new notification testall. |
| `prowlarr_post_search` | Perform a bulk search across multiple indexers. |
| `prowlarr_post_search_bulk` | Add a new search bulk. |
| `prowlarr_post_system_backup_restore_id` | Add a new system backup restore id. |
| `prowlarr_post_system_backup_restore_upload` | Add a new system backup restore upload. |
| `prowlarr_post_system_restart` | Add a new system restart. |
| `prowlarr_post_system_shutdown` | Add a new system shutdown. |
| `prowlarr_post_tag` | Add a new tag. |
| `prowlarr_put_applications_bulk` | Update applications bulk. |
| `prowlarr_put_applications_id` | Update an existing application configuration. |
| `prowlarr_put_appprofile_id` | Update appprofile id. |
| `prowlarr_put_config_development_id` | Update config development id. |
| `prowlarr_put_config_downloadclient_id` | Update config downloadclient id. |
| `prowlarr_put_config_host_id` | Update config host id. |
| `prowlarr_put_config_ui_id` | Update config ui id. |
| `prowlarr_put_customfilter_id` | Update customfilter id. |
| `prowlarr_put_downloadclient_bulk` | Update downloadclient bulk. |
| `prowlarr_put_downloadclient_id` | Update downloadclient id. |
| `prowlarr_put_indexer_bulk` | Update indexer bulk. |
| `prowlarr_put_indexer_id` | Update indexer id. |
| `prowlarr_put_indexerproxy_id` | Update indexerproxy id. |
| `prowlarr_put_notification_id` | Update notification id. |
| `prowlarr_put_tag_id` | Update tag id. |
| `prowlarr_search` | Search for indexers using the search endpoint. |

</details>

<details>
<summary>Bazarr (subtitles): 84 tools</summary>

| MCP Tool | Description |
|---|---|
| `bazarr_delete_episodes_blacklist` | Delete an episodes subtitles from blacklist |
| `bazarr_delete_episodes_subtitles` | Delete an episode subtitles |
| `bazarr_delete_movies_blacklist` | Delete a movies subtitles from blacklist |
| `bazarr_delete_movies_subtitles` | Delete a movie subtitles |
| `bazarr_delete_system_backups` | Delete a backup file |
| `bazarr_delete_system_jobs` | Delete a job from the queue |
| `bazarr_delete_system_logs` | Force log rotation and create a new log file |
| `bazarr_get_badges` | Get badges count to update the UI |
| `bazarr_get_browse_bazarr_fs` | List Bazarr file system content |
| `bazarr_get_browse_radarr_fs` | List Radarr file system content |
| `bazarr_get_browse_sonarr_fs` | List Sonarr file system content |
| `bazarr_get_episodes` | List episodes metadata for specific series or episodes |
| `bazarr_get_episodes_blacklist` | List blacklisted episodes subtitles |
| `bazarr_get_episodes_history` | List episodes history events |
| `bazarr_get_episodes_wanted` | List episodes wanted subtitles |
| `bazarr_get_history_stats` | Get history statistics |
| `bazarr_get_jellyfin_libraries` | List available movie and series libraries from the Jellyfin server |
| `bazarr_get_languages` | List languages for history filter or for language filter menu |
| `bazarr_get_languages_profiles` | List languages profiles |
| `bazarr_get_movies` | List movies metadata for specific movies |
| `bazarr_get_movies_blacklist` | List blacklisted movies subtitles |
| `bazarr_get_movies_history` | List movies history events |
| `bazarr_get_movies_tags` | List all distinct tags assigned to any movie |
| `bazarr_get_movies_wanted` | List movies wanted subtitles |
| `bazarr_get_plex_autopulse_config` | get /plex/autopulse/config |
| `bazarr_get_plex_libraries` | get /plex/oauth/libraries |
| `bazarr_get_plex_pin` | get /plex/oauth/pin |
| `bazarr_get_plex_pin_check` | get /plex/oauth/pin/{pin_id}/check |
| `bazarr_get_plex_select_server` | get /plex/select-server |
| `bazarr_get_plex_servers` | get /plex/oauth/servers |
| `bazarr_get_plex_test_connection` | get /plex/test-connection |
| `bazarr_get_plex_validate` | get /plex/oauth/validate |
| `bazarr_get_plex_webhook_list` | get /plex/webhook/list |
| `bazarr_get_provider_episodes` | Search manually for an episode subtitles |
| `bazarr_get_provider_movies` | Search manually for a movie subtitles |
| `bazarr_get_providers` | Get providers status |
| `bazarr_get_searches` | List results from query |
| `bazarr_get_series` | List series metadata for specific series |
| `bazarr_get_series_tags` | List all distinct tags assigned to any series |
| `bazarr_get_subtitle_name_contents` | Retrieve subtitle file contents |
| `bazarr_get_subtitle_name_info` | Guessit over subtitles filename |
| `bazarr_get_subtitles` | Return available audio and embedded subtitles tracks with external subtitles |
| `bazarr_get_system_announcements` | List announcements relative to Bazarr |
| `bazarr_get_system_backups` | List backup files |
| `bazarr_get_system_health` | List health issues |
| `bazarr_get_system_jobs` | List jobs from the queue |
| `bazarr_get_system_logs` | List log entries |
| `bazarr_get_system_ping` | Return status and http 200 |
| `bazarr_get_system_releases` | Get Bazarr releases |
| `bazarr_get_system_status` | Return environment information and versions |
| `bazarr_get_system_tasks` | List tasks |
| `bazarr_patch_episodes_subtitles` | Download an episode subtitles |
| `bazarr_patch_movies` | Run actions on specific movies |
| `bazarr_patch_movies_subtitles` | Download a movie subtitles |
| `bazarr_patch_series` | Run actions on specific series |
| `bazarr_patch_subtitles` | Apply mods/tools on external subtitles |
| `bazarr_patch_system_backups` | Restore a backup file |
| `bazarr_patch_system_jobs` | Empty a specific jobs queue |
| `bazarr_post_episodes_blacklist` | Add an episodes subtitles to blacklist |
| `bazarr_post_episodes_subtitles` | Upload an episode subtitles |
| `bazarr_post_jellyfin_test_connection` | Test connection to a Jellyfin server with provided credentials |
| `bazarr_post_movies` | Update specific movies languages profile |
| `bazarr_post_movies_blacklist` | Add a movies subtitles to blacklist |
| `bazarr_post_movies_subtitles` | Upload a movie subtitles |
| `bazarr_post_plex_api_key` | post /plex/apikey |
| `bazarr_post_plex_encrypt_api_key` | post /plex/encrypt-apikey |
| `bazarr_post_plex_logout` | post /plex/oauth/logout |
| `bazarr_post_plex_pin` | post /plex/oauth/pin |
| `bazarr_post_plex_select_server` | post /plex/select-server |
| `bazarr_post_plex_test_connection` | post /plex/test-connection |
| `bazarr_post_plex_webhook_create` | post /plex/webhook/create |
| `bazarr_post_plex_webhook_delete` | post /plex/webhook/delete |
| `bazarr_post_provider_episodes` | Manually download an episode subtitles |
| `bazarr_post_provider_movies` | Manually download a movie subtitles |
| `bazarr_post_providers` | Reset providers status |
| `bazarr_post_series` | Update specific series languages profile |
| `bazarr_post_system_announcements` | Mark announcement as dismissed |
| `bazarr_post_system_backups` | Create a new backup |
| `bazarr_post_system_jobs` | Force start, move to top or move to bottom of the queue a specific job |
| `bazarr_post_system_tasks` | Run task |
| `bazarr_post_system_webhook_test` | Test external webhook connection |
| `bazarr_post_web_hooks_plex` | Trigger subtitles search on play media event in Plex |
| `bazarr_post_web_hooks_radarr` | Search for missing subtitles based on Radarr webhooks |
| `bazarr_post_web_hooks_sonarr` | Search for missing subtitles based on Sonarr webhooks |

</details>

<details>
<summary>Seerr (requests): 217 tools</summary>

| MCP Tool | Description |
|---|---|
| `seerr_delete_blacklist_tmdb_id` | Remove media from blocklist |
| `seerr_delete_blocklist_collection_id` | Remove collection from blocklist |
| `seerr_delete_blocklist_tmdb_id` | Remove media from blocklist |
| `seerr_delete_issue_comment_comment_id` | Delete issue comment |
| `seerr_delete_issue_id` | Delete issue |
| `seerr_delete_media_id` | Delete media item |
| `seerr_delete_media_id_file` | Delete media file |
| `seerr_delete_override_rule_rule_id` | Delete override rule by ID |
| `seerr_delete_request_id` | Delete request |
| `seerr_delete_settings_discover_slider_id` | Delete slider by ID |
| `seerr_delete_settings_radarr_id` | Delete Radarr instance |
| `seerr_delete_settings_sonarr_id` | Delete Sonarr instance |
| `seerr_delete_user_id` | Delete user by ID |
| `seerr_delete_user_id_push_subscription_endpoint` | Delete user push subscription by key |
| `seerr_delete_user_id_settings_linked_accounts_jellyfin` | Remove the linked Jellyfin account for a user |
| `seerr_delete_user_id_settings_linked_accounts_plex` | Remove the linked Plex account for a user |
| `seerr_delete_watchlist_tmdb_id` | Delete watchlist item |
| `seerr_get_auth_jellyfin_quickconnect_check` | Check Quick Connect authorization status |
| `seerr_get_auth_me` | Get logged-in user |
| `seerr_get_backdrops` | Get backdrops of trending items |
| `seerr_get_blacklist` | Returns blocklisted items |
| `seerr_get_blacklist_tmdb_id` | Get media from blocklist |
| `seerr_get_blocklist` | Returns blocklisted items |
| `seerr_get_blocklist_tmdb_id` | Get media from blocklist |
| `seerr_get_certifications_movie` | Get movie certifications |
| `seerr_get_certifications_tv` | Get TV certifications |
| `seerr_get_collection_id` | Get collection details |
| `seerr_get_discover_genreslider_movie` | Get genre slider data for movies |
| `seerr_get_discover_genreslider_tv` | Get genre slider data for TV series |
| `seerr_get_discover_keyword_id_movies` | Get movies from keyword |
| `seerr_get_discover_movies` | Discover movies |
| `seerr_get_discover_movies_genre_id` | Discover movies by genre |
| `seerr_get_discover_movies_language_language` | Discover movies by original language |
| `seerr_get_discover_movies_studio_id` | Discover movies by studio |
| `seerr_get_discover_movies_upcoming` | Upcoming movies |
| `seerr_get_discover_trending` | Trending movies and TV |
| `seerr_get_discover_tv` | Discover TV shows |
| `seerr_get_discover_tv_genre_id` | Discover TV shows by genre |
| `seerr_get_discover_tv_language_language` | Discover TV shows by original language |
| `seerr_get_discover_tv_network_id` | Discover TV shows by network |
| `seerr_get_discover_tv_upcoming` | Discover Upcoming TV shows |
| `seerr_get_discover_watchlist` | Get the Plex watchlist. |
| `seerr_get_genres_movie` | Get list of official TMDB movie genres |
| `seerr_get_genres_tv` | Get list of official TMDB movie genres |
| `seerr_get_issue` | Get all issues |
| `seerr_get_issue_comment_comment_id` | Get issue comment |
| `seerr_get_issue_count` | Gets issue counts |
| `seerr_get_issue_id` | Get issue |
| `seerr_get_keyword_id` | Get keyword |
| `seerr_get_languages` | Languages supported by TMDB |
| `seerr_get_media` | Get media |
| `seerr_get_media_id_watch_data` | Get watch data |
| `seerr_get_movie_id` | Get movie details |
| `seerr_get_movie_id_ratings` | Get movie ratings |
| `seerr_get_movie_id_ratingscombined` | Get RT and IMDB movie ratings combined |
| `seerr_get_movie_id_recommendations` | Get recommended movies |
| `seerr_get_movie_id_similar` | Get similar movies |
| `seerr_get_network_id` | Get TV network details |
| `seerr_get_override_rule` | Get override rules |
| `seerr_get_person_id` | Get person details |
| `seerr_get_person_id_combined_credits` | Get combined credits |
| `seerr_get_regions` | Regions supported by TMDB |
| `seerr_get_request` | Get all requests |
| `seerr_get_request_count` | Gets request counts |
| `seerr_get_request_id` | Get MediaRequest |
| `seerr_get_search` | Search for movies, TV shows, or people |
| `seerr_get_search_company` | Search for companies |
| `seerr_get_search_keyword` | Search for keywords |
| `seerr_get_service_radarr` | Get non-sensitive Radarr server list |
| `seerr_get_service_radarr_id` | Get Radarr server quality profiles and root folders |
| `seerr_get_service_sonarr` | Get non-sensitive Sonarr server list |
| `seerr_get_service_sonarr_id` | Get Sonarr server quality profiles and root folders |
| `seerr_get_service_sonarr_lookup_tmdb_id` | Get series from Sonarr |
| `seerr_get_settings_about` | Get server stats |
| `seerr_get_settings_cache` | Get a list of active caches |
| `seerr_get_settings_discover` | Get all discover sliders |
| `seerr_get_settings_discover_reset` | Reset all discover sliders |
| `seerr_get_settings_jellyfin` | Get Jellyfin settings |
| `seerr_get_settings_jellyfin_library` | Get Jellyfin libraries |
| `seerr_get_settings_jellyfin_sync` | Get status of full Jellyfin library sync |
| `seerr_get_settings_jellyfin_users` | Get Jellyfin Users |
| `seerr_get_settings_jobs` | Get scheduled jobs |
| `seerr_get_settings_logs` | Returns logs |
| `seerr_get_settings_main` | Get main settings |
| `seerr_get_settings_metadatas` | Get Metadata settings |
| `seerr_get_settings_network` | Get network settings |
| `seerr_get_settings_notifications_discord` | Get Discord notification settings |
| `seerr_get_settings_notifications_email` | Get email notification settings |
| `seerr_get_settings_notifications_gotify` | Get Gotify notification settings |
| `seerr_get_settings_notifications_ntfy` | Get ntfy.sh notification settings |
| `seerr_get_settings_notifications_pushbullet` | Get Pushbullet notification settings |
| `seerr_get_settings_notifications_pushover` | Get Pushover notification settings |
| `seerr_get_settings_notifications_pushover_sounds` | Get Pushover sounds |
| `seerr_get_settings_notifications_slack` | Get Slack notification settings |
| `seerr_get_settings_notifications_telegram` | Get Telegram notification settings |
| `seerr_get_settings_notifications_webhook` | Get webhook notification settings |
| `seerr_get_settings_notifications_webpush` | Get Web Push notification settings |
| `seerr_get_settings_plex` | Get Plex settings |
| `seerr_get_settings_plex_devices_servers` | Gets the user's available Plex servers |
| `seerr_get_settings_plex_library` | Get Plex libraries |
| `seerr_get_settings_plex_sync` | Get status of full Plex library scan |
| `seerr_get_settings_plex_users` | Get Plex users |
| `seerr_get_settings_public` | Get public settings |
| `seerr_get_settings_radarr` | Get Radarr settings |
| `seerr_get_settings_radarr_id_profiles` | Get available Radarr profiles |
| `seerr_get_settings_sonarr` | Get Sonarr settings |
| `seerr_get_settings_tautulli` | Get Tautulli settings |
| `seerr_get_status` | Get Seerr status |
| `seerr_get_status_appdata` | Get application data volume status |
| `seerr_get_studio_id` | Get movie studio details |
| `seerr_get_tv_id` | Get TV details |
| `seerr_get_tv_id_ratings` | Get TV ratings |
| `seerr_get_tv_id_recommendations` | Get recommended TV series |
| `seerr_get_tv_id_season_number` | Get season details and episode list |
| `seerr_get_tv_id_similar` | Get similar TV series |
| `seerr_get_user` | Get all users |
| `seerr_get_user_id` | Get user by ID |
| `seerr_get_user_id_push_subscription_endpoint` | Get web push notification settings for a user |
| `seerr_get_user_id_push_subscriptions` | Get all web push notification settings for a user |
| `seerr_get_user_id_quota` | Get quotas for a specific user |
| `seerr_get_user_id_requests` | Get requests for a specific user |
| `seerr_get_user_id_settings_main` | Get general settings for a user |
| `seerr_get_user_id_settings_notifications` | Get notification settings for a user |
| `seerr_get_user_id_settings_password` | Get password page information |
| `seerr_get_user_id_settings_permissions` | Get permission settings for a user |
| `seerr_get_user_id_watch_data` | Get watch data |
| `seerr_get_user_id_watchlist` | Get the Plex watchlist for a specific user |
| `seerr_get_user_jellyfin_user_id` | Get user by Jellyfin user ID |
| `seerr_get_watchproviders_movies` | Get watch provider movies |
| `seerr_get_watchproviders_regions` | Get watch provider regions |
| `seerr_get_watchproviders_tv` | Get watch provider series |
| `seerr_post_auth_jellyfin` | Sign in using a Jellyfin username and password |
| `seerr_post_auth_jellyfin_quickconnect_authenticate` | Authenticate with Quick Connect |
| `seerr_post_auth_jellyfin_quickconnect_initiate` | Initiate Jellyfin Quick Connect |
| `seerr_post_auth_local` | Sign in using a local account |
| `seerr_post_auth_logout` | Sign out and clear session cookie |
| `seerr_post_auth_plex` | Sign in using a Plex token |
| `seerr_post_auth_reset_password` | Send a reset password email |
| `seerr_post_auth_reset_password_guid` | Reset the password for a user |
| `seerr_post_blacklist` | Add media to blocklist |
| `seerr_post_blocklist` | Add media to blocklist |
| `seerr_post_blocklist_collection_id` | Add collection to blocklist |
| `seerr_post_issue` | Create new issue |
| `seerr_post_issue_id_comment` | Create a comment |
| `seerr_post_issue_id_status` | Update an issue's status |
| `seerr_post_media_id_status` | Update media status |
| `seerr_post_override_rule` | Create override rule |
| `seerr_post_override_rule_advanced_request` | Advanced override rule request |
| `seerr_post_request` | Create new request |
| `seerr_post_request_id_retry` | Retry failed request |
| `seerr_post_request_id_status` | Update a request's status |
| `seerr_post_settings_cache_dns_entry_flush` | Flush a specific DNS cache entry |
| `seerr_post_settings_cache_id_flush` | Flush a specific cache |
| `seerr_post_settings_discover` | Batch update all sliders. |
| `seerr_post_settings_discover_add` | Add a new slider |
| `seerr_post_settings_initialize` | Initialize application |
| `seerr_post_settings_jellyfin` | Update Jellyfin settings |
| `seerr_post_settings_jellyfin_library_sync` | Sync Jellyfin libraries |
| `seerr_post_settings_jellyfin_sync` | Start full Jellyfin library sync |
| `seerr_post_settings_jobs_job_id_cancel` | Cancel a specific job |
| `seerr_post_settings_jobs_job_id_run` | Invoke a specific job |
| `seerr_post_settings_jobs_job_id_schedule` | Modify job schedule |
| `seerr_post_settings_main` | Update main settings |
| `seerr_post_settings_main_regenerate` | Get main settings with newly-generated API key |
| `seerr_post_settings_metadatas_test` | Test Provider configuration |
| `seerr_post_settings_network` | Update network settings |
| `seerr_post_settings_notifications_discord` | Update Discord notification settings |
| `seerr_post_settings_notifications_discord_test` | Test Discord settings |
| `seerr_post_settings_notifications_email` | Update email notification settings |
| `seerr_post_settings_notifications_email_test` | Test email settings |
| `seerr_post_settings_notifications_gotify` | Update Gotify notification settings |
| `seerr_post_settings_notifications_gotify_test` | Test Gotify settings |
| `seerr_post_settings_notifications_ntfy` | Update ntfy.sh notification settings |
| `seerr_post_settings_notifications_ntfy_test` | Test ntfy.sh settings |
| `seerr_post_settings_notifications_pushbullet` | Update Pushbullet notification settings |
| `seerr_post_settings_notifications_pushbullet_test` | Test Pushbullet settings |
| `seerr_post_settings_notifications_pushover` | Update Pushover notification settings |
| `seerr_post_settings_notifications_pushover_test` | Test Pushover settings |
| `seerr_post_settings_notifications_slack` | Update Slack notification settings |
| `seerr_post_settings_notifications_slack_test` | Test Slack settings |
| `seerr_post_settings_notifications_telegram` | Update Telegram notification settings |
| `seerr_post_settings_notifications_telegram_test` | Test Telegram settings |
| `seerr_post_settings_notifications_webhook` | Update webhook notification settings |
| `seerr_post_settings_notifications_webhook_test` | Test webhook settings |
| `seerr_post_settings_notifications_webpush` | Update Web Push notification settings |
| `seerr_post_settings_notifications_webpush_test` | Test Web Push settings |
| `seerr_post_settings_plex` | Update Plex settings |
| `seerr_post_settings_plex_library_sync` | Sync Plex libraries |
| `seerr_post_settings_plex_sync` | Start full Plex library scan |
| `seerr_post_settings_radarr` | Create Radarr instance |
| `seerr_post_settings_radarr_test` | Test Radarr configuration |
| `seerr_post_settings_sonarr` | Create Sonarr instance |
| `seerr_post_settings_sonarr_test` | Test Sonarr configuration |
| `seerr_post_settings_tautulli` | Update Tautulli settings |
| `seerr_post_user` | Create new user |
| `seerr_post_user_id_settings_linked_accounts_jellyfin` | Link the provided Jellyfin account to the current user |
| `seerr_post_user_id_settings_linked_accounts_jellyfin_quickconnect` | Link Jellyfin/Emby account with Quick Connect |
| `seerr_post_user_id_settings_linked_accounts_plex` | Link the provided Plex account to the current user |
| `seerr_post_user_id_settings_main` | Update general settings for a user |
| `seerr_post_user_id_settings_notifications` | Update notification settings for a user |
| `seerr_post_user_id_settings_password` | Update password for a user |
| `seerr_post_user_id_settings_permissions` | Update permission settings for a user |
| `seerr_post_user_import_from_jellyfin` | Import all users from Jellyfin |
| `seerr_post_user_import_from_plex` | Import all users from Plex |
| `seerr_post_user_register_push_subscription` | Register a web push /user/registerPushSubscription |
| `seerr_post_watchlist` | Add media to watchlist |
| `seerr_put_issue_comment_comment_id` | Update issue comment |
| `seerr_put_override_rule_rule_id` | Update override rule |
| `seerr_put_request_id` | Update MediaRequest |
| `seerr_put_settings_discover_slider_id` | Update a single slider |
| `seerr_put_settings_jellyfin_library_id` | Update a single Jellyfin library |
| `seerr_put_settings_metadatas` | Update Metadata settings |
| `seerr_put_settings_plex_library_id` | Update a single Plex library |
| `seerr_put_settings_radarr_id` | Update Radarr instance |
| `seerr_put_settings_sonarr_id` | Update Sonarr instance |
| `seerr_put_user` | Update batch of users |
| `seerr_put_user_id` | Update a user by user ID |

</details>

_1375 tools in all._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md#mcp-tools](docs/index.md#mcp-tools).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows the operator to restrict the set of exposed tools to prevent blowing up the LLM's context window.

The operator can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to the operator's transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are provided, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `arr-mcp[mcp]` to add
> FastMCP / FastAPI through `scion-sdk`; the required Scion SDK core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "arr-mcp[mcp]",
        "arr-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "BAZARRTOOL": "True",
        "BAZARR_API_KEY": "your_bazarr_api_key_here",
        "BAZARR_BASE_URL": "http://localhost:6767",
        "CHAPTARRTOOL": "True",
        "CHAPTARR_BASE_URL": "http://localhost:8006",
        "CHAPTARR_TOKEN": "your_chaptarr_token_here",
        "LIDARRTOOL": "True",
        "LIDARR_BASE_URL": "http://localhost:8686",
        "LIDARR_TOKEN": "your_lidarr_token_here",
        "PROWLARRTOOL": "True",
        "PROWLARR_BASE_URL": "http://localhost:9696",
        "PROWLARR_TOKEN": "your_prowlarr_token_here",
        "RADARRTOOL": "True",
        "RADARR_BASE_URL": "http://localhost:7878",
        "RADARR_TOKEN": "your_radarr_token_here",
        "SEERRTOOL": "True",
        "SEERR_API_KEY": "your_seerr_api_key_here",
        "SEERR_BASE_URL": "http://localhost:5055",
        "SONARRTOOL": "True",
        "SONARR_BASE_URL": "http://localhost:8989",
        "SONARR_TOKEN": "your_sonarr_token_here"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as Arbora. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "arr-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "arr-mcp[mcp]",
        "arr-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "BAZARRTOOL": "True",
        "BAZARR_API_KEY": "your_bazarr_api_key_here",
        "BAZARR_BASE_URL": "http://localhost:6767",
        "CHAPTARRTOOL": "True",
        "CHAPTARR_BASE_URL": "http://localhost:8006",
        "CHAPTARR_TOKEN": "your_chaptarr_token_here",
        "LIDARRTOOL": "True",
        "LIDARR_BASE_URL": "http://localhost:8686",
        "LIDARR_TOKEN": "your_lidarr_token_here",
        "PROWLARRTOOL": "True",
        "PROWLARR_BASE_URL": "http://localhost:9696",
        "PROWLARR_TOKEN": "your_prowlarr_token_here",
        "RADARRTOOL": "True",
        "RADARR_BASE_URL": "http://localhost:7878",
        "RADARR_TOKEN": "your_radarr_token_here",
        "SEERRTOOL": "True",
        "SEERR_API_KEY": "your_seerr_api_key_here",
        "SEERR_BASE_URL": "http://localhost:5055",
        "SONARRTOOL": "True",
        "SONARR_BASE_URL": "http://localhost:8989",
        "SONARR_TOKEN": "your_sonarr_token_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "url": "http://localhost:8000/arr-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e BAZARRTOOL=True \
  -e BAZARR_API_KEY=your_bazarr_api_key_here \
  -e BAZARR_BASE_URL=http://localhost:6767 \
  -e CHAPTARRTOOL=True \
  -e CHAPTARR_BASE_URL=http://localhost:8006 \
  -e CHAPTARR_TOKEN=your_chaptarr_token_here \
  -e LIDARRTOOL=True \
  -e LIDARR_BASE_URL=http://localhost:8686 \
  -e LIDARR_TOKEN=your_lidarr_token_here \
  -e PROWLARRTOOL=True \
  -e PROWLARR_BASE_URL=http://localhost:9696 \
  -e PROWLARR_TOKEN=your_prowlarr_token_here \
  -e RADARRTOOL=True \
  -e RADARR_BASE_URL=http://localhost:7878 \
  -e RADARR_TOKEN=your_radarr_token_here \
  -e SEERRTOOL=True \
  -e SEERR_API_KEY=your_seerr_api_key_here \
  -e SEERR_BASE_URL=http://localhost:5055 \
  -e SONARRTOOL=True \
  -e SONARR_BASE_URL=http://localhost:8989 \
  -e SONARR_TOKEN=your_sonarr_token_here \
  registry.example.invalid/arr-mcp@sha256:<digest> arr-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`arr-mcp` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/arr-mcp/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

## Agent

# Set credentials
export SONARR_BASE_URL="http://localhost:8989"
export SONARR_TOKEN="your_value"
export RADARR_BASE_URL="http://localhost:7878"
export RADARR_TOKEN="your_value"

# Connector-focused MCP server (includes the shared graph engine)
uv pip install "arr-mcp[mcp]"

# Everything (development)
uv pip install "arr-mcp[all]"      # or: python -m pip install "arr-mcp[all]"
```

### Container images (`:mcp`)

One multi-stage `docker/Dockerfile` builds the MCP-only image (`--target mcp`):

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/arr-mcp:mcp` | `--target mcp` | `arr-mcp[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `arr-mcp` |

```bash
docker build --target mcp   -t example/arr-mcp:mcp    docker/   # connector-focused MCP server
```

agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Scion SDK core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

---

## Usage & Quick Start

To start and run `arr-mcp` services:

### 1. Starting the MCP Server
Start the MCP server in standard `I/O` mode (ideal for IDEs):
```bash
arr-mcp
```

Or start it as a Streamable-HTTP server on port `8000`:
```bash
arr-mcp --transport streamable-http --port 8000
