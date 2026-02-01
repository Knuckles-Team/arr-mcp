---
name: chaptarr-custom-format
description: "Generated skill for CustomFormat operations. Contains 6 tools."
---

### Overview
This skill handles operations related to CustomFormat.

### Available Tools
- `post_customformat`: No description
  - **Parameters**:
    - `data` (Dict)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_customformat`: No description
  - **Parameters**:
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `put_customformat_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `delete_customformat_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_customformat_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_customformat_schema`: No description
  - **Parameters**:
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
