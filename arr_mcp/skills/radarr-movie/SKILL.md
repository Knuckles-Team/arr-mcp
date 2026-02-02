---
name: radarr-movie
description: "Generated skill for Movie operations. Contains 5 tools."
---

### Overview
This skill handles operations related to Movie.

### Available Tools
- `get_movie`: No description
  - **Parameters**:
    - `tmdbId` (int)
    - `excludeLocalCovers` (bool)
    - `languageId` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_movie`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_movie_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `moveFiles` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `delete_movie_id`: No description
  - **Parameters**:
    - `id` (int)
    - `deleteFiles` (bool)
    - `addImportExclusion` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_movie_id`: No description
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
