---
name: radarr-movie-lookup
description: "Generated skill for MovieLookup operations. Contains 3 tools."
---

### Overview
This skill handles operations related to MovieLookup.

### Available Tools
- `get_movie_lookup_tmdb`: No description
  - **Parameters**:
    - `tmdbId` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_movie_lookup_imdb`: No description
  - **Parameters**:
    - `imdbId` (str)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_movie_lookup`: No description
  - **Parameters**:
    - `term` (str)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
