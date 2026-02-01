---
name: sonarr-series
description: "Generated skill for Series operations. Contains 5 tools."
---

### Overview
This skill handles operations related to Series.

### Available Tools
- `get_series`: No description
  - **Parameters**:
    - `tvdbId` (int)
    - `includeSeasonImages` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_series`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_series_id`: No description
  - **Parameters**:
    - `id` (int)
    - `includeSeasonImages` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_series_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `moveFiles` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_series_id`: No description
  - **Parameters**:
    - `id` (int)
    - `deleteFiles` (bool)
    - `addImportListExclusion` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
