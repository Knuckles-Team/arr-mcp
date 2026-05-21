with open("scripts/generate_api.py") as f:
    content = f.read()

content = content.replace(
    "client = Api(base_url={self.service_name}_base_url, token={self.service_name}_api_key, verify={self.service_name}_verify)",
    'auth_kw = "api_key" if "{self.service_name}" in ["bazarr", "seerr"] else "token"\\n        client = Api(base_url={self.service_name}_base_url, **{auth_kw: {self.service_name}_api_key}, verify={self.service_name}_verify)  # type: ignore',
)

with open("scripts/generate_api.py", "w") as f:
    f.write(content)
