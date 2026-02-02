---
name: lidarr-artist
description: "Generated skill for Artist operations. Contains 5 tools."
---

### Overview
This skill handles operations related to Artist.

### Available Tools
- `get_artist_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_artist_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `moveFiles` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `delete_artist_id`: No description
  - **Parameters**:
    - `id` (int)
    - `deleteFiles` (bool)
    - `addImportListExclusion` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_artist`: No description
  - **Parameters**:
    - `mbId` (str)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `post_artist`: No description
  - **Parameters**:
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
