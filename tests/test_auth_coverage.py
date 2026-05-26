from unittest.mock import patch, MagicMock
import pytest
import os

from arr_mcp.auth import (
    get_sonarr_client,
    get_radarr_client,
    get_lidarr_client,
    get_prowlarr_client,
    get_bazarr_client,
    get_seerr_client,
    get_chaptarr_client,
)


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


def test_get_sonarr_client_success():
    with patch.dict(
        os.environ,
        {
            "SONARR_BASE_URL": "http://sonarr.test",
            "SONARR_TOKEN": "sonarr-token",
            "SONARR_SSL_VERIFY": "True",
        },
    ):
        with patch("arr_mcp.auth.SonarrApi") as mock_api:
            client = get_sonarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://sonarr.test", token="sonarr-token", verify=True
            )


def test_get_radarr_client_success():
    with patch.dict(
        os.environ,
        {
            "RADARR_BASE_URL": "http://radarr.test",
            "RADARR_TOKEN": "radarr-token",
            "RADARR_SSL_VERIFY": "False",
        },
    ):
        with patch("arr_mcp.auth.RadarrApi") as mock_api:
            client = get_radarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://radarr.test", token="radarr-token", verify=False
            )


def test_get_lidarr_client_success():
    with patch.dict(
        os.environ,
        {
            "LIDARR_BASE_URL": "http://lidarr.test",
            "LIDARR_TOKEN": "lidarr-token",
            "LIDARR_SSL_VERIFY": "True",
        },
    ):
        with patch("arr_mcp.auth.LidarrApi") as mock_api:
            client = get_lidarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://lidarr.test", token="lidarr-token", verify=True
            )


def test_get_prowlarr_client_success():
    with patch.dict(
        os.environ,
        {
            "PROWLARR_BASE_URL": "http://prowlarr.test",
            "PROWLARR_TOKEN": "prowlarr-token",
            "PROWLARR_SSL_VERIFY": "False",
        },
    ):
        with patch("arr_mcp.auth.ProwlarrApi") as mock_api:
            client = get_prowlarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://prowlarr.test", token="prowlarr-token", verify=False
            )


def test_get_bazarr_client_success():
    with patch.dict(
        os.environ,
        {
            "BAZARR_BASE_URL": "http://bazarr.test",
            "BAZARR_API_KEY": "bazarr-key",
            "BAZARR_SSL_VERIFY": "True",
        },
    ):
        with patch("arr_mcp.auth.BazarrApi") as mock_api:
            client = get_bazarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://bazarr.test", api_key="bazarr-key", verify=True
            )


def test_get_seerr_client_success():
    with patch.dict(
        os.environ,
        {
            "SEERR_BASE_URL": "http://seerr.test",
            "SEERR_API_KEY": "seerr-key",
            "SEERR_SSL_VERIFY": "False",
        },
    ):
        with patch("arr_mcp.auth.SeerrApi") as mock_api:
            client = get_seerr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://seerr.test", api_key="seerr-key", verify=False
            )


def test_get_chaptarr_client_success():
    with patch.dict(
        os.environ,
        {
            "CHAPTARR_BASE_URL": "http://chaptarr.test",
            "CHAPTARR_TOKEN": "chaptarr-token",
            "CHAPTARR_SSL_VERIFY": "True",
        },
    ):
        with patch("arr_mcp.auth.ChaptarrApi") as mock_api:
            client = get_chaptarr_client()
            assert client is not None
            mock_api.assert_called_once_with(
                base_url="http://chaptarr.test", token="chaptarr-token", verify=True
            )
