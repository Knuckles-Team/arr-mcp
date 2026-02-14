"""
Bazarr API Client.

This module provides a class to interact with the Bazarr API for managing subtitles.
"""

import requests
from typing import Dict, Optional, Any
from urllib.parse import urljoin
import urllib3


class Api:
    """
    API client for Bazarr.

    Handles authentication, request session management, and provides methods
    for various Bazarr endpoints including series, movies, subtitles, and system status.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        verify: bool = False,
    ):
        """
        Initialize the Bazarr API client.

        Args:
            base_url (str): The base URL of the Bazarr instance (e.g., http://localhost:6767).
            api_key (Optional[str]): The API key for authentication.
            verify (bool): Whether to verify SSL certificates. Defaults to False.
        """
        self.base_url = base_url
        self.api_key = api_key
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if api_key:
            self._session.headers.update({"X-Api-Key": api_key})

    def request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ) -> Any:
        """
        Generic request method for the Bazarr API.

        Args:
            method (str): HTTP method (GET, POST, DELETE, etc.).
            endpoint (str): API endpoint path.
            params (Dict, optional): Query parameters for the request.
            data (Dict, optional): JSON body data for the request.

        Returns:
            Any: The JSON response from the API or a success status dictionary.

        Raises:
            Exception: If the API returns a status code >= 400.
        """
        url = urljoin(self.base_url, endpoint)
        response = self._session.request(
            method=method, url=url, params=params, json=data
        )
        if response.status_code >= 400:
            try:
                error_text = response.text
            except Exception:
                error_text = "Unknown error"
            raise Exception(f"API error: {response.status_code} - {error_text}")
        if response.status_code == 204:
            return {"status": "success"}
        try:
            return response.json()
        except Exception:
            return {"status": "success", "text": response.text}

    def get_series(self, page: int = 1, page_size: int = 20) -> Any:
        """Get all series managed by Bazarr."""
        return self.request(
            "GET", "/api/series", params={"page": page, "pageSize": page_size}
        )

    def get_series_subtitles(self, series_id: int) -> Any:
        """Get subtitle information for a specific series."""
        return self.request("GET", f"/api/series/{series_id}")

    def get_episode_subtitles(self, episode_id: int) -> Any:
        """Get subtitle information for a specific episode."""
        return self.request("GET", f"/api/episodes/{episode_id}")

    def search_series_subtitles(
        self, series_id: int, episode_id: Optional[int] = None
    ) -> Any:
        """Search for subtitles for a series or episode."""
        if episode_id:
            return self.request(
                "POST", "/api/episodes/search", data={"episodeId": episode_id}
            )
        return self.request("POST", "/api/series/search", data={"seriesId": series_id})

    def download_series_subtitle(
        self,
        episode_id: int,
        language: str,
        forced: bool = False,
        hi: bool = False,
    ) -> Any:
        """Download a subtitle for an episode."""
        data = {
            "episodeId": episode_id,
            "language": language,
            "forced": forced,
            "hi": hi,
        }
        return self.request("POST", "/api/episodes/subtitles", data=data)

    def get_movies(self, page: int = 1, page_size: int = 20) -> Any:
        """Get all movies managed by Bazarr."""
        return self.request(
            "GET", "/api/movies", params={"page": page, "pageSize": page_size}
        )

    def get_movie_subtitles(self, movie_id: int) -> Any:
        """Get subtitle information for a specific movie."""
        return self.request("GET", f"/api/movies/{movie_id}")

    def search_movie_subtitles(self, movie_id: int) -> Any:
        """Search for subtitles for a movie."""
        return self.request("POST", "/api/movies/search", data={"movieId": movie_id})

    def download_movie_subtitle(
        self,
        movie_id: int,
        language: str,
        forced: bool = False,
        hi: bool = False,
    ) -> Any:
        """Download a subtitle for a movie."""
        data = {
            "movieId": movie_id,
            "language": language,
            "forced": forced,
            "hi": hi,
        }
        return self.request("POST", "/api/movies/subtitles", data=data)

    def get_history(self, page: int = 1, page_size: int = 20) -> Any:
        """Get subtitle download history."""
        return self.request(
            "GET", "/api/history", params={"page": page, "pageSize": page_size}
        )

    def get_languages(self) -> Any:
        """Get all available subtitle languages."""
        return self.request("GET", "/api/languages")

    def get_enabled_languages(self) -> Any:
        """Get currently enabled subtitle languages."""
        return self.request("GET", "/api/languages/enabled")

    def get_providers(self) -> Any:
        """Get all subtitle providers."""
        return self.request("GET", "/api/providers")

    def get_enabled_providers(self) -> Any:
        """Get enabled subtitle providers."""
        return self.request("GET", "/api/providers/enabled")

    def test_provider(self, provider_name: str) -> Any:
        """Test a subtitle provider."""
        return self.request(
            "POST", "/api/providers/test", data={"provider": provider_name}
        )

    def get_system_status(self) -> Any:
        """Get Bazarr system status."""
        return self.request("GET", "/api/system/status")

    def get_system_health(self) -> Any:
        """Get system health issues."""
        return self.request("GET", "/api/system/health")

    def get_system_logs(self, lines: int = 50) -> Any:
        """Get system logs."""
        return self.request("GET", "/api/system/logs", params={"lines": lines})

    def get_settings(self) -> Any:
        """Get Bazarr settings."""
        return self.request("GET", "/api/system/settings")

    def update_settings(self, settings_data: Dict) -> Any:
        """Update Bazarr settings."""
        return self.request("POST", "/api/system/settings", data=settings_data)

    def get_wanted_series(self, page: int = 1, page_size: int = 20) -> Any:
        """Get series episodes with wanted/missing subtitles."""
        return self.request(
            "GET", "/api/episodes/wanted", params={"page": page, "pageSize": page_size}
        )

    def get_wanted_movies(self, page: int = 1, page_size: int = 20) -> Any:
        """Get movies with wanted/missing subtitles."""
        return self.request(
            "GET", "/api/movies/wanted", params={"page": page, "pageSize": page_size}
        )

    def get_blacklist(self) -> Any:
        """Get blacklisted subtitles."""
        return self.request("GET", "/api/blacklist")

    def add_to_blacklist(self, subtitle_id: str, media_type: str) -> Any:
        """Add a subtitle to blacklist."""
        data = {"subtitleId": subtitle_id, "mediaType": media_type}
        return self.request("POST", "/api/blacklist", data=data)

    def remove_from_blacklist(self, blacklist_id: int) -> Any:
        """Remove a subtitle from blacklist."""
        return self.request("DELETE", f"/api/blacklist/{blacklist_id}")
