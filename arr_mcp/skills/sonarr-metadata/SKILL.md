---
name: sonarr-metadata
description: "Generated skill for Metadata operations. Contains 9 tools."
---

### Overview
This skill handles operations related to Metadata.

### Available Tools
- `get_metadata`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_metadata`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceSave` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_metadata_id`: No description
  - **Parameters**:
    - `id` (int)
    - `data` (Dict)
    - `forceSave` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_metadata_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_metadata_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_metadata_schema`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_metadata_test`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceTest` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_metadata_testall`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_metadata_action_name`: No description
  - **Parameters**:
    - `name` (str)
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
