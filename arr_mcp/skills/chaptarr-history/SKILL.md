---
name: chaptarr-history
description: "Generated skill for History operations. Contains 4 tools."
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
    - `includeAuthor` (bool)
    - `includeBook` (bool)
    - `eventType` (List)
    - `bookId` (int)
    - `downloadId` (str)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_history_since`: No description
  - **Parameters**:
    - `date` (str)
    - `eventType` (str)
    - `includeAuthor` (bool)
    - `includeBook` (bool)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_history_author`: No description
  - **Parameters**:
    - `authorId` (int)
    - `bookId` (int)
    - `eventType` (str)
    - `includeAuthor` (bool)
    - `includeBook` (bool)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `post_history_failed_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
