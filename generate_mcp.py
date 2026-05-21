import json

with open("arr_mcp/tool_tags.json") as f:
    tool_tags = json.load(f)

print(tool_tags.keys())
