---
name: prowlarr-newznab
description: "Generated skill for Newznab operations. Contains 4 tools."
---

### Overview
This skill handles operations related to Newznab.

### Available Tools
- `get_indexer_id_newznab`: No description
  - **Parameters**:
    - `id` (int)
    - `t` (str)
    - `q` (str)
    - `cat` (str)
    - `imdbid` (str)
    - `tmdbid` (int)
    - `extended` (str)
    - `limit` (int)
    - `offset` (int)
    - `minage` (int)
    - `maxage` (int)
    - `minsize` (int)
    - `maxsize` (int)
    - `rid` (int)
    - `tvmazeid` (int)
    - `traktid` (int)
    - `tvdbid` (int)
    - `doubanid` (int)
    - `season` (int)
    - `ep` (str)
    - `album` (str)
    - `artist` (str)
    - `label` (str)
    - `track` (str)
    - `year` (int)
    - `genre` (str)
    - `author` (str)
    - `title` (str)
    - `publisher` (str)
    - `configured` (str)
    - `source` (str)
    - `host` (str)
    - `server` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_id_api`: No description
  - **Parameters**:
    - `id` (int)
    - `t` (str)
    - `q` (str)
    - `cat` (str)
    - `imdbid` (str)
    - `tmdbid` (int)
    - `extended` (str)
    - `limit` (int)
    - `offset` (int)
    - `minage` (int)
    - `maxage` (int)
    - `minsize` (int)
    - `maxsize` (int)
    - `rid` (int)
    - `tvmazeid` (int)
    - `traktid` (int)
    - `tvdbid` (int)
    - `doubanid` (int)
    - `season` (int)
    - `ep` (str)
    - `album` (str)
    - `artist` (str)
    - `label` (str)
    - `track` (str)
    - `year` (int)
    - `genre` (str)
    - `author` (str)
    - `title` (str)
    - `publisher` (str)
    - `configured` (str)
    - `source` (str)
    - `host` (str)
    - `server` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_indexer_id_download`: No description
  - **Parameters**:
    - `id` (int)
    - `link` (str)
    - `file` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)
- `get_id_download`: No description
  - **Parameters**:
    - `id` (int)
    - `link` (str)
    - `file` (str)
    - `prowlarr_base_url` (str)
    - `prowlarr_api_key` (Optional[str])
    - `prowlarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
