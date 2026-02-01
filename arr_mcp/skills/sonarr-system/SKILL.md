---
name: sonarr-system
description: "Generated skill for System operations. Contains 5 tools."
---

### Overview
This skill handles operations related to System.

### Available Tools
- `get_system_status`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_system_routes`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_system_routes_duplicate`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_system_shutdown`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_system_restart`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
