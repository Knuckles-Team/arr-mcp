---
name: prowlarr-operations
description: "Generated skill for Operations operations. Contains 4 tools."
tags: [prowlarr, operations]
---

### Overview
This skill handles operations related to Operations.

### Available Tools
- `get_command_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_command_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_command`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_command`: No description
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
