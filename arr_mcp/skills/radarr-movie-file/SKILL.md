---
name: radarr-movie-file
description: "Generated skill for MovieFile operations. Contains 7 tools."
---

### Overview
This skill handles operations related to MovieFile.

### Available Tools
- `get_moviefile`: No description
  - **Parameters**:
    - `movieId` (List)
    - `movieFileIds` (List)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_moviefile_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `delete_moviefile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_moviefile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_moviefile_editor`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `delete_moviefile_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_moviefile_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
