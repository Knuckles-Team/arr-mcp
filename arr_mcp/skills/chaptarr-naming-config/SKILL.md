---
name: chaptarr-naming-config
description: "Generated skill for NamingConfig operations. Contains 4 tools."
---

### Overview
This skill handles operations related to NamingConfig.

### Available Tools
- `get_config_naming`: No description
  - **Parameters**:
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `put_config_naming_id`: No description
  - **Parameters**:
    - `id` (str)
    - `data` (Dict)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_config_naming_id`: No description
  - **Parameters**:
    - `id` (int)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)
- `get_config_naming_examples`: No description
  - **Parameters**:
    - `renameBooks` (bool)
    - `replaceIllegalCharacters` (bool)
    - `colonReplacementFormat` (int)
    - `standardBookFormat` (str)
    - `authorFolderFormat` (str)
    - `includeAuthorName` (bool)
    - `includeBookTitle` (bool)
    - `includeQuality` (bool)
    - `replaceSpaces` (bool)
    - `separator` (str)
    - `numberStyle` (str)
    - `id` (int)
    - `resourceName` (str)
    - `chaptarr_base_url` (str)
    - `chaptarr_api_key` (Optional[str])
    - `chaptarr_verify` (bool)

### Usage Instructions
1. Review the tool available in this skill.
2. Call the tool with the required parameters.

### Error Handling
- Ensure all required parameters are provided.
- Check return values for error messages.
