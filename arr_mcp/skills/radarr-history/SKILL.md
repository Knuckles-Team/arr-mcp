---
name: radarr-history
description: "Generated skill for History operations. Contains 4 tools."
tags: [radarr-history]
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
    - `includeMovie` (bool)
    - `eventType` (List)
    - `downloadId` (str)
    - `movieIds` (List)
    - `languages` (List)
    - `quality` (List)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_history_since`: No description
  - **Parameters**:
    - `date` (str)
    - `eventType` (str)
    - `includeMovie` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_history_movie`: No description
  - **Parameters**:
    - `movieId` (int)
    - `eventType` (str)
    - `includeMovie` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_history_failed_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
