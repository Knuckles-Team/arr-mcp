---
name: seerr-search
description: "Generated skill for Search operations. Contains 8 tools."
---

### Overview
This skill handles operations related to Search.

### Available Tools
- `post_request`: Create a new request
  - **Parameters**:
    - `media_type` (str)
    - `media_id` (int)
    - `seasons` (List[int])
    - `is4k` (bool)
    - `server_id` (int)
    - `profile_id` (int)
    - `root_folder` (str)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_request`: Get all requests
  - **Parameters**:
    - `take` (int)
    - `skip` (int)
    - `filter` (str)
    - `sort` (str)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_request_id`: Get a specific request
  - **Parameters**:
    - `request_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `put_request_id`: Update a request
  - **Parameters**:
    - `request_id` (int)
    - `media_type` (str)
    - `seasons` (List[int])
    - `server_id` (int)
    - `profile_id` (int)
    - `root_folder` (str)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `delete_request_id`: Delete a request
  - **Parameters**:
    - `request_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `approve_request`: Approve a request
  - **Parameters**:
    - `request_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `decline_request`: Decline a request
  - **Parameters**:
    - `request_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `search`: Search for content
  - **Parameters**:
    - `query` (str)
    - `page` (int)
    - `language` (str)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
