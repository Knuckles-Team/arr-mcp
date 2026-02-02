---
name: prowlarr-search
description: "Generated skill for Search operations. Contains 3 tools."
---

### Overview
This skill handles operations related to Search.

### Available Tools
- `post_search`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_search`: No description
  - **Parameters**:
    - `query` (str)
    - `type` (str)
    - `indexerIds` (List)
    - `categories` (List)
    - `limit` (int)
    - `offset` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_search_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
