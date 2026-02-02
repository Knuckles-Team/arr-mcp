---
name: radarr-import-list-movies
description: "Generated skill for ImportListMovies operations. Contains 2 tools."
---

### Overview
This skill handles operations related to ImportListMovies.

### Available Tools
- `get_importlist_movie`: No description
  - **Parameters**:
    - `includeRecommendations` (bool)
    - `includeTrending` (bool)
    - `includePopular` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_importlist_movie`: No description
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
