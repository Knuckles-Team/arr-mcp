---
name: sonarr-release
description: "Generated skill for Release operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Release.

### Available Tools
- `post_release`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_release`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `episodeId` (int)
    - `seasonNumber` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
