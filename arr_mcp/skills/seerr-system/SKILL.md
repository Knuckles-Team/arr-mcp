---
name: seerr-system
description: "Generated skill for System operations. Contains 5 tools."
tags: [seerr, system]
---

### Overview
This skill handles operations related to System.

### Available Tools
- `get_status`: Get Seerr status
  - **Parameters**:
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_status_appdata`: Get application data volume status
  - **Parameters**:
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_auth_me`: Get logged-in user
  - **Parameters**:
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_users`: Get all users
  - **Parameters**:
    - `take` (int)
    - `skip` (int)
    - `sort` (str)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_user_id`: Get user details
  - **Parameters**:
    - `user_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
