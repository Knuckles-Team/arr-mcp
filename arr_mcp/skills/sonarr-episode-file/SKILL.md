---
name: sonarr-episode-file
description: "Generated skill for EpisodeFile operations. Contains 7 tools."
---

### Overview
This skill handles operations related to EpisodeFile.

### Available Tools
- `get_episodefile`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `episodeFileIds` (List)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_episodefile_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_episodefile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_episodefile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_episodefile_editor`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_episodefile_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_episodefile_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
