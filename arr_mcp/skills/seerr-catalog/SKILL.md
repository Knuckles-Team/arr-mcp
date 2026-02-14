---
name: seerr-catalog
description: "Generated skill for Catalog operations. Contains 2 tools."
---

### Overview
This skill handles operations related to Catalog.

### Available Tools
- `get_movie`: Get movie details
  - **Parameters**:
    - `movie_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)
- `get_tv`: Get TV details
  - **Parameters**:
    - `tv_id` (int)
    - `seerr_base_url` (str)
    - `seerr_api_key` (Optional[str])
    - `seerr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
