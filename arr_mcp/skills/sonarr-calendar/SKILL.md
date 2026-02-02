---
name: sonarr-calendar
description: "Generated skill for Calendar operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Calendar.

### Available Tools
- `get_calendar`: No description
  - **Parameters**:
    - `start` (str)
    - `end` (str)
    - `unmonitored` (bool)
    - `includeSeries` (bool)
    - `includeEpisodeFile` (bool)
    - `includeEpisodeImages` (bool)
    - `tags` (str)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_calendar_id`: No description
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
