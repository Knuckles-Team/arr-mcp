"""
Sonarr API Client.

This module provides a class to interact with the Sonarr API for managing TV show collections.
"""

from typing import Any
from urllib.parse import urljoin

import requests
import urllib3


class Api:
    """
    API client for Sonarr.

    Handles authentication, request session management, and provides methods
    for various Sonarr endpoints including series, episodes, quality profiles, and system settings.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        verify: bool = False,
    ):
        """
        Initialize the Sonarr API client.

        Args:
            base_url (str): The base URL of the Sonarr instance.
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
        Generic request method for the Sonarr API.

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

    def get_api(self) -> Any:
        """Get the base API information."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api", params=params, data=None)

    def post_login(self, returnUrl: str | None = None) -> Any:
        """Log in to the Sonarr web interface."""
        params: dict[str, Any] = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get the login status and information."""
        params: dict[str, Any] = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Log out from the Sonarr web interface."""
        params: dict[str, Any] = {}
        return self.request("GET", "/logout", params=params, data=None)

    def post_autotagging(self, data: dict) -> Any:
        """Add a new auto-tagging rule."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """Get all auto-tagging rules."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/autotagging", params=params, data=None)

    def put_autotagging_id(self, id: str, data: dict) -> Any:
        """Update an existing auto-tagging rule by ID."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """Delete an auto-tagging rule by ID."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_id(self, id: int) -> Any:
        """Get details for a specific auto-tagging rule by ID."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_schema(self) -> Any:
        """Get the schema for auto-tagging rules."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """Get information about available system backups."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """Delete a system backup file by ID."""
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
        seriesIds: list | None = None,
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
        if seriesIds is not None:
            params["seriesIds"] = seriesIds
        if protocols is not None:
            params["protocols"] = protocols
        return self.request("GET", "/api/v3/blocklist", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """Delete a blocklisted item by ID."""
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
        includeSeries: bool | None = None,
        includeEpisodeFile: bool | None = None,
        includeEpisodeImages: bool | None = None,
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
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisodeFile is not None:
            params["includeEpisodeFile"] = includeEpisodeFile
        if includeEpisodeImages is not None:
            params["includeEpisodeImages"] = includeEpisodeImages
        if tags is not None:
            params["tags"] = tags
        return self.request("GET", "/api/v3/calendar", params=params, data=None)

    def get_calendar_id(self, id: int) -> Any:
        """Get specific calendar."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/calendar/{id}", params=params, data=None)

    def get_feed_v3_calendar_sonarrics(
        self,
        pastDays: int | None = None,
        futureDays: int | None = None,
        tags: str | None = None,
        unmonitored: bool | None = None,
        premieresOnly: bool | None = None,
        asAllDay: bool | None = None,
    ) -> Any:
        """Get feed v3 calendar sonarrics."""
        params: dict[str, Any] = {}
        if pastDays is not None:
            params["pastDays"] = pastDays
        if futureDays is not None:
            params["futureDays"] = futureDays
        if tags is not None:
            params["tags"] = tags
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        if premieresOnly is not None:
            params["premieresOnly"] = premieresOnly
        if asAllDay is not None:
            params["asAllDay"] = asAllDay
        return self.request(
            "GET", "/feed/v3/calendar/sonarr.ics", params=params, data=None
        )

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
        includeSeries: bool | None = None,
        includeEpisodeFile: bool | None = None,
        includeImages: bool | None = None,
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
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisodeFile is not None:
            params["includeEpisodeFile"] = includeEpisodeFile
        if includeImages is not None:
            params["includeImages"] = includeImages
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v3/wanted/cutoff", params=params, data=None)

    def get_wanted_cutoff_id(self, id: int) -> Any:
        """Get specific wanted cutoff."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/wanted/cutoff/{id}", params=params, data=None
        )

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

    def get_episode(
        self,
        seriesId: int | None = None,
        seasonNumber: int | None = None,
        episodeIds: list | None = None,
        episodeFileId: int | None = None,
        includeSeries: bool | None = None,
        includeEpisodeFile: bool | None = None,
        includeImages: bool | None = None,
    ) -> Any:
        """Get episode."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
        if episodeIds is not None:
            params["episodeIds"] = episodeIds
        if episodeFileId is not None:
            params["episodeFileId"] = episodeFileId
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisodeFile is not None:
            params["includeEpisodeFile"] = includeEpisodeFile
        if includeImages is not None:
            params["includeImages"] = includeImages
        return self.request("GET", "/api/v3/episode", params=params, data=None)

    def put_episode_id(self, id: int, data: dict) -> Any:
        """Update episode id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/episode/{id}", params=params, data=data)

    def get_episode_id(self, id: int) -> Any:
        """Get specific episode."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/episode/{id}", params=params, data=None)

    def put_episode_monitor(self, data: dict, includeImages: bool | None = None) -> Any:
        """Update episode monitor."""
        params: dict[str, Any] = {}
        if includeImages is not None:
            params["includeImages"] = includeImages
        return self.request("PUT", "/api/v3/episode/monitor", params=params, data=data)

    def get_episodefile(
        self, seriesId: int | None = None, episodeFileIds: list | None = None
    ) -> Any:
        """Get episodefile."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if episodeFileIds is not None:
            params["episodeFileIds"] = episodeFileIds
        return self.request("GET", "/api/v3/episodefile", params=params, data=None)

    def put_episodefile_id(self, id: str, data: dict) -> Any:
        """Update episodefile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/episodefile/{id}", params=params, data=data
        )

    def delete_episodefile_id(self, id: int) -> Any:
        """Delete episodefile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/episodefile/{id}", params=params, data=None
        )

    def get_episodefile_id(self, id: int) -> Any:
        """Get specific episodefile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/episodefile/{id}", params=params, data=None
        )

    def put_episodefile_editor(self, data: dict) -> Any:
        """Update episodefile editor."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", "/api/v3/episodefile/editor", params=params, data=data
        )

    def delete_episodefile_bulk(self, data: dict) -> Any:
        """Delete episodefile bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/episodefile/bulk", params=params, data=data
        )

    def put_episodefile_bulk(self, data: dict) -> Any:
        """Update episodefile bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/episodefile/bulk", params=params, data=data)

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
        includeSeries: bool | None = None,
        includeEpisode: bool | None = None,
        eventType: list | None = None,
        episodeId: int | None = None,
        downloadId: str | None = None,
        seriesIds: list | None = None,
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
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisode is not None:
            params["includeEpisode"] = includeEpisode
        if eventType is not None:
            params["eventType"] = eventType
        if episodeId is not None:
            params["episodeId"] = episodeId
        if downloadId is not None:
            params["downloadId"] = downloadId
        if seriesIds is not None:
            params["seriesIds"] = seriesIds
        if languages is not None:
            params["languages"] = languages
        if quality is not None:
            params["quality"] = quality
        return self.request("GET", "/api/v3/history", params=params, data=None)

    def get_history_since(
        self,
        date: str | None = None,
        eventType: str | None = None,
        includeSeries: bool | None = None,
        includeEpisode: bool | None = None,
    ) -> Any:
        """Get history since."""
        params: dict[str, Any] = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisode is not None:
            params["includeEpisode"] = includeEpisode
        return self.request("GET", "/api/v3/history/since", params=params, data=None)

    def get_history_series(
        self,
        seriesId: int | None = None,
        seasonNumber: int | None = None,
        eventType: str | None = None,
        includeSeries: bool | None = None,
        includeEpisode: bool | None = None,
    ) -> Any:
        """Get history series."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
        if eventType is not None:
            params["eventType"] = eventType
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisode is not None:
            params["includeEpisode"] = includeEpisode
        return self.request("GET", "/api/v3/history/series", params=params, data=None)

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
        """Add a new import list configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/importlist", params=params, data=data)

    def put_importlist_id(
        self, id: int, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update an existing import list configuration."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete an import list configuration by ID."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """Get details for a specific import list by ID."""
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

    def get_importlistexclusion(self) -> Any:
        """Get importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/importlistexclusion", params=params, data=None
        )

    def post_importlistexclusion(self, data: dict) -> Any:
        """Add a new importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v3/importlistexclusion", params=params, data=data
        )

    def get_importlistexclusion_paged(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
    ) -> Any:
        """Get importlistexclusion paged."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        return self.request(
            "GET", "/api/v3/importlistexclusion/paged", params=params, data=None
        )

    def put_importlistexclusion_id(self, id: str, data: dict) -> Any:
        """Update importlistexclusion id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/importlistexclusion/{id}", params=params, data=data
        )

    def delete_importlistexclusion_id(self, id: int) -> Any:
        """Delete importlistexclusion id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/importlistexclusion/{id}", params=params, data=None
        )

    def get_importlistexclusion_id(self, id: int) -> Any:
        """Get specific importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/importlistexclusion/{id}", params=params, data=None
        )

    def delete_importlistexclusion_bulk(self, data: dict) -> Any:
        """Delete importlistexclusion bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v3/importlistexclusion/bulk", params=params, data=data
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
        """Delete an indexer configuration by ID."""
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

    def post_languageprofile(self, data: dict) -> Any:
        """Add a new languageprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/languageprofile", params=params, data=data)

    def get_languageprofile(self) -> Any:
        """Get languageprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/languageprofile", params=params, data=None)

    def delete_languageprofile_id(self, id: int) -> Any:
        """Delete languageprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v3/languageprofile/{id}", params=params, data=None
        )

    def put_languageprofile_id(self, id: str, data: dict) -> Any:
        """Update languageprofile id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/languageprofile/{id}", params=params, data=data
        )

    def get_languageprofile_id(self, id: int) -> Any:
        """Get specific languageprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/languageprofile/{id}", params=params, data=None
        )

    def get_languageprofile_schema(self) -> Any:
        """Get languageprofile schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/languageprofile/schema", params=params, data=None
        )

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

    def get_localization_id(self, id: int) -> Any:
        """Get specific localization."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/localization/{id}", params=params, data=None
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
        seriesId: int | None = None,
        seasonNumber: int | None = None,
        filterExistingFiles: bool | None = None,
    ) -> Any:
        """Get manualimport."""
        params: dict[str, Any] = {}
        if folder is not None:
            params["folder"] = folder
        if downloadId is not None:
            params["downloadId"] = downloadId
        if seriesId is not None:
            params["seriesId"] = seriesId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
        if filterExistingFiles is not None:
            params["filterExistingFiles"] = filterExistingFiles
        return self.request("GET", "/api/v3/manualimport", params=params, data=None)

    def post_manualimport(self, data: dict) -> Any:
        """Add a new manualimport."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/manualimport", params=params, data=data)

    def get_mediacover_series_id_filename(self, seriesId: int, filename: str) -> Any:
        """Get specific mediacover series filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/mediacover/{seriesId}/{filename}", params=params, data=None
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

    def get_wanted_missing(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeSeries: bool | None = None,
        includeImages: bool | None = None,
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
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeImages is not None:
            params["includeImages"] = includeImages
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v3/wanted/missing", params=params, data=None)

    def get_wanted_missing_id(self, id: int) -> Any:
        """Get specific wanted missing."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/wanted/missing/{id}", params=params, data=None
        )

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
        renameEpisodes: bool | None = None,
        replaceIllegalCharacters: bool | None = None,
        colonReplacementFormat: int | None = None,
        customColonReplacementFormat: str | None = None,
        multiEpisodeStyle: int | None = None,
        standardEpisodeFormat: str | None = None,
        dailyEpisodeFormat: str | None = None,
        animeEpisodeFormat: str | None = None,
        seriesFolderFormat: str | None = None,
        seasonFolderFormat: str | None = None,
        specialsFolderFormat: str | None = None,
        id: int | None = None,
        resourceName: str | None = None,
    ) -> Any:
        """Get config naming examples."""
        params: dict[str, Any] = {}
        if renameEpisodes is not None:
            params["renameEpisodes"] = renameEpisodes
        if replaceIllegalCharacters is not None:
            params["replaceIllegalCharacters"] = replaceIllegalCharacters
        if colonReplacementFormat is not None:
            params["colonReplacementFormat"] = colonReplacementFormat
        if customColonReplacementFormat is not None:
            params["customColonReplacementFormat"] = customColonReplacementFormat
        if multiEpisodeStyle is not None:
            params["multiEpisodeStyle"] = multiEpisodeStyle
        if standardEpisodeFormat is not None:
            params["standardEpisodeFormat"] = standardEpisodeFormat
        if dailyEpisodeFormat is not None:
            params["dailyEpisodeFormat"] = dailyEpisodeFormat
        if animeEpisodeFormat is not None:
            params["animeEpisodeFormat"] = animeEpisodeFormat
        if seriesFolderFormat is not None:
            params["seriesFolderFormat"] = seriesFolderFormat
        if seasonFolderFormat is not None:
            params["seasonFolderFormat"] = seasonFolderFormat
        if specialsFolderFormat is not None:
            params["specialsFolderFormat"] = specialsFolderFormat
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

    def get_parse(self, title: str | None = None, path: str | None = None) -> Any:
        """Get parse."""
        params: dict[str, Any] = {}
        if title is not None:
            params["title"] = title
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v3/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """Ping the Sonarr API to check connectivity."""
        params: dict[str, Any] = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: dict) -> Any:
        """Update qualitydefinition id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v3/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """Get a specific quality definition by ID."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """Get all quality definitions."""
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
        includeUnknownSeriesItems: bool | None = None,
        includeSeries: bool | None = None,
        includeEpisode: bool | None = None,
        seriesIds: list | None = None,
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
        if includeUnknownSeriesItems is not None:
            params["includeUnknownSeriesItems"] = includeUnknownSeriesItems
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisode is not None:
            params["includeEpisode"] = includeEpisode
        if seriesIds is not None:
            params["seriesIds"] = seriesIds
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
        self,
        seriesId: int | None = None,
        episodeIds: list | None = None,
        includeSeries: bool | None = None,
        includeEpisode: bool | None = None,
    ) -> Any:
        """Get queue details."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if episodeIds is not None:
            params["episodeIds"] = episodeIds
        if includeSeries is not None:
            params["includeSeries"] = includeSeries
        if includeEpisode is not None:
            params["includeEpisode"] = includeEpisode
        return self.request("GET", "/api/v3/queue/details", params=params, data=None)

    def get_queue_status(self) -> Any:
        """Get queue status."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/queue/status", params=params, data=None)

    def post_release(self, data: dict) -> Any:
        """Add a new release."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/release", params=params, data=data)

    def get_release(
        self,
        seriesId: int | None = None,
        episodeId: int | None = None,
        seasonNumber: int | None = None,
    ) -> Any:
        """Get release."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if episodeId is not None:
            params["episodeId"] = episodeId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
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

    def get_rename(
        self, seriesId: int | None = None, seasonNumber: int | None = None
    ) -> Any:
        """Get rename."""
        params: dict[str, Any] = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
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

    def post_seasonpass(self, data: dict) -> Any:
        """Add a new seasonpass."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/seasonpass", params=params, data=data)

    def get_series(
        self, tvdbId: int | None = None, includeSeasonImages: bool | None = None
    ) -> Any:
        """Get series."""
        params: dict[str, Any] = {}
        if tvdbId is not None:
            params["tvdbId"] = tvdbId
        if includeSeasonImages is not None:
            params["includeSeasonImages"] = includeSeasonImages
        return self.request("GET", "/api/v3/series", params=params, data=None)

    def post_series(self, data: dict) -> Any:
        """Add a new series."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/series", params=params, data=data)

    def get_series_id(self, id: int, includeSeasonImages: bool | None = None) -> Any:
        """Get specific series."""
        params: dict[str, Any] = {}
        if includeSeasonImages is not None:
            params["includeSeasonImages"] = includeSeasonImages
        return self.request("GET", f"/api/v3/series/{id}", params=params, data=None)

    def put_series_id(self, id: str, data: dict, moveFiles: bool | None = None) -> Any:
        """Update series id."""
        params: dict[str, Any] = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v3/series/{id}", params=params, data=data)

    def delete_series_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportListExclusion: bool | None = None,
    ) -> Any:
        """Delete series."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v3/series/{id}", params=params, data=None)

    def put_series_editor(self, data: dict) -> Any:
        """Update series editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v3/series/editor", params=params, data=data)

    def delete_series_editor(self, data: dict) -> Any:
        """Delete series editor."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v3/series/editor", params=params, data=data)

    def get_series_id_folder(self, id: int) -> Any:
        """Get series folder."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/series/{id}/folder", params=params, data=None
        )

    def post_series_import(self, data: dict) -> Any:
        """Import series."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/series/import", params=params, data=data)

    def get_series_lookup(self, term: str | None = None) -> Any:
        """Lookup series."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v3/series/lookup", params=params, data=None)

    def get_content_path(self, path: str) -> Any:
        """Get content path."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/content/{path}", params=params, data=None)

    def get_(self, path: str) -> Any:
        """Get resource by path."""
        params: dict[str, Any] = {}
        return self.request("GET", "/", params=params, data=None)

    def get_path(self, path: str) -> Any:
        """Get system routes."""
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
        """Get duplicate system routes."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v3/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """Trigger system shutdown."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """Trigger system restart."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/system/restart", params=params, data=None)

    def get_tag(self) -> Any:
        """Get tags."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/tag", params=params, data=None)

    def post_tag(self, data: dict) -> Any:
        """Add a new tag."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v3/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: dict) -> Any:
        """Update a tag."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete a tag."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag usage details."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag usage details."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/tag/detail/{id}", params=params, data=None)

    def get_system_task(self) -> Any:
        """Get system tasks."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """Get specific system task."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/system/task/{id}", params=params, data=None
        )

    def put_config_ui_id(self, id: str, data: dict) -> Any:
        """Update UI configuration."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v3/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """Get specific UI configuration."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v3/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """Get UI configuration."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """Get available updates."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """Get log file update."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v3/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """Get log file update content."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v3/log/file/update/{filename}", params=params, data=None
        )

    def lookup_series(self, term: str) -> list[dict]:
        """
        Search for a series using the lookup endpoint.
        """
        return self.get_series_lookup(term=term)

    def add_series(
        self,
        term: str,
        root_folder_path: str,
        quality_profile_id: int,
        monitored: bool = True,
        search_for_missing_episodes: bool = True,
    ) -> dict:
        """
        Lookup a series by term, pick the first result, and add it to Sonarr.
        """
        results = self.lookup_series(term)
        if not results:
            return {"error": f"No series found for term: {term}"}

        series = results[0]

        payload = {
            "title": series.get("title"),
            "qualityProfileId": quality_profile_id,
            "rootFolderPath": root_folder_path,
            "monitored": monitored,
            "tvdbId": series.get("tvdbId"),
            "year": series.get("year"),
            "titleSlug": series.get("titleSlug"),
            "images": series.get("images", []),
            "addOptions": {"searchForMissingEpisodes": search_for_missing_episodes},
        }

        return self.post_series(data=payload)
