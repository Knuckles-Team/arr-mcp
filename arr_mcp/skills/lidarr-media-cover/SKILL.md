---
name: lidarr-media-cover
description: "Generated skill for MediaCover operations. Contains 2 tools."
---

### Overview
This skill handles operations related to MediaCover.

### Available Tools
- `get_mediacover_artist_artist_id_filename`: No description
  - **Parameters**:
    - `artistId` (int)
    - `filename` (str)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_mediacover_album_album_id_filename`: No description
  - **Parameters**:
    - `albumId` (int)
    - `filename` (str)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
