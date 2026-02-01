---
name: sonarr-file-system
description: "Generated skill for FileSystem operations. Contains 3 tools."
---

### Overview
This skill handles operations related to FileSystem.

### Available Tools
- `get_filesystem`: No description
  - **Parameters**:
    - `path` (str)
    - `includeFiles` (bool)
    - `allowFoldersWithoutTrailingSlashes` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_filesystem_type`: No description
  - **Parameters**:
    - `path` (str)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_filesystem_mediafiles`: No description
  - **Parameters**:
    - `path` (str)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
