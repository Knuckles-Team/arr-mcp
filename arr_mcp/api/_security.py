"""Shared outbound-request boundaries for generated arr API clients."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import SplitResult, urljoin, urlsplit

import httpx
from scion_sdk.auth.static import ApiKeyAuth
from scion_sdk.http.client import build_http_client
from scion_sdk.http.options import HttpClientOptions
from scion_sdk.tls.profile import ResolvedTLSProfile

_MAX_ENDPOINT_CHARS = 4096
_MAX_RESPONSE_BYTES = 16 * 1024 * 1024
#: Indexer and download-client tests, provider subtitle searches and FlareSolverr
#: challenges routinely take one to four minutes upstream; a shorter read
#: timeout reported a working call as "Upstream timed out".
_MAX_RESPONSE_SECONDS = 300.0
REQUEST_TIMEOUT = httpx.Timeout(300.0, connect=5.0)
#: Bytes of an error body read to explain a failed call.
_MAX_ERROR_BYTES = 16 * 1024
#: Characters of explanation kept in the raised message.
_MAX_ERROR_CHARS = 1500


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


def build_client(
    base_url: str, tls_profile: ResolvedTLSProfile, api_key: str | None = None
) -> httpx.Client:
    """A governed SDK client for one arr service; the key travels as ``X-Api-Key``."""
    return build_http_client(
        HttpClientOptions(
            base_url=base_url,
            timeout=REQUEST_TIMEOUT,
            tls=tls_profile,
            auth=ApiKeyAuth(api_key, header="X-Api-Key") if api_key else None,
            allow_plaintext=base_url.lower().startswith("http://"),
        )
    )


def send_request(
    client: httpx.Client,
    method: str,
    url: str,
    params: dict[str, Any] | None,
    data: Any,
    *,
    form: dict[str, Any] | None = None,
) -> httpx.Response:
    """Send one request and leave the body unread so it can be size-bounded.

    ``data`` travels as a JSON body, ``form`` as a form-encoded body; a call
    names at most one of them.
    """
    if form:
        request = client.build_request(method, url, params=params, data=form)
    else:
        request = client.build_request(method, url, params=params, json=data)
    return client.send(request, stream=True)


#: Refusal raised when an API call answers with a web page instead of data.
NOT_AN_API_RESPONSE = "NOT_AN_API_RESPONSE"


def _refuse_html(response: httpx.Response) -> None:
    """An HTML page is the app's web UI (a wrong route or a login redirect), never data."""
    kind = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if kind in {"text/html", "application/xhtml+xml"}:
        raise RuntimeError(
            f"{NOT_AN_API_RESPONSE}: HTTP {response.status_code} returned a web page; "
            "the route does not exist on this app version or the API key was refused"
        )


def _error_detail(payload: Any) -> str:
    """Flatten an arr / Seerr / Bazarr error body into one readable line."""
    if isinstance(payload, list):
        parts = []
        for item in payload:
            if isinstance(item, dict):
                message = item.get("errorMessage") or item.get("message")
                prop = item.get("propertyName")
                if message:
                    parts.append(f"{prop}: {message}" if prop else str(message))
                    continue
            parts.append(str(item))
        return "; ".join(parts)
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, dict):
            flat = [
                f"{key}: {' '.join(map(str, value)) if isinstance(value, list) else value}"
                for key, value in errors.items()
            ]
            title = payload.get("title")
            return "; ".join(([str(title)] if title else []) + flat)
        for key in ("message", "detail", "error", "title"):
            if payload.get(key):
                return str(payload[key])
    return str(payload)


def raise_for_api_error(response: httpx.Response) -> None:
    """Raise when the call failed, carrying the status and the app's own reason.

    The reason is the upstream validation or error message (for example
    ``baseUrl: Unable to connect to indexer``), read from a bounded body, so an
    agent can act on it instead of seeing only ``HTTP 400``.
    """
    if response.status_code < 400:
        return
    status = response.status_code
    raw = bytearray()
    try:
        if isinstance(response, httpx.Response):
            for chunk in response.iter_bytes(chunk_size=4096):
                raw.extend(chunk)
                if len(raw) >= _MAX_ERROR_BYTES:
                    break
        else:
            raw.extend(str(getattr(response, "text", "") or "").encode())
    except Exception:  # noqa: BLE001 - an unreadable body still raises the status
        raw.clear()
    text = raw[:_MAX_ERROR_BYTES].decode("utf-8", errors="replace").strip()
    kind = (
        str(response.headers.get("content-type", "")).split(";", 1)[0].strip().lower()
    )
    if not text:
        detail = ""
    elif kind in {"text/html", "application/xhtml+xml"} or text.startswith("<"):
        detail = (
            "the app answered with a web page (wrong route, proxy error or refused key)"
        )
    else:
        try:
            detail = _error_detail(json.loads(text))
        except (json.JSONDecodeError, ValueError):
            detail = text
    detail = " ".join(detail.split())[:_MAX_ERROR_CHARS]
    raise RuntimeError(
        f"API error: HTTP {status}: {detail}" if detail else f"API error: HTTP {status}"
    )


def decode_response(response: httpx.Response) -> Any:
    """Decode one response while bounding decompressed production content."""
    if isinstance(response, httpx.Response):
        _refuse_html(response)
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
        for chunk in response.iter_bytes(chunk_size=64 * 1024):
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
    "NOT_AN_API_RESPONSE",
    "REQUEST_TIMEOUT",
    "build_client",
    "send_request",
    "decode_response",
    "raise_for_api_error",
    "request_url",
    "validate_base_url",
]
