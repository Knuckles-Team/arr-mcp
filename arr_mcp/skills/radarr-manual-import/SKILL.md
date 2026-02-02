---
name: radarr-manual-import
description: "Generated skill for ManualImport operations. Contains 2 tools."
---

### Overview
This skill handles operations related to ManualImport.

### Available Tools
- `get_manualimport`: No description
  - **Parameters**:
    - `folder` (str)
    - `downloadId` (str)
    - `movieId` (int)
    - `filterExistingFiles` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `post_manualimport`: No description
  - **Parameters**:
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
