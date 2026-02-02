---
name: sonarr-queue-details
description: "Generated skill for QueueDetails operations. Contains 1 tools."
---

### Overview
This skill handles operations related to QueueDetails.

### Available Tools
- `get_queue_details`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `episodeIds` (List)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
