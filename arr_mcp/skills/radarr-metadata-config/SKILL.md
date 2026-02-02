---
name: radarr-metadata-config
description: "Generated skill for MetadataConfig operations. Contains 3 tools."
---

### Overview
This skill handles operations related to MetadataConfig.

### Available Tools
- `get_config_metadata`: No description
  - **Parameters**:
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `put_config_metadata_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_config_metadata_id`: No description
  - **Parameters**:
    - `id` (int)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
