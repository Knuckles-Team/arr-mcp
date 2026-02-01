---
name: radarr-collection
description: "Generated skill for Collection operations. Contains 4 tools."
---

### Overview
This skill handles operations related to Collection.

### Available Tools
- `get_collection`: No description
  - **Parameters**:
    - `tmdbId` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_collection`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_collection_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_collection_id`: No description
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
