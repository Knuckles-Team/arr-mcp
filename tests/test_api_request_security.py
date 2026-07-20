"""Outbound request boundary tests shared by generated arr clients."""

import importlib.util
import json
from pathlib import Path

import pytest
import requests

from arr_mcp.api._security import decode_response, request_url, validate_base_url

GENERATOR_PATH = Path(__file__).parents[1] / "scripts" / "generate_api.py"


def _load_generator_module():
    spec = importlib.util.spec_from_file_location("_arr_secure_generator", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_request_url_preserves_configured_origin():
    base_url, origin = validate_base_url("https://media.example.test:8443")

    assert (
        request_url(base_url, origin, "/api/v3/series/1")
        == "https://media.example.test:8443/api/v3/series/1"
    )


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://attacker.example/api",
        "//attacker.example/api",
        "\r\nX-Injected: true",
    ],
)
def test_request_url_rejects_origin_and_header_injection(endpoint):
    base_url, origin = validate_base_url("http://media.example.test")

    with pytest.raises(ValueError):
        request_url(base_url, origin, endpoint)


@pytest.mark.parametrize(
    "base_url",
    [
        "file:///tmp/service",
        "https://user:password@media.example.test",
        "https://media.example.test?token=secret",
    ],
)
def test_validate_base_url_rejects_non_origin_configuration(base_url):
    with pytest.raises(ValueError):
        validate_base_url(base_url)


def test_response_decoder_rejects_oversized_streamed_content():
    response = requests.Response()
    response.status_code = 200
    response.headers = {}
    response.iter_content = lambda **_kwargs: iter([b"x" * (16 * 1024 * 1024 + 1)])

    with pytest.raises(RuntimeError, match="size limit"):
        decode_response(response)


def test_generator_quotes_untrusted_openapi_text(tmp_path):
    module = _load_generator_module()
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "generated"
    output_dir.mkdir()
    spec_path.write_text(
        json.dumps(
            {
                "paths": {
                    '/api/items/{item_id}/\"; injected = True; #': {
                        "get": {
                            "operationId": "getItem",
                            "description": '\"\"\"; injected = True; #',
                            "parameters": [
                                {
                                    "name": "item_id",
                                    "in": "path",
                                    "required": True,
                                    "schema": {"type": "string"},
                                }
                            ],
                        }
                    }
                }
            }
        )
    )
    generator = module.Generator(str(spec_path), str(output_dir), "synthetic")

    generator.parse_spec()
    generator.write_api_file()

    source = (output_dir / "synthetic_api.py").read_text()
    compile(source, "<generated-arr-client>", "exec")
    assert "injected = True\n" not in source


def test_generator_rejects_names_that_collide_after_normalization(tmp_path):
    module = _load_generator_module()
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(
        json.dumps(
            {
                "paths": {
                    "/api/items": {
                        "get": {
                            "operationId": "items",
                            "parameters": [
                                {"name": "item-id", "in": "query"},
                                {"name": "itemid", "in": "query"},
                            ],
                        }
                    }
                }
            }
        )
    )
    generator = module.Generator(str(spec_path), str(tmp_path), "synthetic")

    with pytest.raises(ValueError, match="collide"):
        generator.parse_spec()
