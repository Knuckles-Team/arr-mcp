"""
Chaptarr API Client.

This module provides a class to interact with the Chaptarr API,
which appears to be a specialized instance or variant of Readarr
for managing books and authors.
"""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib3


class Api:
    """
    API client for Chaptarr.

    Handles authentication, request session management, and provides methods
    for various Chaptarr endpoints including authors, books, calendar, and system configuration.
    """

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        verify: bool = False,
    ):
        """
        Initialize the Chaptarr API client.

        Args:
            base_url (str): The base URL of the Chaptarr instance.
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
        Generic request method for the Chaptarr API.

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

    def post_login(self, returnUrl: str = None) -> Any:
        """Log in to the Chaptarr instance."""
        params = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get the login status or page."""
        params = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Log out from the Chaptarr instance."""
        params = {}
        return self.request("GET", "/logout", params=params, data=None)

    def get_author(self) -> Any:
        """Get all authors managed by Chaptarr."""
        params = {}
        return self.request("GET", "/api/v1/author", params=params, data=None)

    def post_author(self, data: Dict) -> Any:
        """Add a new author."""
        params = {}
        return self.request("POST", "/api/v1/author", params=params, data=data)

    def put_author_id(self, id: str, data: Dict, moveFiles: bool = None) -> Any:
        """Update an existing author by ID."""
        params = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v1/author/{id}", params=params, data=data)

    def delete_author_id(
        self, id: int, deleteFiles: bool = None, addImportListExclusion: bool = None
    ) -> Any:
        """Delete an author by ID."""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/author/{id}", params=params, data=None)

    def get_author_id(self, id: int) -> Any:
        """Get specific author."""
        params = {}
        return self.request("GET", f"/api/v1/author/{id}", params=params, data=None)

    def put_author_editor(self, data: Dict) -> Any:
        """Update author editor."""
        params = {}
        return self.request("PUT", "/api/v1/author/editor", params=params, data=data)

    def delete_author_editor(self, data: Dict) -> Any:
        """Delete author editor."""
        params = {}
        return self.request("DELETE", "/api/v1/author/editor", params=params, data=data)

    def get_author_lookup(self, term: str = None) -> Any:
        """Get author lookup."""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/author/lookup", params=params, data=None)

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

    def get_blocklist(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
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
        return self.request("GET", "/api/v1/blocklist", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """Delete blocklist id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: Dict) -> Any:
        """Delete blocklist bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v1/blocklist/bulk", params=params, data=data
        )

    def get_book(
        self,
        authorId: int = None,
        bookIds: List = None,
        titleSlug: str = None,
        includeAllAuthorBooks: bool = None,
    ) -> Any:
        """Get book."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookIds is not None:
            params["bookIds"] = bookIds
        if titleSlug is not None:
            params["titleSlug"] = titleSlug
        if includeAllAuthorBooks is not None:
            params["includeAllAuthorBooks"] = includeAllAuthorBooks
        return self.request("GET", "/api/v1/book", params=params, data=None)

    def post_book(self, data: Dict) -> Any:
        """Add a new book."""
        params = {}
        return self.request("POST", "/api/v1/book", params=params, data=data)

    def get_book_id_overview(self, id: int) -> Any:
        """Get specific book overview."""
        params = {}
        return self.request(
            "GET", f"/api/v1/book/{id}/overview", params=params, data=None
        )

    def put_book_id(self, id: str, data: Dict) -> Any:
        """Update book id."""
        params = {}
        return self.request("PUT", f"/api/v1/book/{id}", params=params, data=data)

    def delete_book_id(
        self, id: int, deleteFiles: bool = None, addImportListExclusion: bool = None
    ) -> Any:
        """Delete book id."""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/book/{id}", params=params, data=None)

    def get_book_id(self, id: int) -> Any:
        """Get specific book."""
        params = {}
        return self.request("GET", f"/api/v1/book/{id}", params=params, data=None)

    def put_book_monitor(self, data: Dict) -> Any:
        """Update book monitor."""
        params = {}
        return self.request("PUT", "/api/v1/book/monitor", params=params, data=data)

    def put_book_editor(self, data: Dict) -> Any:
        """Update book editor."""
        params = {}
        return self.request("PUT", "/api/v1/book/editor", params=params, data=data)

    def delete_book_editor(self, data: Dict) -> Any:
        """Delete book editor."""
        params = {}
        return self.request("DELETE", "/api/v1/book/editor", params=params, data=data)

    def get_bookfile(
        self,
        authorId: int = None,
        bookFileIds: List = None,
        bookId: List = None,
        unmapped: bool = None,
    ) -> Any:
        """Get bookfile."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookFileIds is not None:
            params["bookFileIds"] = bookFileIds
        if bookId is not None:
            params["bookId"] = bookId
        if unmapped is not None:
            params["unmapped"] = unmapped
        return self.request("GET", "/api/v1/bookfile", params=params, data=None)

    def put_bookfile_id(self, id: str, data: Dict) -> Any:
        """Update bookfile id."""
        params = {}
        return self.request("PUT", f"/api/v1/bookfile/{id}", params=params, data=data)

    def delete_bookfile_id(self, id: int) -> Any:
        """Delete bookfile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/bookfile/{id}", params=params, data=None
        )

    def get_bookfile_id(self, id: int) -> Any:
        """Get specific bookfile."""
        params = {}
        return self.request("GET", f"/api/v1/bookfile/{id}", params=params, data=None)

    def put_bookfile_editor(self, data: Dict) -> Any:
        """Update bookfile editor."""
        params = {}
        return self.request("PUT", "/api/v1/bookfile/editor", params=params, data=data)

    def delete_bookfile_bulk(self, data: Dict) -> Any:
        """Delete bookfile bulk."""
        params = {}
        return self.request("DELETE", "/api/v1/bookfile/bulk", params=params, data=data)

    def get_book_lookup(self, term: str = None) -> Any:
        """Get book lookup."""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/book/lookup", params=params, data=None)

    def post_bookshelf(self, data: Dict) -> Any:
        """Add a new bookshelf."""
        params = {}
        return self.request("POST", "/api/v1/bookshelf", params=params, data=data)

    def get_calendar(
        self,
        start: str = None,
        end: str = None,
        unmonitored: bool = None,
        includeAuthor: bool = None,
    ) -> Any:
        """Get calendar."""
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        return self.request("GET", "/api/v1/calendar", params=params, data=None)

    def get_calendar_id(self, id: int) -> Any:
        """Get specific calendar."""
        params = {}
        return self.request("GET", f"/api/v1/calendar/{id}", params=params, data=None)

    def get_feed_v1_calendar_readarrics(
        self,
        pastDays: int = None,
        futureDays: int = None,
        tagList: str = None,
        unmonitored: bool = None,
    ) -> Any:
        """Get feed v1 calendar readarrics."""
        params = {}
        if pastDays is not None:
            params["pastDays"] = pastDays
        if futureDays is not None:
            params["futureDays"] = futureDays
        if tagList is not None:
            params["tagList"] = tagList
        if unmonitored is not None:
            params["unmonitored"] = unmonitored
        return self.request(
            "GET", "/feed/v1/calendar/readarr.ics", params=params, data=None
        )

    def post_command(self, data: Dict) -> Any:
        """Add a new command."""
        params = {}
        return self.request("POST", "/api/v1/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params = {}
        return self.request("GET", "/api/v1/command", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params = {}
        return self.request("DELETE", f"/api/v1/command/{id}", params=params, data=None)

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params = {}
        return self.request("GET", f"/api/v1/command/{id}", params=params, data=None)

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params = {}
        return self.request("GET", "/api/v1/customfilter", params=params, data=None)

    def post_customfilter(self, data: Dict) -> Any:
        """Add a new customfilter."""
        params = {}
        return self.request("POST", "/api/v1/customfilter", params=params, data=data)

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

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params = {}
        return self.request(
            "GET", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def post_customformat(self, data: Dict) -> Any:
        """Add a new customformat."""
        params = {}
        return self.request("POST", "/api/v1/customformat", params=params, data=data)

    def get_customformat(self) -> Any:
        """Get customformat."""
        params = {}
        return self.request("GET", "/api/v1/customformat", params=params, data=None)

    def put_customformat_id(self, id: str, data: Dict) -> Any:
        """Update customformat id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """Delete customformat id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def get_customformat_id(self, id: int) -> Any:
        """Get specific customformat."""
        params = {}
        return self.request(
            "GET", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def get_customformat_schema(self) -> Any:
        """Get customformat schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/customformat/schema", params=params, data=None
        )

    def get_wanted_cutoff(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeAuthor: bool = None,
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
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/cutoff", params=params, data=None)

    def get_wanted_cutoff_id(self, id: int) -> Any:
        """Get specific wanted cutoff."""
        params = {}
        return self.request(
            "GET", f"/api/v1/wanted/cutoff/{id}", params=params, data=None
        )

    def post_delayprofile(self, data: Dict) -> Any:
        """Add a new delayprofile."""
        params = {}
        return self.request("POST", "/api/v1/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """Get delayprofile."""
        params = {}
        return self.request("GET", "/api/v1/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """Delete delayprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: Dict) -> Any:
        """Update delayprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """Get specific delayprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, afterId: int = None) -> Any:
        """Update delayprofile reorder id."""
        params = {}
        if afterId is not None:
            params["afterId"] = afterId
        return self.request(
            "PUT", f"/api/v1/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_config_development(self) -> Any:
        """Get config development."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/development", params=params, data=None
        )

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

    def get_diskspace(self) -> Any:
        """Get diskspace."""
        params = {}
        return self.request("GET", "/api/v1/diskspace", params=params, data=None)

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

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

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

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/downloadclient", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: Dict) -> Any:
        """Update config downloadclient id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/downloadclient/{id}", params=params, data=None
        )

    def get_edition(self, bookId: List = None) -> Any:
        """Get edition."""
        params = {}
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/edition", params=params, data=None)

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

    def get_filesystem_mediafiles(self, path: str = None) -> Any:
        """Get filesystem mediafiles."""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v1/filesystem/mediafiles", params=params, data=None
        )

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
        includeAuthor: bool = None,
        includeBook: bool = None,
        eventType: List = None,
        bookId: int = None,
        downloadId: str = None,
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
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
        if eventType is not None:
            params["eventType"] = eventType
        if bookId is not None:
            params["bookId"] = bookId
        if downloadId is not None:
            params["downloadId"] = downloadId
        return self.request("GET", "/api/v1/history", params=params, data=None)

    def get_history_since(
        self,
        date: str = None,
        eventType: str = None,
        includeAuthor: bool = None,
        includeBook: bool = None,
    ) -> Any:
        """Get history since."""
        params = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
        return self.request("GET", "/api/v1/history/since", params=params, data=None)

    def get_history_author(
        self,
        authorId: int = None,
        bookId: int = None,
        eventType: str = None,
        includeAuthor: bool = None,
        includeBook: bool = None,
    ) -> Any:
        """Get history author."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookId is not None:
            params["bookId"] = bookId
        if eventType is not None:
            params["eventType"] = eventType
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
        return self.request("GET", "/api/v1/history/author", params=params, data=None)

    def post_history_failed_id(self, id: int) -> Any:
        """Add a new history failed id."""
        params = {}
        return self.request(
            "POST", f"/api/v1/history/failed/{id}", params=params, data=None
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params = {}
        return self.request("GET", "/api/v1/config/host", params=params, data=None)

    def put_config_host_id(self, id: str, data: Dict) -> Any:
        """Update config host id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/host/{id}", params=params, data=data
        )

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/host/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """Get importlist."""
        params = {}
        return self.request("GET", "/api/v1/importlist", params=params, data=None)

    def post_importlist(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new importlist."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/importlist", params=params, data=data)

    def put_importlist_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update importlist id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete importlist id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """Get specific importlist."""
        params = {}
        return self.request("GET", f"/api/v1/importlist/{id}", params=params, data=None)

    def put_importlist_bulk(self, data: Dict) -> Any:
        """Update importlist bulk."""
        params = {}
        return self.request("PUT", "/api/v1/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: Dict) -> Any:
        """Delete importlist bulk."""
        params = {}
        return self.request(
            "DELETE", "/api/v1/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """Get importlist schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test importlist."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """Add a new importlist testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: Dict) -> Any:
        """Add a new importlist action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/importlist/action/{name}", params=params, data=data
        )

    def get_importlistexclusion(self) -> Any:
        """Get importlistexclusion."""
        params = {}
        return self.request(
            "GET", "/api/v1/importlistexclusion", params=params, data=None
        )

    def post_importlistexclusion(self, data: Dict) -> Any:
        """Add a new importlistexclusion."""
        params = {}
        return self.request(
            "POST", "/api/v1/importlistexclusion", params=params, data=data
        )

    def put_importlistexclusion_id(self, id: str, data: Dict) -> Any:
        """Update importlistexclusion id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/importlistexclusion/{id}", params=params, data=data
        )

    def delete_importlistexclusion_id(self, id: int) -> Any:
        """Delete importlistexclusion id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def get_importlistexclusion_id(self, id: int) -> Any:
        """Get specific importlistexclusion."""
        params = {}
        return self.request(
            "GET", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

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

    def get_indexer_id(self, id: int) -> Any:
        """Get specific indexer."""
        params = {}
        return self.request("GET", f"/api/v1/indexer/{id}", params=params, data=None)

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

    def get_config_indexer(self) -> Any:
        """Get config indexer."""
        params = {}
        return self.request("GET", "/api/v1/config/indexer", params=params, data=None)

    def put_config_indexer_id(self, id: str, data: Dict) -> Any:
        """Update config indexer id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """Get specific config indexer."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/indexer/{id}", params=params, data=None
        )

    def get_indexerflag(self) -> Any:
        """Get indexerflag."""
        params = {}
        return self.request("GET", "/api/v1/indexerflag", params=params, data=None)

    def get_language(self) -> Any:
        """Get language."""
        params = {}
        return self.request("GET", "/api/v1/language", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """Get specific language."""
        params = {}
        return self.request("GET", f"/api/v1/language/{id}", params=params, data=None)

    def get_localization(self) -> Any:
        """Get localization."""
        params = {}
        return self.request("GET", "/api/v1/localization", params=params, data=None)

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

    def post_manualimport(self, data: Dict) -> Any:
        """Add a new manualimport."""
        params = {}
        return self.request("POST", "/api/v1/manualimport", params=params, data=data)

    def get_manualimport(
        self,
        folder: str = None,
        downloadId: str = None,
        authorId: int = None,
        filterExistingFiles: bool = None,
        replaceExistingFiles: bool = None,
    ) -> Any:
        """Get manualimport."""
        params = {}
        if folder is not None:
            params["folder"] = folder
        if downloadId is not None:
            params["downloadId"] = downloadId
        if authorId is not None:
            params["authorId"] = authorId
        if filterExistingFiles is not None:
            params["filterExistingFiles"] = filterExistingFiles
        if replaceExistingFiles is not None:
            params["replaceExistingFiles"] = replaceExistingFiles
        return self.request("GET", "/api/v1/manualimport", params=params, data=None)

    def get_mediacover_author_author_id_filename(
        self, authorId: int, filename: str
    ) -> Any:
        """Get specific mediacover author author filename."""
        params = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/author/{authorId}/{filename}",
            params=params,
            data=None,
        )

    def get_mediacover_book_book_id_filename(self, bookId: int, filename: str) -> Any:
        """Get specific mediacover book book filename."""
        params = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/book/{bookId}/{filename}",
            params=params,
            data=None,
        )

    def get_config_mediamanagement(self) -> Any:
        """Get config mediamanagement."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/mediamanagement", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: Dict) -> Any:
        """Update config mediamanagement id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """Get specific config mediamanagement."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/mediamanagement/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """Get metadata."""
        params = {}
        return self.request("GET", "/api/v1/metadata", params=params, data=None)

    def post_metadata(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new metadata."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/metadata", params=params, data=data)

    def put_metadata_id(self, id: str, data: Dict, forceSave: bool = None) -> Any:
        """Update metadata id."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """Delete metadata id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/metadata/{id}", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """Get specific metadata."""
        params = {}
        return self.request("GET", f"/api/v1/metadata/{id}", params=params, data=None)

    def get_metadata_schema(self) -> Any:
        """Get metadata schema."""
        params = {}
        return self.request("GET", "/api/v1/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: Dict, forceTest: bool = None) -> Any:
        """Test metadata."""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """Add a new metadata testall."""
        params = {}
        return self.request(
            "POST", "/api/v1/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: Dict) -> Any:
        """Add a new metadata action name."""
        params = {}
        return self.request(
            "POST", f"/api/v1/metadata/action/{name}", params=params, data=data
        )

    def post_metadataprofile(self, data: Dict) -> Any:
        """Add a new metadataprofile."""
        params = {}
        return self.request("POST", "/api/v1/metadataprofile", params=params, data=data)

    def get_metadataprofile(self) -> Any:
        """Get metadataprofile."""
        params = {}
        return self.request("GET", "/api/v1/metadataprofile", params=params, data=None)

    def delete_metadataprofile_id(self, id: int) -> Any:
        """Delete metadataprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def put_metadataprofile_id(self, id: str, data: Dict) -> Any:
        """Update metadataprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/metadataprofile/{id}", params=params, data=data
        )

    def get_metadataprofile_id(self, id: int) -> Any:
        """Get specific metadataprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def get_metadataprofile_schema(self) -> Any:
        """Get metadataprofile schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/metadataprofile/schema", params=params, data=None
        )

    def get_config_metadataprovider(self) -> Any:
        """Get config metadataprovider."""
        params = {}
        return self.request(
            "GET", "/api/v1/config/metadataprovider", params=params, data=None
        )

    def put_config_metadataprovider_id(self, id: str, data: Dict) -> Any:
        """Update config metadataprovider id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/metadataprovider/{id}", params=params, data=data
        )

    def get_config_metadataprovider_id(self, id: int) -> Any:
        """Get specific config metadataprovider."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/metadataprovider/{id}", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeAuthor: bool = None,
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
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/missing", params=params, data=None)

    def get_wanted_missing_id(self, id: int) -> Any:
        """Get specific wanted missing."""
        params = {}
        return self.request(
            "GET", f"/api/v1/wanted/missing/{id}", params=params, data=None
        )

    def get_config_naming(self) -> Any:
        """Get config naming."""
        params = {}
        return self.request("GET", "/api/v1/config/naming", params=params, data=None)

    def put_config_naming_id(self, id: str, data: Dict) -> Any:
        """Update config naming id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/naming/{id}", params=params, data=data
        )

    def get_config_naming_id(self, id: int) -> Any:
        """Get specific config naming."""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/naming/{id}", params=params, data=None
        )

    def get_config_naming_examples(
        self,
        renameBooks: bool = None,
        replaceIllegalCharacters: bool = None,
        colonReplacementFormat: int = None,
        standardBookFormat: str = None,
        authorFolderFormat: str = None,
        includeAuthorName: bool = None,
        includeBookTitle: bool = None,
        includeQuality: bool = None,
        replaceSpaces: bool = None,
        separator: str = None,
        numberStyle: str = None,
        id: int = None,
        resourceName: str = None,
    ) -> Any:
        """Get config naming examples."""
        params = {}
        if renameBooks is not None:
            params["renameBooks"] = renameBooks
        if replaceIllegalCharacters is not None:
            params["replaceIllegalCharacters"] = replaceIllegalCharacters
        if colonReplacementFormat is not None:
            params["colonReplacementFormat"] = colonReplacementFormat
        if standardBookFormat is not None:
            params["standardBookFormat"] = standardBookFormat
        if authorFolderFormat is not None:
            params["authorFolderFormat"] = authorFolderFormat
        if includeAuthorName is not None:
            params["includeAuthorName"] = includeAuthorName
        if includeBookTitle is not None:
            params["includeBookTitle"] = includeBookTitle
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

    def get_notification(self) -> Any:
        """Get notification."""
        params = {}
        return self.request("GET", "/api/v1/notification", params=params, data=None)

    def post_notification(self, data: Dict, forceSave: bool = None) -> Any:
        """Add a new notification."""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/notification", params=params, data=data)

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

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params = {}
        return self.request(
            "GET", f"/api/v1/notification/{id}", params=params, data=None
        )

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

    def get_parse(self, title: str = None) -> Any:
        """Get parse."""
        params = {}
        if title is not None:
            params["title"] = title
        return self.request("GET", "/api/v1/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """Get ping."""
        params = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: Dict) -> Any:
        """Update qualitydefinition id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """Get specific qualitydefinition."""
        params = {}
        return self.request(
            "GET", f"/api/v1/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """Get qualitydefinition."""
        params = {}
        return self.request(
            "GET", "/api/v1/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: Dict) -> Any:
        """Update qualitydefinition update."""
        params = {}
        return self.request(
            "PUT", "/api/v1/qualitydefinition/update", params=params, data=data
        )

    def post_qualityprofile(self, data: Dict) -> Any:
        """Add a new qualityprofile."""
        params = {}
        return self.request("POST", "/api/v1/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """Get qualityprofile."""
        params = {}
        return self.request("GET", "/api/v1/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """Delete qualityprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: Dict) -> Any:
        """Update qualityprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """Get specific qualityprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """Get qualityprofile schema."""
        params = {}
        return self.request(
            "GET", "/api/v1/qualityprofile/schema", params=params, data=None
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
        return self.request("DELETE", f"/api/v1/queue/{id}", params=params, data=None)

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
        return self.request("DELETE", "/api/v1/queue/bulk", params=params, data=data)

    def get_queue(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeUnknownAuthorItems: bool = None,
        includeAuthor: bool = None,
        includeBook: bool = None,
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
        if includeUnknownAuthorItems is not None:
            params["includeUnknownAuthorItems"] = includeUnknownAuthorItems
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
        return self.request("GET", "/api/v1/queue", params=params, data=None)

    def post_queue_grab_id(self, id: int) -> Any:
        """Add a new queue grab id."""
        params = {}
        return self.request(
            "POST", f"/api/v1/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: Dict) -> Any:
        """Add a new queue grab bulk."""
        params = {}
        return self.request("POST", "/api/v1/queue/grab/bulk", params=params, data=data)

    def get_queue_details(
        self,
        authorId: int = None,
        bookIds: List = None,
        includeAuthor: bool = None,
        includeBook: bool = None,
    ) -> Any:
        """Get queue details."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookIds is not None:
            params["bookIds"] = bookIds
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
        return self.request("GET", "/api/v1/queue/details", params=params, data=None)

    def get_queue_status(self) -> Any:
        """Get queue status."""
        params = {}
        return self.request("GET", "/api/v1/queue/status", params=params, data=None)

    def post_release(self, data: Dict) -> Any:
        """Add a new release."""
        params = {}
        return self.request("POST", "/api/v1/release", params=params, data=data)

    def get_release(self, bookId: int = None, authorId: int = None) -> Any:
        """Get release."""
        params = {}
        if bookId is not None:
            params["bookId"] = bookId
        if authorId is not None:
            params["authorId"] = authorId
        return self.request("GET", "/api/v1/release", params=params, data=None)

    def get_releaseprofile(self) -> Any:
        """Get releaseprofile."""
        params = {}
        return self.request("GET", "/api/v1/releaseprofile", params=params, data=None)

    def post_releaseprofile(self, data: Dict) -> Any:
        """Add a new releaseprofile."""
        params = {}
        return self.request("POST", "/api/v1/releaseprofile", params=params, data=data)

    def put_releaseprofile_id(self, id: str, data: Dict) -> Any:
        """Update releaseprofile id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/releaseprofile/{id}", params=params, data=data
        )

    def delete_releaseprofile_id(self, id: int) -> Any:
        """Delete releaseprofile id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def get_releaseprofile_id(self, id: int) -> Any:
        """Get specific releaseprofile."""
        params = {}
        return self.request(
            "GET", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def post_release_push(self, data: Dict) -> Any:
        """Add a new release push."""
        params = {}
        return self.request("POST", "/api/v1/release/push", params=params, data=data)

    def post_remotepathmapping(self, data: Dict) -> Any:
        """Add a new remotepathmapping."""
        params = {}
        return self.request(
            "POST", "/api/v1/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """Get remotepathmapping."""
        params = {}
        return self.request(
            "GET", "/api/v1/remotepathmapping", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """Delete remotepathmapping id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: Dict) -> Any:
        """Update remotepathmapping id."""
        params = {}
        return self.request(
            "PUT", f"/api/v1/remotepathmapping/{id}", params=params, data=data
        )

    def get_remotepathmapping_id(self, id: int) -> Any:
        """Get specific remotepathmapping."""
        params = {}
        return self.request(
            "GET", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def get_rename(self, authorId: int = None, bookId: int = None) -> Any:
        """Get rename."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/rename", params=params, data=None)

    def get_retag(self, authorId: int = None, bookId: int = None) -> Any:
        """Get retag."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/retag", params=params, data=None)

    def post_rootfolder(self, data: Dict) -> Any:
        """Add a new rootfolder."""
        params = {}
        return self.request("POST", "/api/v1/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """Get rootfolder."""
        params = {}
        return self.request("GET", "/api/v1/rootfolder", params=params, data=None)

    def put_rootfolder_id(self, id: str, data: Dict) -> Any:
        """Update rootfolder id."""
        params = {}
        return self.request("PUT", f"/api/v1/rootfolder/{id}", params=params, data=data)

    def delete_rootfolder_id(self, id: int) -> Any:
        """Delete rootfolder id."""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/rootfolder/{id}", params=params, data=None
        )

    def get_rootfolder_id(self, id: int) -> Any:
        """Get specific rootfolder."""
        params = {}
        return self.request("GET", f"/api/v1/rootfolder/{id}", params=params, data=None)

    def get_search(self, term: str = None) -> Any:
        """Get search."""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/search", params=params, data=None)

    def get_series(self, authorId: int = None) -> Any:
        """Get series."""
        params = {}
        if authorId is not None:
            params["authorId"] = authorId
        return self.request("GET", "/api/v1/series", params=params, data=None)

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

    def get_tag(self) -> Any:
        """Get tag."""
        params = {}
        return self.request("GET", "/api/v1/tag", params=params, data=None)

    def post_tag(self, data: Dict) -> Any:
        """Add a new tag."""
        params = {}
        return self.request("POST", "/api/v1/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: Dict) -> Any:
        """Update tag id."""
        params = {}
        return self.request("PUT", f"/api/v1/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete tag id."""
        params = {}
        return self.request("DELETE", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params = {}
        return self.request("GET", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag detail."""
        params = {}
        return self.request("GET", "/api/v1/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag detail."""
        params = {}
        return self.request("GET", f"/api/v1/tag/detail/{id}", params=params, data=None)

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
