---
name: lidarr-auto-tagging
description: "Generated skill for AutoTagging operations. Contains 6 tools."
---

### Overview
This skill handles operations related to AutoTagging.

### Available Tools
- `get_autotagging_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_autotagging_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `delete_autotagging_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `post_autotagging`: No description
  - **Parameters**:
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_autotagging`: No description
  - **Parameters**:
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_autotagging_schema`: No description
  - **Parameters**:
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
