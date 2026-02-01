---
name: lidarr-history
description: "Generated skill for History operations. Contains 4 tools."
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
    - `includeArtist` (bool)
    - `includeAlbum` (bool)
    - `includeTrack` (bool)
    - `eventType` (List)
    - `albumId` (int)
    - `downloadId` (str)
    - `artistIds` (List)
    - `quality` (List)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_history_since`: No description
  - **Parameters**:
    - `date` (str)
    - `eventType` (str)
    - `includeArtist` (bool)
    - `includeAlbum` (bool)
    - `includeTrack` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_history_artist`: No description
  - **Parameters**:
    - `artistId` (int)
    - `albumId` (int)
    - `eventType` (str)
    - `includeArtist` (bool)
    - `includeAlbum` (bool)
    - `includeTrack` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `post_history_failed_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
