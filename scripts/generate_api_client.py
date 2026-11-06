"""Write one arr API client from the app's OpenAPI or Swagger description.

Usage::

    python scripts/generate_api_client.py <app> <spec.json|spec.yml> <api-prefix>

One method per upstream operation (CONN-ARR-MCP-SUITE-R001): the method name is
the operation id in snake case, or ``<verb>_<path segments>`` when the
description has none; path, query, form and JSON-body fields become typed
keyword parameters with the upstream description. The scion-sdk serves each
method as one typed MCP tool. The output is source: review it and commit it.
"""

from __future__ import annotations

import json
import keyword
import re
import sys
from pathlib import Path
from typing import Any

import yaml

_VERBS = ("get", "post", "put", "patch", "delete")
_TYPES = {"integer": "int", "number": "float", "boolean": "bool", "string": "str"}

_HEADER = '''"""{title} API client: one method per upstream operation.

Written by ``scripts/generate_api_client.py`` from the {title} API description
({source}); every method is served as one typed MCP tool
(CONN-ARR-MCP-SUITE-R001).
"""

# ruff: noqa: E501

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile

from arr_mcp.api._security import (
    build_client,
    decode_response,
    raise_for_api_error,
    request_url,
    send_request,
    validate_base_url,
)


def _clean(values: dict[str, Any] | None) -> dict[str, Any] | None:
    if values is None:
        return None
    kept = {{key: value for key, value in values.items() if value is not None}}
    return kept or None


class Api:
    """API client for {title}."""

    def __init__(
        self,
        base_url: str,
        {auth_kw}: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url, self._origin = validate_base_url(base_url)
        self.{auth_kw} = {auth_kw}
        self._tls_profile = tls_profile or resolve_tls_profile("{app}")
        self._session = build_client(self.base_url, self._tls_profile, {auth_kw})

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any = None,
        form: dict[str, Any] | None = None,
    ) -> Any:
        """Send one request; an error status or an HTML page raises."""
        url = request_url(self.base_url, self._origin, endpoint)
        response = send_request(
            self._session, method, url, _clean(params), data, form=_clean(form)
        )
        try:
            raise_for_api_error(response)
            if response.status_code == 204:
                return {{"status": "success"}}
            result = decode_response(response)
            if isinstance(result, list):
                return {{"result": result}}
            return result
        finally:
            response.close()
'''


