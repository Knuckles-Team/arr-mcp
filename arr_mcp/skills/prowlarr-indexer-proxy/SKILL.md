---
name: prowlarr-indexer-proxy
description: "Generated skill for IndexerProxy operations. Contains 9 tools."
---

### Overview
This skill handles operations related to IndexerProxy.

### Available Tools
- `get_indexerproxy_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `put_indexerproxy_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `delete_indexerproxy_id`: No description
  - **Parameters**:
    - `id` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_indexerproxy`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexerproxy`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceSave` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_indexerproxy_schema`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexerproxy_test`: No description
  - **Parameters**:
    - `data` (Dict)
    - `forceTest` (bool)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexerproxy_testall`: No description
  - **Parameters**:
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `post_indexerproxy_action_name`: No description
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
