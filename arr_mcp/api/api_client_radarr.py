"""
Radarr API Client.

This module provides a class to interact with the Radarr API for managing movie collections.
"""

from typing import Any
from urllib.parse import urljoin

import requests
import urllib3


class Api:
    """
    API client for Radarr.

    Handles authentication, request session management, and provides methods
    for various Radarr endpoints including movies, collections, custom formats, and system backup.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        verify: bool = False,
    ):
        """
        Initialize the Radarr API client.

        Args:
            base_url (str): The base URL of the Radarr instance.
            token (Optional[str]): The API key or token for authentication.
            verify (bool): Whether to verify SSL certificates. Defaults to False.
        """
        self.base_url = base_url
        self.token = token
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            self._session.headers.update({"X-Api-Key": token})

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """
        Generic request method for the Radarr API.

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
            result = response.json()
            if isinstance(result, list):
                return {"result": result}
            return result
        except Exception:
            return {"status": "success", "text": response.text}

    def get_alttitle(
        self, movieId: int | None = None, movieMetadataId: int | None = None
    ) -> Any:
        """Get alternative titles for movies."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieMetadataId is not None:
            params["movieMetadataId"] = movieMetadataId
        return self.request("GET", "/api/v3/alttitle", params=params, data=None)

    def get_alttitle_id(self, id: int) -> Any:
        """Get a specific alternative title by ID."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/alttitle/{id}", params=params, data=None)

    def get_api(self) -> Any:
        """Get the base API information."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api", params=params, data=None)

    def post_login(self, returnUrl: str | None = None) -> Any:
        """Log in to the Radarr web interface."""
        params: dict[str, Any] = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get login."""
        params: dict[str, Any] = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Get logout."""
        params: dict[str, Any] = {}
        return self.request("GET", "/logout", params=params, data=None)

    def post_autotagging(self, data: dict) -> Any:
        """Add a new autotagging."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """Get autotagging."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/autotagging", params=params, data=None)

    def put_autotagging_id(self, id: str, data: dict) -> Any:
        """Update autotagging id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """Delete autotagging id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_id(self, id: int) -> Any:
        """Get specific autotagging."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_schema(self) -> Any:
        """Get autotagging schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """Get system backup."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """Delete system backup id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """Add a new system backup restore id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """Add a new system backup restore upload."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/system/backup/restore/upload", params=params, data=None
        )

    def get_blocklist(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        movieIds: list | None = None,
        protocols: list | None = None,
    ) -> Any:
        """Get blocklist."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if movieIds is not None:
            params["movieIds"] = movieIds
        if protocols is not None:
            params["protocols"] = protocols
        return self.request("GET", "/api/v3/blocklist", params=params, data=None)

    def get_blocklist_movie(self, movieId: int | None = None) -> Any:
        """Get blocklisted items for a specific movie."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/blocklist/movie", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """Delete blocklist id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: dict) -> Any:
        """Delete blocklist bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/blocklist/bulk", params=params, data=data
        )

    def get_calendar(
        self,
        start: str | None = None,
        end: str | None = None,
        unmonitored: bool | None = None,
        tags: str | None = None,
    ) -> Any:
        """Get calendar."""
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        if tags is not None:
            params["tags"] = tags
        return self.request("GET", "/api/v3/calendar", params=params, data=None)

    def get_feed_v3_calendar_radarrics(
        self,
        pastDays: int | None = None,
        futureDays: int | None = None,
        tags: str | None = None,
        unmonitored: bool | None = None,
        releaseTypes: list | None = None,
    ) -> Any:
        """Get feed v3 calendar radarrics."""
        params: dict[str, Any] = {}
        if pastDays is not None:
            params["pastDays"] = pastDays
        if futureDays is not None:
            params["futureDays"] = futureDays
        if tags is not None:
            params["tags"] = tags
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        if releaseTypes is not None:
            params["releaseTypes"] = releaseTypes
        return self.request(
            "GET", "/feed/v3/calendar/radarr.ics", params=params, data=None
        )

    def get_collection(self, tmdbId: int | None = None) -> Any:
        """Get collection."""
        params: dict[str, Any] = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        return self.request("GET", "/api/v3/collection", params=params, data=None)

    def put_collection(self, data: dict) -> Any:
        """Update collection."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/collection", params=params, data=data)

    def put_collection_id(self, id: str, data: dict) -> Any:
        """Update collection id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/collection/{id}", params=params, data=data)

    def get_collection_id(self, id: int) -> Any:
        """Get specific collection."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/collection/{id}", params=params, data=None)

    def post_command(self, data: dict) -> Any:
        """Add a new command."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/command", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v3/command/{id}", params=params, data=None)

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/command/{id}", params=params, data=None)

    def get_credit(
        self, movieId: int | None = None, movieMetadataId: int | None = None
    ) -> Any:
        """Get credit."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieMetadataId is not None:
            params["movieMetadataId"] = movieMetadataId
        return self.request("GET", "/api/v3/credit", params=params, data=None)

    def get_credit_id(self, id: int) -> Any:
        """Get specific credit."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/credit/{id}", params=params, data=None)

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/customfilter", params=params, data=None)

    def post_customfilter(self, data: dict) -> Any:
        """Add a new customfilter."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/customfilter", params=params, data=data)

    def put_customfilter_id(self, id: str, data: dict) -> Any:
        """Update customfilter id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """Delete customfilter id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customformat(self) -> Any:
        """Get customformat."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/customformat", params=params, data=None)

    def post_customformat(self, data: dict) -> Any:
        """Add a new customformat."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/customformat", params=params, data=data)

    def put_customformat_id(self, id: str, data: dict) -> Any:
        """Update customformat id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """Delete customformat id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def get_customformat_id(self, id: int) -> Any:
        """Get specific customformat."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def put_customformat_bulk(self, data: dict) -> Any:
        """Update customformat bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v3/customformat/bulk", params=params, data=data
        )

    def delete_customformat_bulk(self, data: dict) -> Any:
        """Delete customformat bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/customformat/bulk", params=params, data=data
        )

    def get_customformat_schema(self) -> Any:
        """Get customformat schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/customformat/schema", params=params, data=None
        )

    def get_wanted_cutoff(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        monitored: bool | None = None,
    ) -> Any:
        """Get wanted cutoff."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v3/wanted/cutoff", params=params, data=None)

    def post_delayprofile(self, data: dict) -> Any:
        """Add a new delayprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """Get delayprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """Delete delayprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: dict) -> Any:
        """Update delayprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """Get specific delayprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, after: int | None = None) -> Any:
        """Update delayprofile reorder id."""
        params: dict[str, Any] = {}
        if after is not None:
            params["after"] = after
        return self.request(
            "PUT", f"/api/v3/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """Get diskspace."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/diskspace", params=params, data=None)

    def get_downloadclient(self) -> Any:
        """Get downloadclient."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new downloadclient."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/downloadclient", params=params, data=data)

    def put_downloadclient_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update downloadclient id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """Delete downloadclient id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_bulk(self, data: dict) -> Any:
        """Update downloadclient bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: dict) -> Any:
        """Delete downloadclient bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """Get downloadclient schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(
        self, data: dict, forceTest: bool | None = None
    ) -> Any:
        """Test downloadclient."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """Add a new downloadclient testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: dict) -> Any:
        """Add a new downloadclient action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/config/downloadclient", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: dict) -> Any:
        """Update config downloadclient id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/downloadclient/{id}", params=params, data=None
        )

    def get_extrafile(self, movieId: int | None = None) -> Any:
        """Get extrafile."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/extrafile", params=params, data=None)

    def get_filesystem(
        self,
        path: str | None = None,
        includeFiles: bool | None = None,
        allowFoldersWithoutTrailingSlashes: bool | None = None,
    ) -> Any:
        """Get filesystem."""
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        if includeFiles is not None:
            params["includeFiles"] = includeFiles
        if allowFoldersWithoutTrailingSlashes is not None:
            params["allowFoldersWithoutTrailingSlashes"] = (
                allowFoldersWithoutTrailingSlashes
            )
        return self.request("GET", "/api/v3/filesystem", params=params, data=None)

    def get_filesystem_type(self, path: str | None = None) -> Any:
        """Get filesystem type."""
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v3/filesystem/type", params=params, data=None)

    def get_filesystem_mediafiles(self, path: str | None = None) -> Any:
        """Get filesystem mediafiles."""
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v3/filesystem/mediafiles", params=params, data=None
        )

    def get_health(self) -> Any:
        """Get health."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/health", params=params, data=None)

    def get_history(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeMovie: bool | None = None,
        eventType: list | None = None,
        downloadId: str | None = None,
        movieIds: list | None = None,
        languages: list | None = None,
        quality: list | None = None,
    ) -> Any:
        """Get history."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        if eventType is not None:
            params["eventType"] = eventType
        if downloadId is not None:
            params["downloadId"] = downloadId
        if movieIds is not None:
            params["movieIds"] = movieIds
        if languages is not None:
            params["languages"] = languages
        if quality is not None:
            params["quality"] = quality
        return self.request("GET", "/api/v3/history", params=params, data=None)

    def get_history_since(
        self,
        date: str | None = None,
        eventType: str | None = None,
        includeMovie: bool | None = None,
    ) -> Any:
        """Get history since."""
        params: dict[str, Any] = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/history/since", params=params, data=None)

    def get_history_movie(
        self,
        movieId: int | None = None,
        eventType: str | None = None,
        includeMovie: bool | None = None,
    ) -> Any:
        """Get history movie."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        if eventType is not None:
            params["eventType"] = eventType
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/history/movie", params=params, data=None)

    def post_history_failed_id(self, id: int) -> Any:
        """Add a new history failed id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/history/failed/{id}", params=params, data=None
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/host", params=params, data=None)

    def put_config_host_id(self, id: str, data: dict) -> Any:
        """Update config host id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/host/{id}", params=params, data=data
        )

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/host/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """Get importlist."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/importlist", params=params, data=None)

    def post_importlist(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new importlist."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/importlist", params=params, data=data)

    def put_importlist_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update importlist id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete importlist id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """Get specific importlist."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/importlist/{id}", params=params, data=None)

    def put_importlist_bulk(self, data: dict) -> Any:
        """Update importlist bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: dict) -> Any:
        """Delete importlist bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """Get importlist schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test importlist."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """Add a new importlist testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: dict) -> Any:
        """Add a new importlist action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/importlist/action/{name}", params=params, data=data
        )

    def get_config_importlist(self) -> Any:
        """Get config importlist."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/config/importlist", params=params, data=None
        )

    def put_config_importlist_id(self, id: str, data: dict) -> Any:
        """Update config importlist id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/importlist/{id}", params=params, data=data
        )

    def get_config_importlist_id(self, id: int) -> Any:
        """Get specific config importlist."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/importlist/{id}", params=params, data=None
        )

    def get_exclusions(self) -> Any:
        """Get all movie import exclusions."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/exclusions", params=params, data=None)

    def post_exclusions(self, data: dict) -> Any:
        """Add a new exclusions."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/exclusions", params=params, data=data)

    def get_exclusions_paged(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
    ) -> Any:
        """Get exclusions paged."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        return self.request("GET", "/api/v3/exclusions/paged", params=params, data=None)

    def put_exclusions_id(self, id: str, data: dict) -> Any:
        """Update exclusions id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/exclusions/{id}", params=params, data=data)

    def delete_exclusions_id(self, id: int) -> Any:
        """Delete exclusions id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/exclusions/{id}", params=params, data=None
        )

    def get_exclusions_id(self, id: int) -> Any:
        """Get specific exclusions."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/exclusions/{id}", params=params, data=None)

    def post_exclusions_bulk(self, data: dict) -> Any:
        """Add a new exclusions bulk."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/exclusions/bulk", params=params, data=data)

    def delete_exclusions_bulk(self, data: dict) -> Any:
        """Delete exclusions bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/exclusions/bulk", params=params, data=data
        )

    def get_importlist_movie(
        self,
        includeRecommendations: bool | None = None,
        includeTrending: bool | None = None,
        includePopular: bool | None = None,
    ) -> Any:
        """Get importlist movie."""
        params: dict[str, Any] = {}
        if includeRecommendations is not None:
            params["includeRecommendations"] = includeRecommendations
        if includeTrending is not None:
            params["includeTrending"] = includeTrending
        if includePopular is not None:
            params["includePopular"] = includePopular
        return self.request("GET", "/api/v3/importlist/movie", params=params, data=None)

    def post_importlist_movie(self, data: dict) -> Any:
        """Add a new importlist movie."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/importlist/movie", params=params, data=data
        )

    def get_indexer(self) -> Any:
        """Get indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/indexer", params=params, data=None)

    def post_indexer(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new indexer configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/indexer", params=params, data=data)

    def put_indexer_id(self, id: int, data: dict, forceSave: bool | None = None) -> Any:
        """Update an existing indexer configuration by ID."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """Delete indexer id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v3/indexer/{id}", params=params, data=None)

    def get_indexer_id(self, id: int) -> Any:
        """Get specific indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/indexer/{id}", params=params, data=None)

    def put_indexer_bulk(self, data: dict) -> Any:
        """Update indexer bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: dict) -> Any:
        """Delete indexer bulk."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v3/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """Get indexer schema."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test indexer."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """Add a new indexer testall."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: dict) -> Any:
        """Add a new indexer action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/indexer/action/{name}", params=params, data=data
        )

    def get_config_indexer(self) -> Any:
        """Get config indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/indexer", params=params, data=None)

    def put_config_indexer_id(self, id: str, data: dict) -> Any:
        """Update config indexer id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """Get specific config indexer."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/indexer/{id}", params=params, data=None
        )

    def get_indexerflag(self) -> Any:
        """Get indexerflag."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/indexerflag", params=params, data=None)

    def get_language(self) -> Any:
        """Get language."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/language", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """Get specific language."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/language/{id}", params=params, data=None)

    def get_localization(self) -> Any:
        """Get localization."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/localization", params=params, data=None)

    def get_localization_language(self) -> Any:
        """Get localization language."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/localization/language", params=params, data=None
        )

    def get_log(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        level: str | None = None,
    ) -> Any:
        """Get log."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if level is not None:
            params["level"] = level
        return self.request("GET", "/api/v3/log", params=params, data=None)

    def get_log_file(self) -> Any:
        """Get log file."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """Get log file filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/log/file/{filename}", params=params, data=None
        )

    def get_manualimport(
        self,
        folder: str | None = None,
        downloadId: str | None = None,
        movieId: int | None = None,
        filterExistingFiles: bool | None = None,
    ) -> Any:
        """Get manualimport."""
        params: dict[str, Any] = {}
        if folder is not None:
            params["folder"] = folder
        if downloadId is not None:
            params["downloadId"] = downloadId
        if movieId is not None:
            params["movieId"] = movieId
        if filterExistingFiles is not None:
            params["filterExistingFiles"] = filterExistingFiles
        return self.request("GET", "/api/v3/manualimport", params=params, data=None)

    def post_manualimport(self, data: dict) -> Any:
        """Add a new manualimport."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/manualimport", params=params, data=data)

    def get_mediacover_movie_id_filename(self, movieId: int, filename: str) -> Any:
        """Get specific mediacover movie filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/mediacover/{movieId}/{filename}", params=params, data=None
        )

    def get_config_mediamanagement(self) -> Any:
        """Get config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/config/mediamanagement", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: dict) -> Any:
        """Update config mediamanagement id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """Get specific config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/mediamanagement/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """Get metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/metadata", params=params, data=None)

    def post_metadata(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new metadata."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/metadata", params=params, data=data)

    def put_metadata_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update metadata id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """Delete metadata id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/metadata/{id}", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """Get specific metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/metadata/{id}", params=params, data=None)

    def get_metadata_schema(self) -> Any:
        """Get metadata schema."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test metadata."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """Add a new metadata testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: dict) -> Any:
        """Add a new metadata action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/metadata/action/{name}", params=params, data=data
        )

    def get_config_metadata(self) -> Any:
        """Get config metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/metadata", params=params, data=None)

    def put_config_metadata_id(self, id: str, data: dict) -> Any:
        """Update config metadata id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/metadata/{id}", params=params, data=data
        )

    def get_config_metadata_id(self, id: int) -> Any:
        """Get specific config metadata."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/metadata/{id}", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        monitored: bool | None = None,
    ) -> Any:
        """Get wanted missing."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v3/wanted/missing", params=params, data=None)

    def get_movie(
        self,
        tmdbId: int | None = None,
        excludeLocalCovers: bool | None = None,
        languageId: int | None = None,
    ) -> Any:
        """Get movie."""
        params: dict[str, Any] = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        if excludeLocalCovers is not None:
            params["excludeLocalCovers"] = excludeLocalCovers
        if languageId is not None:
            params["languageId"] = languageId
        return self.request("GET", "/api/v3/movie", params=params, data=None)

    def post_movie(self, data: dict) -> Any:
        """Add a new movie to Radarr."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/movie", params=params, data=data)

    def put_movie_id(self, id: str, data: dict, moveFiles: bool | None = None) -> Any:
        """Update an existing movie configuration."""
        params: dict[str, Any] = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v3/movie/{id}", params=params, data=data)

    def delete_movie_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportExclusion: bool | None = None,
    ) -> Any:
        """Delete movie id."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportExclusion is not None:
            params["addImportExclusion"] = addImportExclusion
        return self.request("DELETE", f"/api/v3/movie/{id}", params=params, data=None)

    def get_movie_id(self, id: int) -> Any:
        """Get specific movie."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/movie/{id}", params=params, data=None)

    def put_movie_editor(self, data: dict) -> Any:
        """Update movie editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/movie/editor", params=params, data=data)

    def delete_movie_editor(self, data: dict) -> Any:
        """Delete movie editor."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v3/movie/editor", params=params, data=data)

    def get_moviefile(
        self, movieId: list | None = None, movieFileIds: list | None = None
    ) -> Any:
        """Get moviefile."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieFileIds is not None:
            params["movieFileIds"] = movieFileIds
        return self.request("GET", "/api/v3/moviefile", params=params, data=None)

    def put_moviefile_id(self, id: str, data: dict) -> Any:
        """Update moviefile id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/moviefile/{id}", params=params, data=data)

    def delete_moviefile_id(self, id: int) -> Any:
        """Delete moviefile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/moviefile/{id}", params=params, data=None
        )

    def get_moviefile_id(self, id: int) -> Any:
        """Get specific moviefile."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/moviefile/{id}", params=params, data=None)

    def put_moviefile_editor(self, data: dict) -> Any:
        """Update moviefile editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/moviefile/editor", params=params, data=data)

    def delete_moviefile_bulk(self, data: dict) -> Any:
        """Delete moviefile bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/moviefile/bulk", params=params, data=data
        )

    def put_moviefile_bulk(self, data: dict) -> Any:
        """Update moviefile bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/moviefile/bulk", params=params, data=data)

    def get_movie_id_folder(self, id: int) -> Any:
        """Get specific movie folder."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/movie/{id}/folder", params=params, data=None
        )

    def post_movie_import(self, data: dict) -> Any:
        """Add a new movie import."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/movie/import", params=params, data=data)

    def get_movie_lookup_tmdb(self, tmdbId: int | None = None) -> Any:
        """Get movie lookup tmdb."""
        params: dict[str, Any] = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        return self.request(
            "GET", "/api/v3/movie/lookup/tmdb", params=params, data=None
        )

    def get_movie_lookup_imdb(self, imdbId: str | None = None) -> Any:
        """Get movie lookup imdb."""
        params: dict[str, Any] = {}
        if imdbId is not None:
            params["imdbId"] = imdbId
        return self.request(
            "GET", "/api/v3/movie/lookup/imdb", params=params, data=None
        )

    def get_movie_lookup(self, term: str | None = None) -> Any:
        """Get movie lookup."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v3/movie/lookup", params=params, data=None)

    def get_config_naming(self) -> Any:
        """Get config naming."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/naming", params=params, data=None)

    def put_config_naming_id(self, id: str, data: dict) -> Any:
        """Update config naming id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/config/naming/{id}", params=params, data=data
        )

    def get_config_naming_id(self, id: int) -> Any:
        """Get specific config naming."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/config/naming/{id}", params=params, data=None
        )

    def get_config_naming_examples(
        self,
        renameMovies: bool | None = None,
        replaceIllegalCharacters: bool | None = None,
        colonReplacementFormat: str | None = None,
        standardMovieFormat: str | None = None,
        movieFolderFormat: str | None = None,
        id: int | None = None,
        resourceName: str | None = None,
    ) -> Any:
        """Get config naming examples."""
        params: dict[str, Any] = {}
        if renameMovies is not None:
            params["renameMovies"] = renameMovies
        if replaceIllegalCharacters is not None:
            params["replaceIllegalCharacters"] = replaceIllegalCharacters
        if colonReplacementFormat is not None:
            params["colonReplacementFormat"] = colonReplacementFormat
        if standardMovieFormat is not None:
            params["standardMovieFormat"] = standardMovieFormat
        if movieFolderFormat is not None:
            params["movieFolderFormat"] = movieFolderFormat
        if id is not None:
            params["id"] = id
        if resourceName is not None:
            params["resourceName"] = resourceName
        return self.request(
            "GET", "/api/v3/config/naming/examples", params=params, data=None
        )

    def get_notification(self) -> Any:
        """Get notification."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/notification", params=params, data=None)

    def post_notification(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new notification."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/notification", params=params, data=data)

    def put_notification_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update notification id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """Delete notification id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_schema(self) -> Any:
        """Get notification schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test notification."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """Add a new notification testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: dict) -> Any:
        """Add a new notification action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/notification/action/{name}", params=params, data=data
        )

    def get_parse(self, title: str | None = None) -> Any:
        """Get parse."""
        params: dict[str, Any] = {}
        if title is not None:
            params["title"] = title
        return self.request("GET", "/api/v3/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """Get ping."""
        params: dict[str, Any] = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: dict) -> Any:
        """Update qualitydefinition id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """Get specific qualitydefinition."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """Get qualitydefinition."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: dict) -> Any:
        """Update qualitydefinition update."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v3/qualitydefinition/update", params=params, data=data
        )

    def get_qualitydefinition_limits(self) -> Any:
        """Get qualitydefinition limits."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition/limits", params=params, data=None
        )

    def post_qualityprofile(self, data: dict) -> Any:
        """Add a new qualityprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """Get qualityprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """Delete qualityprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: dict) -> Any:
        """Update qualityprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """Get specific qualityprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """Get qualityprofile schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/qualityprofile/schema", params=params, data=None
        )

    def delete_queue_id(
        self,
        id: int,
        removeFromClient: bool | None = None,
        blocklist: bool | None = None,
        skipRedownload: bool | None = None,
        changeCategory: bool | None = None,
    ) -> Any:
        """Delete an item from the download queue."""
        params: dict[str, Any] = {}
        if removeFromClient is not None:
            params["removeFromClient"] = removeFromClient
        if blocklist is not None:
            params["blocklist"] = blocklist
        if skipRedownload is not None:
            params["skipRedownload"] = skipRedownload
        if changeCategory is not None:
            params["changeCategory"] = changeCategory
        return self.request("DELETE", f"/api/v3/queue/{id}", params=params, data=None)

    def delete_queue_bulk(
        self,
        data: dict,
        removeFromClient: bool | None = None,
        blocklist: bool | None = None,
        skipRedownload: bool | None = None,
        changeCategory: bool | None = None,
    ) -> Any:
        """Delete queue bulk."""
        params: dict[str, Any] = {}
        if removeFromClient is not None:
            params["removeFromClient"] = removeFromClient
        if blocklist is not None:
            params["blocklist"] = blocklist
        if skipRedownload is not None:
            params["skipRedownload"] = skipRedownload
        if changeCategory is not None:
            params["changeCategory"] = changeCategory
        return self.request("DELETE", "/api/v3/queue/bulk", params=params, data=data)

    def get_queue(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeUnknownMovieItems: bool | None = None,
        includeMovie: bool | None = None,
        movieIds: list | None = None,
        protocol: str | None = None,
        languages: list | None = None,
        quality: list | None = None,
        status: list | None = None,
    ) -> Any:
        """Get queue."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        if includeUnknownMovieItems is not None:
            params["includeUnknownMovieItems"] = includeUnknownMovieItems
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        if movieIds is not None:
            params["movieIds"] = movieIds
        if protocol is not None:
            params["protocol"] = protocol
        if languages is not None:
            params["languages"] = languages
        if quality is not None:
            params["quality"] = quality
        if status is not None:
            params["status"] = status
        return self.request("GET", "/api/v3/queue", params=params, data=None)

    def post_queue_grab_id(self, id: int) -> Any:
        """Add a new queue grab id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v3/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: dict) -> Any:
        """Add a new queue grab bulk."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/queue/grab/bulk", params=params, data=data)

    def get_queue_details(
        self, movieId: int | None = None, includeMovie: bool | None = None
    ) -> Any:
        """Get queue details."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/queue/details", params=params, data=None)

    def get_queue_status(self) -> Any:
        """Get queue status."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/queue/status", params=params, data=None)

    def post_release(self, data: dict) -> Any:
        """Add a new release."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/release", params=params, data=data)

    def get_release(self, movieId: int | None = None) -> Any:
        """Get release."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/release", params=params, data=None)

    def post_releaseprofile(self, data: dict) -> Any:
        """Add a new releaseprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/releaseprofile", params=params, data=data)

    def get_releaseprofile(self) -> Any:
        """Get releaseprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/releaseprofile", params=params, data=None)

    def delete_releaseprofile_id(self, id: int) -> Any:
        """Delete releaseprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def put_releaseprofile_id(self, id: str, data: dict) -> Any:
        """Update releaseprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/releaseprofile/{id}", params=params, data=data
        )

    def get_releaseprofile_id(self, id: int) -> Any:
        """Get specific releaseprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def post_release_push(self, data: dict) -> Any:
        """Add a new release push."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/release/push", params=params, data=data)

    def post_remotepathmapping(self, data: dict) -> Any:
        """Add a new remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """Get remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/remotepathmapping", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """Delete remotepathmapping id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: dict) -> Any:
        """Update remotepathmapping id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/remotepathmapping/{id}", params=params, data=data
        )

    def get_remotepathmapping_id(self, id: int) -> Any:
        """Get specific remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def get_rename(self, movieId: list | None = None) -> Any:
        """Get rename."""
        params: dict[str, Any] = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/rename", params=params, data=None)

    def post_rootfolder(self, data: dict) -> Any:
        """Add a new rootfolder."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """Get rootfolder."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/rootfolder", params=params, data=None)

    def delete_rootfolder_id(self, id: int) -> Any:
        """Delete rootfolder id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/rootfolder/{id}", params=params, data=None
        )

    def get_rootfolder_id(self, id: int) -> Any:
        """Get specific rootfolder."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/rootfolder/{id}", params=params, data=None)

    def get_content_path(self, path: str) -> Any:
        """Get content path."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/content/{path}", params=params, data=None)

    def get_(self, path: str) -> Any:
        """Get ."""
        params: dict[str, Any] = {}
        return self.request("GET", "/", params=params, data=None)

    def get_path(self, path: str) -> Any:
        """Get path."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/{path}", params=params, data=None)

    def get_system_status(self) -> Any:
        """Get system status."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """Get system routes."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """Get system routes duplicate."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """Add a new system shutdown."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """Add a new system restart."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/system/restart", params=params, data=None)

    def get_tag(self) -> Any:
        """Get tag."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/tag", params=params, data=None)

    def post_tag(self, data: dict) -> Any:
        """Add a new tag."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: dict) -> Any:
        """Update tag id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete tag id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/tag/detail/{id}", params=params, data=None)

    def get_system_task(self) -> Any:
        """Get system task."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """Get specific system task."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/system/task/{id}", params=params, data=None
        )

    def put_config_ui_id(self, id: str, data: dict) -> Any:
        """Update config ui id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """Get specific config ui."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """Get config ui."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """Get update."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """Get log file update."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """Get log file update filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/log/file/update/{filename}", params=params, data=None
        )

    def lookup_movie(self, term: str) -> list[dict]:
        """
        Search for a movie using the lookup endpoint.
        """
        return self.get_movie_lookup(term=term)

    def add_movie(
        self,
        term: str,
        root_folder_path: str,
        quality_profile_id: int,
        monitored: bool = True,
        search_for_movie: bool = True,
    ) -> dict:
        """
        Lookup a movie by term, pick the first result, and add it to Radarr.
        """
        results = self.lookup_movie(term)
        if not results:
            return {"error": f"No movie found for term: {term}"}

        movie = results[0]

        payload = {
            "title": movie.get("title"),
            "qualityProfileId": quality_profile_id,
            "rootFolderPath": root_folder_path,
            "monitored": monitored,
            "tmdbId": movie.get("tmdbId"),
            "year": movie.get("year"),
            "titleSlug": movie.get("titleSlug"),
            "images": movie.get("images", []),
            "addOptions": {"searchForMovie": search_for_movie},
        }

        return self.post_movie(data=payload)
