---
name: radarr-credit
description: "Generated skill for Credit operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Credit.

### Available Tools
- `get_credit`: No description
  - **Parameters**:
    - `movieId` (int)
    - `movieMetadataId` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_credit_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
