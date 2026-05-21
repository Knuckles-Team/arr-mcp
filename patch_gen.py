with open("gen_mcp.py") as f:
    content = f.read()

content = content.replace(
    "client = API_CLASSES['{service}'](base_url={service}_base_url, token={service}_api_key, verify={service}_verify)",
    'auth_kw = "api_key" if "{service}" in ["bazarr", "seerr"] else "token"\n        client = API_CLASSES[\'{service}\'](base_url={service}_base_url, **{auth_kw: {service}_api_key}, verify={service}_verify)  # type: ignore',
)

with open("gen_mcp.py", "w") as f:
    f.write(content)
