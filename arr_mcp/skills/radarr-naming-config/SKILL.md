---
name: radarr-naming-config
description: "Generated skill for NamingConfig operations. Contains 4 tools."
---

### Overview
This skill handles operations related to NamingConfig.

### Available Tools
- `get_config_naming`: No description
  - **Parameters**:
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_config_naming_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_config_naming_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_config_naming_examples`: No description
  - **Parameters**:
    - `renameMovies` (bool)
    - `replaceIllegalCharacters` (bool)
    - `colonReplacementFormat` (str)
    - `standardMovieFormat` (str)
    - `movieFolderFormat` (str)
    - `id` (int)
    - `resourceName` (str)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
