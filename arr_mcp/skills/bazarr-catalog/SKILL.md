---
name: bazarr-catalog
description: "Generated skill for Catalog operations. Contains 11 tools."
tags: [bazarr-catalog]
---

### Overview
This skill handles operations related to Catalog.

### Available Tools
- `get_series`: Get all series managed by Bazarr.
  - **Parameters**:
    - `page` (int)
    - `page_size` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_series_subtitles`: Get subtitle information for a specific series.
  - **Parameters**:
    - `series_id` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_episode_subtitles`: Get subtitle information for a specific episode.
  - **Parameters**:
    - `episode_id` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `search_series_subtitles`: Search for subtitles for a series or episode. Note: This triggers a search, it doesn't just list them.
  - **Parameters**:
    - `series_id` (int)
    - `episode_id` (Optional[int])
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `download_series_subtitle`: Download a subtitle for an episode.
  - **Parameters**:
    - `episode_id` (int)
    - `language` (str)
    - `forced` (bool)
    - `hi` (bool)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_movies`: Get all movies managed by Bazarr.
  - **Parameters**:
    - `page` (int)
    - `page_size` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_movie_subtitles`: Get subtitle information for a specific movie.
  - **Parameters**:
    - `movie_id` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `search_movie_subtitles`: Search for subtitles for a movie. Note: This triggers a search, it doesn't just list them.
  - **Parameters**:
    - `movie_id` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `download_movie_subtitle`: Download a subtitle for a movie.
  - **Parameters**:
    - `movie_id` (int)
    - `language` (str)
    - `forced` (bool)
    - `hi` (bool)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_wanted_series`: Get series episodes with wanted/missing subtitles.
  - **Parameters**:
    - `page` (int)
    - `page_size` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_wanted_movies`: Get movies with wanted/missing subtitles.
  - **Parameters**:
    - `page` (int)
    - `page_size` (int)
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
