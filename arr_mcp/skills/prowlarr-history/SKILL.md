---
name: prowlarr-history
description: "Generated skill for History operations. Contains 3 tools."
tags: [prowlarr-history]
---

### Overview
This skill handles operations related to History.

### Available Tools
- `get_history`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `eventType` (List)
    - `successful` (bool)
    - `downloadId` (str)
    - `indexerIds` (List)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_history_since`: No description
  - **Parameters**:
    - `date` (str)
    - `eventType` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_history_indexer`: No description
  - **Parameters**:
    - `indexerId` (int)
    - `eventType` (str)
    - `limit` (int)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
