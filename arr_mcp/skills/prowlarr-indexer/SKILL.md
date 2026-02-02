---
name: prowlarr-indexer
description: "Generated skill for Indexer operations. Contains 11 tools."
---

### Overview
This skill handles operations related to Indexer.

### Available Tools
- `get_indexer_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_indexer_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_indexer_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_indexer`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexer`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_indexer_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_indexer_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_indexer_schema`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexer_test`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceTest` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexer_testall`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexer_action_name`: No description
  - **Parameters**:
    - `name` (str)
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
