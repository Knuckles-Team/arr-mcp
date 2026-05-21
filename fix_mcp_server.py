import re

with open("arr_mcp/mcp_server.py") as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for: client = API_CLASSES["..."](
    if 'client = API_CLASSES["' in line:
        # Extract service name
        match = re.search(r'API_CLASSES\["([^"]+)"\]', line)
        if match:
            service = match.group(1)
            # The next two lines contain the arguments:
            # base_url=..., token=..., verify=...
            # )

            # Read until we hit the closing parenthesis of client initialization
            call_lines = [line]
            while i + 1 < len(lines) and ")" not in call_lines[-1]:
                i += 1
                call_lines.append(lines[i])

            # Now we have the full call. Let's rewrite it.
            # We want:
            # auth_kw = "api_key" if "service" in ["bazarr", "seerr"] else "token"
            # client = API_CLASSES["service"](base_url=..., **{auth_kw: ..._api_key}, verify=..._verify)  # type: ignore

            indent = line[: len(line) - len(line.lstrip())]

            new_lines.append(
                f'{indent}auth_kw = "api_key" if "{service}" in ["bazarr", "seerr"] else "token"\n'
            )
            new_lines.append(f'{indent}client = API_CLASSES["{service}"](\n')
            new_lines.append(
                f"{indent}    base_url={service}_base_url, **{{auth_kw: {service}_api_key}}, verify={service}_verify\n"
            )
            new_lines.append(f"{indent})  # type: ignore\n")

            i += 1
            continue

    new_lines.append(line)
    i += 1

with open("arr_mcp/mcp_server.py", "w") as f:
    f.writelines(new_lines)
