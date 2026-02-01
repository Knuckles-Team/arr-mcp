---
name: lidarr-delay-profile
description: "Generated skill for DelayProfile operations. Contains 6 tools."
---

### Overview
This skill handles operations related to DelayProfile.

### Available Tools
- `post_delayprofile`: No description
  - **Parameters**:
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_delayprofile`: No description
  - **Parameters**:
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `delete_delayprofile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_delayprofile_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_delayprofile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_delayprofile_reorder_id`: No description
  - **Parameters**:
    - `id` (int)
    - `afterId` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
