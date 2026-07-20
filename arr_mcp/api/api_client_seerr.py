"""
Seerr API Client.

This module provides a class to interact with the Overseerr/Jellyseerr (Seerr) API
for managing media requests.
"""

from typing import Any

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_tls_profile,
)

from arr_mcp.api._security import (
    REQUEST_TIMEOUT,
    decode_response,
    request_url,
    validate_base_url,
)


class Api:
    """
    API client for Seerr (Overseerr/Jellyseerr).

    Handles authentication, request session management, and provides methods
    for managing media requests, authentication, and status.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        """
        Initialize the Seerr API client.

        Args:
            base_url (str): The base URL of the Seerr instance.
            api_key (Optional[str]): The API key for authentication.
            tls_profile: Runtime trust, mTLS, and proxy policy. Resolved automatically when omitted.
        """
        self.base_url, self._origin = validate_base_url(base_url)
        self.api_key = api_key
        self._session = requests.Session()
        self._tls_profile = tls_profile or resolve_tls_profile("seerr")
        self._tls_profile.configure_requests_session(self._session)

        if api_key:
            self._session.headers.update({"X-Api-Key": api_key})

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """
        Generic request method for the Seerr API.

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
        url = request_url(self.base_url, self._origin, endpoint)
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=data,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
            stream=True,
        )
        try:
            if response.status_code >= 400:
                raise RuntimeError(f"API error: HTTP {response.status_code}")
            if response.status_code == 204:
                return {"status": "success"}
            result = decode_response(response)
            if isinstance(result, list):
                return {"result": result}
            return result
        finally:
            response.close()

    def get_status(self) -> Any:
        """Get Seerr status"""
        return self.request("GET", "/api/v1/status")

    def get_status_appdata(self) -> Any:
        """Get application data volume status"""
        return self.request("GET", "/api/v1/status/appdata")

    def post_auth_local(self, email: str, password: str) -> Any:
        """Sign in using a local account"""
        data = {"email": email, "password": password}
        return self.request("POST", "/api/v1/auth/local", data=data)

    def post_auth_plex(self, authToken: str) -> Any:
        """Sign in using a Plex token"""
        data = {"authToken": authToken}
        return self.request("POST", "/api/v1/auth/plex", data=data)

    def post_auth_jellyfin(
        self,
        username: str,
        password: str,
        hostname: str | None = None,
        email: str | None = None,
    ) -> Any:
        """Sign in using a Jellyfin username and password"""
        data = {"username": username, "password": password}
        if hostname:
            data["hostname"] = hostname
        if email:
            data["email"] = email
        return self.request("POST", "/api/v1/auth/jellyfin", data=data)

    def post_auth_logout(self) -> Any:
        """Sign out and clear session cookie"""
        return self.request("POST", "/api/v1/auth/logout")

    def get_auth_me(self) -> Any:
        """Get logged-in user"""
        return self.request("GET", "/api/v1/auth/me")

    def post_request(
        self,
        media_type: str,
        media_id: int,
        seasons: list[int] | None = None,
        is4k: bool = False,
        server_id: int | None = None,
        profile_id: int | None = None,
        root_folder: str | None = None,
    ) -> Any:
        """Create a new request"""
        data: dict[str, Any] = {
            "mediaType": media_type,
            "mediaId": media_id,
            "is4k": is4k,
        }
        if seasons:
            data["seasons"] = seasons
        if server_id:
            data["serverId"] = server_id
        if profile_id:
            data["profileId"] = profile_id
        if root_folder:
            data["rootFolder"] = root_folder

        return self.request("POST", "/api/v1/request", data=data)

    def get_request(
        self,
        take: int = 20,
        skip: int = 0,
        filter: str | None = None,
        sort: str = "added",
    ) -> Any:
        """Get all requests"""
        params = {"take": take, "skip": skip, "sort": sort}
        if filter:
            params["filter"] = filter
        return self.request("GET", "/api/v1/request", params=params)

    def get_request_id(self, request_id: int) -> Any:
        """Get a specific request"""
        return self.request("GET", f"/api/v1/request/{request_id}")

    def put_request_id(
        self,
        request_id: int,
        media_type: str,
        seasons: list[int] | None = None,
        server_id: int | None = None,
        profile_id: int | None = None,
        root_folder: str | None = None,
    ) -> Any:
        """Update a request"""
        data: dict[str, Any] = {"mediaType": media_type}
        if seasons:
            data["seasons"] = seasons
        if server_id:
            data["serverId"] = server_id
        if profile_id:
            data["profileId"] = profile_id
        if root_folder:
            data["rootFolder"] = root_folder
        return self.request("PUT", f"/api/v1/request/{request_id}", data=data)

    def delete_request_id(self, request_id: int) -> Any:
        """Delete a request"""
        return self.request("DELETE", f"/api/v1/request/{request_id}")

    def post_request_id_approve(self, request_id: int) -> Any:
        """Approve a request"""
        return self.request("POST", f"/api/v1/request/{request_id}/approve")

    def post_request_id_decline(self, request_id: int) -> Any:
        """Decline a request"""
        return self.request("POST", f"/api/v1/request/{request_id}/decline")

    def get_movie_id(self, movie_id: int) -> Any:
        """Get movie details"""
        return self.request("GET", f"/api/v1/movie/{movie_id}")

    def get_tv_id(self, tv_id: int) -> Any:
        """Get TV details"""
        return self.request("GET", f"/api/v1/tv/{tv_id}")

    def get_search(self, query: str, page: int = 1, language: str = "en") -> Any:
        """Search for content"""
        params = {"query": query, "page": page, "language": language}
        return self.request("GET", "/api/v1/search", params=params)

    def get_user(self, take: int = 20, skip: int = 0, sort: str = "created") -> Any:
        """Get all users"""
        params = {"take": take, "skip": skip, "sort": sort}
        return self.request("GET", "/api/v1/user", params=params)

    def get_user_id(self, user_id: int) -> Any:
        """Get user details"""
        return self.request("GET", f"/api/v1/user/{user_id}")
