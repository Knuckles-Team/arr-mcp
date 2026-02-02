---
name: sonarr-episode
description: "Generated skill for Episode operations. Contains 4 tools."
---

### Overview
This skill handles operations related to Episode.

### Available Tools
- `get_episode`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `seasonNumber` (int)
    - `episodeIds` (List)
    - `episodeFileId` (int)
    - `includeSeries` (bool)
    - `includeEpisodeFile` (bool)
    - `includeImages` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_episode_id`: No description
  - **Parameters**:
    - `id` (int)
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_episode_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_episode_monitor`: No description
  - **Parameters**:
    - `data` (Dict)
    - `includeImages` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
