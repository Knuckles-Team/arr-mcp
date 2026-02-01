---
name: chaptarr-release
description: "Generated skill for Release operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Release.

### Available Tools
- `post_release`: No description
  - **Parameters**:
    - `data` (Dict)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_release`: No description
  - **Parameters**:
    - `bookId` (int)
    - `authorId` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