def _snake(name: str) -> str:
    name = re.sub(r"[^0-9A-Za-z]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    if not name or name[0].isdigit():
        name = f"p_{name}"
    if keyword.iskeyword(name) or name in {"self", "params", "data", "form"}:
        name = f"{name}_"
    return name


def _method_name(verb: str, path: str, op: dict[str, Any]) -> str:
    if op.get("operationId"):
        return _snake(op["operationId"])
    parts: list[str] = [verb]
    for segment in [s for s in path.split("/") if s]:
        if segment.startswith("{"):
            param = _snake(segment.strip("{}"))
            if parts and param.startswith(parts[-1] + "_"):
                parts[-1] = param
            else:
                parts.append(param)
        else:
            parts.append(_snake(segment))
    return "_".join(parts)


def _resolve(spec: dict[str, Any], node: Any) -> Any:
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 20:
        ref = node["$ref"].lstrip("#/").split("/")
        target: Any = spec
        for key in ref:
            target = target[key]
        node = target
        seen += 1
    return node


def _pytype(spec: dict[str, Any], schema: dict[str, Any] | None) -> str:
    schema = _resolve(spec, schema or {})
    kind = schema.get("type")
    if kind == "array":
        return f"list[{_pytype(spec, schema.get('items'))}]"
    if kind == "object" or "properties" in schema or "allOf" in schema:
        return "dict[str, Any]"
    return _TYPES.get(str(kind), "Any")


def _doc(text: Any) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text.replace("\\", "\\\\").replace('"', '\\"')


class _Param:
    def __init__(self, name, wire, where, pytype, required, description, default):
        self.name, self.wire, self.where = name, wire, where
        self.pytype, self.required = pytype, required
        self.description, self.default = description, default


def _params(spec, path_item, op) -> list[_Param]:
    out: list[_Param] = []
    raw = list(path_item.get("parameters", [])) + list(op.get("parameters", []))
    for item in raw:
        item = _resolve(spec, item)
        where = item.get("in")
        if where not in ("path", "query", "formData", "body"):
            continue
        if where == "body":
            schema = _resolve(spec, item.get("schema") or {})
            out += _body_fields(spec, schema, bool(item.get("required")), "")
            continue
        schema = item.get("schema") or item
        pytype = _pytype(spec, schema)
        wire = item["name"]
        name = _snake(wire.removesuffix("[]"))
        default = None
        out.append(
            _Param(
                name,
                wire,
                where,
                pytype,
                where == "path" or bool(item.get("required")),
                _doc(item.get("description")),
                default,
            )
        )
    body = op.get("requestBody")
    if body:
        body = _resolve(spec, body)
        content = body.get("content", {})
        media = content.get("application/json") or next(iter(content.values()), {})
        schema = _resolve(spec, media.get("schema") or {})
        out += _body_fields(spec, schema, bool(body.get("required")), "")
    seen: set[str] = set()
    for param in out:
        while param.name in seen:
            param.name = f"body_{param.name}"
        seen.add(param.name)
    return out


def _body_fields(spec, schema, required, prefix) -> list[_Param]:
    props: dict[str, Any] = {}
    needed: set[str] = set()
    for part in [schema, *[_resolve(spec, s) for s in schema.get("allOf", [])]]:
        props.update(part.get("properties", {}) or {})
        needed |= set(part.get("required", []) or [])
    if schema.get("type") in ("object", None) and props:
        return [
            _Param(
                _snake(name),
                name,
                "json",
                _pytype(spec, prop),
                required and name in needed,
                _doc(_resolve(spec, prop).get("description")),
                None,
            )
            for name, prop in props.items()
        ]
    return [
        _Param(
            "body",
            None,
            "rawjson",
            _pytype(spec, schema) if schema else "Any",
            required,
            "The request body as JSON.",
            None,
        )
    ]


def _render_method(spec, prefix, verb, path, path_item, op) -> tuple[str, str]:
    name = _method_name(verb, path, op)
    params = _params(spec, path_item, op)
    ordered = [p for p in params if p.required] + [p for p in params if not p.required]
    sig = ["self"]
    if ordered:
        sig.append("*")
    for p in ordered:
        hint = f'Annotated[{p.pytype}{"" if p.required else " | None"}, Field(description="{p.description or p.wire or p.name}")]'
        sig.append(f"{p.name}: {hint}" + ("" if p.required else " = None"))
    summary = _doc(op.get("summary") or op.get("description") or f"{verb} {path}")
    lines = [f"    def {name}({', '.join(sig)}) -> Any:"]
    lines.append(
        f'        """{summary}\n\n        {verb.upper()} {prefix}{path}\n        """'
    )
    rendered = prefix + path
    for p in params:
        if p.where == "path":
            rendered = rendered.replace("{" + p.wire + "}", "{" + p.name + "}")
    query = [p for p in params if p.where == "query"]
    form = [p for p in params if p.where == "formData"]
    jsonf = [p for p in params if p.where == "json"]
    raw = [p for p in params if p.where == "rawjson"]
    call = [
        f'"{verb.upper()}"',
        f'f"{rendered}"' if "{" in rendered else f'"{rendered}"',
    ]
    if query:
        call.append(
            "params={" + ", ".join(f'"{p.wire}": {p.name}' for p in query) + "}"
        )
    if jsonf:
        call.append(
            "data=_clean({" + ", ".join(f'"{p.wire}": {p.name}' for p in jsonf) + "})"
        )
    elif raw:
        call.append(f"data={raw[0].name}")
    if form:
        call.append("form={" + ", ".join(f'"{p.wire}": {p.name}' for p in form) + "}")
    lines.append(f"        return self._request({', '.join(call)})")
    return name, "\n".join(lines)


def main() -> None:
    app, spec_path, prefix = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
    auth_kw = sys.argv[4] if len(sys.argv) > 4 else "api_key"
    text = spec_path.read_text(encoding="utf-8")
    spec = json.loads(text) if spec_path.suffix == ".json" else yaml.safe_load(text)
    title = app.title()
    methods: dict[str, str] = {}
    for path, item in spec["paths"].items():
        for verb in _VERBS:
            if verb not in item:
                continue
            name, body = _render_method(spec, prefix, verb, path, item, item[verb])
            if name in methods:
                raise SystemExit(f"duplicate method name {name} for {verb} {path}")
            methods[name] = body
    version = spec.get("info", {}).get("version", "")
    out = _HEADER.format(
        title=title,
        source=f"{spec_path.name} {version}".strip(),
        app=app,
        auth_kw=auth_kw,
    )
    out += "\n" + "\n\n".join(methods[n] for n in methods) + "\n"
    target = Path(f"arr_mcp/api/api_client_{app}.py")
    target.write_text(out, encoding="utf-8")
    print(f"{target}: {len(methods)} operations")


if __name__ == "__main__":
    main()
