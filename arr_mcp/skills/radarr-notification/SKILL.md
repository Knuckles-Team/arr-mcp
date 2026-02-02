---
name: radarr-notification
description: "Generated skill for Notification operations. Contains 9 tools."
---

### Overview
This skill handles operations related to Notification.

### Available Tools
- `get_notification`: No description
  - **Parameters**:
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_notification`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceSave` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_notification_id`: No description
  - **Parameters**:
    - `id` (int)
    - `data` (Dict)
    - `forceSave` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `delete_notification_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_notification_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_notification_schema`: No description
  - **Parameters**:
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_notification_test`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceTest` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_notification_testall`: No description
  - **Parameters**:
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_notification_action_name`: No description
  - **Parameters**:
    - `name` (str)
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
