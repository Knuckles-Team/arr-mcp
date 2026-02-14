---
name: chaptarr-operations
description: "Generated skill for Operations operations. Contains 8 tools."
---

### Overview
This skill handles operations related to Operations.

### Available Tools
- `get_calendar`: No description
  - **Parameters**:
    - `start` (str)
    - `end` (str)
    - `unmonitored` (bool)
    - `includeAuthor` (bool)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_calendar_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_feed_v1_calendar_readarrics`: No description
  - **Parameters**:
    - `pastDays` (int)
    - `futureDays` (int)
    - `tagList` (str)
    - `unmonitored` (bool)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `post_command`: No description
  - **Parameters**:
    - `data` (Dict)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_command`: No description
  - **Parameters**:
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `delete_command_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_command_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_parse`: No description
  - **Parameters**:
    - `title` (str)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
