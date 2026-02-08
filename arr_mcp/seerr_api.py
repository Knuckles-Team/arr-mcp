#!/usr/bin/env python
# coding: utf-8

import requests
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin
import urllib3


class Api:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        verify: bool = False,
    ):
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
        hostname: Optional[str] = None,
        email: Optional[str] = None,
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

    def post_request(self, media_type: str, media_id: int, seasons: List[int] = None, is4k: bool = False, server_id: int = None, profile_id: int = None, root_folder: str = None) -> Any:
        """Create a new request"""
        data = {
            "mediaType": media_type,
            "mediaId": media_id,
            "is4k": is4k
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

    def get_request(self, take: int = 20, skip: int = 0, filter: str = None, sort: str = 'added') -> Any:
        """Get all requests"""
        params = {
            "take": take,
            "skip": skip,
            "sort": sort
        }
        if filter:
            params["filter"] = filter
        return self.request("GET", "/api/v1/request", params=params)

    def get_request_id(self, request_id: int) -> Any:
         """Get a specific request"""
         return self.request("GET", f"/api/v1/request/{request_id}")

    def put_request_id(self, request_id: int, media_type: str, seasons: List[int] = None, server_id: int = None, profile_id: int = None, root_folder: str = None) -> Any:
        """Update a request"""
        data = {
            "mediaType": media_type
        }
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
    
    def get_search(self, query: str, page: int = 1, language: str = 'en') -> Any:
        """Search for content"""
        params = {
            "query": query,
            "page": page,
            "language": language
        }
        return self.request("GET", "/api/v1/search", params=params)
    
    def get_user(self, take: int = 20, skip: int = 0, sort: str = 'created') -> Any:
        """Get all users"""
        params = {
            "take": take,
            "skip": skip,
            "sort": sort
        }
        return self.request("GET", "/api/v1/user", params=params)

    def get_user_id(self, user_id: int) -> Any:
        """Get user details"""
        return self.request("GET", f"/api/v1/user/{user_id}")
