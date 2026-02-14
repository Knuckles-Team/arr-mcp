"""
Prowlarr API Client.

This module provides a class to interact with the Prowlarr API for managing indexers and applications.
"""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib3


class Api:
    """
    API client for Prowlarr.

    Handles authentication, request session management, and provides methods
    for various Prowlarr endpoints including applications, indexers, and system settings.
    """

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        verify: bool = False,
    ):
        """
        Initialize the Prowlarr API client.

        Args:
            base_url (str): The base URL of the Prowlarr instance.
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
        Generic request method for the Prowlarr API.

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

    def get_api(self) -> Any:
        """Get the base API information."""
        params = {}
        return self.request("GET", "/api", params=params, data=None)

    def get_applications_id(self, id: int) -> Any:
        """Get details for a specific application by ID."""
        params = {}
        return self.request(
            "GET", f"/api/v1/applications/{id}", params=params, data=None
        )

    def put_applications_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update an existing application configuration."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/applications/{id}", params=params, data=data
        )

    def delete_applications_id(self, id: int) -> Any:
        """Delete an application configuration."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/applications/{id}", params=params, data=None
        )

    def get_applications(self) -> Any:
        """Get all applications managed by Prowlarr."""
        params = {}
        return self.request("GET", "/api/v1/applications", params=params, data=None)

    def post_applications(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new applications."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/applications", params=params, data=data)

    def put_applications_bulk(self, data: Dict) -> Any:
        """Update applications bulk."""
        params = {}
        return self.request(
            "PUT", "/api/v1/applications/bulk", params=params, data=data
        )

    def delete_applications_bulk(self, data: Dict) -> Any:
        """Delete applications bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v1/applications/bulk", params=params, data=data
        )

    def get_applications_schema(self) -> Any:
        """Get applications schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/applications/schema", params=params, data=None
        )

    def post_applications_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test applications."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/applications/test", params=params, data=data
        )

    def post_applications_testall(self) -> Any:
        """Add a new applications testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/applications/testall", params=params, data=None
        )

    def post_applications_action_name(self, name: str, data: Dict) -> Any:
        """Add a new applications action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/applications/action/{name}", params=params, data=data
        )

    def post_appprofile(self, data: Dict) -> Any:
        """Add a new appprofile."""
        params = {}
        return self.request("POST", "/api/v1/appprofile", params=params, data=data)

    def get_appprofile(self) -> Any:
        """Get appprofile."""
        params = {}
        return self.request("GET", "/api/v1/appprofile", params=params, data=None)

    def delete_appprofile_id(self, id: int) -> Any:
        """Delete appprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/appprofile/{id}", params=params, data=None
        )

    def put_appprofile_id(self, id: str, data: Dict) -> Any:
        """Update appprofile id."""
        params = {}
        return self.request("PUT", f"/api/v1/appprofile/{id}", params=params, data=data)

    def get_appprofile_id(self, id: int) -> Any:
        """Get specific appprofile."""
        params = {}
        return self.request("GET", f"/api/v1/appprofile/{id}", params=params, data=None)

    def get_appprofile_schema(self) -> Any:
        """Get appprofile schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/appprofile/schema", params=params, data=None
        )

    def post_login(self, returnUrl: str = None) -> Any:
        """Add a new login."""
        params = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get login."""
        params = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Get logout."""
        params = {}
        return self.request("GET", "/logout", params=params, data=None)

    def get_system_backup(self) -> Any:
        """Get system backup."""
        params = {}
        return self.request("GET", "/api/v1/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """Delete system backup id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """Add a new system backup restore id."""
        params = {}
        return self.request(
            "POST", f"/api/v1/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """Add a new system backup restore upload."""
        params = {}
        return self.request(
            "POST", "/api/v1/system/backup/restore/upload", params=params, data=None
        )

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params = {}
        return self.request("GET", f"/api/v1/command/{id}", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params = {}
        return self.request("DELETE", f"/api/v1/command/{id}", params=params, data=None)

    def post_command(self, data: Dict) -> Any:
        """Add a new command."""
        params = {}
        return self.request("POST", "/api/v1/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params = {}
        return self.request("GET", "/api/v1/command", params=params, data=None)

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params = {}
        return self.request(
            "GET", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def put_customfilter_id(self, id: str, data: Dict) -> Any:
        """Update customfilter id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """Delete customfilter id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params = {}
        return self.request("GET", "/api/v1/customfilter", params=params, data=None)

    def post_customfilter(self, data: Dict) -> Any:
        """Add a new customfilter."""
        params = {}
        return self.request("POST", "/api/v1/customfilter", params=params, data=data)

    def put_config_development_id(self, id: str, data: Dict) -> Any:
        """Update config development id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/development/{id}", params=params, data=data
        )

    def get_config_development_id(self, id: int) -> Any:
        """Get specific config development."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/development/{id}", params=params, data=None
        )

    def get_config_development(self) -> Any:
        """Get config development."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/development", params=params, data=None
        )

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update downloadclient id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """Delete downloadclient id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient(self) -> Any:
        """Get downloadclient."""
        params = {}
        return self.request("GET", "/api/v1/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new downloadclient."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/downloadclient", params=params, data=data)

    def put_downloadclient_bulk(self, data: Dict) -> Any:
        """Update downloadclient bulk."""
        params = {}
        return self.request(
            "PUT", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: Dict) -> Any:
        """Delete downloadclient bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """Get downloadclient schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test downloadclient."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """Add a new downloadclient testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: Dict) -> Any:
        """Add a new downloadclient action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/downloadclient/{id}", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: Dict) -> Any:
        """Update config downloadclient id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/downloadclient", params=params, data=None
        )

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
        return self.request("GET", "/api/v1/filesystem", params=params, data=None)

    def get_filesystem_type(self, path: str = None) -> Any:
        """Get filesystem type."""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v1/filesystem/type", params=params, data=None)

    def get_health(self) -> Any:
        """Get health."""
        params = {}
        return self.request("GET", "/api/v1/health", params=params, data=None)

    def get_history(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        eventType: List = None,
        successful: bool = None,
        downloadId: str = None,
        indexerIds: List = None,
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
        if eventType is not None:
            params["eventType"] = eventType
        if successful is not None:
            params["successful"] = successful
        if downloadId is not None:
            params["downloadId"] = downloadId
        if indexerIds is not None:
            params["indexerIds"] = indexerIds
        return self.request("GET", "/api/v1/history", params=params, data=None)

    def get_history_since(self, date: str = None, eventType: str = None) -> Any:
        """Get history since."""
        params = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        return self.request("GET", "/api/v1/history/since", params=params, data=None)

    def get_history_indexer(
        self, indexerId: int = None, eventType: str = None, limit: int = None
    ) -> Any:
        """Get history indexer."""
        params = {}
        if indexerId is not None:
            params["indexerId"] = indexerId
        if eventType is not None:
            params["eventType"] = eventType
        if limit is not None:
            params["limit"] = limit
        return self.request("GET", "/api/v1/history/indexer", params=params, data=None)

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/host/{id}", params=params, data=None
        )

    def put_config_host_id(self, id: str, data: Dict) -> Any:
        """Update config host id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/host/{id}", params=params, data=data
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params = {}
        return self.request("GET", "/api/v1/config/host", params=params, data=None)

    def get_indexer_id(self, id: int) -> Any:
        """Get specific indexer."""
        params = {}
        return self.request("GET", f"/api/v1/indexer/{id}", params=params, data=None)

    def put_indexer_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update indexer id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """Delete indexer id."""
        params = {}
        return self.request("DELETE", f"/api/v1/indexer/{id}", params=params, data=None)

    def get_indexer(self) -> Any:
        """Get indexer."""
        params = {}
        return self.request("GET", "/api/v1/indexer", params=params, data=None)

    def post_indexer(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new indexer."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/indexer", params=params, data=data)

    def put_indexer_bulk(self, data: Dict) -> Any:
        """Update indexer bulk."""
        params = {}
        return self.request("PUT", "/api/v1/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: Dict) -> Any:
        """Delete indexer bulk."""
        params = {}
        return self.request("DELETE", "/api/v1/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """Get indexer schema."""
        params = {}
        return self.request("GET", "/api/v1/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test indexer."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """Add a new indexer testall."""
        params = {}
        return self.request("POST", "/api/v1/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: Dict) -> Any:
        """Add a new indexer action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/indexer/action/{name}", params=params, data=data
        )

    def get_indexer_categories(self) -> Any:
        """Get indexer categories."""
        params = {}
        return self.request(
            "GET", "/api/v1/indexer/categories", params=params, data=None
        )

    def get_indexerproxy_id(self, id: int) -> Any:
        """Get specific indexerproxy."""
        params = {}
        return self.request(
            "GET", f"/api/v1/indexerproxy/{id}", params=params, data=None
        )

    def put_indexerproxy_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update indexerproxy id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/indexerproxy/{id}", params=params, data=data
        )

    def delete_indexerproxy_id(self, id: int) -> Any:
        """Delete indexerproxy id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/indexerproxy/{id}", params=params, data=None
        )

    def get_indexerproxy(self) -> Any:
        """Get indexerproxy."""
        params = {}
        return self.request("GET", "/api/v1/indexerproxy", params=params, data=None)

    def post_indexerproxy(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new indexerproxy."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/indexerproxy", params=params, data=data)

    def get_indexerproxy_schema(self) -> Any:
        """Get indexerproxy schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/indexerproxy/schema", params=params, data=None
        )

    def post_indexerproxy_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test indexerproxy."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/indexerproxy/test", params=params, data=data
        )

    def post_indexerproxy_testall(self) -> Any:
        """Add a new indexerproxy testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/indexerproxy/testall", params=params, data=None
        )

    def post_indexerproxy_action_name(self, name: str, data: Dict) -> Any:
        """Add a new indexerproxy action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/indexerproxy/action/{name}", params=params, data=data
        )

    def get_indexerstats(
        self,
        startDate: str = None,
        endDate: str = None,
        indexers: str = None,
        protocols: str = None,
        tags: str = None,
    ) -> Any:
        """Get indexerstats."""
        params = {}
        if startDate is not None:
            params["startDate"] = startDate
        if endDate is not None:
            params["endDate"] = endDate
        if indexers is not None:
            params["indexers"] = indexers
        if protocols is not None:
            params["protocols"] = protocols
        if tags is not None:
            params["tags"] = tags
        return self.request("GET", "/api/v1/indexerstats", params=params, data=None)

    def get_indexerstatus(self) -> Any:
        """Get indexerstatus."""
        params = {}
        return self.request("GET", "/api/v1/indexerstatus", params=params, data=None)

    def get_localization(self) -> Any:
        """Get localization."""
        params = {}
        return self.request("GET", "/api/v1/localization", params=params, data=None)

    def get_localization_options(self) -> Any:
        """Get localization options."""
        params = {}
        return self.request(
            "GET", "/api/v1/localization/options", params=params, data=None
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
        return self.request("GET", "/api/v1/log", params=params, data=None)

    def get_log_file(self) -> Any:
        """Get log file."""
        params = {}
        return self.request("GET", "/api/v1/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """Get log file filename."""
        params = {}
        return self.request(
            "GET", f"/api/v1/log/file/{filename}", params=params, data=None
        )

    def get_indexer_id_newznab(
        self,
        id: int,
        t: str = None,
        q: str = None,
        cat: str = None,
        imdbid: str = None,
        tmdbid: int = None,
        extended: str = None,
        limit: int = None,
        offset: int = None,
        minage: int = None,
        maxage: int = None,
        minsize: int = None,
        maxsize: int = None,
        rid: int = None,
        tvmazeid: int = None,
        traktid: int = None,
        tvdbid: int = None,
        doubanid: int = None,
        season: int = None,
        ep: str = None,
        album: str = None,
        artist: str = None,
        label: str = None,
        track: str = None,
        year: int = None,
        genre: str = None,
        author: str = None,
        title: str = None,
        publisher: str = None,
        configured: str = None,
        source: str = None,
        host: str = None,
        server: str = None,
    ) -> Any:
        """Get specific indexer newznab."""
        params = {}
        if t is not None:
            params["t"] = t
        if q is not None:
            params["q"] = q
        if cat is not None:
            params["cat"] = cat
        if imdbid is not None:
            params["imdbid"] = imdbid
        if tmdbid is not None:
            params["tmdbid"] = tmdbid
        if extended is not None:
            params["extended"] = extended
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if minage is not None:
            params["minage"] = minage
        if maxage is not None:
            params["maxage"] = maxage
        if minsize is not None:
            params["minsize"] = minsize
        if maxsize is not None:
            params["maxsize"] = maxsize
        if rid is not None:
            params["rid"] = rid
        if tvmazeid is not None:
            params["tvmazeid"] = tvmazeid
        if traktid is not None:
            params["traktid"] = traktid
        if tvdbid is not None:
            params["tvdbid"] = tvdbid
        if doubanid is not None:
            params["doubanid"] = doubanid
        if season is not None:
            params["season"] = season
        if ep is not None:
            params["ep"] = ep
        if album is not None:
            params["album"] = album
        if artist is not None:
            params["artist"] = artist
        if label is not None:
            params["label"] = label
        if track is not None:
            params["track"] = track
        if year is not None:
            params["year"] = year
        if genre is not None:
            params["genre"] = genre
        if author is not None:
            params["author"] = author
        if title is not None:
            params["title"] = title
        if publisher is not None:
            params["publisher"] = publisher
        if configured is not None:
            params["configured"] = configured
        if source is not None:
            params["source"] = source
        if host is not None:
            params["host"] = host
        if server is not None:
            params["server"] = server
        return self.request(
            "GET", f"/api/v1/indexer/{id}/newznab", params=params, data=None
        )

    def get_id_api(
        self,
        id: int,
        t: str = None,
        q: str = None,
        cat: str = None,
        imdbid: str = None,
        tmdbid: int = None,
        extended: str = None,
        limit: int = None,
        offset: int = None,
        minage: int = None,
        maxage: int = None,
        minsize: int = None,
        maxsize: int = None,
        rid: int = None,
        tvmazeid: int = None,
        traktid: int = None,
        tvdbid: int = None,
        doubanid: int = None,
        season: int = None,
        ep: str = None,
        album: str = None,
        artist: str = None,
        label: str = None,
        track: str = None,
        year: int = None,
        genre: str = None,
        author: str = None,
        title: str = None,
        publisher: str = None,
        configured: str = None,
        source: str = None,
        host: str = None,
        server: str = None,
    ) -> Any:
        """Get results for a specific indexer endpoint in Newznab format."""
        params = {}
        if t is not None:
            params["t"] = t
        if q is not None:
            params["q"] = q
        if cat is not None:
            params["cat"] = cat
        if imdbid is not None:
            params["imdbid"] = imdbid
        if tmdbid is not None:
            params["tmdbid"] = tmdbid
        if extended is not None:
            params["extended"] = extended
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if minage is not None:
            params["minage"] = minage
        if maxage is not None:
            params["maxage"] = maxage
        if minsize is not None:
            params["minsize"] = minsize
        if maxsize is not None:
            params["maxsize"] = maxsize
        if rid is not None:
            params["rid"] = rid
        if tvmazeid is not None:
            params["tvmazeid"] = tvmazeid
        if traktid is not None:
            params["traktid"] = traktid
        if tvdbid is not None:
            params["tvdbid"] = tvdbid
        if doubanid is not None:
            params["doubanid"] = doubanid
        if season is not None:
            params["season"] = season
        if ep is not None:
            params["ep"] = ep
        if album is not None:
            params["album"] = album
        if artist is not None:
            params["artist"] = artist
        if label is not None:
            params["label"] = label
        if track is not None:
            params["track"] = track
        if year is not None:
            params["year"] = year
        if genre is not None:
            params["genre"] = genre
        if author is not None:
            params["author"] = author
        if title is not None:
            params["title"] = title
        if publisher is not None:
            params["publisher"] = publisher
        if configured is not None:
            params["configured"] = configured
        if source is not None:
            params["source"] = source
        if host is not None:
            params["host"] = host
        if server is not None:
            params["server"] = server
        return self.request("GET", f"/{id}/api", params=params, data=None)

    def get_indexer_id_download(
        self, id: int, link: str = None, file: str = None
    ) -> Any:
        """Download a release from a specific indexer."""
        params = {}
        if link is not None:
            params["link"] = link
        if file is not None:
            params["file"] = file
        return self.request(
            "GET", f"/api/v1/indexer/{id}/download", params=params, data=None
        )

    def get_id_download(self, id: int, link: str = None, file: str = None) -> Any:
        """Get specific id download."""
        params = {}
        if link is not None:
            params["link"] = link
        if file is not None:
            params["file"] = file
        return self.request("GET", f"/{id}/download", params=params, data=None)

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params = {}
        return self.request(
            "GET", f"/api/v1/notification/{id}", params=params, data=None
        )

    def put_notification_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update notification id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """Delete notification id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/notification/{id}", params=params, data=None
        )

    def get_notification(self) -> Any:
        """Get all configured notifications."""
        params = {}
        return self.request("GET", "/api/v1/notification", params=params, data=None)

    def post_notification(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new notification."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/notification", params=params, data=data)

    def get_notification_schema(self) -> Any:
        """Get notification schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test notification."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """Add a new notification testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: Dict) -> Any:
        """Add a new notification action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/notification/action/{name}", params=params, data=data
        )

    def get_ping(self) -> Any:
        """Ping the Prowlarr API to check connectivity."""
        params = {}
        return self.request("GET", "/ping", params=params, data=None)

    def post_search(self, data: Dict) -> Any:
        """Perform a bulk search across multiple indexers."""
        params = {}
        return self.request("POST", "/api/v1/search", params=params, data=data)

    def get_search(
        self,
        query: str = None,
        type: str = None,
        indexerIds: List = None,
        categories: List = None,
        limit: int = None,
        offset: int = None,
    ) -> Any:
        """Get search."""
        params = {}
        if query is not None:
            params["query"] = query
        if type is not None:
            params["type"] = type
        if indexerIds is not None:
            params["indexerIds"] = indexerIds
        if categories is not None:
            params["categories"] = categories
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self.request("GET", "/api/v1/search", params=params, data=None)

    def post_search_bulk(self, data: Dict) -> Any:
        """Add a new search bulk."""
        params = {}
        return self.request("POST", "/api/v1/search/bulk", params=params, data=data)

    def get_content_path(self, path: str) -> Any:
        """Get content path."""
        params = {}
        return self.request("GET", f"/content/{path}", params=params, data=None)

    def get_(self, path: str) -> Any:
        """Get ."""
        params = {}
        return self.request("GET", "/", params=params, data=None)

    def get_path(self, path: str) -> Any:
        """Get path."""
        params = {}
        return self.request("GET", f"/{path}", params=params, data=None)

    def get_system_status(self) -> Any:
        """Get system status."""
        params = {}
        return self.request("GET", "/api/v1/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """Get system routes."""
        params = {}
        return self.request("GET", "/api/v1/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """Get system routes duplicate."""
        params = {}
        return self.request(
            "GET", "/api/v1/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """Add a new system shutdown."""
        params = {}
        return self.request("POST", "/api/v1/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """Add a new system restart."""
        params = {}
        return self.request("POST", "/api/v1/system/restart", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params = {}
        return self.request("GET", f"/api/v1/tag/{id}", params=params, data=None)

    def put_tag_id(self, id: str, data: Dict) -> Any:
        """Update tag id."""
        params = {}
        return self.request("PUT", f"/api/v1/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete tag id."""
        params = {}
        return self.request("DELETE", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag(self) -> Any:
        """Get tag."""
        params = {}
        return self.request("GET", "/api/v1/tag", params=params, data=None)

    def post_tag(self, data: Dict) -> Any:
        """Add a new tag."""
        params = {}
        return self.request("POST", "/api/v1/tag", params=params, data=data)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag detail."""
        params = {}
        return self.request("GET", f"/api/v1/tag/detail/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag detail."""
        params = {}
        return self.request("GET", "/api/v1/tag/detail", params=params, data=None)

    def get_system_task(self) -> Any:
        """Get system task."""
        params = {}
        return self.request("GET", "/api/v1/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """Get specific system task."""
        params = {}
        return self.request(
            "GET", f"/api/v1/system/task/{id}", params=params, data=None
        )

    def put_config_ui_id(self, id: str, data: Dict) -> Any:
        """Update config ui id."""
        params = {}
        return self.request("PUT", f"/api/v1/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """Get specific config ui."""
        params = {}
        return self.request("GET", f"/api/v1/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """Get config ui."""
        params = {}
        return self.request("GET", "/api/v1/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """Get update."""
        params = {}
        return self.request("GET", "/api/v1/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """Get log file update."""
        params = {}
        return self.request("GET", "/api/v1/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """Get log file update filename."""
        params = {}
        return self.request(
            "GET", f"/api/v1/log/file/update/{filename}", params=params, data=None
        )

    def search(self, query: str) -> List[Dict]:
        """
        Search for indexers using the search endpoint.
        """
        return self.get_search(query=query)
