---
name: prowlarr-authentication
description: "Generated skill for Authentication operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Authentication.

### Available Tools
- `post_login`: No description
  - **Parameters**:
    - `returnUrl` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_logout`: No description
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
