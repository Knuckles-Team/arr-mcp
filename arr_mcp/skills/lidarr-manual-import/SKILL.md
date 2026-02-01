---
name: lidarr-manual-import
description: "Generated skill for ManualImport operations. Contains 2 tools."
---

### Overview
This skill handles operations related to ManualImport.

### Available Tools
- `post_manualimport`: No description
  - **Parameters**:
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_manualimport`: No description
  - **Parameters**:
    - `folder` (str)
    - `downloadId` (str)
    - `artistId` (int)
    - `filterExistingFiles` (bool)
    - `replaceExistingFiles` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
