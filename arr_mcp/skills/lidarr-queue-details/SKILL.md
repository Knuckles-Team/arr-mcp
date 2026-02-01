---
name: lidarr-queue-details
description: "Generated skill for QueueDetails operations. Contains 1 tools."
---

### Overview
This skill handles operations related to QueueDetails.

### Available Tools
- `get_queue_details`: No description
  - **Parameters**:
    - `artistId` (int)
    - `albumIds` (List)
    - `includeArtist` (bool)
    - `includeAlbum` (bool)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
