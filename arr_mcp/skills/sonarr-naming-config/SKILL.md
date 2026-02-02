---
name: sonarr-naming-config
description: "Generated skill for NamingConfig operations. Contains 4 tools."
---

### Overview
This skill handles operations related to NamingConfig.

### Available Tools
- `get_config_naming`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `put_config_naming_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_config_naming_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_config_naming_examples`: No description
  - **Parameters**:
    - `renameEpisodes` (bool)
    - `replaceIllegalCharacters` (bool)
    - `colonReplacementFormat` (int)
    - `customColonReplacementFormat` (str)
    - `multiEpisodeStyle` (int)
    - `standardEpisodeFormat` (str)
    - `dailyEpisodeFormat` (str)
    - `animeEpisodeFormat` (str)
    - `seriesFolderFormat` (str)
    - `seasonFolderFormat` (str)
    - `specialsFolderFormat` (str)
    - `id` (int)
    - `resourceName` (str)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
