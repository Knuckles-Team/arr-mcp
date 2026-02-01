---
name: sonarr-download-client-config
description: "Generated skill for DownloadClientConfig operations. Contains 3 tools."
---

### Overview
This skill handles operations related to DownloadClientConfig.

### Available Tools
- `get_config_downloadclient`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_config_downloadclient_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_config_downloadclient_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
