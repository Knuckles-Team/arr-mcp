---
name: sonarr-cutoff
description: "Generated skill for Cutoff operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Cutoff.

### Available Tools
- `get_wanted_cutoff`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `includeSeries` (bool)
    - `includeEpisodeFile` (bool)
    - `includeImages` (bool)
    - `monitored` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_wanted_cutoff_id`: No description
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
