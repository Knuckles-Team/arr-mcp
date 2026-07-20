import os
from unittest.mock import MagicMock, patch

import pytest

from arr_mcp.api.api_client_sonarr import Api as SonarrApi
from arr_mcp.auth import (
    get_bazarr_client,
    get_chaptarr_client,
    get_lidarr_client,
    get_prowlarr_client,
    get_radarr_client,
    get_seerr_client,
    get_sonarr_client,
)


@pytest.fixture
def tls_profile():
    profile = MagicMock()
    with patch("arr_mcp.auth.resolve_tls_profile", return_value=profile) as resolver:
        yield profile
    resolver.assert_called_once()


def test_requests_session_uses_resolved_tls_profile():
    profile = MagicMock()
    client = SonarrApi(
        base_url="https://sonarr.example.invalid",
        token="token",
        tls_profile=profile,
    )
    profile.configure_requests_session.assert_called_once_with(client._session)


@pytest.mark.parametrize(
    "getter,env_var",
    [
        (get_sonarr_client, "SONARR_BASE_URL"),
        (get_radarr_client, "RADARR_BASE_URL"),
        (get_lidarr_client, "LIDARR_BASE_URL"),
        (get_prowlarr_client, "PROWLARR_BASE_URL"),
        (get_bazarr_client, "BAZARR_BASE_URL"),
        (get_seerr_client, "SEERR_BASE_URL"),
        (get_chaptarr_client, "CHAPTARR_BASE_URL"),
    ],
)
def test_auth_missing_base_url(getter, env_var):
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(RuntimeError, match=f"{env_var} not set"):
            getter()


def test_get_sonarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "SONARR_BASE_URL": "http://sonarr.test",
            "SONARR_TOKEN": "sonarr-token",
        },
    ):
        with patch("arr_mcp.auth.SonarrApi") as mock_api:
            client = get_sonarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://sonarr.test", token="sonarr-token", tls_profile=tls_profile
            )


def test_get_radarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "RADARR_BASE_URL": "http://radarr.test",
            "RADARR_TOKEN": "radarr-token",
        },
    ):
        with patch("arr_mcp.auth.RadarrApi") as mock_api:
            client = get_radarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://radarr.test", token="radarr-token", tls_profile=tls_profile
            )


def test_get_lidarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "LIDARR_BASE_URL": "http://lidarr.test",
            "LIDARR_TOKEN": "lidarr-token",
        },
    ):
        with patch("arr_mcp.auth.LidarrApi") as mock_api:
            client = get_lidarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://lidarr.test", token="lidarr-token", tls_profile=tls_profile
            )


def test_get_prowlarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "PROWLARR_BASE_URL": "http://prowlarr.test",
            "PROWLARR_TOKEN": "prowlarr-token",
        },
    ):
        with patch("arr_mcp.auth.ProwlarrApi") as mock_api:
            client = get_prowlarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://prowlarr.test", token="prowlarr-token", tls_profile=tls_profile
            )


def test_get_bazarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "BAZARR_BASE_URL": "http://bazarr.test",
            "BAZARR_API_KEY": "bazarr-key",
        },
    ):
        with patch("arr_mcp.auth.BazarrApi") as mock_api:
            client = get_bazarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://bazarr.test", api_key="bazarr-key", tls_profile=tls_profile
            )


def test_get_seerr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "SEERR_BASE_URL": "http://seerr.test",
            "SEERR_API_KEY": "seerr-key",
        },
    ):
        with patch("arr_mcp.auth.SeerrApi") as mock_api:
            client = get_seerr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://seerr.test", api_key="seerr-key", tls_profile=tls_profile
            )


def test_get_chaptarr_client_success(tls_profile):
    with patch.dict(
        os.environ,
        {
            "CHAPTARR_BASE_URL": "http://chaptarr.test",
            "CHAPTARR_TOKEN": "chaptarr-token",
        },
    ):
        with patch("arr_mcp.auth.ChaptarrApi") as mock_api:
            client = get_chaptarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://chaptarr.test", token="chaptarr-token", tls_profile=tls_profile
            )
