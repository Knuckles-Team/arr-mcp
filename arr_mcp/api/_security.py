"""Shared outbound-request boundaries for generated arr API clients."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import SplitResult, urljoin, urlsplit

import requests

_MAX_ENDPOINT_CHARS = 4096
_MAX_RESPONSE_BYTES = 16 * 1024 * 1024
_MAX_RESPONSE_SECONDS = 60.0
REQUEST_TIMEOUT = (5.0, 30.0)


def _origin(parsed: SplitResult) -> tuple[str, str, int]:
    scheme = parsed.scheme.lower()
    default_port = 443 if scheme == "https" else 80
    return scheme, (parsed.hostname or "").lower(), parsed.port or default_port


def validate_base_url(base_url: str) -> tuple[str, tuple[str, str, int]]:
    """Validate a configured service URL and return its canonical origin."""
    rendered = str(base_url or "").strip()
    if (
        not rendered
        or len(rendered) > 2048
        or any(char in rendered for char in "\x00\r\n")
    ):
        raise ValueError("Invalid service base URL")
    try:
        parsed = urlsplit(rendered)
        origin = _origin(parsed)
    except ValueError as exc:
        raise ValueError("Invalid service base URL") from exc
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "Service base URL must be an HTTP(S) origin without credentials"
        )
    return rendered.rstrip("/") + "/", origin


def request_url(
    base_url: str,
    expected_origin: tuple[str, str, int],
    endpoint: str,
) -> str:
    """Join one endpoint without permitting authority/scheme changes."""
    rendered = str(endpoint or "")
    if len(rendered) > _MAX_ENDPOINT_CHARS or any(
        char in rendered for char in "\x00\r\n"
    ):
        raise ValueError("Invalid API endpoint")
    try:
        url = urljoin(base_url, rendered)
        parsed = urlsplit(url)
        actual_origin = _origin(parsed)
    except ValueError as exc:
        raise ValueError("Invalid API endpoint") from exc
    if actual_origin != expected_origin:
        raise ValueError("API endpoint changed the configured service origin")
    return url


def decode_response(response: requests.Response) -> Any:
    """Decode one response while bounding decompressed production content."""
    if isinstance(response, requests.Response):
        declared = response.headers.get("content-length")
        if declared:
            try:
                declared_size = int(declared)
            except ValueError as exc:
                raise RuntimeError("Invalid API response content length") from exc
            if declared_size < 0 or declared_size > _MAX_RESPONSE_BYTES:
                raise RuntimeError("API response size limit exceeded")
        body = bytearray()
        deadline = time.monotonic() + _MAX_RESPONSE_SECONDS
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if time.monotonic() > deadline:
                raise RuntimeError("API response time limit exceeded")
            if not chunk:
                continue
            body.extend(chunk)
            if len(body) > _MAX_RESPONSE_BYTES:
                raise RuntimeError("API response size limit exceeded")
        try:
            return json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {
                "status": "success",
                "text": body.decode("utf-8", errors="replace")[:4096],
            }

    # Protocol-compatible test doubles and injected sessions retain the same
    # behavior without pretending their synthetic bodies came from the network.
    try:
        return response.json()
    except Exception:
        return {"status": "success", "text": response.text[:4096]}


__all__ = [
    "REQUEST_TIMEOUT",
    "decode_response",
    "request_url",
    "validate_base_url",
]
