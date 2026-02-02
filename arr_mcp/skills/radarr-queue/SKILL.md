---
name: radarr-queue
description: "Generated skill for Queue operations. Contains 3 tools."
---

### Overview
This skill handles operations related to Queue.

### Available Tools
- `delete_queue_id`: No description
  - **Parameters**:
    - `id` (int)
    - `removeFromClient` (bool)
    - `blocklist` (bool)
    - `skipRedownload` (bool)
    - `changeCategory` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `delete_queue_bulk`: No description
  - **Parameters**:
    - `data` (Dict)
    - `removeFromClient` (bool)
    - `blocklist` (bool)
    - `skipRedownload` (bool)
    - `changeCategory` (bool)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)
- `get_queue`: No description
  - **Parameters**:
    - `page` (int)
    - `pageSize` (int)
    - `sortKey` (str)
    - `sortDirection` (str)
    - `includeUnknownMovieItems` (bool)
    - `includeMovie` (bool)
    - `movieIds` (List)
    - `protocol` (str)
    - `languages` (List)
    - `quality` (List)
    - `status` (List)
    - `radarr_base_url` (str)
    - `radarr_api_key` (Optional[str])
    - `radarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
