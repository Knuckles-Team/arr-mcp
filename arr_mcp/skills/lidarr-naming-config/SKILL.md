---
name: lidarr-naming-config
description: "Generated skill for NamingConfig operations. Contains 4 tools."
---

### Overview
This skill handles operations related to NamingConfig.

### Available Tools
- `get_config_naming_id`: No description
  - **Parameters**:
    - `id` (int)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `put_config_naming_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_config_naming`: No description
  - **Parameters**:
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)
- `get_config_naming_examples`: No description
  - **Parameters**:
    - `renameTracks` (bool)
    - `replaceIllegalCharacters` (bool)
    - `colonReplacementFormat` (int)
    - `standardTrackFormat` (str)
    - `multiDiscTrackFormat` (str)
    - `artistFolderFormat` (str)
    - `includeArtistName` (bool)
    - `includeAlbumTitle` (bool)
    - `includeQuality` (bool)
    - `replaceSpaces` (bool)
    - `separator` (str)
    - `numberStyle` (str)
    - `id` (int)
    - `resourceName` (str)
    - `lidarr_base_url` (str)
    - `lidarr_api_key` (Optional[str])
    - `lidarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
