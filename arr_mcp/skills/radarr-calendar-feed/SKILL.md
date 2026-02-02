---
name: radarr-calendar-feed
description: "Generated skill for CalendarFeed operations. Contains 1 tools."
---

### Overview
This skill handles operations related to CalendarFeed.

### Available Tools
- `get_feed_v3_calendar_radarrics`: No description
  - **Parameters**:
    - `pastDays` (int)
    - `futureDays` (int)
    - `tags` (str)
    - `unmonitored` (bool)
    - `releaseTypes` (List)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
