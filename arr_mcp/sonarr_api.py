"""
Sonarr API Client.

This module provides a class to interact with the Sonarr API for managing TV show collections.
"""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
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
        token: Optional[str] = None,
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
        params: Dict = None,
        data: Dict = None,
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
        params = {}
        return self.request("GET", "/api", params=params, data=None)

    def post_login(self, returnUrl: str = None) -> Any:
        """Log in to the Sonarr web interface."""
        params = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get the login status and information."""
        params = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Log out from the Sonarr web interface."""
        params = {}
        return self.request("GET", "/logout", params=params, data=None)

    def post_autotagging(self, data: Dict) -> Any:
        """Add a new auto-tagging rule."""
        params = {}
        return self.request("POST", "/api/v3/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """Get all auto-tagging rules."""
        params = {}
        return self.request("GET", "/api/v3/autotagging", params=params, data=None)

    def put_autotagging_id(self, id: str, data: Dict) -> Any:
        """Update an existing auto-tagging rule by ID."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """Delete an auto-tagging rule by ID."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_id(self, id: int) -> Any:
        """Get details for a specific auto-tagging rule by ID."""
        params = {}
        return self.request(
            "GET", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_schema(self) -> Any:
        """Get the schema for auto-tagging rules."""
        params = {}
        return self.request(
            "GET", "/api/v3/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """Get information about available system backups."""
        params = {}
        return self.request("GET", "/api/v3/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """Delete a system backup file by ID."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """Add a new system backup restore id."""
        params = {}
        return self.request(
            "POST", f"/api/v3/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """Add a new system backup restore upload."""
        params = {}
        return self.request(
            "POST", "/api/v3/system/backup/restore/upload", params=params, data=None
        )

    def get_blocklist(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        seriesIds: List = None,
        protocols: List = None,
    ) -> Any:
        """Get blocklist."""
        params = {}
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
        params = {}
        return self.request(
            "DELETE", f"/api/v3/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: Dict) -> Any:
        """Delete blocklist bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/blocklist/bulk", params=params, data=data
        )

    def get_calendar(
        self,
        start: str = None,
        end: str = None,
        unmonitored: bool = None,
        includeSeries: bool = None,
        includeEpisodeFile: bool = None,
        includeEpisodeImages: bool = None,
        tags: str = None,
    ) -> Any:
        """Get calendar."""
        params = {}
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
        params = {}
        return self.request("GET", f"/api/v3/calendar/{id}", params=params, data=None)

    def get_feed_v3_calendar_sonarrics(
        self,
        pastDays: int = None,
        futureDays: int = None,
        tags: str = None,
        unmonitored: bool = None,
        premieresOnly: bool = None,
        asAllDay: bool = None,
    ) -> Any:
        """Get feed v3 calendar sonarrics."""
        params = {}
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

    def post_command(self, data: Dict) -> Any:
        """Add a new command."""
        params = {}
        return self.request("POST", "/api/v3/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params = {}
        return self.request("GET", "/api/v3/command", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params = {}
        return self.request("DELETE", f"/api/v3/command/{id}", params=params, data=None)

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params = {}
        return self.request("GET", f"/api/v3/command/{id}", params=params, data=None)

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params = {}
        return self.request("GET", "/api/v3/customfilter", params=params, data=None)

    def post_customfilter(self, data: Dict) -> Any:
        """Add a new customfilter."""
        params = {}
        return self.request("POST", "/api/v3/customfilter", params=params, data=data)

    def put_customfilter_id(self, id: str, data: Dict) -> Any:
        """Update customfilter id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """Delete customfilter id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params = {}
        return self.request(
            "GET", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customformat(self) -> Any:
        """Get customformat."""
        params = {}
        return self.request("GET", "/api/v3/customformat", params=params, data=None)

    def post_customformat(self, data: Dict) -> Any:
        """Add a new customformat."""
        params = {}
        return self.request("POST", "/api/v3/customformat", params=params, data=data)

    def put_customformat_id(self, id: str, data: Dict) -> Any:
        """Update customformat id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """Delete customformat id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def get_customformat_id(self, id: int) -> Any:
        """Get specific customformat."""
        params = {}
        return self.request(
            "GET", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def put_customformat_bulk(self, data: Dict) -> Any:
        """Update customformat bulk."""
        params = {}
        return self.request(
            "PUT", "/api/v3/customformat/bulk", params=params, data=data
        )

    def delete_customformat_bulk(self, data: Dict) -> Any:
        """Delete customformat bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/customformat/bulk", params=params, data=data
        )

    def get_customformat_schema(self) -> Any:
        """Get customformat schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/customformat/schema", params=params, data=None
        )

    def get_wanted_cutoff(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeSeries: bool = None,
        includeEpisodeFile: bool = None,
        includeImages: bool = None,
        monitored: bool = None,
    ) -> Any:
        """Get wanted cutoff."""
        params = {}
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
        params = {}
        return self.request(
            "GET", f"/api/v3/wanted/cutoff/{id}", params=params, data=None
        )

    def post_delayprofile(self, data: Dict) -> Any:
        """Add a new delayprofile."""
        params = {}
        return self.request("POST", "/api/v3/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """Get delayprofile."""
        params = {}
        return self.request("GET", "/api/v3/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """Delete delayprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: Dict) -> Any:
        """Update delayprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """Get specific delayprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, after: int = None) -> Any:
        """Update delayprofile reorder id."""
        params = {}
        if after is not None:
            params["after"] = after
        return self.request(
            "PUT", f"/api/v3/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """Get diskspace."""
        params = {}
        return self.request("GET", "/api/v3/diskspace", params=params, data=None)

    def get_downloadclient(self) -> Any:
        """Get downloadclient."""
        params = {}
        return self.request("GET", "/api/v3/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new downloadclient."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/downloadclient", params=params, data=data)

    def put_downloadclient_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """Update downloadclient id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """Delete downloadclient id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_bulk(self, data: Dict) -> Any:
        """Update downloadclient bulk."""
        params = {}
        return self.request(
            "PUT", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: Dict) -> Any:
        """Delete downloadclient bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """Get downloadclient schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test downloadclient."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """Add a new downloadclient testall."""
        params = {}
        return self.request(
            "POST", "/api/v3/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: Dict) -> Any:
        """Add a new downloadclient action name."""
        params = {}
        return self.request(
            "POST", f"/api/v3/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params = {}
        return self.request(
            "GET", "/api/v3/config/downloadclient", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: Dict) -> Any:
        """Update config downloadclient id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/downloadclient/{id}", params=params, data=None
        )

    def get_episode(
        self,
        seriesId: int = None,
        seasonNumber: int = None,
        episodeIds: List = None,
        episodeFileId: int = None,
        includeSeries: bool = None,
        includeEpisodeFile: bool = None,
        includeImages: bool = None,
    ) -> Any:
        """Get episode."""
        params = {}
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

    def put_episode_id(self, id: int, data: Dict) -> Any:
        """Update episode id."""
        params = {}
        return self.request("PUT", f"/api/v3/episode/{id}", params=params, data=data)

    def get_episode_id(self, id: int) -> Any:
        """Get specific episode."""
        params = {}
        return self.request("GET", f"/api/v3/episode/{id}", params=params, data=None)

    def put_episode_monitor(self, data: Dict, includeImages: bool = None) -> Any:
        """Update episode monitor."""
        params = {}
        if includeImages is not None:
            params["includeImages"] = includeImages
        return self.request("PUT", "/api/v3/episode/monitor", params=params, data=data)

    def get_episodefile(self, seriesId: int = None, episodeFileIds: List = None) -> Any:
        """Get episodefile."""
        params = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if episodeFileIds is not None:
            params["episodeFileIds"] = episodeFileIds
        return self.request("GET", "/api/v3/episodefile", params=params, data=None)

    def put_episodefile_id(self, id: str, data: Dict) -> Any:
        """Update episodefile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/episodefile/{id}", params=params, data=data
        )

    def delete_episodefile_id(self, id: int) -> Any:
        """Delete episodefile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/episodefile/{id}", params=params, data=None
        )

    def get_episodefile_id(self, id: int) -> Any:
        """Get specific episodefile."""
        params = {}
        return self.request(
            "GET", f"/api/v3/episodefile/{id}", params=params, data=None
        )

    def put_episodefile_editor(self, data: Dict) -> Any:
        """Update episodefile editor."""
        params = {}
        return self.request(
            "PUT", "/api/v3/episodefile/editor", params=params, data=data
        )

    def delete_episodefile_bulk(self, data: Dict) -> Any:
        """Delete episodefile bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/episodefile/bulk", params=params, data=data
        )

    def put_episodefile_bulk(self, data: Dict) -> Any:
        """Update episodefile bulk."""
        params = {}
        return self.request("PUT", "/api/v3/episodefile/bulk", params=params, data=data)

    def get_filesystem(
        self,
        path: str = None,
        includeFiles: bool = None,
        allowFoldersWithoutTrailingSlashes: bool = None,
    ) -> Any:
        """Get filesystem."""
        params = {}
        if path is not None:
            params["path"] = path
        if includeFiles is not None:
            params["includeFiles"] = includeFiles
        if allowFoldersWithoutTrailingSlashes is not None:
            params["allowFoldersWithoutTrailingSlashes"] = (
                allowFoldersWithoutTrailingSlashes
            )
        return self.request("GET", "/api/v3/filesystem", params=params, data=None)

    def get_filesystem_type(self, path: str = None) -> Any:
        """Get filesystem type."""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v3/filesystem/type", params=params, data=None)

    def get_filesystem_mediafiles(self, path: str = None) -> Any:
        """Get filesystem mediafiles."""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v3/filesystem/mediafiles", params=params, data=None
        )

    def get_health(self) -> Any:
        """Get health."""
        params = {}
        return self.request("GET", "/api/v3/health", params=params, data=None)

    def get_history(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeSeries: bool = None,
        includeEpisode: bool = None,
        eventType: List = None,
        episodeId: int = None,
        downloadId: str = None,
        seriesIds: List = None,
        languages: List = None,
        quality: List = None,
    ) -> Any:
        """Get history."""
        params = {}
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
        date: str = None,
        eventType: str = None,
        includeSeries: bool = None,
        includeEpisode: bool = None,
    ) -> Any:
        """Get history since."""
        params = {}
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
        seriesId: int = None,
        seasonNumber: int = None,
        eventType: str = None,
        includeSeries: bool = None,
        includeEpisode: bool = None,
    ) -> Any:
        """Get history series."""
        params = {}
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
        params = {}
        return self.request(
            "POST", f"/api/v3/history/failed/{id}", params=params, data=None
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params = {}
        return self.request("GET", "/api/v3/config/host", params=params, data=None)

    def put_config_host_id(self, id: str, data: Dict) -> Any:
        """Update config host id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/host/{id}", params=params, data=data
        )

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/host/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """Get importlist."""
        params = {}
        return self.request("GET", "/api/v3/importlist", params=params, data=None)

    def post_importlist(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new import list configuration."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/importlist", params=params, data=data)

    def put_importlist_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """Update an existing import list configuration."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete an import list configuration by ID."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """Get details for a specific import list by ID."""
        params = {}
        return self.request("GET", f"/api/v3/importlist/{id}", params=params, data=None)

    def put_importlist_bulk(self, data: Dict) -> Any:
        """Update importlist bulk."""
        params = {}
        return self.request("PUT", "/api/v3/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: Dict) -> Any:
        """Delete importlist bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """Get importlist schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test importlist."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """Add a new importlist testall."""
        params = {}
        return self.request(
            "POST", "/api/v3/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: Dict) -> Any:
        """Add a new importlist action name."""
        params = {}
        return self.request(
            "POST", f"/api/v3/importlist/action/{name}", params=params, data=data
        )

    def get_config_importlist(self) -> Any:
        """Get config importlist."""
        params = {}
        return self.request(
            "GET", "/api/v3/config/importlist", params=params, data=None
        )

    def put_config_importlist_id(self, id: str, data: Dict) -> Any:
        """Update config importlist id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/importlist/{id}", params=params, data=data
        )

    def get_config_importlist_id(self, id: int) -> Any:
        """Get specific config importlist."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/importlist/{id}", params=params, data=None
        )

    def get_importlistexclusion(self) -> Any:
        """Get importlistexclusion."""
        params = {}
        return self.request(
            "GET", "/api/v3/importlistexclusion", params=params, data=None
        )

    def post_importlistexclusion(self, data: Dict) -> Any:
        """Add a new importlistexclusion."""
        params = {}
        return self.request(
            "POST", "/api/v3/importlistexclusion", params=params, data=data
        )

    def get_importlistexclusion_paged(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
    ) -> Any:
        """Get importlistexclusion paged."""
        params = {}
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

    def put_importlistexclusion_id(self, id: str, data: Dict) -> Any:
        """Update importlistexclusion id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/importlistexclusion/{id}", params=params, data=data
        )

    def delete_importlistexclusion_id(self, id: int) -> Any:
        """Delete importlistexclusion id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/importlistexclusion/{id}", params=params, data=None
        )

    def get_importlistexclusion_id(self, id: int) -> Any:
        """Get specific importlistexclusion."""
        params = {}
        return self.request(
            "GET", f"/api/v3/importlistexclusion/{id}", params=params, data=None
        )

    def delete_importlistexclusion_bulk(self, data: Dict) -> Any:
        """Delete importlistexclusion bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v3/importlistexclusion/bulk", params=params, data=data
        )

    def get_indexer(self) -> Any:
        """Get indexer."""
        params = {}
        return self.request("GET", "/api/v3/indexer", params=params, data=None)

    def post_indexer(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new indexer configuration."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/indexer", params=params, data=data)

    def put_indexer_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """Update an existing indexer configuration by ID."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """Delete an indexer configuration by ID."""
        params = {}
        return self.request("DELETE", f"/api/v3/indexer/{id}", params=params, data=None)

    def get_indexer_id(self, id: int) -> Any:
        """Get specific indexer."""
        params = {}
        return self.request("GET", f"/api/v3/indexer/{id}", params=params, data=None)

    def put_indexer_bulk(self, data: Dict) -> Any:
        """Update indexer bulk."""
        params = {}
        return self.request("PUT", "/api/v3/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: Dict) -> Any:
        """Delete indexer bulk."""
        params = {}
        return self.request("DELETE", "/api/v3/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """Get indexer schema."""
        params = {}
        return self.request("GET", "/api/v3/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test indexer."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """Add a new indexer testall."""
        params = {}
        return self.request("POST", "/api/v3/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: Dict) -> Any:
        """Add a new indexer action name."""
        params = {}
        return self.request(
            "POST", f"/api/v3/indexer/action/{name}", params=params, data=data
        )

    def get_config_indexer(self) -> Any:
        """Get config indexer."""
        params = {}
        return self.request("GET", "/api/v3/config/indexer", params=params, data=None)

    def put_config_indexer_id(self, id: str, data: Dict) -> Any:
        """Update config indexer id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """Get specific config indexer."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/indexer/{id}", params=params, data=None
        )

    def get_indexerflag(self) -> Any:
        """Get indexerflag."""
        params = {}
        return self.request("GET", "/api/v3/indexerflag", params=params, data=None)

    def get_language(self) -> Any:
        """Get language."""
        params = {}
        return self.request("GET", "/api/v3/language", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """Get specific language."""
        params = {}
        return self.request("GET", f"/api/v3/language/{id}", params=params, data=None)

    def post_languageprofile(self, data: Dict) -> Any:
        """Add a new languageprofile."""
        params = {}
        return self.request("POST", "/api/v3/languageprofile", params=params, data=data)

    def get_languageprofile(self) -> Any:
        """Get languageprofile."""
        params = {}
        return self.request("GET", "/api/v3/languageprofile", params=params, data=None)

    def delete_languageprofile_id(self, id: int) -> Any:
        """Delete languageprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/languageprofile/{id}", params=params, data=None
        )

    def put_languageprofile_id(self, id: str, data: Dict) -> Any:
        """Update languageprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/languageprofile/{id}", params=params, data=data
        )

    def get_languageprofile_id(self, id: int) -> Any:
        """Get specific languageprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v3/languageprofile/{id}", params=params, data=None
        )

    def get_languageprofile_schema(self) -> Any:
        """Get languageprofile schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/languageprofile/schema", params=params, data=None
        )

    def get_localization(self) -> Any:
        """Get localization."""
        params = {}
        return self.request("GET", "/api/v3/localization", params=params, data=None)

    def get_localization_language(self) -> Any:
        """Get localization language."""
        params = {}
        return self.request(
            "GET", "/api/v3/localization/language", params=params, data=None
        )

    def get_localization_id(self, id: int) -> Any:
        """Get specific localization."""
        params = {}
        return self.request(
            "GET", f"/api/v3/localization/{id}", params=params, data=None
        )

    def get_log(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        level: str = None,
    ) -> Any:
        """Get log."""
        params = {}
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
        params = {}
        return self.request("GET", "/api/v3/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """Get log file filename."""
        params = {}
        return self.request(
            "GET", f"/api/v3/log/file/{filename}", params=params, data=None
        )

    def get_manualimport(
        self,
        folder: str = None,
        downloadId: str = None,
        seriesId: int = None,
        seasonNumber: int = None,
        filterExistingFiles: bool = None,
    ) -> Any:
        """Get manualimport."""
        params = {}
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

    def post_manualimport(self, data: Dict) -> Any:
        """Add a new manualimport."""
        params = {}
        return self.request("POST", "/api/v3/manualimport", params=params, data=data)

    def get_mediacover_series_id_filename(self, seriesId: int, filename: str) -> Any:
        """Get specific mediacover series filename."""
        params = {}
        return self.request(
            "GET", f"/api/v3/mediacover/{seriesId}/{filename}", params=params, data=None
        )

    def get_config_mediamanagement(self) -> Any:
        """Get config mediamanagement."""
        params = {}
        return self.request(
            "GET", "/api/v3/config/mediamanagement", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: Dict) -> Any:
        """Update config mediamanagement id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """Get specific config mediamanagement."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/mediamanagement/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """Get metadata."""
        params = {}
        return self.request("GET", "/api/v3/metadata", params=params, data=None)

    def post_metadata(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new metadata."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/metadata", params=params, data=data)

    def put_metadata_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """Update metadata id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """Delete metadata id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/metadata/{id}", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """Get specific metadata."""
        params = {}
        return self.request("GET", f"/api/v3/metadata/{id}", params=params, data=None)

    def get_metadata_schema(self) -> Any:
        """Get metadata schema."""
        params = {}
        return self.request("GET", "/api/v3/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test metadata."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """Add a new metadata testall."""
        params = {}
        return self.request(
            "POST", "/api/v3/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: Dict) -> Any:
        """Add a new metadata action name."""
        params = {}
        return self.request(
            "POST", f"/api/v3/metadata/action/{name}", params=params, data=data
        )

    def get_wanted_missing(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeSeries: bool = None,
        includeImages: bool = None,
        monitored: bool = None,
    ) -> Any:
        """Get wanted missing."""
        params = {}
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
        params = {}
        return self.request(
            "GET", f"/api/v3/wanted/missing/{id}", params=params, data=None
        )

    def get_config_naming(self) -> Any:
        """Get config naming."""
        params = {}
        return self.request("GET", "/api/v3/config/naming", params=params, data=None)

    def put_config_naming_id(self, id: str, data: Dict) -> Any:
        """Update config naming id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/naming/{id}", params=params, data=data
        )

    def get_config_naming_id(self, id: int) -> Any:
        """Get specific config naming."""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/naming/{id}", params=params, data=None
        )

    def get_config_naming_examples(
        self,
        renameEpisodes: bool = None,
        replaceIllegalCharacters: bool = None,
        colonReplacementFormat: int = None,
        customColonReplacementFormat: str = None,
        multiEpisodeStyle: int = None,
        standardEpisodeFormat: str = None,
        dailyEpisodeFormat: str = None,
        animeEpisodeFormat: str = None,
        seriesFolderFormat: str = None,
        seasonFolderFormat: str = None,
        specialsFolderFormat: str = None,
        id: int = None,
        resourceName: str = None,
    ) -> Any:
        """Get config naming examples."""
        params = {}
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
        params = {}
        return self.request("GET", "/api/v3/notification", params=params, data=None)

    def post_notification(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new notification."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/notification", params=params, data=data)

    def put_notification_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """Update notification id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """Delete notification id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params = {}
        return self.request(
            "GET", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_schema(self) -> Any:
        """Get notification schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test notification."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """Add a new notification testall."""
        params = {}
        return self.request(
            "POST", "/api/v3/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: Dict) -> Any:
        """Add a new notification action name."""
        params = {}
        return self.request(
            "POST", f"/api/v3/notification/action/{name}", params=params, data=data
        )

    def get_parse(self, title: str = None, path: str = None) -> Any:
        """Get parse."""
        params = {}
        if title is not None:
            params["title"] = title
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v3/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """Ping the Sonarr API to check connectivity."""
        params = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: Dict) -> Any:
        """Update qualitydefinition id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """Get a specific quality definition by ID."""
        params = {}
        return self.request(
            "GET", f"/api/v3/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """Get all quality definitions."""
        params = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: Dict) -> Any:
        """Update qualitydefinition update."""
        params = {}
        return self.request(
            "PUT", "/api/v3/qualitydefinition/update", params=params, data=data
        )

    def get_qualitydefinition_limits(self) -> Any:
        """Get qualitydefinition limits."""
        params = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition/limits", params=params, data=None
        )

    def post_qualityprofile(self, data: Dict) -> Any:
        """Add a new qualityprofile."""
        params = {}
        return self.request("POST", "/api/v3/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """Get qualityprofile."""
        params = {}
        return self.request("GET", "/api/v3/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """Delete qualityprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: Dict) -> Any:
        """Update qualityprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """Get specific qualityprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """Get qualityprofile schema."""
        params = {}
        return self.request(
            "GET", "/api/v3/qualityprofile/schema", params=params, data=None
        )

    def delete_queue_id(
        self,
        id: int,
        removeFromClient: bool = None,
        blocklist: bool = None,
        skipRedownload: bool = None,
        changeCategory: bool = None,
    ) -> Any:
        """Delete queue id."""
        params = {}
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
        data: Dict,
        removeFromClient: bool = None,
        blocklist: bool = None,
        skipRedownload: bool = None,
        changeCategory: bool = None,
    ) -> Any:
        """Delete queue bulk."""
        params = {}
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
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeUnknownSeriesItems: bool = None,
        includeSeries: bool = None,
        includeEpisode: bool = None,
        seriesIds: List = None,
        protocol: str = None,
        languages: List = None,
        quality: List = None,
        status: List = None,
    ) -> Any:
        """Get queue."""
        params = {}
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
        params = {}
        return self.request(
            "POST", f"/api/v3/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: Dict) -> Any:
        """Add a new queue grab bulk."""
        params = {}
        return self.request("POST", "/api/v3/queue/grab/bulk", params=params, data=data)

    def get_queue_details(
        self,
        seriesId: int = None,
        episodeIds: List = None,
        includeSeries: bool = None,
        includeEpisode: bool = None,
    ) -> Any:
        """Get queue details."""
        params = {}
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
        params = {}
        return self.request("GET", "/api/v3/queue/status", params=params, data=None)

    def post_release(self, data: Dict) -> Any:
        """Add a new release."""
        params = {}
        return self.request("POST", "/api/v3/release", params=params, data=data)

    def get_release(
        self, seriesId: int = None, episodeId: int = None, seasonNumber: int = None
    ) -> Any:
        """Get release."""
        params = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if episodeId is not None:
            params["episodeId"] = episodeId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
        return self.request("GET", "/api/v3/release", params=params, data=None)

    def post_releaseprofile(self, data: Dict) -> Any:
        """Add a new releaseprofile."""
        params = {}
        return self.request("POST", "/api/v3/releaseprofile", params=params, data=data)

    def get_releaseprofile(self) -> Any:
        """Get releaseprofile."""
        params = {}
        return self.request("GET", "/api/v3/releaseprofile", params=params, data=None)

    def delete_releaseprofile_id(self, id: int) -> Any:
        """Delete releaseprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def put_releaseprofile_id(self, id: str, data: Dict) -> Any:
        """Update releaseprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/releaseprofile/{id}", params=params, data=data
        )

    def get_releaseprofile_id(self, id: int) -> Any:
        """Get specific releaseprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def post_release_push(self, data: Dict) -> Any:
        """Add a new release push."""
        params = {}
        return self.request("POST", "/api/v3/release/push", params=params, data=data)

    def post_remotepathmapping(self, data: Dict) -> Any:
        """Add a new remotepathmapping."""
        params = {}
        return self.request(
            "POST", "/api/v3/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """Get remotepathmapping."""
        params = {}
        return self.request(
            "GET", "/api/v3/remotepathmapping", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """Delete remotepathmapping id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: Dict) -> Any:
        """Update remotepathmapping id."""
        params = {}
        return self.request(
            "PUT", f"/api/v3/remotepathmapping/{id}", params=params, data=data
        )

    def get_remotepathmapping_id(self, id: int) -> Any:
        """Get specific remotepathmapping."""
        params = {}
        return self.request(
            "GET", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def get_rename(self, seriesId: int = None, seasonNumber: int = None) -> Any:
        """Get rename."""
        params = {}
        if seriesId is not None:
            params["seriesId"] = seriesId
        if seasonNumber is not None:
            params["seasonNumber"] = seasonNumber
        return self.request("GET", "/api/v3/rename", params=params, data=None)

    def post_rootfolder(self, data: Dict) -> Any:
        """Add a new rootfolder."""
        params = {}
        return self.request("POST", "/api/v3/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """Get rootfolder."""
        params = {}
        return self.request("GET", "/api/v3/rootfolder", params=params, data=None)

    def delete_rootfolder_id(self, id: int) -> Any:
        """Delete rootfolder id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/rootfolder/{id}", params=params, data=None
        )

    def get_rootfolder_id(self, id: int) -> Any:
        """Get specific rootfolder."""
        params = {}
        return self.request("GET", f"/api/v3/rootfolder/{id}", params=params, data=None)

    def post_seasonpass(self, data: Dict) -> Any:
        """Add a new seasonpass."""
        params = {}
        return self.request("POST", "/api/v3/seasonpass", params=params, data=data)

    def get_series(self, tvdbId: int = None, includeSeasonImages: bool = None) -> Any:
        """Get series."""
        params = {}
        if tvdbId is not None:
            params["tvdbId"] = tvdbId
        if includeSeasonImages is not None:
            params["includeSeasonImages"] = includeSeasonImages
        return self.request("GET", "/api/v3/series", params=params, data=None)

    def post_series(self, data: Dict) -> Any:
        """Add a new series."""
        params = {}
        return self.request("POST", "/api/v3/series", params=params, data=data)

    def get_series_id(self, id: int, includeSeasonImages: bool = None) -> Any:
        """Get specific series."""
        params = {}
        if includeSeasonImages is not None:
            params["includeSeasonImages"] = includeSeasonImages
        return self.request("GET", f"/api/v3/series/{id}", params=params, data=None)

    def put_series_id(self, id: str, data: Dict, moveFiles: bool = None) -> Any:
        """Update series id."""
        params = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v3/series/{id}", params=params, data=data)

    def delete_series_id(
        self, id: int, deleteFiles: bool = None, addImportListExclusion: bool = None
    ) -> Any:
        """Delete series."""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v3/series/{id}", params=params, data=None)

    def put_series_editor(self, data: Dict) -> Any:
        """Update series editor."""
        params = {}
        return self.request("PUT", "/api/v3/series/editor", params=params, data=data)

    def delete_series_editor(self, data: Dict) -> Any:
        """Delete series editor."""
        params = {}
        return self.request("DELETE", "/api/v3/series/editor", params=params, data=data)

    def get_series_id_folder(self, id: int) -> Any:
        """Get series folder."""
        params = {}
        return self.request(
            "GET", f"/api/v3/series/{id}/folder", params=params, data=None
        )

    def post_series_import(self, data: Dict) -> Any:
        """Import series."""
        params = {}
        return self.request("POST", "/api/v3/series/import", params=params, data=data)

    def get_series_lookup(self, term: str = None) -> Any:
        """Lookup series."""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v3/series/lookup", params=params, data=None)

    def get_content_path(self, path: str) -> Any:
        """Get content path."""
        params = {}
        return self.request("GET", f"/content/{path}", params=params, data=None)

    def get_(self, path: str) -> Any:
        """Get resource by path."""
        params = {}
        return self.request("GET", "/", params=params, data=None)

    def get_path(self, path: str) -> Any:
        """Get system routes."""
        params = {}
        return self.request("GET", f"/{path}", params=params, data=None)

    def get_system_status(self) -> Any:
        """Get system status."""
        params = {}
        return self.request("GET", "/api/v3/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """Get system routes."""
        params = {}
        return self.request("GET", "/api/v3/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """Get duplicate system routes."""
        params = {}
        return self.request(
            "GET", "/api/v3/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """Trigger system shutdown."""
        params = {}
        return self.request("POST", "/api/v3/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """Trigger system restart."""
        params = {}
        return self.request("POST", "/api/v3/system/restart", params=params, data=None)

    def get_tag(self) -> Any:
        """Get tags."""
        params = {}
        return self.request("GET", "/api/v3/tag", params=params, data=None)

    def post_tag(self, data: Dict) -> Any:
        """Add a new tag."""
        params = {}
        return self.request("POST", "/api/v3/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: Dict) -> Any:
        """Update a tag."""
        params = {}
        return self.request("PUT", f"/api/v3/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete a tag."""
        params = {}
        return self.request("DELETE", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params = {}
        return self.request("GET", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag usage details."""
        params = {}
        return self.request("GET", "/api/v3/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag usage details."""
        params = {}
        return self.request("GET", f"/api/v3/tag/detail/{id}", params=params, data=None)

    def get_system_task(self) -> Any:
        """Get system tasks."""
        params = {}
        return self.request("GET", "/api/v3/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """Get specific system task."""
        params = {}
        return self.request(
            "GET", f"/api/v3/system/task/{id}", params=params, data=None
        )

    def put_config_ui_id(self, id: str, data: Dict) -> Any:
        """Update UI configuration."""
        params = {}
        return self.request("PUT", f"/api/v3/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """Get specific UI configuration."""
        params = {}
        return self.request("GET", f"/api/v3/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """Get UI configuration."""
        params = {}
        return self.request("GET", "/api/v3/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """Get available updates."""
        params = {}
        return self.request("GET", "/api/v3/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """Get log file update."""
        params = {}
        return self.request("GET", "/api/v3/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """Get log file update content."""
        params = {}
        return self.request(
            "GET", f"/api/v3/log/file/update/{filename}", params=params, data=None
        )

    def lookup_series(self, term: str) -> List[Dict]:
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
    ) -> Dict:
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
