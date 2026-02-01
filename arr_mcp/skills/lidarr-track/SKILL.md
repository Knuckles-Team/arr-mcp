---
name: lidarr-track
description: "Generated skill for Track operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Track.

### Available Tools
- `get_track`: No description
  - **Parameters**:
    - `artistId` (int)
    - `albumId` (int)
    - `albumReleaseId` (int)
    - `trackIds` (List)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_track_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
