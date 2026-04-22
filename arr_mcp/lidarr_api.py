"""
Lidarr API Client.

This module provides a class to interact with the Lidarr API for managing music collections.
"""

from typing import Any
from urllib.parse import urljoin

import requests
import urllib3


class Api:
    """
    API client for Lidarr.

    Handles authentication, request session management, and provides methods
    for various Lidarr endpoints including artists, albums, tracks, and system settings.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        verify: bool = False,
    ):
        """
        Initialize the Lidarr API client.

        Args:
            base_url (str): The base URL of the Lidarr instance.
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
        Generic request method for the Lidarr API.

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

    def get_album(
        self,
        artistId: int | None = None,
        albumIds: list | None = None,
        foreignAlbumId: str | None = None,
        includeAllArtistAlbums: bool | None = None,
    ) -> Any:
        """Get albums managed by Lidarr."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumIds is not None:
            params["albumIds"] = albumIds
        if foreignAlbumId is not None:
            params["foreignAlbumId"] = foreignAlbumId
        if includeAllArtistAlbums is not None:
            params["includeAllArtistAlbums"] = includeAllArtistAlbums
        return self.request("GET", "/api/v1/album", params=params, data=None)

    def post_album(self, data: dict) -> Any:
        """Add a new album to Lidarr."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/album", params=params, data=data)

    def put_album_id(self, id: str, data: dict) -> Any:
        """Update an existing album by ID."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/album/{id}", params=params, data=data)

    def delete_album_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportListExclusion: bool | None = None,
    ) -> Any:
        """Delete an album and optionally its files and add exclusion."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/album/{id}", params=params, data=None)

    def get_album_id(self, id: int) -> Any:
        """Get details for a specific album by ID."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/album/{id}", params=params, data=None)

    def put_album_monitor(self, data: dict) -> Any:
        """Update monitoring status for multiple albums."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/album/monitor", params=params, data=data)

    def get_album_lookup(self, term: str | None = None) -> Any:
        """Search for new albums to add to Lidarr."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/album/lookup", params=params, data=None)

    def post_albumstudio(self, data: dict) -> Any:
        """Perform studio operations on albums."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/albumstudio", params=params, data=data)

    def get_api(self) -> Any:
        """Get the base API information."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api", params=params, data=None)

    def get_artist_id(self, id: int) -> Any:
        """Get details for a specific artist by ID."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/artist/{id}", params=params, data=None)

    def put_artist_id(self, id: str, data: dict, moveFiles: bool | None = None) -> Any:
        """Update an existing artist configuration."""
        params: dict[str, Any] = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v1/artist/{id}", params=params, data=data)

    def delete_artist_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportListExclusion: bool | None = None,
    ) -> Any:
        """Delete artist id."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/artist/{id}", params=params, data=None)

    def get_artist(self, mbId: str | None = None) -> Any:
        """Get all artists managed by Lidarr."""
        params: dict[str, Any] = {}
        if mbId is not None:
            params["mbId"] = mbId
        return self.request("GET", "/api/v1/artist", params=params, data=None)

    def post_artist(self, data: dict) -> Any:
        """Add a new artist to Lidarr."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/artist", params=params, data=data)

    def put_artist_editor(self, data: dict) -> Any:
        """Update monitoring or tagging for multiple artists."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/artist/editor", params=params, data=data)

    def delete_artist_editor(self, data: dict) -> Any:
        """Delete multiple artists using the artist editor."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v1/artist/editor", params=params, data=data)

    def get_artist_lookup(self, term: str | None = None) -> Any:
        """Search for new artists to add to Lidarr."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/artist/lookup", params=params, data=None)

    def post_login(self, returnUrl: str | None = None) -> Any:
        """Add a new login."""
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

    def get_autotagging_id(self, id: int) -> Any:
        """Get specific autotagging."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/autotagging/{id}", params=params, data=None
        )

    def put_autotagging_id(self, id: str, data: dict) -> Any:
        """Update autotagging id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """Delete autotagging id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/autotagging/{id}", params=params, data=None
        )

    def post_autotagging(self, data: dict) -> Any:
        """Add a new autotagging."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """Get autotagging."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/autotagging", params=params, data=None)

    def get_autotagging_schema(self) -> Any:
        """Get autotagging schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """Get system backup."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """Delete system backup id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """Add a new system backup restore id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """Add a new system backup restore upload."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/system/backup/restore/upload", params=params, data=None
        )

    def get_blocklist(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
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
        return self.request("GET", "/api/v1/blocklist", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """Delete blocklist id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: dict) -> Any:
        """Delete blocklist bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/blocklist/bulk", params=params, data=data
        )

    def get_calendar(
        self,
        start: str | None = None,
        end: str | None = None,
        unmonitored: bool | None = None,
        includeArtist: bool | None = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if tags is not None:
            params["tags"] = tags
        return self.request("GET", "/api/v1/calendar", params=params, data=None)

    def get_calendar_id(self, id: int) -> Any:
        """Get specific calendar."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/calendar/{id}", params=params, data=None)

    def get_feed_v1_calendar_lidarrics(
        self,
        pastDays: int | None = None,
        futureDays: int | None = None,
        tags: str | None = None,
        unmonitored: bool | None = None,
    ) -> Any:
        """Get feed v1 calendar lidarrics."""
        params: dict[str, Any] = {}
        if pastDays is not None:
            params["pastDays"] = pastDays
        if futureDays is not None:
            params["futureDays"] = futureDays
        if tags is not None:
            params["tags"] = tags
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        return self.request(
            "GET", "/feed/v1/calendar/lidarr.ics", params=params, data=None
        )

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/command/{id}", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/command/{id}", params=params, data=None)

    def post_command(self, data: dict) -> Any:
        """Add a new command."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/command", params=params, data=None)

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def put_customfilter_id(self, id: str, data: dict) -> Any:
        """Update customfilter id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """Delete customfilter id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/customfilter", params=params, data=None)

    def post_customfilter(self, data: dict) -> Any:
        """Add a new customfilter."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/customfilter", params=params, data=data)

    def get_customformat_id(self, id: int) -> Any:
        """Get specific customformat."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def put_customformat_id(self, id: str, data: dict) -> Any:
        """Update customformat id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """Delete customformat id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def get_customformat(self) -> Any:
        """Get customformat."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/customformat", params=params, data=None)

    def post_customformat(self, data: dict) -> Any:
        """Add a new customformat."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/customformat", params=params, data=data)

    def put_customformat_bulk(self, data: dict) -> Any:
        """Update customformat bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v1/customformat/bulk", params=params, data=data
        )

    def delete_customformat_bulk(self, data: dict) -> Any:
        """Delete customformat bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/customformat/bulk", params=params, data=data
        )

    def get_customformat_schema(self) -> Any:
        """Get customformat schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/customformat/schema", params=params, data=None
        )

    def get_wanted_cutoff(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeArtist: bool | None = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/cutoff", params=params, data=None)

    def get_wanted_cutoff_id(self, id: int) -> Any:
        """Get specific wanted cutoff."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/wanted/cutoff/{id}", params=params, data=None
        )

    def post_delayprofile(self, data: dict) -> Any:
        """Add a new delayprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """Get delayprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """Delete delayprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: dict) -> Any:
        """Update delayprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """Get specific delayprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, afterId: int | None = None) -> Any:
        """Update delayprofile reorder id."""
        params: dict[str, Any] = {}
        if afterId is not None:
            params["afterId"] = afterId
        return self.request(
            "PUT", f"/api/v1/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """Get diskspace."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/diskspace", params=params, data=None)

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update downloadclient id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """Delete downloadclient id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient(self) -> Any:
        """Get downloadclient."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new downloadclient."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/downloadclient", params=params, data=data)

    def put_downloadclient_bulk(self, data: dict) -> Any:
        """Update downloadclient bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: dict) -> Any:
        """Delete downloadclient bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """Get downloadclient schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(
        self, data: dict, forceTest: bool | None = None
    ) -> Any:
        """Test downloadclient."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """Add a new downloadclient testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: dict) -> Any:
        """Add a new downloadclient action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/downloadclient/{id}", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: dict) -> Any:
        """Update config downloadclient id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/downloadclient", params=params, data=None
        )

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
        return self.request("GET", "/api/v1/filesystem", params=params, data=None)

    def get_filesystem_type(self, path: str | None = None) -> Any:
        """Get filesystem type."""
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v1/filesystem/type", params=params, data=None)

    def get_filesystem_mediafiles(self, path: str | None = None) -> Any:
        """Get filesystem mediafiles."""
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v1/filesystem/mediafiles", params=params, data=None
        )

    def get_health(self) -> Any:
        """Get health."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/health", params=params, data=None)

    def get_history(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeArtist: bool | None = None,
        includeAlbum: bool | None = None,
        includeTrack: bool | None = None,
        eventType: list | None = None,
        albumId: int | None = None,
        downloadId: str | None = None,
        artistIds: list | None = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if includeAlbum is not None:
            params["includeAlbum"] = includeAlbum
        if includeTrack is not None:
            params["includeTrack"] = includeTrack
        if eventType is not None:
            params["eventType"] = eventType
        if albumId is not None:
            params["albumId"] = albumId
        if downloadId is not None:
            params["downloadId"] = downloadId
        if artistIds is not None:
            params["artistIds"] = artistIds
        if quality is not None:
            params["quality"] = quality
        return self.request("GET", "/api/v1/history", params=params, data=None)

    def get_history_since(
        self,
        date: str | None = None,
        eventType: str | None = None,
        includeArtist: bool | None = None,
        includeAlbum: bool | None = None,
        includeTrack: bool | None = None,
    ) -> Any:
        """Get history since."""
        params: dict[str, Any] = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if includeAlbum is not None:
            params["includeAlbum"] = includeAlbum
        if includeTrack is not None:
            params["includeTrack"] = includeTrack
        return self.request("GET", "/api/v1/history/since", params=params, data=None)

    def get_history_artist(
        self,
        artistId: int | None = None,
        albumId: int | None = None,
        eventType: str | None = None,
        includeArtist: bool | None = None,
        includeAlbum: bool | None = None,
        includeTrack: bool | None = None,
    ) -> Any:
        """Get history artist."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if eventType is not None:
            params["eventType"] = eventType
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if includeAlbum is not None:
            params["includeAlbum"] = includeAlbum
        if includeTrack is not None:
            params["includeTrack"] = includeTrack
        return self.request("GET", "/api/v1/history/artist", params=params, data=None)

    def post_history_failed_id(self, id: int) -> Any:
        """Add a new history failed id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/history/failed/{id}", params=params, data=None
        )

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/host/{id}", params=params, data=None
        )

    def put_config_host_id(self, id: str, data: dict) -> Any:
        """Update config host id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/host/{id}", params=params, data=data
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/host", params=params, data=None)

    def get_importlist_id(self, id: int) -> Any:
        """Get details for a specific import list by ID."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/importlist/{id}", params=params, data=None)

    def put_importlist_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update an existing import list configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete an import list configuration."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/importlist/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """Get all import lists."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/importlist", params=params, data=None)

    def post_importlist(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new import list."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/importlist", params=params, data=data)

    def put_importlist_bulk(self, data: dict) -> Any:
        """Update multiple import lists in bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: dict) -> Any:
        """Delete multiple import lists in bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """Get the schema for import list configurations."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test an import list configuration."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """Test all configured import lists."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: dict) -> Any:
        """Perform a specific action on import lists."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/importlist/action/{name}", params=params, data=data
        )

    def get_importlistexclusion_id(self, id: int) -> Any:
        """Get specific importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def put_importlistexclusion_id(self, id: str, data: dict) -> Any:
        """Update importlistexclusion id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/importlistexclusion/{id}", params=params, data=data
        )

    def delete_importlistexclusion_id(self, id: int) -> Any:
        """Delete importlistexclusion id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def get_importlistexclusion(self) -> Any:
        """Get importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/importlistexclusion", params=params, data=None
        )

    def post_importlistexclusion(self, data: dict) -> Any:
        """Add a new importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/importlistexclusion", params=params, data=data
        )

    def get_indexer_id(self, id: int) -> Any:
        """Get details for a specific indexer by ID."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/indexer/{id}", params=params, data=None)

    def put_indexer_id(self, id: int, data: dict, forceSave: bool | None = None) -> Any:
        """Update an existing indexer configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """Delete an indexer configuration by ID."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/indexer/{id}", params=params, data=None)

    def get_indexer(self) -> Any:
        """Get all configured indexers."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/indexer", params=params, data=None)

    def post_indexer(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new indexer configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/indexer", params=params, data=data)

    def put_indexer_bulk(self, data: dict) -> Any:
        """Update indexer bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: dict) -> Any:
        """Delete indexer bulk."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v1/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """Get indexer schema."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test indexer."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """Add a new indexer testall."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: dict) -> Any:
        """Add a new indexer action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/indexer/action/{name}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """Get specific config indexer."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/indexer/{id}", params=params, data=None
        )

    def put_config_indexer_id(self, id: str, data: dict) -> Any:
        """Update config indexer id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer(self) -> Any:
        """Get config indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/indexer", params=params, data=None)

    def get_indexerflag(self) -> Any:
        """Get indexerflag."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/indexerflag", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """Get specific language."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/language/{id}", params=params, data=None)

    def get_language(self) -> Any:
        """Get language."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/language", params=params, data=None)

    def get_localization(self) -> Any:
        """Get localization."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/localization", params=params, data=None)

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
        return self.request("GET", "/api/v1/log", params=params, data=None)

    def get_log_file(self) -> Any:
        """Get log file."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """Get log file filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/log/file/{filename}", params=params, data=None
        )

    def post_manualimport(self, data: dict) -> Any:
        """Add a new manualimport."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/manualimport", params=params, data=data)

    def get_manualimport(
        self,
        folder: str | None = None,
        downloadId: str | None = None,
        artistId: int | None = None,
        filterExistingFiles: bool | None = None,
        replaceExistingFiles: bool | None = None,
    ) -> Any:
        """Get manualimport."""
        params: dict[str, Any] = {}
        if folder is not None:
            params["folder"] = folder
        if downloadId is not None:
            params["downloadId"] = downloadId
        if artistId is not None:
            params["artistId"] = artistId
        if filterExistingFiles is not None:
            params["filterExistingFiles"] = filterExistingFiles
        if replaceExistingFiles is not None:
            params["replaceExistingFiles"] = replaceExistingFiles
        return self.request("GET", "/api/v1/manualimport", params=params, data=None)

    def get_mediacover_artist_artist_id_filename(
        self, artistId: int, filename: str
    ) -> Any:
        """Get specific mediacover artist artist filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/artist/{artistId}/{filename}",
            params=params,
            data=None,
        )

    def get_mediacover_album_album_id_filename(
        self, albumId: int, filename: str
    ) -> Any:
        """Get specific mediacover album album filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/album/{albumId}/{filename}",
            params=params,
            data=None,
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """Get specific config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/mediamanagement/{id}", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: dict) -> Any:
        """Update config mediamanagement id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement(self) -> Any:
        """Get config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/mediamanagement", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """Get specific metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/metadata/{id}", params=params, data=None)

    def put_metadata_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update metadata id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """Delete metadata id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/metadata/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """Get metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/metadata", params=params, data=None)

    def post_metadata(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new metadata."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/metadata", params=params, data=data)

    def get_metadata_schema(self) -> Any:
        """Get metadata schema."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test metadata."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """Add a new metadata testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: dict) -> Any:
        """Add a new metadata action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/metadata/action/{name}", params=params, data=data
        )

    def post_metadataprofile(self, data: dict) -> Any:
        """Add a new metadataprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/metadataprofile", params=params, data=data)

    def get_metadataprofile(self) -> Any:
        """Get metadataprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/metadataprofile", params=params, data=None)

    def delete_metadataprofile_id(self, id: int) -> Any:
        """Delete metadataprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def put_metadataprofile_id(self, id: str, data: dict) -> Any:
        """Update metadataprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/metadataprofile/{id}", params=params, data=data
        )

    def get_metadataprofile_id(self, id: int) -> Any:
        """Get specific metadataprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def get_metadataprofile_schema(self) -> Any:
        """Get metadataprofile schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/metadataprofile/schema", params=params, data=None
        )

    def get_config_metadataprovider_id(self, id: int) -> Any:
        """Get specific config metadataprovider."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/metadataprovider/{id}", params=params, data=None
        )

    def put_config_metadataprovider_id(self, id: str, data: dict) -> Any:
        """Update config metadataprovider id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/metadataprovider/{id}", params=params, data=data
        )

    def get_config_metadataprovider(self) -> Any:
        """Get config metadataprovider."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/metadataprovider", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeArtist: bool | None = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/missing", params=params, data=None)

    def get_wanted_missing_id(self, id: int) -> Any:
        """Get specific wanted missing."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/wanted/missing/{id}", params=params, data=None
        )

    def get_config_naming_id(self, id: int) -> Any:
        """Get specific config naming."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/naming/{id}", params=params, data=None
        )

    def put_config_naming_id(self, id: str, data: dict) -> Any:
        """Update config naming id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/naming/{id}", params=params, data=data
        )

    def get_config_naming(self) -> Any:
        """Get config naming."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/naming", params=params, data=None)

    def get_config_naming_examples(
        self,
        renameTracks: bool | None = None,
        replaceIllegalCharacters: bool | None = None,
        colonReplacementFormat: int | None = None,
        standardTrackFormat: str | None = None,
        multiDiscTrackFormat: str | None = None,
        artistFolderFormat: str | None = None,
        includeArtistName: bool | None = None,
        includeAlbumTitle: bool | None = None,
        includeQuality: bool | None = None,
        replaceSpaces: bool | None = None,
        separator: str | None = None,
        numberStyle: str | None = None,
        id: int | None = None,
        resourceName: str | None = None,
    ) -> Any:
        """Get config naming examples."""
        params: dict[str, Any] = {}
        if renameTracks is not None:
            params["renameTracks"] = renameTracks
        if replaceIllegalCharacters is not None:
            params["replaceIllegalCharacters"] = replaceIllegalCharacters
        if colonReplacementFormat is not None:
            params["colonReplacementFormat"] = colonReplacementFormat
        if standardTrackFormat is not None:
            params["standardTrackFormat"] = standardTrackFormat
        if multiDiscTrackFormat is not None:
            params["multiDiscTrackFormat"] = multiDiscTrackFormat
        if artistFolderFormat is not None:
            params["artistFolderFormat"] = artistFolderFormat
        if includeArtistName is not None:
            params["includeArtistName"] = includeArtistName
        if includeAlbumTitle is not None:
            params["includeAlbumTitle"] = includeAlbumTitle
        if includeQuality is not None:
            params["includeQuality"] = includeQuality
        if replaceSpaces is not None:
            params["replaceSpaces"] = replaceSpaces
        if separator is not None:
            params["separator"] = separator
        if numberStyle is not None:
            params["numberStyle"] = numberStyle
        if id is not None:
            params["id"] = id
        if resourceName is not None:
            params["resourceName"] = resourceName
        return self.request(
            "GET", "/api/v1/config/naming/examples", params=params, data=None
        )

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/notification/{id}", params=params, data=None
        )

    def put_notification_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update notification id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """Delete notification id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/notification/{id}", params=params, data=None
        )

    def get_notification(self) -> Any:
        """Get notification."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/notification", params=params, data=None)

    def post_notification(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new notification."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/notification", params=params, data=data)

    def get_notification_schema(self) -> Any:
        """Get notification schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test notification."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """Add a new notification testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: dict) -> Any:
        """Add a new notification action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/notification/action/{name}", params=params, data=data
        )

    def get_parse(self, title: str | None = None) -> Any:
        """Get parse."""
        params: dict[str, Any] = {}
        if title is not None:
            params["title"] = title
        return self.request("GET", "/api/v1/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """Get ping."""
        params: dict[str, Any] = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: dict) -> Any:
        """Update qualitydefinition id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """Get specific qualitydefinition."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """Get qualitydefinition."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: dict) -> Any:
        """Update qualitydefinition update."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v1/qualitydefinition/update", params=params, data=data
        )

    def post_qualityprofile(self, data: dict) -> Any:
        """Add a new qualityprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """Get qualityprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """Delete qualityprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: dict) -> Any:
        """Update qualityprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """Get specific qualityprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """Get qualityprofile schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/qualityprofile/schema", params=params, data=None
        )

    def delete_queue_id(
        self,
        id: int,
        removeFromClient: bool | None = None,
        blocklist: bool | None = None,
        skipRedownload: bool | None = None,
        changeCategory: bool | None = None,
    ) -> Any:
        """Delete queue id."""
        params: dict[str, Any] = {}
        if removeFromClient is not None:
            params["removeFromClient"] = removeFromClient
        if blocklist is not None:
            params["blocklist"] = blocklist
        if skipRedownload is not None:
            params["skipRedownload"] = skipRedownload
        if changeCategory is not None:
            params["changeCategory"] = changeCategory
        return self.request("DELETE", f"/api/v1/queue/{id}", params=params, data=None)

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
        return self.request("DELETE", "/api/v1/queue/bulk", params=params, data=data)

    def get_queue(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeUnknownArtistItems: bool | None = None,
        includeArtist: bool | None = None,
        includeAlbum: bool | None = None,
        artistIds: list | None = None,
        protocol: str | None = None,
        quality: list | None = None,
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
        if includeUnknownArtistItems is not None:
            params["includeUnknownArtistItems"] = includeUnknownArtistItems
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if includeAlbum is not None:
            params["includeAlbum"] = includeAlbum
        if artistIds is not None:
            params["artistIds"] = artistIds
        if protocol is not None:
            params["protocol"] = protocol
        if quality is not None:
            params["quality"] = quality
        return self.request("GET", "/api/v1/queue", params=params, data=None)

    def post_queue_grab_id(self, id: int) -> Any:
        """Add a new queue grab id."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: dict) -> Any:
        """Add a new queue grab bulk."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/queue/grab/bulk", params=params, data=data)

    def get_queue_details(
        self,
        artistId: int | None = None,
        albumIds: list | None = None,
        includeArtist: bool | None = None,
        includeAlbum: bool | None = None,
    ) -> Any:
        """Get queue details."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumIds is not None:
            params["albumIds"] = albumIds
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if includeAlbum is not None:
            params["includeAlbum"] = includeAlbum
        return self.request("GET", "/api/v1/queue/details", params=params, data=None)

    def get_queue_status(self) -> Any:
        """Get queue status."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/queue/status", params=params, data=None)

    def post_release(self, data: dict) -> Any:
        """Add a new release."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/release", params=params, data=data)

    def get_release(
        self, albumId: int | None = None, artistId: int | None = None
    ) -> Any:
        """Get release."""
        params: dict[str, Any] = {}
        if albumId is not None:
            params["albumId"] = albumId
        if artistId is not None:
            params["artistId"] = artistId
        return self.request("GET", "/api/v1/release", params=params, data=None)

    def get_releaseprofile_id(self, id: int) -> Any:
        """Get specific releaseprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def put_releaseprofile_id(self, id: str, data: dict) -> Any:
        """Update releaseprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/releaseprofile/{id}", params=params, data=data
        )

    def delete_releaseprofile_id(self, id: int) -> Any:
        """Delete releaseprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def get_releaseprofile(self) -> Any:
        """Get all configured release profiles."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/releaseprofile", params=params, data=None)

    def post_releaseprofile(self, data: dict) -> Any:
        """Add a new release profile configuration."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/releaseprofile", params=params, data=data)

    def post_release_push(self, data: dict) -> Any:
        """Add a new release push."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/release/push", params=params, data=data)

    def get_remotepathmapping_id(self, id: int) -> Any:
        """Get specific remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """Delete remotepathmapping id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: dict) -> Any:
        """Update remotepathmapping id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/remotepathmapping/{id}", params=params, data=data
        )

    def post_remotepathmapping(self, data: dict) -> Any:
        """Add a new remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """Get remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/remotepathmapping", params=params, data=None
        )

    def get_rename(
        self, artistId: int | None = None, albumId: int | None = None
    ) -> Any:
        """Get rename."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        return self.request("GET", "/api/v1/rename", params=params, data=None)

    def get_retag(self, artistId: int | None = None, albumId: int | None = None) -> Any:
        """Get retag."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        return self.request("GET", "/api/v1/retag", params=params, data=None)

    def get_rootfolder_id(self, id: int) -> Any:
        """Get specific rootfolder."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/rootfolder/{id}", params=params, data=None)

    def put_rootfolder_id(self, id: str, data: dict) -> Any:
        """Update rootfolder id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/rootfolder/{id}", params=params, data=data)

    def delete_rootfolder_id(self, id: int) -> Any:
        """Delete rootfolder id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/rootfolder/{id}", params=params, data=None
        )

    def post_rootfolder(self, data: dict) -> Any:
        """Add a new root folder."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """Get all configured root folders."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/rootfolder", params=params, data=None)

    def get_search(self, term: str | None = None) -> Any:
        """Get search."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/search", params=params, data=None)

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
        """Get the current system status for Lidarr."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """Get system routes."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """Get system routes duplicate."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """Add a new system shutdown."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """Add a new system restart."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/system/restart", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/tag/{id}", params=params, data=None)

    def put_tag_id(self, id: str, data: dict) -> Any:
        """Update tag id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete tag id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag(self) -> Any:
        """Get all configured tags."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/tag", params=params, data=None)

    def post_tag(self, data: dict) -> Any:
        """Add a new tag."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/tag", params=params, data=data)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/tag/detail/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/tag/detail", params=params, data=None)

    def get_system_task(self) -> Any:
        """Get system task."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """Get specific system task."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/system/task/{id}", params=params, data=None
        )

    def get_track(
        self,
        artistId: int | None = None,
        albumId: int | None = None,
        albumReleaseId: int | None = None,
        trackIds: list | None = None,
    ) -> Any:
        """Get track."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if albumReleaseId is not None:
            params["albumReleaseId"] = albumReleaseId
        if trackIds is not None:
            params["trackIds"] = trackIds
        return self.request("GET", "/api/v1/track", params=params, data=None)

    def get_track_id(self, id: int) -> Any:
        """Get specific track."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/track/{id}", params=params, data=None)

    def get_trackfile_id(self, id: int) -> Any:
        """Get specific trackfile."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/trackfile/{id}", params=params, data=None)

    def put_trackfile_id(self, id: str, data: dict) -> Any:
        """Update trackfile id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/trackfile/{id}", params=params, data=data)

    def delete_trackfile_id(self, id: int) -> Any:
        """Delete trackfile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/trackfile/{id}", params=params, data=None
        )

    def get_trackfile(
        self,
        artistId: int | None = None,
        trackFileIds: list | None = None,
        albumId: list | None = None,
        unmapped: bool | None = None,
    ) -> Any:
        """Get trackfile."""
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if trackFileIds is not None:
            params["trackFileIds"] = trackFileIds
        if albumId is not None:
            params["albumId"] = albumId
        if unmapped is not None:
            params["unmapped"] = unmapped
        return self.request("GET", "/api/v1/trackfile", params=params, data=None)

    def put_trackfile_editor(self, data: dict) -> Any:
        """Update trackfile editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/trackfile/editor", params=params, data=data)

    def delete_trackfile_bulk(self, data: dict) -> Any:
        """Delete trackfile bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/trackfile/bulk", params=params, data=data
        )

    def put_config_ui_id(self, id: str, data: dict) -> Any:
        """Update config ui id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """Get specific config ui."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """Get config ui."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """Get update."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """Get log file update."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """Get log file update filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/log/file/update/{filename}", params=params, data=None
        )
