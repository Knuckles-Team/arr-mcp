---
name: prowlarr-downloads
description: "Generated skill for Downloads operations. Contains 14 tools."
tags: [prowlarr-downloads]
---

### Overview
This skill handles operations related to Downloads.

### Available Tools
- `get_downloadclient_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_downloadclient_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_downloadclient_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_downloadclient`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_downloadclient`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_downloadclient_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_downloadclient_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_downloadclient_schema`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_downloadclient_test`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceTest` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_downloadclient_testall`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_downloadclient_action_name`: No description
  - **Parameters**:
    - `name` (str)
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_config_downloadclient_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_config_downloadclient_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_config_downloadclient`: No description
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
