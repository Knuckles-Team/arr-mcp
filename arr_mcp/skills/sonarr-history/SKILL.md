---
name: sonarr-history
description: "Generated skill for History operations. Contains 4 tools."
tags: [sonarr, history]
---

### Overview
This skill handles operations related to History.

### Available Tools
- `get_history`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `eventType` (List)
    - `episodeId` (int)
    - `downloadId` (str)
    - `seriesIds` (List)
    - `languages` (List)
    - `quality` (List)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_history_since`: No description
  - **Parameters**:
    - `date` (str)
    - `eventType` (str)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_history_series`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `seasonNumber` (int)
    - `eventType` (str)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_history_failed_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
