---
name: prowlarr-app-profile
description: "Generated skill for AppProfile operations. Contains 6 tools."
---

### Overview
This skill handles operations related to AppProfile.

### Available Tools
- `post_appprofile`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_appprofile`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_appprofile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_appprofile_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_appprofile_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_appprofile_schema`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
