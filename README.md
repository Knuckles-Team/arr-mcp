# Arr Mcp
## CLI or API | MCP | Agent

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

*Version: 1.0.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, MCP, and
> A2A agent interfaces, and guidance for provisioning the Arr Suite services are
> maintained in the [official documentation](https://knuckles-team.github.io/arr-mcp/).

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [CLI or API](#cli-or-api)
- [MCP](#mcp)
  - [Dynamic Tool Selection & Visibility](#dynamic-tool-selection--visibility)
- [Agent](#agent)
- [Environment Variables](#environment-variables)
- [Security & Governance](#security--governance)
- [Contribute](#contribute)

---

## Overview

**Arr Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Arr Suite MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Arr Suite MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

The table below is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `bazarr_action` | `BAZARRTOOL` | Execute any Bazarr API action. |
| `chaptarr_action` | `CHAPTARRTOOL` | Execute any Chaptarr API action. |
| `lidarr_action` | `LIDARRTOOL` | Execute any Lidarr API action. |
| `prowlarr_action` | `PROWLARRTOOL` | Execute any Prowlarr API action. |
| `radarr_action` | `RADARRTOOL` | Execute any Radarr API action. |
| `seerr_action` | `SEERRTOOL` | Execute any Seerr API action. |
| `sonarr_action` | `SONARRTOOL` | Execute any Sonarr API action. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>1123 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `bazarr_add_to_blacklist` | `APITOOL` | Add a subtitle to blacklist. |
| `bazarr_download_movie_subtitle` | `APITOOL` | Download a subtitle for a movie. |
| `bazarr_download_series_subtitle` | `APITOOL` | Download a subtitle for an episode. |
| `bazarr_get_blacklist` | `APITOOL` | Get blacklisted subtitles. |
| `bazarr_get_enabled_languages` | `APITOOL` | Get currently enabled subtitle languages. |
| `bazarr_get_enabled_providers` | `APITOOL` | Get enabled subtitle providers. |
| `bazarr_get_episode_subtitles` | `APITOOL` | Get subtitle information for a specific episode. |
| `bazarr_get_history` | `APITOOL` | Get subtitle download history. |
| `bazarr_get_languages` | `APITOOL` | Get all available subtitle languages. |
| `bazarr_get_movie_subtitles` | `APITOOL` | Get subtitle information for a specific movie. |
| `bazarr_get_movies` | `APITOOL` | Get all movies managed by Bazarr. |
| `bazarr_get_providers` | `APITOOL` | Get all subtitle providers. |
| `bazarr_get_series` | `APITOOL` | Get all series managed by Bazarr. |
| `bazarr_get_series_subtitles` | `APITOOL` | Get subtitle information for a specific series. |
| `bazarr_get_settings` | `APITOOL` | Get Bazarr settings. |
| `bazarr_get_system_health` | `APITOOL` | Get system health issues. |
| `bazarr_get_system_logs` | `APITOOL` | Get system logs. |
| `bazarr_get_system_status` | `APITOOL` | Get Bazarr system status. |
| `bazarr_get_wanted_movies` | `APITOOL` | Get movies with wanted/missing subtitles. |
| `bazarr_get_wanted_series` | `APITOOL` | Get series episodes with wanted/missing subtitles. |
| `bazarr_remove_from_blacklist` | `APITOOL` | Remove a subtitle from blacklist. |
| `bazarr_request` | `APITOOL` | Generic request method for the Bazarr API. |
| `bazarr_search_movie_subtitles` | `APITOOL` | Search for subtitles for a movie. |
| `bazarr_search_series_subtitles` | `APITOOL` | Search for subtitles for a series or episode. |
| `bazarr_test_provider` | `APITOOL` | Test a subtitle provider. |
| `bazarr_update_settings` | `APITOOL` | Update Bazarr settings. |
| `chaptarr_delete_author_editor` | `APITOOL` | Delete author editor. |
| `chaptarr_delete_author_id` | `APITOOL` | Delete an author by ID. |
| `chaptarr_delete_blocklist_bulk` | `APITOOL` | Delete blocklist bulk. |
| `chaptarr_delete_blocklist_id` | `APITOOL` | Delete blocklist id. |
| `chaptarr_delete_book_editor` | `APITOOL` | Delete book editor. |
| `chaptarr_delete_book_id` | `APITOOL` | Delete book id. |
| `chaptarr_delete_bookfile_bulk` | `APITOOL` | Delete bookfile bulk. |
| `chaptarr_delete_bookfile_id` | `APITOOL` | Delete bookfile id. |
| `chaptarr_delete_command_id` | `APITOOL` | Delete command id. |
| `chaptarr_delete_customfilter_id` | `APITOOL` | Delete customfilter id. |
| `chaptarr_delete_customformat_id` | `APITOOL` | Delete customformat id. |
| `chaptarr_delete_delayprofile_id` | `APITOOL` | Delete delayprofile id. |
| `chaptarr_delete_downloadclient_bulk` | `APITOOL` | Delete downloadclient bulk. |
| `chaptarr_delete_downloadclient_id` | `APITOOL` | Delete downloadclient id. |
| `chaptarr_delete_importlist_bulk` | `APITOOL` | Delete importlist bulk. |
| `chaptarr_delete_importlist_id` | `APITOOL` | Delete importlist id. |
| `chaptarr_delete_importlistexclusion_id` | `APITOOL` | Delete importlistexclusion id. |
| `chaptarr_delete_indexer_bulk` | `APITOOL` | Delete indexer bulk. |
| `chaptarr_delete_indexer_id` | `APITOOL` | Delete indexer id. |
| `chaptarr_delete_metadata_id` | `APITOOL` | Delete metadata id. |
| `chaptarr_delete_metadataprofile_id` | `APITOOL` | Delete metadataprofile id. |
| `chaptarr_delete_notification_id` | `APITOOL` | Delete notification id. |
| `chaptarr_delete_qualityprofile_id` | `APITOOL` | Delete qualityprofile id. |
| `chaptarr_delete_queue_bulk` | `APITOOL` | Delete queue bulk. |
| `chaptarr_delete_queue_id` | `APITOOL` | Delete queue id. |
| `chaptarr_delete_releaseprofile_id` | `APITOOL` | Delete releaseprofile id. |
| `chaptarr_delete_remotepathmapping_id` | `APITOOL` | Delete remotepathmapping id. |
| `chaptarr_delete_rootfolder_id` | `APITOOL` | Delete rootfolder id. |
| `chaptarr_delete_system_backup_id` | `APITOOL` | Delete system backup id. |
| `chaptarr_delete_tag_id` | `APITOOL` | Delete tag id. |
| `chaptarr_get_` | `APITOOL` | Get . |
| `chaptarr_get_api` | `APITOOL` | Get the base API information. |
| `chaptarr_get_author` | `APITOOL` | Get all authors managed by Chaptarr. |
| `chaptarr_get_author_id` | `APITOOL` | Get specific author. |
| `chaptarr_get_author_lookup` | `APITOOL` | Get author lookup. |
| `chaptarr_get_blocklist` | `APITOOL` | Get blocklist. |
| `chaptarr_get_book` | `APITOOL` | Get book. |
| `chaptarr_get_book_id` | `APITOOL` | Get specific book. |
| `chaptarr_get_book_id_overview` | `APITOOL` | Get specific book overview. |
| `chaptarr_get_book_lookup` | `APITOOL` | Get book lookup. |
| `chaptarr_get_bookfile` | `APITOOL` | Get bookfile. |
| `chaptarr_get_bookfile_id` | `APITOOL` | Get specific bookfile. |
| `chaptarr_get_calendar` | `APITOOL` | Get calendar. |
| `chaptarr_get_calendar_id` | `APITOOL` | Get specific calendar. |
| `chaptarr_get_command` | `APITOOL` | Get command. |
| `chaptarr_get_command_id` | `APITOOL` | Get specific command. |
| `chaptarr_get_config_development` | `APITOOL` | Get config development. |
| `chaptarr_get_config_development_id` | `APITOOL` | Get specific config development. |
| `chaptarr_get_config_downloadclient` | `APITOOL` | Get config downloadclient. |
| `chaptarr_get_config_downloadclient_id` | `APITOOL` | Get specific config downloadclient. |
| `chaptarr_get_config_host` | `APITOOL` | Get config host. |
| `chaptarr_get_config_host_id` | `APITOOL` | Get specific config host. |
| `chaptarr_get_config_indexer` | `APITOOL` | Get config indexer. |
| `chaptarr_get_config_indexer_id` | `APITOOL` | Get specific config indexer. |
| `chaptarr_get_config_mediamanagement` | `APITOOL` | Get config mediamanagement. |
| `chaptarr_get_config_mediamanagement_id` | `APITOOL` | Get specific config mediamanagement. |
| `chaptarr_get_config_metadataprovider` | `APITOOL` | Get config metadataprovider. |
| `chaptarr_get_config_metadataprovider_id` | `APITOOL` | Get specific config metadataprovider. |
| `chaptarr_get_config_naming` | `APITOOL` | Get config naming. |
| `chaptarr_get_config_naming_examples` | `APITOOL` | Get config naming examples. |
| `chaptarr_get_config_naming_id` | `APITOOL` | Get specific config naming. |
| `chaptarr_get_config_ui` | `APITOOL` | Get config ui. |
| `chaptarr_get_config_ui_id` | `APITOOL` | Get specific config ui. |
| `chaptarr_get_content_path` | `APITOOL` | Get content path. |
| `chaptarr_get_customfilter` | `APITOOL` | Get customfilter. |
| `chaptarr_get_customfilter_id` | `APITOOL` | Get specific customfilter. |
| `chaptarr_get_customformat` | `APITOOL` | Get customformat. |
| `chaptarr_get_customformat_id` | `APITOOL` | Get specific customformat. |
| `chaptarr_get_customformat_schema` | `APITOOL` | Get customformat schema. |
| `chaptarr_get_delayprofile` | `APITOOL` | Get delayprofile. |
| `chaptarr_get_delayprofile_id` | `APITOOL` | Get specific delayprofile. |
| `chaptarr_get_diskspace` | `APITOOL` | Get diskspace. |
| `chaptarr_get_downloadclient` | `APITOOL` | Get downloadclient. |
| `chaptarr_get_downloadclient_id` | `APITOOL` | Get specific downloadclient. |
| `chaptarr_get_downloadclient_schema` | `APITOOL` | Get downloadclient schema. |
| `chaptarr_get_edition` | `APITOOL` | Get edition. |
| `chaptarr_get_feed_v1_calendar_readarrics` | `APITOOL` | Get feed v1 calendar readarrics. |
| `chaptarr_get_filesystem` | `APITOOL` | Get filesystem. |
| `chaptarr_get_filesystem_mediafiles` | `APITOOL` | Get filesystem mediafiles. |
| `chaptarr_get_filesystem_type` | `APITOOL` | Get filesystem type. |
| `chaptarr_get_health` | `APITOOL` | Get health. |
| `chaptarr_get_history` | `APITOOL` | Get history. |
| `chaptarr_get_history_author` | `APITOOL` | Get history author. |
| `chaptarr_get_history_since` | `APITOOL` | Get history since. |
| `chaptarr_get_importlist` | `APITOOL` | Get importlist. |
| `chaptarr_get_importlist_id` | `APITOOL` | Get specific importlist. |
| `chaptarr_get_importlist_schema` | `APITOOL` | Get importlist schema. |
| `chaptarr_get_importlistexclusion` | `APITOOL` | Get importlistexclusion. |
| `chaptarr_get_importlistexclusion_id` | `APITOOL` | Get specific importlistexclusion. |
| `chaptarr_get_indexer` | `APITOOL` | Get indexer. |
| `chaptarr_get_indexer_id` | `APITOOL` | Get specific indexer. |
| `chaptarr_get_indexer_schema` | `APITOOL` | Get indexer schema. |
| `chaptarr_get_indexerflag` | `APITOOL` | Get indexerflag. |
| `chaptarr_get_language` | `APITOOL` | Get language. |
| `chaptarr_get_language_id` | `APITOOL` | Get specific language. |
| `chaptarr_get_localization` | `APITOOL` | Get localization. |
| `chaptarr_get_log` | `APITOOL` | Get log. |
| `chaptarr_get_log_file` | `APITOOL` | Get log file. |
| `chaptarr_get_log_file_filename` | `APITOOL` | Get log file filename. |
| `chaptarr_get_log_file_update` | `APITOOL` | Get log file update. |
| `chaptarr_get_log_file_update_filename` | `APITOOL` | Get log file update filename. |
| `chaptarr_get_login` | `APITOOL` | Get the login status or page. |
| `chaptarr_get_logout` | `APITOOL` | Log out from the Chaptarr instance. |
| `chaptarr_get_manualimport` | `APITOOL` | Get manualimport. |
| `chaptarr_get_mediacover_author_author_id_filename` | `APITOOL` | Get specific mediacover author author filename. |
| `chaptarr_get_mediacover_book_book_id_filename` | `APITOOL` | Get specific mediacover book book filename. |
| `chaptarr_get_metadata` | `APITOOL` | Get metadata. |
| `chaptarr_get_metadata_id` | `APITOOL` | Get specific metadata. |
| `chaptarr_get_metadata_schema` | `APITOOL` | Get metadata schema. |
| `chaptarr_get_metadataprofile` | `APITOOL` | Get metadataprofile. |
| `chaptarr_get_metadataprofile_id` | `APITOOL` | Get specific metadataprofile. |
| `chaptarr_get_metadataprofile_schema` | `APITOOL` | Get metadataprofile schema. |
| `chaptarr_get_notification` | `APITOOL` | Get notification. |
| `chaptarr_get_notification_id` | `APITOOL` | Get specific notification. |
| `chaptarr_get_notification_schema` | `APITOOL` | Get notification schema. |
| `chaptarr_get_parse` | `APITOOL` | Get parse. |
| `chaptarr_get_path` | `APITOOL` | Get path. |
| `chaptarr_get_ping` | `APITOOL` | Get ping. |
| `chaptarr_get_qualitydefinition` | `APITOOL` | Get qualitydefinition. |
| `chaptarr_get_qualitydefinition_id` | `APITOOL` | Get specific qualitydefinition. |
| `chaptarr_get_qualityprofile` | `APITOOL` | Get qualityprofile. |
| `chaptarr_get_qualityprofile_id` | `APITOOL` | Get specific qualityprofile. |
| `chaptarr_get_qualityprofile_schema` | `APITOOL` | Get qualityprofile schema. |
| `chaptarr_get_queue` | `APITOOL` | Get queue. |
| `chaptarr_get_queue_details` | `APITOOL` | Get queue details. |
| `chaptarr_get_queue_status` | `APITOOL` | Get queue status. |
| `chaptarr_get_release` | `APITOOL` | Get release. |
| `chaptarr_get_releaseprofile` | `APITOOL` | Get releaseprofile. |
| `chaptarr_get_releaseprofile_id` | `APITOOL` | Get specific releaseprofile. |
| `chaptarr_get_remotepathmapping` | `APITOOL` | Get remotepathmapping. |
| `chaptarr_get_remotepathmapping_id` | `APITOOL` | Get specific remotepathmapping. |
| `chaptarr_get_rename` | `APITOOL` | Get rename. |
| `chaptarr_get_retag` | `APITOOL` | Get retag. |
| `chaptarr_get_rootfolder` | `APITOOL` | Get rootfolder. |
| `chaptarr_get_rootfolder_id` | `APITOOL` | Get specific rootfolder. |
| `chaptarr_get_search` | `APITOOL` | Get search. |
| `chaptarr_get_series` | `APITOOL` | Get series. |
| `chaptarr_get_system_backup` | `APITOOL` | Get system backup. |
| `chaptarr_get_system_routes` | `APITOOL` | Get system routes. |
| `chaptarr_get_system_routes_duplicate` | `APITOOL` | Get system routes duplicate. |
| `chaptarr_get_system_status` | `APITOOL` | Get system status. |
| `chaptarr_get_system_task` | `APITOOL` | Get system task. |
| `chaptarr_get_system_task_id` | `APITOOL` | Get specific system task. |
| `chaptarr_get_tag` | `APITOOL` | Get tag. |
| `chaptarr_get_tag_detail` | `APITOOL` | Get tag detail. |
| `chaptarr_get_tag_detail_id` | `APITOOL` | Get specific tag detail. |
| `chaptarr_get_tag_id` | `APITOOL` | Get specific tag. |
| `chaptarr_get_update` | `APITOOL` | Get update. |
| `chaptarr_get_wanted_cutoff` | `APITOOL` | Get wanted cutoff. |
| `chaptarr_get_wanted_cutoff_id` | `APITOOL` | Get specific wanted cutoff. |
| `chaptarr_get_wanted_missing` | `APITOOL` | Get wanted missing. |
| `chaptarr_get_wanted_missing_id` | `APITOOL` | Get specific wanted missing. |
| `chaptarr_post_author` | `APITOOL` | Add a new author. |
| `chaptarr_post_book` | `APITOOL` | Add a new book. |
| `chaptarr_post_bookshelf` | `APITOOL` | Add a new bookshelf. |
| `chaptarr_post_command` | `APITOOL` | Add a new command. |
| `chaptarr_post_customfilter` | `APITOOL` | Add a new customfilter. |
| `chaptarr_post_customformat` | `APITOOL` | Add a new customformat. |
| `chaptarr_post_delayprofile` | `APITOOL` | Add a new delayprofile. |
| `chaptarr_post_downloadclient` | `APITOOL` | Add a new downloadclient. |
| `chaptarr_post_downloadclient_action_name` | `APITOOL` | Add a new downloadclient action name. |
| `chaptarr_post_downloadclient_test` | `APITOOL` | Test downloadclient. |
| `chaptarr_post_downloadclient_testall` | `APITOOL` | Add a new downloadclient testall. |
| `chaptarr_post_history_failed_id` | `APITOOL` | Add a new history failed id. |
| `chaptarr_post_importlist` | `APITOOL` | Add a new importlist. |
| `chaptarr_post_importlist_action_name` | `APITOOL` | Add a new importlist action name. |
| `chaptarr_post_importlist_test` | `APITOOL` | Test importlist. |
| `chaptarr_post_importlist_testall` | `APITOOL` | Add a new importlist testall. |
| `chaptarr_post_importlistexclusion` | `APITOOL` | Add a new importlistexclusion. |
| `chaptarr_post_indexer` | `APITOOL` | Add a new indexer. |
| `chaptarr_post_indexer_action_name` | `APITOOL` | Add a new indexer action name. |
| `chaptarr_post_indexer_test` | `APITOOL` | Test indexer. |
| `chaptarr_post_indexer_testall` | `APITOOL` | Add a new indexer testall. |
| `chaptarr_post_login` | `APITOOL` | Log in to the Chaptarr instance. |
| `chaptarr_post_manualimport` | `APITOOL` | Add a new manualimport. |
| `chaptarr_post_metadata` | `APITOOL` | Add a new metadata. |
| `chaptarr_post_metadata_action_name` | `APITOOL` | Add a new metadata action name. |
| `chaptarr_post_metadata_test` | `APITOOL` | Test metadata. |
| `chaptarr_post_metadata_testall` | `APITOOL` | Add a new metadata testall. |
| `chaptarr_post_metadataprofile` | `APITOOL` | Add a new metadataprofile. |
| `chaptarr_post_notification` | `APITOOL` | Add a new notification. |
| `chaptarr_post_notification_action_name` | `APITOOL` | Add a new notification action name. |
| `chaptarr_post_notification_test` | `APITOOL` | Test notification. |
| `chaptarr_post_notification_testall` | `APITOOL` | Add a new notification testall. |
| `chaptarr_post_qualityprofile` | `APITOOL` | Add a new qualityprofile. |
| `chaptarr_post_queue_grab_bulk` | `APITOOL` | Add a new queue grab bulk. |
| `chaptarr_post_queue_grab_id` | `APITOOL` | Add a new queue grab id. |
| `chaptarr_post_release` | `APITOOL` | Add a new release. |
| `chaptarr_post_release_push` | `APITOOL` | Add a new release push. |
| `chaptarr_post_releaseprofile` | `APITOOL` | Add a new releaseprofile. |
| `chaptarr_post_remotepathmapping` | `APITOOL` | Add a new remotepathmapping. |
| `chaptarr_post_rootfolder` | `APITOOL` | Add a new rootfolder. |
| `chaptarr_post_system_backup_restore_id` | `APITOOL` | Add a new system backup restore id. |
| `chaptarr_post_system_backup_restore_upload` | `APITOOL` | Add a new system backup restore upload. |
| `chaptarr_post_system_restart` | `APITOOL` | Add a new system restart. |
| `chaptarr_post_system_shutdown` | `APITOOL` | Add a new system shutdown. |
| `chaptarr_post_tag` | `APITOOL` | Add a new tag. |
| `chaptarr_put_author_editor` | `APITOOL` | Update author editor. |
| `chaptarr_put_author_id` | `APITOOL` | Update an existing author by ID. |
| `chaptarr_put_book_editor` | `APITOOL` | Update book editor. |
| `chaptarr_put_book_id` | `APITOOL` | Update book id. |
| `chaptarr_put_book_monitor` | `APITOOL` | Update book monitor. |
| `chaptarr_put_bookfile_editor` | `APITOOL` | Update bookfile editor. |
| `chaptarr_put_bookfile_id` | `APITOOL` | Update bookfile id. |
| `chaptarr_put_config_development_id` | `APITOOL` | Update config development id. |
| `chaptarr_put_config_downloadclient_id` | `APITOOL` | Update config downloadclient id. |
| `chaptarr_put_config_host_id` | `APITOOL` | Update config host id. |
| `chaptarr_put_config_indexer_id` | `APITOOL` | Update config indexer id. |
| `chaptarr_put_config_mediamanagement_id` | `APITOOL` | Update config mediamanagement id. |
| `chaptarr_put_config_metadataprovider_id` | `APITOOL` | Update config metadataprovider id. |
| `chaptarr_put_config_naming_id` | `APITOOL` | Update config naming id. |
| `chaptarr_put_config_ui_id` | `APITOOL` | Update config ui id. |
| `chaptarr_put_customfilter_id` | `APITOOL` | Update customfilter id. |
| `chaptarr_put_customformat_id` | `APITOOL` | Update customformat id. |
| `chaptarr_put_delayprofile_id` | `APITOOL` | Update delayprofile id. |
| `chaptarr_put_delayprofile_reorder_id` | `APITOOL` | Update delayprofile reorder id. |
| `chaptarr_put_downloadclient_bulk` | `APITOOL` | Update downloadclient bulk. |
| `chaptarr_put_downloadclient_id` | `APITOOL` | Update downloadclient id. |
| `chaptarr_put_importlist_bulk` | `APITOOL` | Update importlist bulk. |
| `chaptarr_put_importlist_id` | `APITOOL` | Update importlist id. |
| `chaptarr_put_importlistexclusion_id` | `APITOOL` | Update importlistexclusion id. |
| `chaptarr_put_indexer_bulk` | `APITOOL` | Update indexer bulk. |
| `chaptarr_put_indexer_id` | `APITOOL` | Update indexer id. |
| `chaptarr_put_metadata_id` | `APITOOL` | Update metadata id. |
| `chaptarr_put_metadataprofile_id` | `APITOOL` | Update metadataprofile id. |
| `chaptarr_put_notification_id` | `APITOOL` | Update notification id. |
| `chaptarr_put_qualitydefinition_id` | `APITOOL` | Update qualitydefinition id. |
| `chaptarr_put_qualitydefinition_update` | `APITOOL` | Update qualitydefinition update. |
| `chaptarr_put_qualityprofile_id` | `APITOOL` | Update qualityprofile id. |
| `chaptarr_put_releaseprofile_id` | `APITOOL` | Update releaseprofile id. |
| `chaptarr_put_remotepathmapping_id` | `APITOOL` | Update remotepathmapping id. |
| `chaptarr_put_rootfolder_id` | `APITOOL` | Update rootfolder id. |
| `chaptarr_put_tag_id` | `APITOOL` | Update tag id. |
| `chaptarr_request` | `APITOOL` | Generic request method for the Chaptarr API. |
| `lidarr_delete_album_id` | `APITOOL` | Delete an album and optionally its files and add exclusion. |
| `lidarr_delete_artist_editor` | `APITOOL` | Delete multiple artists using the artist editor. |
| `lidarr_delete_artist_id` | `APITOOL` | Delete artist id. |
| `lidarr_delete_autotagging_id` | `APITOOL` | Delete autotagging id. |
| `lidarr_delete_blocklist_bulk` | `APITOOL` | Delete blocklist bulk. |
| `lidarr_delete_blocklist_id` | `APITOOL` | Delete blocklist id. |
| `lidarr_delete_command_id` | `APITOOL` | Delete command id. |
| `lidarr_delete_customfilter_id` | `APITOOL` | Delete customfilter id. |
| `lidarr_delete_customformat_bulk` | `APITOOL` | Delete customformat bulk. |
| `lidarr_delete_customformat_id` | `APITOOL` | Delete customformat id. |
| `lidarr_delete_delayprofile_id` | `APITOOL` | Delete delayprofile id. |
| `lidarr_delete_downloadclient_bulk` | `APITOOL` | Delete downloadclient bulk. |
| `lidarr_delete_downloadclient_id` | `APITOOL` | Delete downloadclient id. |
| `lidarr_delete_importlist_bulk` | `APITOOL` | Delete multiple import lists in bulk. |
| `lidarr_delete_importlist_id` | `APITOOL` | Delete an import list configuration. |
| `lidarr_delete_importlistexclusion_id` | `APITOOL` | Delete importlistexclusion id. |
| `lidarr_delete_indexer_bulk` | `APITOOL` | Delete indexer bulk. |
| `lidarr_delete_indexer_id` | `APITOOL` | Delete an indexer configuration by ID. |
| `lidarr_delete_metadata_id` | `APITOOL` | Delete metadata id. |
| `lidarr_delete_metadataprofile_id` | `APITOOL` | Delete metadataprofile id. |
| `lidarr_delete_notification_id` | `APITOOL` | Delete notification id. |
| `lidarr_delete_qualityprofile_id` | `APITOOL` | Delete qualityprofile id. |
| `lidarr_delete_queue_bulk` | `APITOOL` | Delete queue bulk. |
| `lidarr_delete_queue_id` | `APITOOL` | Delete queue id. |
| `lidarr_delete_releaseprofile_id` | `APITOOL` | Delete releaseprofile id. |
| `lidarr_delete_remotepathmapping_id` | `APITOOL` | Delete remotepathmapping id. |
| `lidarr_delete_rootfolder_id` | `APITOOL` | Delete rootfolder id. |
| `lidarr_delete_system_backup_id` | `APITOOL` | Delete system backup id. |
| `lidarr_delete_tag_id` | `APITOOL` | Delete tag id. |
| `lidarr_delete_trackfile_bulk` | `APITOOL` | Delete trackfile bulk. |
| `lidarr_delete_trackfile_id` | `APITOOL` | Delete trackfile id. |
| `lidarr_get_` | `APITOOL` | Get . |
| `lidarr_get_album` | `APITOOL` | Get albums managed by Lidarr. |
| `lidarr_get_album_id` | `APITOOL` | Get details for a specific album by ID. |
| `lidarr_get_album_lookup` | `APITOOL` | Search for new albums to add to Lidarr. |
| `lidarr_get_api` | `APITOOL` | Get the base API information. |
| `lidarr_get_artist` | `APITOOL` | Get all artists managed by Lidarr. |
| `lidarr_get_artist_id` | `APITOOL` | Get details for a specific artist by ID. |
| `lidarr_get_artist_lookup` | `APITOOL` | Search for new artists to add to Lidarr. |
| `lidarr_get_autotagging` | `APITOOL` | Get autotagging. |
| `lidarr_get_autotagging_id` | `APITOOL` | Get specific autotagging. |
| `lidarr_get_autotagging_schema` | `APITOOL` | Get autotagging schema. |
| `lidarr_get_blocklist` | `APITOOL` | Get blocklist. |
| `lidarr_get_calendar` | `APITOOL` | Get calendar. |
| `lidarr_get_calendar_id` | `APITOOL` | Get specific calendar. |
| `lidarr_get_command` | `APITOOL` | Get command. |
| `lidarr_get_command_id` | `APITOOL` | Get specific command. |
| `lidarr_get_config_downloadclient` | `APITOOL` | Get config downloadclient. |
| `lidarr_get_config_downloadclient_id` | `APITOOL` | Get specific config downloadclient. |
| `lidarr_get_config_host` | `APITOOL` | Get config host. |
| `lidarr_get_config_host_id` | `APITOOL` | Get specific config host. |
| `lidarr_get_config_indexer` | `APITOOL` | Get config indexer. |
| `lidarr_get_config_indexer_id` | `APITOOL` | Get specific config indexer. |
| `lidarr_get_config_mediamanagement` | `APITOOL` | Get config mediamanagement. |
| `lidarr_get_config_mediamanagement_id` | `APITOOL` | Get specific config mediamanagement. |
| `lidarr_get_config_metadataprovider` | `APITOOL` | Get config metadataprovider. |
| `lidarr_get_config_metadataprovider_id` | `APITOOL` | Get specific config metadataprovider. |
| `lidarr_get_config_naming` | `APITOOL` | Get config naming. |
| `lidarr_get_config_naming_examples` | `APITOOL` | Get config naming examples. |
| `lidarr_get_config_naming_id` | `APITOOL` | Get specific config naming. |
| `lidarr_get_config_ui` | `APITOOL` | Get config ui. |
| `lidarr_get_config_ui_id` | `APITOOL` | Get specific config ui. |
| `lidarr_get_content_path` | `APITOOL` | Get content path. |
| `lidarr_get_customfilter` | `APITOOL` | Get customfilter. |
| `lidarr_get_customfilter_id` | `APITOOL` | Get specific customfilter. |
| `lidarr_get_customformat` | `APITOOL` | Get customformat. |
| `lidarr_get_customformat_id` | `APITOOL` | Get specific customformat. |
| `lidarr_get_customformat_schema` | `APITOOL` | Get customformat schema. |
| `lidarr_get_delayprofile` | `APITOOL` | Get delayprofile. |
| `lidarr_get_delayprofile_id` | `APITOOL` | Get specific delayprofile. |
| `lidarr_get_diskspace` | `APITOOL` | Get diskspace. |
| `lidarr_get_downloadclient` | `APITOOL` | Get downloadclient. |
| `lidarr_get_downloadclient_id` | `APITOOL` | Get specific downloadclient. |
| `lidarr_get_downloadclient_schema` | `APITOOL` | Get downloadclient schema. |
| `lidarr_get_feed_v1_calendar_lidarrics` | `APITOOL` | Get feed v1 calendar lidarrics. |
| `lidarr_get_filesystem` | `APITOOL` | Get filesystem. |
| `lidarr_get_filesystem_mediafiles` | `APITOOL` | Get filesystem mediafiles. |
| `lidarr_get_filesystem_type` | `APITOOL` | Get filesystem type. |
| `lidarr_get_health` | `APITOOL` | Get health. |
| `lidarr_get_history` | `APITOOL` | Get history. |
| `lidarr_get_history_artist` | `APITOOL` | Get history artist. |
| `lidarr_get_history_since` | `APITOOL` | Get history since. |
| `lidarr_get_importlist` | `APITOOL` | Get all import lists. |
| `lidarr_get_importlist_id` | `APITOOL` | Get details for a specific import list by ID. |
| `lidarr_get_importlist_schema` | `APITOOL` | Get the schema for import list configurations. |
| `lidarr_get_importlistexclusion` | `APITOOL` | Get importlistexclusion. |
| `lidarr_get_importlistexclusion_id` | `APITOOL` | Get specific importlistexclusion. |
| `lidarr_get_indexer` | `APITOOL` | Get all configured indexers. |
| `lidarr_get_indexer_id` | `APITOOL` | Get details for a specific indexer by ID. |
| `lidarr_get_indexer_schema` | `APITOOL` | Get indexer schema. |
| `lidarr_get_indexerflag` | `APITOOL` | Get indexerflag. |
| `lidarr_get_language` | `APITOOL` | Get language. |
| `lidarr_get_language_id` | `APITOOL` | Get specific language. |
| `lidarr_get_localization` | `APITOOL` | Get localization. |
| `lidarr_get_log` | `APITOOL` | Get log. |
| `lidarr_get_log_file` | `APITOOL` | Get log file. |
| `lidarr_get_log_file_filename` | `APITOOL` | Get log file filename. |
| `lidarr_get_log_file_update` | `APITOOL` | Get log file update. |
| `lidarr_get_log_file_update_filename` | `APITOOL` | Get log file update filename. |
| `lidarr_get_login` | `APITOOL` | Get login. |
| `lidarr_get_logout` | `APITOOL` | Get logout. |
| `lidarr_get_manualimport` | `APITOOL` | Get manualimport. |
| `lidarr_get_mediacover_album_album_id_filename` | `APITOOL` | Get specific mediacover album album filename. |
| `lidarr_get_mediacover_artist_artist_id_filename` | `APITOOL` | Get specific mediacover artist artist filename. |
| `lidarr_get_metadata` | `APITOOL` | Get metadata. |
| `lidarr_get_metadata_id` | `APITOOL` | Get specific metadata. |
| `lidarr_get_metadata_schema` | `APITOOL` | Get metadata schema. |
| `lidarr_get_metadataprofile` | `APITOOL` | Get metadataprofile. |
| `lidarr_get_metadataprofile_id` | `APITOOL` | Get specific metadataprofile. |
| `lidarr_get_metadataprofile_schema` | `APITOOL` | Get metadataprofile schema. |
| `lidarr_get_notification` | `APITOOL` | Get notification. |
| `lidarr_get_notification_id` | `APITOOL` | Get specific notification. |
| `lidarr_get_notification_schema` | `APITOOL` | Get notification schema. |
| `lidarr_get_parse` | `APITOOL` | Get parse. |
| `lidarr_get_path` | `APITOOL` | Get path. |
| `lidarr_get_ping` | `APITOOL` | Get ping. |
| `lidarr_get_qualitydefinition` | `APITOOL` | Get qualitydefinition. |
| `lidarr_get_qualitydefinition_id` | `APITOOL` | Get specific qualitydefinition. |
| `lidarr_get_qualityprofile` | `APITOOL` | Get qualityprofile. |
| `lidarr_get_qualityprofile_id` | `APITOOL` | Get specific qualityprofile. |
| `lidarr_get_qualityprofile_schema` | `APITOOL` | Get qualityprofile schema. |
| `lidarr_get_queue` | `APITOOL` | Get queue. |
| `lidarr_get_queue_details` | `APITOOL` | Get queue details. |
| `lidarr_get_queue_status` | `APITOOL` | Get queue status. |
| `lidarr_get_release` | `APITOOL` | Get release. |
| `lidarr_get_releaseprofile` | `APITOOL` | Get all configured release profiles. |
| `lidarr_get_releaseprofile_id` | `APITOOL` | Get specific releaseprofile. |
| `lidarr_get_remotepathmapping` | `APITOOL` | Get remotepathmapping. |
| `lidarr_get_remotepathmapping_id` | `APITOOL` | Get specific remotepathmapping. |
| `lidarr_get_rename` | `APITOOL` | Get rename. |
| `lidarr_get_retag` | `APITOOL` | Get retag. |
| `lidarr_get_rootfolder` | `APITOOL` | Get all configured root folders. |
| `lidarr_get_rootfolder_id` | `APITOOL` | Get specific rootfolder. |
| `lidarr_get_search` | `APITOOL` | Get search. |
| `lidarr_get_system_backup` | `APITOOL` | Get system backup. |
| `lidarr_get_system_routes` | `APITOOL` | Get system routes. |
| `lidarr_get_system_routes_duplicate` | `APITOOL` | Get system routes duplicate. |
| `lidarr_get_system_status` | `APITOOL` | Get the current system status for Lidarr. |
| `lidarr_get_system_task` | `APITOOL` | Get system task. |
| `lidarr_get_system_task_id` | `APITOOL` | Get specific system task. |
| `lidarr_get_tag` | `APITOOL` | Get all configured tags. |
| `lidarr_get_tag_detail` | `APITOOL` | Get tag detail. |
| `lidarr_get_tag_detail_id` | `APITOOL` | Get specific tag detail. |
| `lidarr_get_tag_id` | `APITOOL` | Get specific tag. |
| `lidarr_get_track` | `APITOOL` | Get track. |
| `lidarr_get_track_id` | `APITOOL` | Get specific track. |
| `lidarr_get_trackfile` | `APITOOL` | Get trackfile. |
| `lidarr_get_trackfile_id` | `APITOOL` | Get specific trackfile. |
| `lidarr_get_update` | `APITOOL` | Get update. |
| `lidarr_get_wanted_cutoff` | `APITOOL` | Get wanted cutoff. |
| `lidarr_get_wanted_cutoff_id` | `APITOOL` | Get specific wanted cutoff. |
| `lidarr_get_wanted_missing` | `APITOOL` | Get wanted missing. |
| `lidarr_get_wanted_missing_id` | `APITOOL` | Get specific wanted missing. |
| `lidarr_post_album` | `APITOOL` | Add a new album to Lidarr. |
| `lidarr_post_albumstudio` | `APITOOL` | Perform studio operations on albums. |
| `lidarr_post_artist` | `APITOOL` | Add a new artist to Lidarr. |
| `lidarr_post_autotagging` | `APITOOL` | Add a new autotagging. |
| `lidarr_post_command` | `APITOOL` | Add a new command. |
| `lidarr_post_customfilter` | `APITOOL` | Add a new customfilter. |
| `lidarr_post_customformat` | `APITOOL` | Add a new customformat. |
| `lidarr_post_delayprofile` | `APITOOL` | Add a new delayprofile. |
| `lidarr_post_downloadclient` | `APITOOL` | Add a new downloadclient. |
| `lidarr_post_downloadclient_action_name` | `APITOOL` | Add a new downloadclient action name. |
| `lidarr_post_downloadclient_test` | `APITOOL` | Test downloadclient. |
| `lidarr_post_downloadclient_testall` | `APITOOL` | Add a new downloadclient testall. |
| `lidarr_post_history_failed_id` | `APITOOL` | Add a new history failed id. |
| `lidarr_post_importlist` | `APITOOL` | Add a new import list. |
| `lidarr_post_importlist_action_name` | `APITOOL` | Perform a specific action on import lists. |
| `lidarr_post_importlist_test` | `APITOOL` | Test an import list configuration. |
| `lidarr_post_importlist_testall` | `APITOOL` | Test all configured import lists. |
| `lidarr_post_importlistexclusion` | `APITOOL` | Add a new importlistexclusion. |
| `lidarr_post_indexer` | `APITOOL` | Add a new indexer configuration. |
| `lidarr_post_indexer_action_name` | `APITOOL` | Add a new indexer action name. |
| `lidarr_post_indexer_test` | `APITOOL` | Test indexer. |
| `lidarr_post_indexer_testall` | `APITOOL` | Add a new indexer testall. |
| `lidarr_post_login` | `APITOOL` | Add a new login. |
| `lidarr_post_manualimport` | `APITOOL` | Add a new manualimport. |
| `lidarr_post_metadata` | `APITOOL` | Add a new metadata. |
| `lidarr_post_metadata_action_name` | `APITOOL` | Add a new metadata action name. |
| `lidarr_post_metadata_test` | `APITOOL` | Test metadata. |
| `lidarr_post_metadata_testall` | `APITOOL` | Add a new metadata testall. |
| `lidarr_post_metadataprofile` | `APITOOL` | Add a new metadataprofile. |
| `lidarr_post_notification` | `APITOOL` | Add a new notification. |
| `lidarr_post_notification_action_name` | `APITOOL` | Add a new notification action name. |
| `lidarr_post_notification_test` | `APITOOL` | Test notification. |
| `lidarr_post_notification_testall` | `APITOOL` | Add a new notification testall. |
| `lidarr_post_qualityprofile` | `APITOOL` | Add a new qualityprofile. |
| `lidarr_post_queue_grab_bulk` | `APITOOL` | Add a new queue grab bulk. |
| `lidarr_post_queue_grab_id` | `APITOOL` | Add a new queue grab id. |
| `lidarr_post_release` | `APITOOL` | Add a new release. |
| `lidarr_post_release_push` | `APITOOL` | Add a new release push. |
| `lidarr_post_releaseprofile` | `APITOOL` | Add a new release profile configuration. |
| `lidarr_post_remotepathmapping` | `APITOOL` | Add a new remotepathmapping. |
| `lidarr_post_rootfolder` | `APITOOL` | Add a new root folder. |
| `lidarr_post_system_backup_restore_id` | `APITOOL` | Add a new system backup restore id. |
| `lidarr_post_system_backup_restore_upload` | `APITOOL` | Add a new system backup restore upload. |
| `lidarr_post_system_restart` | `APITOOL` | Add a new system restart. |
| `lidarr_post_system_shutdown` | `APITOOL` | Add a new system shutdown. |
| `lidarr_post_tag` | `APITOOL` | Add a new tag. |
| `lidarr_put_album_id` | `APITOOL` | Update an existing album by ID. |
| `lidarr_put_album_monitor` | `APITOOL` | Update monitoring status for multiple albums. |
| `lidarr_put_artist_editor` | `APITOOL` | Update monitoring or tagging for multiple artists. |
| `lidarr_put_artist_id` | `APITOOL` | Update an existing artist configuration. |
| `lidarr_put_autotagging_id` | `APITOOL` | Update autotagging id. |
| `lidarr_put_config_downloadclient_id` | `APITOOL` | Update config downloadclient id. |
| `lidarr_put_config_host_id` | `APITOOL` | Update config host id. |
| `lidarr_put_config_indexer_id` | `APITOOL` | Update config indexer id. |
| `lidarr_put_config_mediamanagement_id` | `APITOOL` | Update config mediamanagement id. |
| `lidarr_put_config_metadataprovider_id` | `APITOOL` | Update config metadataprovider id. |
| `lidarr_put_config_naming_id` | `APITOOL` | Update config naming id. |
| `lidarr_put_config_ui_id` | `APITOOL` | Update config ui id. |
| `lidarr_put_customfilter_id` | `APITOOL` | Update customfilter id. |
| `lidarr_put_customformat_bulk` | `APITOOL` | Update customformat bulk. |
| `lidarr_put_customformat_id` | `APITOOL` | Update customformat id. |
| `lidarr_put_delayprofile_id` | `APITOOL` | Update delayprofile id. |
| `lidarr_put_delayprofile_reorder_id` | `APITOOL` | Update delayprofile reorder id. |
| `lidarr_put_downloadclient_bulk` | `APITOOL` | Update downloadclient bulk. |
| `lidarr_put_downloadclient_id` | `APITOOL` | Update downloadclient id. |
| `lidarr_put_importlist_bulk` | `APITOOL` | Update multiple import lists in bulk. |
| `lidarr_put_importlist_id` | `APITOOL` | Update an existing import list configuration. |
| `lidarr_put_importlistexclusion_id` | `APITOOL` | Update importlistexclusion id. |
| `lidarr_put_indexer_bulk` | `APITOOL` | Update indexer bulk. |
| `lidarr_put_indexer_id` | `APITOOL` | Update an existing indexer configuration. |
| `lidarr_put_metadata_id` | `APITOOL` | Update metadata id. |
| `lidarr_put_metadataprofile_id` | `APITOOL` | Update metadataprofile id. |
| `lidarr_put_notification_id` | `APITOOL` | Update notification id. |
| `lidarr_put_qualitydefinition_id` | `APITOOL` | Update qualitydefinition id. |
| `lidarr_put_qualitydefinition_update` | `APITOOL` | Update qualitydefinition update. |
| `lidarr_put_qualityprofile_id` | `APITOOL` | Update qualityprofile id. |
| `lidarr_put_releaseprofile_id` | `APITOOL` | Update releaseprofile id. |
| `lidarr_put_remotepathmapping_id` | `APITOOL` | Update remotepathmapping id. |
| `lidarr_put_rootfolder_id` | `APITOOL` | Update rootfolder id. |
| `lidarr_put_tag_id` | `APITOOL` | Update tag id. |
| `lidarr_put_trackfile_editor` | `APITOOL` | Update trackfile editor. |
| `lidarr_put_trackfile_id` | `APITOOL` | Update trackfile id. |
| `lidarr_request` | `APITOOL` | Generic request method for the Lidarr API. |
| `prowlarr_delete_applications_bulk` | `APITOOL` | Delete applications bulk. |
| `prowlarr_delete_applications_id` | `APITOOL` | Delete an application configuration. |
| `prowlarr_delete_appprofile_id` | `APITOOL` | Delete appprofile id. |
| `prowlarr_delete_command_id` | `APITOOL` | Delete command id. |
| `prowlarr_delete_customfilter_id` | `APITOOL` | Delete customfilter id. |
| `prowlarr_delete_downloadclient_bulk` | `APITOOL` | Delete downloadclient bulk. |
| `prowlarr_delete_downloadclient_id` | `APITOOL` | Delete downloadclient id. |
| `prowlarr_delete_indexer_bulk` | `APITOOL` | Delete indexer bulk. |
| `prowlarr_delete_indexer_id` | `APITOOL` | Delete indexer id. |
| `prowlarr_delete_indexerproxy_id` | `APITOOL` | Delete indexerproxy id. |
| `prowlarr_delete_notification_id` | `APITOOL` | Delete notification id. |
| `prowlarr_delete_system_backup_id` | `APITOOL` | Delete system backup id. |
| `prowlarr_delete_tag_id` | `APITOOL` | Delete tag id. |
| `prowlarr_get_` | `APITOOL` | Get . |
| `prowlarr_get_api` | `APITOOL` | Get the base API information. |
| `prowlarr_get_applications` | `APITOOL` | Get all applications managed by Prowlarr. |
| `prowlarr_get_applications_id` | `APITOOL` | Get details for a specific application by ID. |
| `prowlarr_get_applications_schema` | `APITOOL` | Get applications schema. |
| `prowlarr_get_appprofile` | `APITOOL` | Get appprofile. |
| `prowlarr_get_appprofile_id` | `APITOOL` | Get specific appprofile. |
| `prowlarr_get_appprofile_schema` | `APITOOL` | Get appprofile schema. |
| `prowlarr_get_command` | `APITOOL` | Get command. |
| `prowlarr_get_command_id` | `APITOOL` | Get specific command. |
| `prowlarr_get_config_development` | `APITOOL` | Get config development. |
| `prowlarr_get_config_development_id` | `APITOOL` | Get specific config development. |
| `prowlarr_get_config_downloadclient` | `APITOOL` | Get config downloadclient. |
| `prowlarr_get_config_downloadclient_id` | `APITOOL` | Get specific config downloadclient. |
| `prowlarr_get_config_host` | `APITOOL` | Get config host. |
| `prowlarr_get_config_host_id` | `APITOOL` | Get specific config host. |
| `prowlarr_get_config_ui` | `APITOOL` | Get config ui. |
| `prowlarr_get_config_ui_id` | `APITOOL` | Get specific config ui. |
| `prowlarr_get_content_path` | `APITOOL` | Get content path. |
| `prowlarr_get_customfilter` | `APITOOL` | Get customfilter. |
| `prowlarr_get_customfilter_id` | `APITOOL` | Get specific customfilter. |
| `prowlarr_get_downloadclient` | `APITOOL` | Get downloadclient. |
| `prowlarr_get_downloadclient_id` | `APITOOL` | Get specific downloadclient. |
| `prowlarr_get_downloadclient_schema` | `APITOOL` | Get downloadclient schema. |
| `prowlarr_get_filesystem` | `APITOOL` | Get filesystem. |
| `prowlarr_get_filesystem_type` | `APITOOL` | Get filesystem type. |
| `prowlarr_get_health` | `APITOOL` | Get health. |
| `prowlarr_get_history` | `APITOOL` | Get history. |
| `prowlarr_get_history_indexer` | `APITOOL` | Get history indexer. |
| `prowlarr_get_history_since` | `APITOOL` | Get history since. |
| `prowlarr_get_id_api` | `APITOOL` | Get results for a specific indexer endpoint in Newznab format. |
| `prowlarr_get_id_download` | `APITOOL` | Get specific id download. |
| `prowlarr_get_indexer` | `APITOOL` | Get indexer. |
| `prowlarr_get_indexer_categories` | `APITOOL` | Get indexer categories. |
| `prowlarr_get_indexer_id` | `APITOOL` | Get specific indexer. |
| `prowlarr_get_indexer_id_download` | `APITOOL` | Download a release from a specific indexer. |
| `prowlarr_get_indexer_id_newznab` | `APITOOL` | Get specific indexer newznab. |
| `prowlarr_get_indexer_schema` | `APITOOL` | Get indexer schema. |
| `prowlarr_get_indexerproxy` | `APITOOL` | Get indexerproxy. |
| `prowlarr_get_indexerproxy_id` | `APITOOL` | Get specific indexerproxy. |
| `prowlarr_get_indexerproxy_schema` | `APITOOL` | Get indexerproxy schema. |
| `prowlarr_get_indexerstats` | `APITOOL` | Get indexerstats. |
| `prowlarr_get_indexerstatus` | `APITOOL` | Get indexerstatus. |
| `prowlarr_get_localization` | `APITOOL` | Get localization. |
| `prowlarr_get_localization_options` | `APITOOL` | Get localization options. |
| `prowlarr_get_log` | `APITOOL` | Get log. |
| `prowlarr_get_log_file` | `APITOOL` | Get log file. |
| `prowlarr_get_log_file_filename` | `APITOOL` | Get log file filename. |
| `prowlarr_get_log_file_update` | `APITOOL` | Get log file update. |
| `prowlarr_get_log_file_update_filename` | `APITOOL` | Get log file update filename. |
| `prowlarr_get_login` | `APITOOL` | Get login. |
| `prowlarr_get_logout` | `APITOOL` | Get logout. |
| `prowlarr_get_notification` | `APITOOL` | Get all configured notifications. |
| `prowlarr_get_notification_id` | `APITOOL` | Get specific notification. |
| `prowlarr_get_notification_schema` | `APITOOL` | Get notification schema. |
| `prowlarr_get_path` | `APITOOL` | Get path. |
| `prowlarr_get_ping` | `APITOOL` | Ping the Prowlarr API to check connectivity. |
| `prowlarr_get_search` | `APITOOL` | Get search. |
| `prowlarr_get_system_backup` | `APITOOL` | Get system backup. |
| `prowlarr_get_system_routes` | `APITOOL` | Get system routes. |
| `prowlarr_get_system_routes_duplicate` | `APITOOL` | Get system routes duplicate. |
| `prowlarr_get_system_status` | `APITOOL` | Get system status. |
| `prowlarr_get_system_task` | `APITOOL` | Get system task. |
| `prowlarr_get_system_task_id` | `APITOOL` | Get specific system task. |
| `prowlarr_get_tag` | `APITOOL` | Get tag. |
| `prowlarr_get_tag_detail` | `APITOOL` | Get tag detail. |
| `prowlarr_get_tag_detail_id` | `APITOOL` | Get specific tag detail. |
| `prowlarr_get_tag_id` | `APITOOL` | Get specific tag. |
| `prowlarr_get_update` | `APITOOL` | Get update. |
| `prowlarr_post_applications` | `APITOOL` | Add a new applications. |
| `prowlarr_post_applications_action_name` | `APITOOL` | Add a new applications action name. |
| `prowlarr_post_applications_test` | `APITOOL` | Test applications. |
| `prowlarr_post_applications_testall` | `APITOOL` | Add a new applications testall. |
| `prowlarr_post_appprofile` | `APITOOL` | Add a new appprofile. |
| `prowlarr_post_command` | `APITOOL` | Add a new command. |
| `prowlarr_post_customfilter` | `APITOOL` | Add a new customfilter. |
| `prowlarr_post_downloadclient` | `APITOOL` | Add a new downloadclient. |
| `prowlarr_post_downloadclient_action_name` | `APITOOL` | Add a new downloadclient action name. |
| `prowlarr_post_downloadclient_test` | `APITOOL` | Test downloadclient. |
| `prowlarr_post_downloadclient_testall` | `APITOOL` | Add a new downloadclient testall. |
| `prowlarr_post_indexer` | `APITOOL` | Add a new indexer. |
| `prowlarr_post_indexer_action_name` | `APITOOL` | Add a new indexer action name. |
| `prowlarr_post_indexer_test` | `APITOOL` | Test indexer. |
| `prowlarr_post_indexer_testall` | `APITOOL` | Add a new indexer testall. |
| `prowlarr_post_indexerproxy` | `APITOOL` | Add a new indexerproxy. |
| `prowlarr_post_indexerproxy_action_name` | `APITOOL` | Add a new indexerproxy action name. |
| `prowlarr_post_indexerproxy_test` | `APITOOL` | Test indexerproxy. |
| `prowlarr_post_indexerproxy_testall` | `APITOOL` | Add a new indexerproxy testall. |
| `prowlarr_post_login` | `APITOOL` | Add a new login. |
| `prowlarr_post_notification` | `APITOOL` | Add a new notification. |
| `prowlarr_post_notification_action_name` | `APITOOL` | Add a new notification action name. |
| `prowlarr_post_notification_test` | `APITOOL` | Test notification. |
| `prowlarr_post_notification_testall` | `APITOOL` | Add a new notification testall. |
| `prowlarr_post_search` | `APITOOL` | Perform a bulk search across multiple indexers. |
| `prowlarr_post_search_bulk` | `APITOOL` | Add a new search bulk. |
| `prowlarr_post_system_backup_restore_id` | `APITOOL` | Add a new system backup restore id. |
| `prowlarr_post_system_backup_restore_upload` | `APITOOL` | Add a new system backup restore upload. |
| `prowlarr_post_system_restart` | `APITOOL` | Add a new system restart. |
| `prowlarr_post_system_shutdown` | `APITOOL` | Add a new system shutdown. |
| `prowlarr_post_tag` | `APITOOL` | Add a new tag. |
| `prowlarr_put_applications_bulk` | `APITOOL` | Update applications bulk. |
| `prowlarr_put_applications_id` | `APITOOL` | Update an existing application configuration. |
| `prowlarr_put_appprofile_id` | `APITOOL` | Update appprofile id. |
| `prowlarr_put_config_development_id` | `APITOOL` | Update config development id. |
| `prowlarr_put_config_downloadclient_id` | `APITOOL` | Update config downloadclient id. |
| `prowlarr_put_config_host_id` | `APITOOL` | Update config host id. |
| `prowlarr_put_config_ui_id` | `APITOOL` | Update config ui id. |
| `prowlarr_put_customfilter_id` | `APITOOL` | Update customfilter id. |
| `prowlarr_put_downloadclient_bulk` | `APITOOL` | Update downloadclient bulk. |
| `prowlarr_put_downloadclient_id` | `APITOOL` | Update downloadclient id. |
| `prowlarr_put_indexer_bulk` | `APITOOL` | Update indexer bulk. |
| `prowlarr_put_indexer_id` | `APITOOL` | Update indexer id. |
| `prowlarr_put_indexerproxy_id` | `APITOOL` | Update indexerproxy id. |
| `prowlarr_put_notification_id` | `APITOOL` | Update notification id. |
| `prowlarr_put_tag_id` | `APITOOL` | Update tag id. |
| `prowlarr_request` | `APITOOL` | Generic request method for the Prowlarr API. |
| `prowlarr_search` | `APITOOL` | Search for indexers using the search endpoint. |
| `radarr_add_movie` | `APITOOL` | Lookup a movie by term, pick the first result, and add it to Radarr. |
| `radarr_delete_autotagging_id` | `APITOOL` | Delete autotagging id. |
| `radarr_delete_blocklist_bulk` | `APITOOL` | Delete blocklist bulk. |
| `radarr_delete_blocklist_id` | `APITOOL` | Delete blocklist id. |
| `radarr_delete_command_id` | `APITOOL` | Delete command id. |
| `radarr_delete_customfilter_id` | `APITOOL` | Delete customfilter id. |
| `radarr_delete_customformat_bulk` | `APITOOL` | Delete customformat bulk. |
| `radarr_delete_customformat_id` | `APITOOL` | Delete customformat id. |
| `radarr_delete_delayprofile_id` | `APITOOL` | Delete delayprofile id. |
| `radarr_delete_downloadclient_bulk` | `APITOOL` | Delete downloadclient bulk. |
| `radarr_delete_downloadclient_id` | `APITOOL` | Delete downloadclient id. |
| `radarr_delete_exclusions_bulk` | `APITOOL` | Delete exclusions bulk. |
| `radarr_delete_exclusions_id` | `APITOOL` | Delete exclusions id. |
| `radarr_delete_importlist_bulk` | `APITOOL` | Delete importlist bulk. |
| `radarr_delete_importlist_id` | `APITOOL` | Delete importlist id. |
| `radarr_delete_indexer_bulk` | `APITOOL` | Delete indexer bulk. |
| `radarr_delete_indexer_id` | `APITOOL` | Delete indexer id. |
| `radarr_delete_metadata_id` | `APITOOL` | Delete metadata id. |
| `radarr_delete_movie_editor` | `APITOOL` | Delete movie editor. |
| `radarr_delete_movie_id` | `APITOOL` | Delete movie id. |
| `radarr_delete_moviefile_bulk` | `APITOOL` | Delete moviefile bulk. |
| `radarr_delete_moviefile_id` | `APITOOL` | Delete moviefile id. |
| `radarr_delete_notification_id` | `APITOOL` | Delete notification id. |
| `radarr_delete_qualityprofile_id` | `APITOOL` | Delete qualityprofile id. |
| `radarr_delete_queue_bulk` | `APITOOL` | Delete queue bulk. |
| `radarr_delete_queue_id` | `APITOOL` | Delete an item from the download queue. |
| `radarr_delete_releaseprofile_id` | `APITOOL` | Delete releaseprofile id. |
| `radarr_delete_remotepathmapping_id` | `APITOOL` | Delete remotepathmapping id. |
| `radarr_delete_rootfolder_id` | `APITOOL` | Delete rootfolder id. |
| `radarr_delete_system_backup_id` | `APITOOL` | Delete system backup id. |
| `radarr_delete_tag_id` | `APITOOL` | Delete tag id. |
| `radarr_get_` | `APITOOL` | Get . |
| `radarr_get_alttitle` | `APITOOL` | Get alternative titles for movies. |
| `radarr_get_alttitle_id` | `APITOOL` | Get a specific alternative title by ID. |
| `radarr_get_api` | `APITOOL` | Get the base API information. |
| `radarr_get_autotagging` | `APITOOL` | Get autotagging. |
| `radarr_get_autotagging_id` | `APITOOL` | Get specific autotagging. |
| `radarr_get_autotagging_schema` | `APITOOL` | Get autotagging schema. |
| `radarr_get_blocklist` | `APITOOL` | Get blocklist. |
| `radarr_get_blocklist_movie` | `APITOOL` | Get blocklisted items for a specific movie. |
| `radarr_get_calendar` | `APITOOL` | Get calendar. |
| `radarr_get_collection` | `APITOOL` | Get collection. |
| `radarr_get_collection_id` | `APITOOL` | Get specific collection. |
| `radarr_get_command` | `APITOOL` | Get command. |
| `radarr_get_command_id` | `APITOOL` | Get specific command. |
| `radarr_get_config_downloadclient` | `APITOOL` | Get config downloadclient. |
| `radarr_get_config_downloadclient_id` | `APITOOL` | Get specific config downloadclient. |
| `radarr_get_config_host` | `APITOOL` | Get config host. |
| `radarr_get_config_host_id` | `APITOOL` | Get specific config host. |
| `radarr_get_config_importlist` | `APITOOL` | Get config importlist. |
| `radarr_get_config_importlist_id` | `APITOOL` | Get specific config importlist. |
| `radarr_get_config_indexer` | `APITOOL` | Get config indexer. |
| `radarr_get_config_indexer_id` | `APITOOL` | Get specific config indexer. |
| `radarr_get_config_mediamanagement` | `APITOOL` | Get config mediamanagement. |
| `radarr_get_config_mediamanagement_id` | `APITOOL` | Get specific config mediamanagement. |
| `radarr_get_config_metadata` | `APITOOL` | Get config metadata. |
| `radarr_get_config_metadata_id` | `APITOOL` | Get specific config metadata. |
| `radarr_get_config_naming` | `APITOOL` | Get config naming. |
| `radarr_get_config_naming_examples` | `APITOOL` | Get config naming examples. |
| `radarr_get_config_naming_id` | `APITOOL` | Get specific config naming. |
| `radarr_get_config_ui` | `APITOOL` | Get config ui. |
| `radarr_get_config_ui_id` | `APITOOL` | Get specific config ui. |
| `radarr_get_content_path` | `APITOOL` | Get content path. |
| `radarr_get_credit` | `APITOOL` | Get credit. |
| `radarr_get_credit_id` | `APITOOL` | Get specific credit. |
| `radarr_get_customfilter` | `APITOOL` | Get customfilter. |
| `radarr_get_customfilter_id` | `APITOOL` | Get specific customfilter. |
| `radarr_get_customformat` | `APITOOL` | Get customformat. |
| `radarr_get_customformat_id` | `APITOOL` | Get specific customformat. |
| `radarr_get_customformat_schema` | `APITOOL` | Get customformat schema. |
| `radarr_get_delayprofile` | `APITOOL` | Get delayprofile. |
| `radarr_get_delayprofile_id` | `APITOOL` | Get specific delayprofile. |
| `radarr_get_diskspace` | `APITOOL` | Get diskspace. |
| `radarr_get_downloadclient` | `APITOOL` | Get downloadclient. |
| `radarr_get_downloadclient_id` | `APITOOL` | Get specific downloadclient. |
| `radarr_get_downloadclient_schema` | `APITOOL` | Get downloadclient schema. |
| `radarr_get_exclusions` | `APITOOL` | Get all movie import exclusions. |
| `radarr_get_exclusions_id` | `APITOOL` | Get specific exclusions. |
| `radarr_get_exclusions_paged` | `APITOOL` | Get exclusions paged. |
| `radarr_get_extrafile` | `APITOOL` | Get extrafile. |
| `radarr_get_feed_v3_calendar_radarrics` | `APITOOL` | Get feed v3 calendar radarrics. |
| `radarr_get_filesystem` | `APITOOL` | Get filesystem. |
| `radarr_get_filesystem_mediafiles` | `APITOOL` | Get filesystem mediafiles. |
| `radarr_get_filesystem_type` | `APITOOL` | Get filesystem type. |
| `radarr_get_health` | `APITOOL` | Get health. |
| `radarr_get_history` | `APITOOL` | Get history. |
| `radarr_get_history_movie` | `APITOOL` | Get history movie. |
| `radarr_get_history_since` | `APITOOL` | Get history since. |
| `radarr_get_importlist` | `APITOOL` | Get importlist. |
| `radarr_get_importlist_id` | `APITOOL` | Get specific importlist. |
| `radarr_get_importlist_movie` | `APITOOL` | Get importlist movie. |
| `radarr_get_importlist_schema` | `APITOOL` | Get importlist schema. |
| `radarr_get_indexer` | `APITOOL` | Get indexer. |
| `radarr_get_indexer_id` | `APITOOL` | Get specific indexer. |
| `radarr_get_indexer_schema` | `APITOOL` | Get indexer schema. |
| `radarr_get_indexerflag` | `APITOOL` | Get indexerflag. |
| `radarr_get_language` | `APITOOL` | Get language. |
| `radarr_get_language_id` | `APITOOL` | Get specific language. |
| `radarr_get_localization` | `APITOOL` | Get localization. |
| `radarr_get_localization_language` | `APITOOL` | Get localization language. |
| `radarr_get_log` | `APITOOL` | Get log. |
| `radarr_get_log_file` | `APITOOL` | Get log file. |
| `radarr_get_log_file_filename` | `APITOOL` | Get log file filename. |
| `radarr_get_log_file_update` | `APITOOL` | Get log file update. |
| `radarr_get_log_file_update_filename` | `APITOOL` | Get log file update filename. |
| `radarr_get_login` | `APITOOL` | Get login. |
| `radarr_get_logout` | `APITOOL` | Get logout. |
| `radarr_get_manualimport` | `APITOOL` | Get manualimport. |
| `radarr_get_mediacover_movie_id_filename` | `APITOOL` | Get specific mediacover movie filename. |
| `radarr_get_metadata` | `APITOOL` | Get metadata. |
| `radarr_get_metadata_id` | `APITOOL` | Get specific metadata. |
| `radarr_get_metadata_schema` | `APITOOL` | Get metadata schema. |
| `radarr_get_movie` | `APITOOL` | Get movie. |
| `radarr_get_movie_id` | `APITOOL` | Get specific movie. |
| `radarr_get_movie_id_folder` | `APITOOL` | Get specific movie folder. |
| `radarr_get_movie_lookup` | `APITOOL` | Get movie lookup. |
| `radarr_get_movie_lookup_imdb` | `APITOOL` | Get movie lookup imdb. |
| `radarr_get_movie_lookup_tmdb` | `APITOOL` | Get movie lookup tmdb. |
| `radarr_get_moviefile` | `APITOOL` | Get moviefile. |
| `radarr_get_moviefile_id` | `APITOOL` | Get specific moviefile. |
| `radarr_get_notification` | `APITOOL` | Get notification. |
| `radarr_get_notification_id` | `APITOOL` | Get specific notification. |
| `radarr_get_notification_schema` | `APITOOL` | Get notification schema. |
| `radarr_get_parse` | `APITOOL` | Get parse. |
| `radarr_get_path` | `APITOOL` | Get path. |
| `radarr_get_ping` | `APITOOL` | Get ping. |
| `radarr_get_qualitydefinition` | `APITOOL` | Get qualitydefinition. |
| `radarr_get_qualitydefinition_id` | `APITOOL` | Get specific qualitydefinition. |
| `radarr_get_qualitydefinition_limits` | `APITOOL` | Get qualitydefinition limits. |
| `radarr_get_qualityprofile` | `APITOOL` | Get qualityprofile. |
| `radarr_get_qualityprofile_id` | `APITOOL` | Get specific qualityprofile. |
| `radarr_get_qualityprofile_schema` | `APITOOL` | Get qualityprofile schema. |
| `radarr_get_queue` | `APITOOL` | Get queue. |
| `radarr_get_queue_details` | `APITOOL` | Get queue details. |
| `radarr_get_queue_status` | `APITOOL` | Get queue status. |
| `radarr_get_release` | `APITOOL` | Get release. |
| `radarr_get_releaseprofile` | `APITOOL` | Get releaseprofile. |
| `radarr_get_releaseprofile_id` | `APITOOL` | Get specific releaseprofile. |
| `radarr_get_remotepathmapping` | `APITOOL` | Get remotepathmapping. |
| `radarr_get_remotepathmapping_id` | `APITOOL` | Get specific remotepathmapping. |
| `radarr_get_rename` | `APITOOL` | Get rename. |
| `radarr_get_rootfolder` | `APITOOL` | Get rootfolder. |
| `radarr_get_rootfolder_id` | `APITOOL` | Get specific rootfolder. |
| `radarr_get_system_backup` | `APITOOL` | Get system backup. |
| `radarr_get_system_routes` | `APITOOL` | Get system routes. |
| `radarr_get_system_routes_duplicate` | `APITOOL` | Get system routes duplicate. |
| `radarr_get_system_status` | `APITOOL` | Get system status. |
| `radarr_get_system_task` | `APITOOL` | Get system task. |
| `radarr_get_system_task_id` | `APITOOL` | Get specific system task. |
| `radarr_get_tag` | `APITOOL` | Get tag. |
| `radarr_get_tag_detail` | `APITOOL` | Get tag detail. |
| `radarr_get_tag_detail_id` | `APITOOL` | Get specific tag detail. |
| `radarr_get_tag_id` | `APITOOL` | Get specific tag. |
| `radarr_get_update` | `APITOOL` | Get update. |
| `radarr_get_wanted_cutoff` | `APITOOL` | Get wanted cutoff. |
| `radarr_get_wanted_missing` | `APITOOL` | Get wanted missing. |
| `radarr_lookup_movie` | `APITOOL` | Search for a movie using the lookup endpoint. |
| `radarr_post_autotagging` | `APITOOL` | Add a new autotagging. |
| `radarr_post_command` | `APITOOL` | Add a new command. |
| `radarr_post_customfilter` | `APITOOL` | Add a new customfilter. |
| `radarr_post_customformat` | `APITOOL` | Add a new customformat. |
| `radarr_post_delayprofile` | `APITOOL` | Add a new delayprofile. |
| `radarr_post_downloadclient` | `APITOOL` | Add a new downloadclient. |
| `radarr_post_downloadclient_action_name` | `APITOOL` | Add a new downloadclient action name. |
| `radarr_post_downloadclient_test` | `APITOOL` | Test downloadclient. |
| `radarr_post_downloadclient_testall` | `APITOOL` | Add a new downloadclient testall. |
| `radarr_post_exclusions` | `APITOOL` | Add a new exclusions. |
| `radarr_post_exclusions_bulk` | `APITOOL` | Add a new exclusions bulk. |
| `radarr_post_history_failed_id` | `APITOOL` | Add a new history failed id. |
| `radarr_post_importlist` | `APITOOL` | Add a new importlist. |
| `radarr_post_importlist_action_name` | `APITOOL` | Add a new importlist action name. |
| `radarr_post_importlist_movie` | `APITOOL` | Add a new importlist movie. |
| `radarr_post_importlist_test` | `APITOOL` | Test importlist. |
| `radarr_post_importlist_testall` | `APITOOL` | Add a new importlist testall. |
| `radarr_post_indexer` | `APITOOL` | Add a new indexer configuration. |
| `radarr_post_indexer_action_name` | `APITOOL` | Add a new indexer action name. |
| `radarr_post_indexer_test` | `APITOOL` | Test indexer. |
| `radarr_post_indexer_testall` | `APITOOL` | Add a new indexer testall. |
| `radarr_post_login` | `APITOOL` | Log in to the Radarr web interface. |
| `radarr_post_manualimport` | `APITOOL` | Add a new manualimport. |
| `radarr_post_metadata` | `APITOOL` | Add a new metadata. |
| `radarr_post_metadata_action_name` | `APITOOL` | Add a new metadata action name. |
| `radarr_post_metadata_test` | `APITOOL` | Test metadata. |
| `radarr_post_metadata_testall` | `APITOOL` | Add a new metadata testall. |
| `radarr_post_movie` | `APITOOL` | Add a new movie to Radarr. |
| `radarr_post_movie_import` | `APITOOL` | Add a new movie import. |
| `radarr_post_notification` | `APITOOL` | Add a new notification. |
| `radarr_post_notification_action_name` | `APITOOL` | Add a new notification action name. |
| `radarr_post_notification_test` | `APITOOL` | Test notification. |
| `radarr_post_notification_testall` | `APITOOL` | Add a new notification testall. |
| `radarr_post_qualityprofile` | `APITOOL` | Add a new qualityprofile. |
| `radarr_post_queue_grab_bulk` | `APITOOL` | Add a new queue grab bulk. |
| `radarr_post_queue_grab_id` | `APITOOL` | Add a new queue grab id. |
| `radarr_post_release` | `APITOOL` | Add a new release. |
| `radarr_post_release_push` | `APITOOL` | Add a new release push. |
| `radarr_post_releaseprofile` | `APITOOL` | Add a new releaseprofile. |
| `radarr_post_remotepathmapping` | `APITOOL` | Add a new remotepathmapping. |
| `radarr_post_rootfolder` | `APITOOL` | Add a new rootfolder. |
| `radarr_post_system_backup_restore_id` | `APITOOL` | Add a new system backup restore id. |
| `radarr_post_system_backup_restore_upload` | `APITOOL` | Add a new system backup restore upload. |
| `radarr_post_system_restart` | `APITOOL` | Add a new system restart. |
| `radarr_post_system_shutdown` | `APITOOL` | Add a new system shutdown. |
| `radarr_post_tag` | `APITOOL` | Add a new tag. |
| `radarr_put_autotagging_id` | `APITOOL` | Update autotagging id. |
| `radarr_put_collection` | `APITOOL` | Update collection. |
| `radarr_put_collection_id` | `APITOOL` | Update collection id. |
| `radarr_put_config_downloadclient_id` | `APITOOL` | Update config downloadclient id. |
| `radarr_put_config_host_id` | `APITOOL` | Update config host id. |
| `radarr_put_config_importlist_id` | `APITOOL` | Update config importlist id. |
| `radarr_put_config_indexer_id` | `APITOOL` | Update config indexer id. |
| `radarr_put_config_mediamanagement_id` | `APITOOL` | Update config mediamanagement id. |
| `radarr_put_config_metadata_id` | `APITOOL` | Update config metadata id. |
| `radarr_put_config_naming_id` | `APITOOL` | Update config naming id. |
| `radarr_put_config_ui_id` | `APITOOL` | Update config ui id. |
| `radarr_put_customfilter_id` | `APITOOL` | Update customfilter id. |
| `radarr_put_customformat_bulk` | `APITOOL` | Update customformat bulk. |
| `radarr_put_customformat_id` | `APITOOL` | Update customformat id. |
| `radarr_put_delayprofile_id` | `APITOOL` | Update delayprofile id. |
| `radarr_put_delayprofile_reorder_id` | `APITOOL` | Update delayprofile reorder id. |
| `radarr_put_downloadclient_bulk` | `APITOOL` | Update downloadclient bulk. |
| `radarr_put_downloadclient_id` | `APITOOL` | Update downloadclient id. |
| `radarr_put_exclusions_id` | `APITOOL` | Update exclusions id. |
| `radarr_put_importlist_bulk` | `APITOOL` | Update importlist bulk. |
| `radarr_put_importlist_id` | `APITOOL` | Update importlist id. |
| `radarr_put_indexer_bulk` | `APITOOL` | Update indexer bulk. |
| `radarr_put_indexer_id` | `APITOOL` | Update an existing indexer configuration by ID. |
| `radarr_put_metadata_id` | `APITOOL` | Update metadata id. |
| `radarr_put_movie_editor` | `APITOOL` | Update movie editor. |
| `radarr_put_movie_id` | `APITOOL` | Update an existing movie configuration. |
| `radarr_put_moviefile_bulk` | `APITOOL` | Update moviefile bulk. |
| `radarr_put_moviefile_editor` | `APITOOL` | Update moviefile editor. |
| `radarr_put_moviefile_id` | `APITOOL` | Update moviefile id. |
| `radarr_put_notification_id` | `APITOOL` | Update notification id. |
| `radarr_put_qualitydefinition_id` | `APITOOL` | Update qualitydefinition id. |
| `radarr_put_qualitydefinition_update` | `APITOOL` | Update qualitydefinition update. |
| `radarr_put_qualityprofile_id` | `APITOOL` | Update qualityprofile id. |
| `radarr_put_releaseprofile_id` | `APITOOL` | Update releaseprofile id. |
| `radarr_put_remotepathmapping_id` | `APITOOL` | Update remotepathmapping id. |
| `radarr_put_tag_id` | `APITOOL` | Update tag id. |
| `radarr_request` | `APITOOL` | Generic request method for the Radarr API. |
| `seerr_delete_request_id` | `APITOOL` | Delete a request |
| `seerr_get_auth_me` | `APITOOL` | Get logged-in user |
| `seerr_get_movie_id` | `APITOOL` | Get movie details |
| `seerr_get_request` | `APITOOL` | Get all requests |
| `seerr_get_request_id` | `APITOOL` | Get a specific request |
| `seerr_get_search` | `APITOOL` | Search for content |
| `seerr_get_status` | `APITOOL` | Get Seerr status |
| `seerr_get_status_appdata` | `APITOOL` | Get application data volume status |
| `seerr_get_tv_id` | `APITOOL` | Get TV details |
| `seerr_get_user` | `APITOOL` | Get all users |
| `seerr_get_user_id` | `APITOOL` | Get user details |
| `seerr_post_auth_jellyfin` | `APITOOL` | Sign in using a Jellyfin username and password |
| `seerr_post_auth_local` | `APITOOL` | Sign in using a local account |
| `seerr_post_auth_logout` | `APITOOL` | Sign out and clear session cookie |
| `seerr_post_auth_plex` | `APITOOL` | Sign in using a Plex token |
| `seerr_post_request` | `APITOOL` | Create a new request |
| `seerr_post_request_id_approve` | `APITOOL` | Approve a request |
| `seerr_post_request_id_decline` | `APITOOL` | Decline a request |
| `seerr_put_request_id` | `APITOOL` | Update a request |
| `seerr_request` | `APITOOL` | Generic request method for the Seerr API. |
| `sonarr_add_series` | `APITOOL` | Lookup a series by term, pick the first result, and add it to Sonarr. |
| `sonarr_delete_autotagging_id` | `APITOOL` | Delete an auto-tagging rule by ID. |
| `sonarr_delete_blocklist_bulk` | `APITOOL` | Delete blocklist bulk. |
| `sonarr_delete_blocklist_id` | `APITOOL` | Delete a blocklisted item by ID. |
| `sonarr_delete_command_id` | `APITOOL` | Delete command id. |
| `sonarr_delete_customfilter_id` | `APITOOL` | Delete customfilter id. |
| `sonarr_delete_customformat_bulk` | `APITOOL` | Delete customformat bulk. |
| `sonarr_delete_customformat_id` | `APITOOL` | Delete customformat id. |
| `sonarr_delete_delayprofile_id` | `APITOOL` | Delete delayprofile id. |
| `sonarr_delete_downloadclient_bulk` | `APITOOL` | Delete downloadclient bulk. |
| `sonarr_delete_downloadclient_id` | `APITOOL` | Delete downloadclient id. |
| `sonarr_delete_episodefile_bulk` | `APITOOL` | Delete episodefile bulk. |
| `sonarr_delete_episodefile_id` | `APITOOL` | Delete episodefile id. |
| `sonarr_delete_importlist_bulk` | `APITOOL` | Delete importlist bulk. |
| `sonarr_delete_importlist_id` | `APITOOL` | Delete an import list configuration by ID. |
| `sonarr_delete_importlistexclusion_bulk` | `APITOOL` | Delete importlistexclusion bulk. |
| `sonarr_delete_importlistexclusion_id` | `APITOOL` | Delete importlistexclusion id. |
| `sonarr_delete_indexer_bulk` | `APITOOL` | Delete indexer bulk. |
| `sonarr_delete_indexer_id` | `APITOOL` | Delete an indexer configuration by ID. |
| `sonarr_delete_languageprofile_id` | `APITOOL` | Delete languageprofile id. |
| `sonarr_delete_metadata_id` | `APITOOL` | Delete metadata id. |
| `sonarr_delete_notification_id` | `APITOOL` | Delete notification id. |
| `sonarr_delete_qualityprofile_id` | `APITOOL` | Delete qualityprofile id. |
| `sonarr_delete_queue_bulk` | `APITOOL` | Delete queue bulk. |
| `sonarr_delete_queue_id` | `APITOOL` | Delete queue id. |
| `sonarr_delete_releaseprofile_id` | `APITOOL` | Delete releaseprofile id. |
| `sonarr_delete_remotepathmapping_id` | `APITOOL` | Delete remotepathmapping id. |
| `sonarr_delete_rootfolder_id` | `APITOOL` | Delete rootfolder id. |
| `sonarr_delete_series_editor` | `APITOOL` | Delete series editor. |
| `sonarr_delete_series_id` | `APITOOL` | Delete series. |
| `sonarr_delete_system_backup_id` | `APITOOL` | Delete a system backup file by ID. |
| `sonarr_delete_tag_id` | `APITOOL` | Delete a tag. |
| `sonarr_get_` | `APITOOL` | Get resource by path. |
| `sonarr_get_api` | `APITOOL` | Get the base API information. |
| `sonarr_get_autotagging` | `APITOOL` | Get all auto-tagging rules. |
| `sonarr_get_autotagging_id` | `APITOOL` | Get details for a specific auto-tagging rule by ID. |
| `sonarr_get_autotagging_schema` | `APITOOL` | Get the schema for auto-tagging rules. |
| `sonarr_get_blocklist` | `APITOOL` | Get blocklist. |
| `sonarr_get_calendar` | `APITOOL` | Get calendar. |
| `sonarr_get_calendar_id` | `APITOOL` | Get specific calendar. |
| `sonarr_get_command` | `APITOOL` | Get command. |
| `sonarr_get_command_id` | `APITOOL` | Get specific command. |
| `sonarr_get_config_downloadclient` | `APITOOL` | Get config downloadclient. |
| `sonarr_get_config_downloadclient_id` | `APITOOL` | Get specific config downloadclient. |
| `sonarr_get_config_host` | `APITOOL` | Get config host. |
| `sonarr_get_config_host_id` | `APITOOL` | Get specific config host. |
| `sonarr_get_config_importlist` | `APITOOL` | Get config importlist. |
| `sonarr_get_config_importlist_id` | `APITOOL` | Get specific config importlist. |
| `sonarr_get_config_indexer` | `APITOOL` | Get config indexer. |
| `sonarr_get_config_indexer_id` | `APITOOL` | Get specific config indexer. |
| `sonarr_get_config_mediamanagement` | `APITOOL` | Get config mediamanagement. |
| `sonarr_get_config_mediamanagement_id` | `APITOOL` | Get specific config mediamanagement. |
| `sonarr_get_config_naming` | `APITOOL` | Get config naming. |
| `sonarr_get_config_naming_examples` | `APITOOL` | Get config naming examples. |
| `sonarr_get_config_naming_id` | `APITOOL` | Get specific config naming. |
| `sonarr_get_config_ui` | `APITOOL` | Get UI configuration. |
| `sonarr_get_config_ui_id` | `APITOOL` | Get specific UI configuration. |
| `sonarr_get_content_path` | `APITOOL` | Get content path. |
| `sonarr_get_customfilter` | `APITOOL` | Get customfilter. |
| `sonarr_get_customfilter_id` | `APITOOL` | Get specific customfilter. |
| `sonarr_get_customformat` | `APITOOL` | Get customformat. |
| `sonarr_get_customformat_id` | `APITOOL` | Get specific customformat. |
| `sonarr_get_customformat_schema` | `APITOOL` | Get customformat schema. |
| `sonarr_get_delayprofile` | `APITOOL` | Get delayprofile. |
| `sonarr_get_delayprofile_id` | `APITOOL` | Get specific delayprofile. |
| `sonarr_get_diskspace` | `APITOOL` | Get diskspace. |
| `sonarr_get_downloadclient` | `APITOOL` | Get downloadclient. |
| `sonarr_get_downloadclient_id` | `APITOOL` | Get specific downloadclient. |
| `sonarr_get_downloadclient_schema` | `APITOOL` | Get downloadclient schema. |
| `sonarr_get_episode` | `APITOOL` | Get episode. |
| `sonarr_get_episode_id` | `APITOOL` | Get specific episode. |
| `sonarr_get_episodefile` | `APITOOL` | Get episodefile. |
| `sonarr_get_episodefile_id` | `APITOOL` | Get specific episodefile. |
| `sonarr_get_feed_v3_calendar_sonarrics` | `APITOOL` | Get feed v3 calendar sonarrics. |
| `sonarr_get_filesystem` | `APITOOL` | Get filesystem. |
| `sonarr_get_filesystem_mediafiles` | `APITOOL` | Get filesystem mediafiles. |
| `sonarr_get_filesystem_type` | `APITOOL` | Get filesystem type. |
| `sonarr_get_health` | `APITOOL` | Get health. |
| `sonarr_get_history` | `APITOOL` | Get history. |
| `sonarr_get_history_series` | `APITOOL` | Get history series. |
| `sonarr_get_history_since` | `APITOOL` | Get history since. |
| `sonarr_get_importlist` | `APITOOL` | Get importlist. |
| `sonarr_get_importlist_id` | `APITOOL` | Get details for a specific import list by ID. |
| `sonarr_get_importlist_schema` | `APITOOL` | Get importlist schema. |
| `sonarr_get_importlistexclusion` | `APITOOL` | Get importlistexclusion. |
| `sonarr_get_importlistexclusion_id` | `APITOOL` | Get specific importlistexclusion. |
| `sonarr_get_importlistexclusion_paged` | `APITOOL` | Get importlistexclusion paged. |
| `sonarr_get_indexer` | `APITOOL` | Get indexer. |
| `sonarr_get_indexer_id` | `APITOOL` | Get specific indexer. |
| `sonarr_get_indexer_schema` | `APITOOL` | Get indexer schema. |
| `sonarr_get_indexerflag` | `APITOOL` | Get indexerflag. |
| `sonarr_get_language` | `APITOOL` | Get language. |
| `sonarr_get_language_id` | `APITOOL` | Get specific language. |
| `sonarr_get_languageprofile` | `APITOOL` | Get languageprofile. |
| `sonarr_get_languageprofile_id` | `APITOOL` | Get specific languageprofile. |
| `sonarr_get_languageprofile_schema` | `APITOOL` | Get languageprofile schema. |
| `sonarr_get_localization` | `APITOOL` | Get localization. |
| `sonarr_get_localization_id` | `APITOOL` | Get specific localization. |
| `sonarr_get_localization_language` | `APITOOL` | Get localization language. |
| `sonarr_get_log` | `APITOOL` | Get log. |
| `sonarr_get_log_file` | `APITOOL` | Get log file. |
| `sonarr_get_log_file_filename` | `APITOOL` | Get log file filename. |
| `sonarr_get_log_file_update` | `APITOOL` | Get log file update. |
| `sonarr_get_log_file_update_filename` | `APITOOL` | Get log file update content. |
| `sonarr_get_login` | `APITOOL` | Get the login status and information. |
| `sonarr_get_logout` | `APITOOL` | Log out from the Sonarr web interface. |
| `sonarr_get_manualimport` | `APITOOL` | Get manualimport. |
| `sonarr_get_mediacover_series_id_filename` | `APITOOL` | Get specific mediacover series filename. |
| `sonarr_get_metadata` | `APITOOL` | Get metadata. |
| `sonarr_get_metadata_id` | `APITOOL` | Get specific metadata. |
| `sonarr_get_metadata_schema` | `APITOOL` | Get metadata schema. |
| `sonarr_get_notification` | `APITOOL` | Get notification. |
| `sonarr_get_notification_id` | `APITOOL` | Get specific notification. |
| `sonarr_get_notification_schema` | `APITOOL` | Get notification schema. |
| `sonarr_get_parse` | `APITOOL` | Get parse. |
| `sonarr_get_path` | `APITOOL` | Get system routes. |
| `sonarr_get_ping` | `APITOOL` | Ping the Sonarr API to check connectivity. |
| `sonarr_get_qualitydefinition` | `APITOOL` | Get all quality definitions. |
| `sonarr_get_qualitydefinition_id` | `APITOOL` | Get a specific quality definition by ID. |
| `sonarr_get_qualitydefinition_limits` | `APITOOL` | Get qualitydefinition limits. |
| `sonarr_get_qualityprofile` | `APITOOL` | Get qualityprofile. |
| `sonarr_get_qualityprofile_id` | `APITOOL` | Get specific qualityprofile. |
| `sonarr_get_qualityprofile_schema` | `APITOOL` | Get qualityprofile schema. |
| `sonarr_get_queue` | `APITOOL` | Get queue. |
| `sonarr_get_queue_details` | `APITOOL` | Get queue details. |
| `sonarr_get_queue_status` | `APITOOL` | Get queue status. |
| `sonarr_get_release` | `APITOOL` | Get release. |
| `sonarr_get_releaseprofile` | `APITOOL` | Get releaseprofile. |
| `sonarr_get_releaseprofile_id` | `APITOOL` | Get specific releaseprofile. |
| `sonarr_get_remotepathmapping` | `APITOOL` | Get remotepathmapping. |
| `sonarr_get_remotepathmapping_id` | `APITOOL` | Get specific remotepathmapping. |
| `sonarr_get_rename` | `APITOOL` | Get rename. |
| `sonarr_get_rootfolder` | `APITOOL` | Get rootfolder. |
| `sonarr_get_rootfolder_id` | `APITOOL` | Get specific rootfolder. |
| `sonarr_get_series` | `APITOOL` | Get series. |
| `sonarr_get_series_id` | `APITOOL` | Get specific series. |
| `sonarr_get_series_id_folder` | `APITOOL` | Get series folder. |
| `sonarr_get_series_lookup` | `APITOOL` | Lookup series. |
| `sonarr_get_system_backup` | `APITOOL` | Get information about available system backups. |
| `sonarr_get_system_routes` | `APITOOL` | Get system routes. |
| `sonarr_get_system_routes_duplicate` | `APITOOL` | Get duplicate system routes. |
| `sonarr_get_system_status` | `APITOOL` | Get system status. |
| `sonarr_get_system_task` | `APITOOL` | Get system tasks. |
| `sonarr_get_system_task_id` | `APITOOL` | Get specific system task. |
| `sonarr_get_tag` | `APITOOL` | Get tags. |
| `sonarr_get_tag_detail` | `APITOOL` | Get tag usage details. |
| `sonarr_get_tag_detail_id` | `APITOOL` | Get specific tag usage details. |
| `sonarr_get_tag_id` | `APITOOL` | Get specific tag. |
| `sonarr_get_update` | `APITOOL` | Get available updates. |
| `sonarr_get_wanted_cutoff` | `APITOOL` | Get wanted cutoff. |
| `sonarr_get_wanted_cutoff_id` | `APITOOL` | Get specific wanted cutoff. |
| `sonarr_get_wanted_missing` | `APITOOL` | Get wanted missing. |
| `sonarr_get_wanted_missing_id` | `APITOOL` | Get specific wanted missing. |
| `sonarr_lookup_series` | `APITOOL` | Search for a series using the lookup endpoint. |
| `sonarr_post_autotagging` | `APITOOL` | Add a new auto-tagging rule. |
| `sonarr_post_command` | `APITOOL` | Add a new command. |
| `sonarr_post_customfilter` | `APITOOL` | Add a new customfilter. |
| `sonarr_post_customformat` | `APITOOL` | Add a new customformat. |
| `sonarr_post_delayprofile` | `APITOOL` | Add a new delayprofile. |
| `sonarr_post_downloadclient` | `APITOOL` | Add a new downloadclient. |
| `sonarr_post_downloadclient_action_name` | `APITOOL` | Add a new downloadclient action name. |
| `sonarr_post_downloadclient_test` | `APITOOL` | Test downloadclient. |
| `sonarr_post_downloadclient_testall` | `APITOOL` | Add a new downloadclient testall. |
| `sonarr_post_history_failed_id` | `APITOOL` | Add a new history failed id. |
| `sonarr_post_importlist` | `APITOOL` | Add a new import list configuration. |
| `sonarr_post_importlist_action_name` | `APITOOL` | Add a new importlist action name. |
| `sonarr_post_importlist_test` | `APITOOL` | Test importlist. |
| `sonarr_post_importlist_testall` | `APITOOL` | Add a new importlist testall. |
| `sonarr_post_importlistexclusion` | `APITOOL` | Add a new importlistexclusion. |
| `sonarr_post_indexer` | `APITOOL` | Add a new indexer configuration. |
| `sonarr_post_indexer_action_name` | `APITOOL` | Add a new indexer action name. |
| `sonarr_post_indexer_test` | `APITOOL` | Test indexer. |
| `sonarr_post_indexer_testall` | `APITOOL` | Add a new indexer testall. |
| `sonarr_post_languageprofile` | `APITOOL` | Add a new languageprofile. |
| `sonarr_post_login` | `APITOOL` | Log in to the Sonarr web interface. |
| `sonarr_post_manualimport` | `APITOOL` | Add a new manualimport. |
| `sonarr_post_metadata` | `APITOOL` | Add a new metadata. |
| `sonarr_post_metadata_action_name` | `APITOOL` | Add a new metadata action name. |
| `sonarr_post_metadata_test` | `APITOOL` | Test metadata. |
| `sonarr_post_metadata_testall` | `APITOOL` | Add a new metadata testall. |
| `sonarr_post_notification` | `APITOOL` | Add a new notification. |
| `sonarr_post_notification_action_name` | `APITOOL` | Add a new notification action name. |
| `sonarr_post_notification_test` | `APITOOL` | Test notification. |
| `sonarr_post_notification_testall` | `APITOOL` | Add a new notification testall. |
| `sonarr_post_qualityprofile` | `APITOOL` | Add a new qualityprofile. |
| `sonarr_post_queue_grab_bulk` | `APITOOL` | Add a new queue grab bulk. |
| `sonarr_post_queue_grab_id` | `APITOOL` | Add a new queue grab id. |
| `sonarr_post_release` | `APITOOL` | Add a new release. |
| `sonarr_post_release_push` | `APITOOL` | Add a new release push. |
| `sonarr_post_releaseprofile` | `APITOOL` | Add a new releaseprofile. |
| `sonarr_post_remotepathmapping` | `APITOOL` | Add a new remotepathmapping. |
| `sonarr_post_rootfolder` | `APITOOL` | Add a new rootfolder. |
| `sonarr_post_seasonpass` | `APITOOL` | Add a new seasonpass. |
| `sonarr_post_series` | `APITOOL` | Add a new series. |
| `sonarr_post_series_import` | `APITOOL` | Import series. |
| `sonarr_post_system_backup_restore_id` | `APITOOL` | Add a new system backup restore id. |
| `sonarr_post_system_backup_restore_upload` | `APITOOL` | Add a new system backup restore upload. |
| `sonarr_post_system_restart` | `APITOOL` | Trigger system restart. |
| `sonarr_post_system_shutdown` | `APITOOL` | Trigger system shutdown. |
| `sonarr_post_tag` | `APITOOL` | Add a new tag. |
| `sonarr_put_autotagging_id` | `APITOOL` | Update an existing auto-tagging rule by ID. |
| `sonarr_put_config_downloadclient_id` | `APITOOL` | Update config downloadclient id. |
| `sonarr_put_config_host_id` | `APITOOL` | Update config host id. |
| `sonarr_put_config_importlist_id` | `APITOOL` | Update config importlist id. |
| `sonarr_put_config_indexer_id` | `APITOOL` | Update config indexer id. |
| `sonarr_put_config_mediamanagement_id` | `APITOOL` | Update config mediamanagement id. |
| `sonarr_put_config_naming_id` | `APITOOL` | Update config naming id. |
| `sonarr_put_config_ui_id` | `APITOOL` | Update UI configuration. |
| `sonarr_put_customfilter_id` | `APITOOL` | Update customfilter id. |
| `sonarr_put_customformat_bulk` | `APITOOL` | Update customformat bulk. |
| `sonarr_put_customformat_id` | `APITOOL` | Update customformat id. |
| `sonarr_put_delayprofile_id` | `APITOOL` | Update delayprofile id. |
| `sonarr_put_delayprofile_reorder_id` | `APITOOL` | Update delayprofile reorder id. |
| `sonarr_put_downloadclient_bulk` | `APITOOL` | Update downloadclient bulk. |
| `sonarr_put_downloadclient_id` | `APITOOL` | Update downloadclient id. |
| `sonarr_put_episode_id` | `APITOOL` | Update episode id. |
| `sonarr_put_episode_monitor` | `APITOOL` | Update episode monitor. |
| `sonarr_put_episodefile_bulk` | `APITOOL` | Update episodefile bulk. |
| `sonarr_put_episodefile_editor` | `APITOOL` | Update episodefile editor. |
| `sonarr_put_episodefile_id` | `APITOOL` | Update episodefile id. |
| `sonarr_put_importlist_bulk` | `APITOOL` | Update importlist bulk. |
| `sonarr_put_importlist_id` | `APITOOL` | Update an existing import list configuration. |
| `sonarr_put_importlistexclusion_id` | `APITOOL` | Update importlistexclusion id. |
| `sonarr_put_indexer_bulk` | `APITOOL` | Update indexer bulk. |
| `sonarr_put_indexer_id` | `APITOOL` | Update an existing indexer configuration by ID. |
| `sonarr_put_languageprofile_id` | `APITOOL` | Update languageprofile id. |
| `sonarr_put_metadata_id` | `APITOOL` | Update metadata id. |
| `sonarr_put_notification_id` | `APITOOL` | Update notification id. |
| `sonarr_put_qualitydefinition_id` | `APITOOL` | Update qualitydefinition id. |
| `sonarr_put_qualitydefinition_update` | `APITOOL` | Update qualitydefinition update. |
| `sonarr_put_qualityprofile_id` | `APITOOL` | Update qualityprofile id. |
| `sonarr_put_releaseprofile_id` | `APITOOL` | Update releaseprofile id. |
| `sonarr_put_remotepathmapping_id` | `APITOOL` | Update remotepathmapping id. |
| `sonarr_put_series_editor` | `APITOOL` | Update series editor. |
| `sonarr_put_series_id` | `APITOOL` | Update series id. |
| `sonarr_put_tag_id` | `APITOOL` | Update a tag. |
| `sonarr_request` | `APITOOL` | Generic request method for the Sonarr API. |

</details>

_7 action-routed tool(s) (default) · 1123 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md#mcp-tools](docs/index.md#mcp-tools).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

> **Install the slim `[mcp]` extra.** All examples below install
> `arr-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

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
        "SONARR_BASE_URL": "http://localhost:8989",
        "SONARR_TOKEN": "your_sonarr_token_here",
        "RADARR_BASE_URL": "http://localhost:7878",
        "RADARR_TOKEN": "your_radarr_token_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

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
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "SONARR_BASE_URL": "http://localhost:8989",
        "SONARR_TOKEN": "your_sonarr_token_here",
        "RADARR_BASE_URL": "http://localhost:7878",
        "RADARR_TOKEN": "your_radarr_token_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "arr-mcp": {
      "url": "http://localhost:8000/arr-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name arr-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e SONARR_BASE_URL="http://localhost:8989" \
  -e SONARR_TOKEN="your_value" \
  -e RADARR_BASE_URL="http://localhost:7878" \
  -e RADARR_TOKEN="your_value" \
  knucklessg1/arr-mcp:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `arr-mcp[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `arr-mcp[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `arr-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`arr-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/arr-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://arr-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export SONARR_BASE_URL="http://localhost:8989"
export SONARR_TOKEN="your_value"
export RADARR_BASE_URL="http://localhost:7878"
export RADARR_TOKEN="your_value"

# Run the agent server
arr-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  arr-mcp-mcp:
    image: knucklessg1/arr-mcp:mcp
    container_name: arr-mcp-mcp
    hostname: arr-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  arr-mcp-agent:
    image: knucklessg1/arr-mcp:latest
    container_name: arr-mcp-agent
    hostname: arr-mcp-agent
    restart: always
    depends_on:
      - arr-mcp-mcp
    env_file:
      - ../.env
    command: [ "arr-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9099
      - MCP_URL=http://arr-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9099:9099"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9099/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/index.md#a2a-agent](docs/index.md#a2a-agent).

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `SONARR_BASE_URL` | `http://localhost:8989` | Sonarr Client |
| `SONARR_TOKEN` | `your_sonarr_token_here` |  |
| `SONARR_SSL_VERIFY` | `False` |  |
| `RADARR_BASE_URL` | `http://localhost:7878` | Radarr Client |
| `RADARR_TOKEN` | `your_radarr_token_here` |  |
| `RADARR_SSL_VERIFY` | `False` |  |
| `LIDARR_BASE_URL` | `http://localhost:8686` | Lidarr Client |
| `LIDARR_TOKEN` | `your_lidarr_token_here` |  |
| `LIDARR_SSL_VERIFY` | `False` |  |
| `PROWLARR_BASE_URL` | `http://localhost:9696` | Prowlarr Client |
| `PROWLARR_TOKEN` | `your_prowlarr_token_here` |  |
| `PROWLARR_SSL_VERIFY` | `False` |  |
| `BAZARR_BASE_URL` | `http://localhost:6767` | Bazarr Client |
| `BAZARR_API_KEY` | `your_bazarr_api_key_here` |  |
| `BAZARR_SSL_VERIFY` | `False` |  |
| `SEERR_BASE_URL` | `http://localhost:5055` | Seerr Client |
| `SEERR_API_KEY` | `your_seerr_api_key_here` |  |
| `SEERR_SSL_VERIFY` | `False` |  |
| `CHAPTARR_BASE_URL` | `http://localhost:8006` | Chaptarr Client |
| `CHAPTARR_TOKEN` | `your_chaptarr_token_here` |  |
| `CHAPTARR_SSL_VERIFY` | `False` |  |
| `SONARRTOOL` | `True` | MCP tools table (condensed action-routed surface). |
| `RADARRTOOL` | `True` |  |
| `LIDARRTOOL` | `True` |  |
| `PROWLARRTOOL` | `True` |  |
| `BAZARRTOOL` | `True` |  |
| `SEERRTOOL` | `True` |  |
| `CHAPTARRTOOL` | `True` |  |
| `DEFAULT_AGENT_NAME` | `Arr Mcp` |  |
| `AUTH_TYPE` | — |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_41 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by concern. arr-mcp fronts seven independent
*arr services — each is wired by setting that service's `_BASE_URL` and
`_TOKEN`/`_API_KEY` (plus an optional `_SSL_VERIFY` flag).

### Connection & Credentials — per service
Each service accepts a `_BASE_URL`, an auth token (`_TOKEN` for
Sonarr/Radarr/Lidarr/Prowlarr/Chaptarr; `_API_KEY` for Bazarr/Seerr), and a `_SSL_VERIFY` flag.

| Variable | Description | Default |
|----------|-------------|---------|
| `SONARR_BASE_URL` / `SONARR_TOKEN` / `SONARR_SSL_VERIFY` | Sonarr connection + API token + TLS verify | — / — / `False` |
| `RADARR_BASE_URL` / `RADARR_TOKEN` / `RADARR_SSL_VERIFY` | Radarr connection + API token + TLS verify | — / — / `False` |
| `LIDARR_BASE_URL` / `LIDARR_TOKEN` / `LIDARR_SSL_VERIFY` | Lidarr connection + API token + TLS verify | — / — / `False` |
| `PROWLARR_BASE_URL` / `PROWLARR_TOKEN` / `PROWLARR_SSL_VERIFY` | Prowlarr connection + API token + TLS verify | — / — / `False` |
| `BAZARR_BASE_URL` / `BAZARR_API_KEY` / `BAZARR_SSL_VERIFY` | Bazarr connection + API key + TLS verify | — / — / `False` |
| `SEERR_BASE_URL` / `SEERR_API_KEY` / `SEERR_SSL_VERIFY` | Seerr connection + API key + TLS verify | — / — / `False` |
| `CHAPTARR_BASE_URL` / `CHAPTARR_TOKEN` / `CHAPTARR_SSL_VERIFY` | Chaptarr connection + API token + TLS verify | — / — / `False` |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above
(e.g. `SONARRTOOL`, `RADARRTOOL`, `PROWLARRTOOL`, `BAZARRTOOL`, `SEERRTOOL`, `CHAPTARRTOOL`,
`LIDARRTOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |
| `DEFAULT_AGENT_NAME` | Custom name for the Graph Agent | `Arr Mcp` |
| `AUTH_TYPE` | Authentication type for A2A endpoints | — |

See [`.env.example`](.env.example) for a copy-paste starting point.

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `arr-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `arr-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `arr-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "arr-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "arr-mcp[agent]"

# Everything (development)
uv pip install "arr-mcp[all]"      # or: python -m pip install "arr-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/arr-mcp:mcp` | `--target mcp` | `arr-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `arr-mcp` |
| `knucklessg1/arr-mcp:latest` | `--target agent` (default) | `arr-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `arr-agent` |

```bash
docker build --target mcp   -t knucklessg1/arr-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/arr-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Usage & Quick Start

To launch and run `arr-mcp` services:

### 1. Launching the MCP Server
Launch the MCP server in standard I/O mode (ideal for IDEs):
```bash
arr-mcp
```

Or launch it as a Streamable-HTTP server on port `8000`:
```bash
arr-mcp --transport streamable-http --port 8000
```

### 2. Running the Graph Agent Server
Start the interactive Pydantic AI Graph Agent CLI with OIDC token delegation and Eunomia policies:
```bash
arr-agent --provider openai --model-id gpt-4o
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/arr-mcp/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/arr-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/arr-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/arr-mcp/usage/) | the MCP tools, the Python API clients, the CLI |
| [Backing Platform](https://knuckles-team.github.io/arr-mcp/platform/) | provision the Arr Suite services with Docker |
| [Overview](https://knuckles-team.github.io/arr-mcp/overview/) | ecosystem role, enterprise readiness, configuration |
| [Concepts](https://knuckles-team.github.io/arr-mcp/concepts/) | concept registry (`CONCEPT:ARR-*`) |

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `arr-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx arr-mcp` · or `uv tool install arr-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/arr-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
