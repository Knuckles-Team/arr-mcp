---
name: lidarr-root-folder
description: "Generated skill for RootFolder operations. Contains 5 tools."
---

### Overview
This skill handles operations related to RootFolder.

### Available Tools
- `get_rootfolder_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_rootfolder_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `delete_rootfolder_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `post_rootfolder`: No description
  - **Parameters**:
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_rootfolder`: No description
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
