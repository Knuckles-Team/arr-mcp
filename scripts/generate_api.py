import json
import os
import re
from typing import Dict

# Mapping OpenAPI types to Python types
TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "boolean": "bool",
    "number": "float",
    "array": "List",
    "object": "Dict",
}


def clean_param_name(name: str) -> str:
    # Remove characters that are not allowed in python variable names
    clean = re.sub(r"[^0-9a-zA-Z_]", "", name)
    # Ensure it doesn't start with a number
    if clean and clean[0].isdigit():
        clean = f"param_{clean}"
    # Handle reserved keywords if necessary, though simpler to just append _ if needed
    if clean in [
        "from",
        "import",
        "class",
        "def",
        "return",
        "pass",
        "global",
        "lambda",
        "yield",
    ]:
        clean = f"{clean}_"
    return clean


def to_snake_case(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def load_json(path: str) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


class Generator:
    def __init__(self, spec_path: str, output_dir: str, service_name: str):
        self.spec = load_json(spec_path)
        self.output_dir = output_dir
        self.service_name = service_name
        self.api_methods = []
        self.mcp_tools = []
        self.agent_config = {}

    def run(self):
        print(f"Generating code for {self.service_name}...")
        self.parse_spec()
        self.write_api_file()
        self.write_mcp_file()
        self.write_agent_file()

    def parse_spec(self):
        paths = self.spec.get("paths", {})
        for path, methods in paths.items():
            for method, operation in methods.items():
                if method not in ["get", "post", "put", "delete", "patch"]:
                    continue

                operation_id = operation.get("operationId")
                if not operation_id:
                    # Generate operationId if missing
                    operation_id = f"{method}_{path.replace('/', '_').strip('_')}"

                # Clean operation_id to be a valid python function name
                func_name = to_snake_case(clean_param_name(operation_id))

                description = (
                    operation.get("description")
                    or operation.get("summary")
                    or "No description"
                )
                tags = operation.get("tags", [])

                params = []

                # Check for parameters
                for param in operation.get("parameters", []):
                    p_name = clean_param_name(param["name"])
                    p_type = TYPE_MAPPING.get(
                        param.get("schema", {}).get("type", "string"), "Any"
                    )
                    p_required = param.get("required", False)
                    p_in = param.get("in", "query")  # query, path, header, etc.
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

                # Check for request body
                req_body_desc = operation.get("requestBody", {})
                if req_body_desc:
                    # Simplified handling: just accept a Dict called 'data'
                    # unless it's a file upload, which we might skip or handle as optional
                    content = req_body_desc.get("content", {})
                    if "application/json" in content:
                        params.append(
                            {
                                "name": "data",
                                "orig_name": "data",
                                "type": "Dict",
                                "required": True,  # Usually required if body exists
                                "in": "body",
                                "default": "...",  # Ellipsis for required field
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
            "import json",
            "import requests",
            "from typing import Dict, List, Optional, Any",
            "from urllib.parse import urljoin",
            "import urllib3",
            "",
            "class Api:",
            "    def __init__(",
            "        self,",
            "        base_url: str,",
            "        token: Optional[str] = None,",
            "        verify: bool = False,",
            "    ):",
            "        self.base_url = base_url",
            "        self.token = token",
            "        self._session = requests.Session()",
            "        self._session.verify = verify",
            "",
            "        if not verify:",
            "            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)",
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
            "        params: Dict = None,",
            "        data: Dict = None,",
            "    ) -> Any:",
            "        url = urljoin(self.base_url, endpoint)",
            "        response = self._session.request(method=method, url=url, params=params, json=data)",
            "        if response.status_code >= 400:",
            "            try:",
            "                error_text = response.text",
            "            except:",
            "                error_text = 'Unknown error'",
            "            raise Exception(f'API error: {response.status_code} - {error_text}')",
            "        if response.status_code == 204:",
            "            return {'status': 'success'}",
            "        try:",
            "            return response.json()",
            "        except:",
            "            return {'status': 'success', 'text': response.text}",
            "",
        ]

        for method in self.api_methods:
            # Function signature
            # Group params: required first, then optional

            sorted_params = sorted(method["params"], key=lambda x: not x["required"])

            sig_parts = ["self"]
            for p in sorted_params:
                default_val = f" = {p['default']}" if not p["required"] else ""
                sig_parts.append(f"{p['name']}: {p['type']}{default_val}")

            sig_str = ", ".join(sig_parts)

            content.append(f"    def {method['name']}({sig_str}) -> Any:")
            content.append(f"        \"\"\"{method['description']}\"\"\"")

            # Prepare params dict
            path_params = [p for p in method["params"] if p["in"] == "path"]
            query_params = [p for p in method["params"] if p["in"] == "query"]

            # Construct endpoint with path params
            endpoint_str = f"f\"{method['path']}\""
            if path_params:
                # Replace {id} with {id} (f-string format)
                # But we need to match the python var name
                # The spec uses {id}, but our var might be id or param_id
                # So we replace {p['orig_name']} with {p['name']}
                target_endpoint = method["path"]
                for p in path_params:
                    target_endpoint = target_endpoint.replace(
                        f"{{{p['orig_name']}}}", f"{{{p['name']}}}"
                    )
                endpoint_str = f'f"{target_endpoint}"'

            content.append("        params = {}")
            for p in query_params:
                content.append(
                    f"        if {p['name']} is not None: params['{p['orig_name']}'] = {p['name']}"
                )

            data_arg = (
                "data" if any(p["name"] == "data" for p in method["params"]) else "None"
            )

            content.append(
                f"        return self.request(\"{method['method']}\", {endpoint_str}, params=params, data={data_arg})"
            )
            content.append("")

        with open(filepath, "w") as f:
            f.write("\n".join(content))

    def write_mcp_file(self):
        filename = f"{self.service_name}_mcp.py"
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
            f"from arr_mcp.{self.service_name}_api import Api",
            "from arr_mcp.utils import to_boolean, to_integer",
            "",
            f'mcp = FastMCP("{self.service_name}", dependencies=["arr-mcp"])',
            "",
            'DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")',
            'DEFAULT_PORT = to_integer(os.getenv("PORT", "8000"))',
            "",
        ]

        for method in self.api_methods:
            # Decorator
            # We add hidden args for connection details
            exclude_args_str = f"exclude_args=['{self.service_name}_base_url', '{self.service_name}_api_key', '{self.service_name}_verify']"

            tags_str = ""
            if method["tags"]:
                tags_str = f", tags={str(set(method['tags']))}"

            content.append(f"@mcp.tool({exclude_args_str}{tags_str})")

            # Signature
            # Standard args + hidden connection args
            sorted_params = sorted(method["params"], key=lambda x: not x["required"])

            func_name = method["name"]

            sig_lines = []
            sig_lines.append(f"async def {func_name}(")

            for p in sorted_params:
                default_val = "..." if p["required"] else "None"
                field_desc = (
                    f"Field(default={default_val}, description=\"{p['orig_name']}\")"
                )
                sig_lines.append(f"    {p['name']}: {p['type']} = {field_desc},")

            # Append connection args
            sig_lines.append(
                f'    {self.service_name}_base_url: str = Field(default=os.environ.get("{service_upper}_BASE_URL", None), description="Base URL"),'
            )
            sig_lines.append(
                f'    {self.service_name}_api_key: Optional[str] = Field(default=os.environ.get("{service_upper}_API_KEY", None), description="API Key"),'
            )
            sig_lines.append(
                f'    {self.service_name}_verify: bool = Field(default=to_boolean(os.environ.get("{service_upper}_VERIFY", "False")), description="Verify SSL"),'
            )

            sig_lines.append(") -> Dict:")

            content.extend(sig_lines)

            # Docstring
            content.append(f"    \"\"\"{method['description']}\"\"\"")

            # Implementation
            content.append(
                f"    client = Api(base_url={self.service_name}_base_url, token={self.service_name}_api_key, verify={self.service_name}_verify)"
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
# Actually, the agent usually CONNECTS to the MCP server.
# For simplicity, we just created tools files.
# Usage: python -m arr_mcp.{self.service_name}_mcp

def agent_server():
    app = FastAPI(title="{self.service_name}-agent")

    @app.get("/health")
    def health():
        return {{"status": "ok"}}

    # TODO: Implement full agent logic overlapping with existing MCP tools

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 9000)))

if __name__ == "__main__":
    agent_server()
"""
        # Writing the file
        with open(filepath, "w") as f:
            f.write(content)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root_dir, "arr_mcp")

    # ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    # Scan for json specs

    # Add manually known ones if pattern matching fails or catches extra
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
