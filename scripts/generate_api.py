import json
import keyword
import os
import re
from typing import Any

TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "boolean": "bool",
    "number": "float",
    "array": "List",
    "object": "Dict",
}
_MAX_SPEC_BYTES = 16 * 1024 * 1024
_MAX_OPERATIONS = 5_000
_MAX_PARAMETERS_PER_OPERATION = 100
_RESERVED_METHOD_NAMES = {"request"}
_RESERVED_PARAMETER_NAMES = {"params", "self"}


def clean_param_name(name: str) -> str:
    if not isinstance(name, str) or len(name) > 256:
        raise ValueError("Parameter names must be bounded strings")
    clean = re.sub(r"[^0-9a-zA-Z_]", "", name)
    if not clean:
        raise ValueError("Parameter name does not contain a Python identifier")
    if clean and clean[0].isdigit():
        clean = f"param_{clean}"
    if keyword.iskeyword(clean):
        clean = f"{clean}_"
    return clean


def to_snake_case(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def load_json(path: str) -> dict:
    with open(path, "rb") as spec_file:
        payload = spec_file.read(_MAX_SPEC_BYTES + 1)
    if len(payload) > _MAX_SPEC_BYTES:
        raise ValueError("OpenAPI specification exceeds its size limit")
    return json.loads(payload)


class Generator:
    def __init__(self, spec_path: str, output_dir: str, service_name: str):
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", service_name):
            raise ValueError("Service name must be a bounded Python identifier")
        self.spec = load_json(spec_path)
        if not isinstance(self.spec, dict):
            raise ValueError("OpenAPI specification must be a JSON object")
        self.output_dir = output_dir
        self.service_name = service_name
        self.api_methods: list[Any] = []
        self.mcp_tools: list[Any] = []
        self.agent_config: dict[str, Any] = {}

    def run(self):
        print(f"Generating code for {self.service_name}...")
        self.parse_spec()
        self.write_api_file()
        self.write_mcp_file()
        self.write_agent_file()

    def parse_spec(self):
        paths = self.spec.get("paths", {})
        if not isinstance(paths, dict) or len(paths) > _MAX_OPERATIONS:
            raise ValueError("OpenAPI paths must be a bounded object")
        method_names: set[str] = set()
        operation_count = 0
        for path, methods in paths.items():
            if (
                not isinstance(path, str)
                or not path.startswith("/")
                or len(path) > 2048
                or any(char in path for char in "\x00\r\n")
                or not isinstance(methods, dict)
            ):
                raise ValueError("OpenAPI paths must be bounded absolute URL paths")
            for method, operation in methods.items():
                if method not in ["get", "post", "put", "delete", "patch"]:
                    continue
                if not isinstance(operation, dict):
                    raise ValueError("OpenAPI operation must be an object")
                operation_count += 1
                if operation_count > _MAX_OPERATIONS:
                    raise ValueError("OpenAPI operation count exceeds its limit")

                operation_id = operation.get("operationId")
                if not operation_id:
                    operation_id = f"{method}_{path.replace('/', '_').strip('_')}"

                func_name = to_snake_case(clean_param_name(operation_id))
                if func_name.startswith("_") or func_name in _RESERVED_METHOD_NAMES:
                    func_name = f"operation_{func_name.lstrip('_')}"
                if func_name in method_names:
                    raise ValueError("OpenAPI operation names collide after normalization")
                method_names.add(func_name)

                description = (
                    operation.get("description")
                    or operation.get("summary")
                    or "No description"
                )
                if not isinstance(description, str) or len(description) > 4096:
                    raise ValueError("OpenAPI descriptions must be bounded strings")
                tags = operation.get("tags", [])
                if (
                    not isinstance(tags, list)
                    or len(tags) > 32
                    or any(
                        not isinstance(tag, str)
                        or not tag
                        or len(tag) > 64
                        or any(char in tag for char in "\x00\r\n")
                        for tag in tags
                    )
                ):
                    raise ValueError("OpenAPI tags must be bounded strings")

                params = []
                parameter_names: set[str] = set()

                operation_params = operation.get("parameters", [])
                if (
                    not isinstance(operation_params, list)
                    or len(operation_params) > _MAX_PARAMETERS_PER_OPERATION
                ):
                    raise ValueError("OpenAPI parameter count exceeds its limit")
                for param in operation_params:
                    if not isinstance(param, dict) or "name" not in param:
                        raise ValueError("OpenAPI parameters must be named objects")
                    p_name = clean_param_name(param["name"])
                    if p_name in _RESERVED_PARAMETER_NAMES:
                        p_name = f"param_{p_name}"
                    if p_name in parameter_names:
                        raise ValueError(
                            "OpenAPI parameter names collide after normalization"
                        )
                    parameter_names.add(p_name)
                    schema = param.get("schema", {})
                    if not isinstance(schema, dict):
                        raise ValueError("OpenAPI parameter schema must be an object")
                    p_type = TYPE_MAPPING.get(
                        schema.get("type", "string"), "Any"
                    )
                    p_required = param.get("required", False)
                    p_in = param.get("in", "query")
                    if not isinstance(p_required, bool) or p_in not in {
                        "body",
                        "path",
                        "query",
                    }:
                        raise ValueError("OpenAPI parameter location is invalid")
                    params.append(
                        {
                            "name": p_name,
                            "orig_name": param["name"],
                            "type": p_type,
                            "required": p_required,
                            "in": p_in,
                            "default": None if p_required else "None",
                        }
                    )

                req_body_desc = operation.get("requestBody", {})
                if req_body_desc:
                    if not isinstance(req_body_desc, dict):
                        raise ValueError("OpenAPI request body must be an object")
                    content = req_body_desc.get("content", {})
                    if not isinstance(content, dict):
                        raise ValueError("OpenAPI request content must be an object")
                    if "application/json" in content:
                        if "data" in parameter_names:
                            raise ValueError("OpenAPI body collides with a data parameter")
                        params.append(
                            {
                                "name": "data",
                                "orig_name": "data",
                                "type": "Dict",
                                "required": True,
                                "in": "body",
                                "default": "...",
                            }
                        )

                self.api_methods.append(
                    {
                        "name": func_name,
                        "path": path,
                        "method": method.upper(),
                        "params": params,
                        "description": description.replace("\n", " "),
                        "tags": tags,
                    }
                )

    def write_api_file(self):
        filename = f"{self.service_name}_api.py"
        filepath = os.path.join(self.output_dir, filename)

        content = [
            "#!/usr/bin/env python",
            "# coding: utf-8",
            "",
            "import requests",
            "from typing import Dict, List, Optional, Any",
            "from agent_utilities.core.transport_security import ResolvedTLSProfile, resolve_tls_profile",
            "from arr_mcp.api._security import (",
            "    REQUEST_TIMEOUT, decode_response, request_url, validate_base_url,",
            ")",
            "",
            "class Api:",
            "    def __init__(",
            "        self,",
            "        base_url: str,",
            "        token: Optional[str] | None = None,",
            "        tls_profile: ResolvedTLSProfile | None = None,",
            "    ):",
            "        self.base_url, self._origin = validate_base_url(base_url)",
            "        self.token = token",
            "        self._session = requests.Session()",
            f'        self._tls_profile = tls_profile or resolve_tls_profile("{self.service_name}")',
            "        self._tls_profile.configure_requests_session(self._session)",
            "",
            "        if token:",
            "            # Some arr apps accept key in header X-Api-Key",
            "            self._session.headers.update({'X-Api-Key': token})",
            "            # Also support query param in requests if needed, but header is cleaner",
            "",
            "    def request(",
            "        self,",
            "        method: str,",
            "        endpoint: str,",
            "        params: Dict | None = None,",
            "        data: Dict | None = None,",
            "    ) -> Any:",
            "        url = request_url(self.base_url, self._origin, endpoint)",
            "        response = self._session.request(",
            "            method=method, url=url, params=params, json=data,",
            "            timeout=REQUEST_TIMEOUT, allow_redirects=False, stream=True,",
            "        )",
            "        try:",
            "            if response.status_code >= 400:",
            "                raise RuntimeError(f'API error: HTTP {response.status_code}')",
            "            if response.status_code == 204:",
            "                return {'status': 'success'}",
            "            return decode_response(response)",
            "        finally:",
            "            response.close()",
            "",
        ]

        for method in self.api_methods:
            sorted_params = sorted(method["params"], key=lambda x: not x["required"])

            sig_parts = ["self"]
            for p in sorted_params:
                default_val = f" = {p['default']}" if not p["required"] else ""
                sig_parts.append(f"{p['name']}: {p['type']}{default_val}")

            sig_str = ", ".join(sig_parts)

            content.append(f"    def {method['name']}({sig_str}) -> Any:")
            content.append(f"        {method['description']!r}")

            path_params = [p for p in method["params"] if p["in"] == "path"]
            query_params = [p for p in method["params"] if p["in"] == "query"]

            endpoint_str = repr(method["path"])
            if path_params:
                for p in path_params:
                    placeholder = "{" + p["orig_name"] + "}"
                    endpoint_str += f".replace({placeholder!r}, str({p['name']}))"

            content.append("        params: dict[str, Any] = {}")
            for p in query_params:
                content.append(
                    f"        if {p['name']} is not None: params[{p['orig_name']!r}] = {p['name']}"
                )

            data_arg = (
                "data" if any(p["name"] == "data" for p in method["params"]) else "None"
            )

            content.append(
                f'        return self.request("{method["method"]}", {endpoint_str}, params=params, data={data_arg})'
            )
            content.append("")
        with open(filepath, "w") as f:
            f.write("\n".join(content))

    def write_mcp_file(self):
        filename = f"{self.service_name}_mcp_server.py"
        filepath = os.path.join(self.output_dir, filename)
        service_upper = self.service_name.upper()

        content = [
            "#!/usr/bin/env python",
            "# coding: utf-8",
            "",
            "import os",
            "from typing import Optional, List, Dict, Any",
            "from pydantic import Field",
            "from fastmcp import FastMCP, Context",
            "from agent_utilities.core.transport_security import resolve_tls_profile",
            f"from arr_mcp.{self.service_name}_api import Api",
            "from arr_mcp.utils import to_integer",
            "",
            f'mcp = FastMCP("{self.service_name}", dependencies=["arr-mcp"])',
            "",
            'DEFAULT_HOST = os.getenv("HOST", "127.0.0.1")',
            'DEFAULT_PORT = to_integer(os.getenv("PORT", "8000"))',
            "",
        ]

        for method in self.api_methods:
            exclude_args_str = f"exclude_args=['{self.service_name}_base_url', '{self.service_name}_api_key']"

            tags_str = ""
            if method["tags"]:
                tags_str = f", tags={set(method['tags'])!r}"

            content.append(f"@mcp.tool({exclude_args_str}{tags_str})")

            sorted_params = sorted(method["params"], key=lambda x: not x["required"])

            func_name = method["name"]

            sig_lines = []
            sig_lines.append(f"async def {func_name}(")

            for p in sorted_params:
                default_val = "..." if p["required"] else "None"
                field_desc = f"Field(default={default_val}, description={p['orig_name']!r})"
                sig_lines.append(f"    {p['name']}: {p['type']} = {field_desc},")

            sig_lines.append(
                f'    {self.service_name}_base_url: str = Field(default=os.environ.get("{service_upper}_BASE_URL", None), description="Base URL"),'
            )
            sig_lines.append(
                f'    {self.service_name}_api_key: Optional[str] = Field(default=os.environ.get("{service_upper}_API_KEY", None), description="API Key"),'
            )
            sig_lines.append(") -> Dict:")

            content.extend(sig_lines)

            content.append(f"    {method['description']!r}")

            content.append(
                f'    auth_kw = "api_key" if "{self.service_name}" in ["bazarr", "seerr"] else "token"\n'
                f'    client = Api(base_url={self.service_name}_base_url, **{{auth_kw: {self.service_name}_api_key}}, tls_profile=resolve_tls_profile("{self.service_name}"))  # type: ignore'
            )

            call_args = []
            for p in sorted_params:
                call_args.append(f"{p['name']}={p['name']}")

            content.append(
                f"    return client.{method['name']}({', '.join(call_args)})"
            )
            content.append("")

        with open(filepath, "w") as f:
            f.write("\n".join(content))

    def write_agent_file(self):
        filename = f"{self.service_name}_agent.py"
        filepath = os.path.join(self.output_dir, filename)

        content = f"""#!/usr/bin/env python
# coding: utf-8

import os
import logging
import uvicorn
from typing import Optional

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerSSE, MCPServerStreamableHTTP
from fastapi import FastAPI

# Requires arr_mcp.{self.service_name}_mcp to be running or accessible?
# For simplicity, we just created tools files.
# Usage: python -m arr_mcp.{self.service_name}_mcp

def agent_server():
    app = FastAPI(title="{self.service_name}-agent")

    @app.get("/health")
    def health():
        return {{"status": "ok"}}

    # Note: Implement full agent logic overlapping with existing MCP tools

    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 9000)),
    )

if __name__ == "__main__":
    agent_server()
"""
        with open(filepath, "w") as f:
            f.write(content)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root_dir, "arr_mcp")

    os.makedirs(output_dir, exist_ok=True)

    known_specs = [
        "chaptarr.json",
        "homarr.json",
        "lidarr.json",
        "prowlarr.json",
        "radarr.json",
        "sonarr.json",
    ]

    for spec_file in known_specs:
        spec_path = os.path.join(root_dir, spec_file)
        if os.path.exists(spec_path):
            service_name = spec_file.replace(".json", "")
            generator = Generator(spec_path, output_dir, service_name)
            generator.run()


if __name__ == "__main__":
    main()
