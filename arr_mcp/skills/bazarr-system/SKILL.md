---
name: bazarr-system
description: "Generated skill for System operations. Contains 2 tools."
tags: [bazarr, system]
---

### Overview
This skill handles operations related to System.

### Available Tools
- `get_system_status`: Get Bazarr system status.
  - **Parameters**:
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)
- `get_system_health`: Get system health issues.
  - **Parameters**:
    - `bazarr_base_url` (str)
    - `bazarr_api_key` (str)
    - `bazarr_verify_ssl` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
