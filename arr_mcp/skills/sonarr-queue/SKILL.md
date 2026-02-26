---
name: sonarr-queue
description: "Generated skill for Queue operations. Contains 10 tools."
tags: [sonarr, queue]
---

### Overview
This skill handles operations related to Queue.

### Available Tools
- `get_blocklist`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `seriesIds` (List)
    - `protocols` (List)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_blocklist_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_blocklist_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_queue_id`: No description
  - **Parameters**:
    - `id` (int)
    - `removeFromClient` (bool)
    - `blocklist` (bool)
    - `skipRedownload` (bool)
    - `changeCategory` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `delete_queue_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `removeFromClient` (bool)
    - `blocklist` (bool)
    - `skipRedownload` (bool)
    - `changeCategory` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_queue`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `includeUnknownSeriesItems` (bool)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `seriesIds` (List)
    - `protocol` (str)
    - `languages` (List)
    - `quality` (List)
    - `status` (List)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_queue_grab_id`: No description
  - **Parameters**:
    - `id` (int)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `post_queue_grab_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_queue_details`: No description
  - **Parameters**:
    - `seriesId` (int)
    - `episodeIds` (List)
    - `includeSeries` (bool)
    - `includeEpisode` (bool)
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)
- `get_queue_status`: No description
  - **Parameters**:
    - `sonarr_base_url` (str)
    - `sonarr_api_key` (Optional[str])
    - `sonarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
