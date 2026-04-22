"""
Chaptarr API Client.

This module provides a class to interact with the Chaptarr API,
which appears to be a specialized instance or variant of Readarr
for managing books and authors.
"""

from typing import Any
from urllib.parse import urljoin

import requests
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
        token: str | None = None,
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
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
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
        """Log in to the Chaptarr instance."""
        params: dict[str, Any] = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """Get the login status or page."""
        params: dict[str, Any] = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """Log out from the Chaptarr instance."""
        params: dict[str, Any] = {}
        return self.request("GET", "/logout", params=params, data=None)

    def get_author(self) -> Any:
        """Get all authors managed by Chaptarr."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/author", params=params, data=None)

    def post_author(self, data: dict) -> Any:
        """Add a new author."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/author", params=params, data=data)

    def put_author_id(self, id: str, data: dict, moveFiles: bool | None = None) -> Any:
        """Update an existing author by ID."""
        params: dict[str, Any] = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v1/author/{id}", params=params, data=data)

    def delete_author_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportListExclusion: bool | None = None,
    ) -> Any:
        """Delete an author by ID."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/author/{id}", params=params, data=None)

    def get_author_id(self, id: int) -> Any:
        """Get specific author."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/author/{id}", params=params, data=None)

    def put_author_editor(self, data: dict) -> Any:
        """Update author editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/author/editor", params=params, data=data)

    def delete_author_editor(self, data: dict) -> Any:
        """Delete author editor."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v1/author/editor", params=params, data=data)

    def get_author_lookup(self, term: str | None = None) -> Any:
        """Get author lookup."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/author/lookup", params=params, data=None)

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

    def get_book(
        self,
        authorId: int | None = None,
        bookIds: list | None = None,
        titleSlug: str | None = None,
        includeAllAuthorBooks: bool | None = None,
    ) -> Any:
        """Get book."""
        params: dict[str, Any] = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookIds is not None:
            params["bookIds"] = bookIds
        if titleSlug is not None:
            params["titleSlug"] = titleSlug
        if includeAllAuthorBooks is not None:
            params["includeAllAuthorBooks"] = includeAllAuthorBooks
        return self.request("GET", "/api/v1/book", params=params, data=None)

    def post_book(self, data: dict) -> Any:
        """Add a new book."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/book", params=params, data=data)

    def get_book_id_overview(self, id: int) -> Any:
        """Get specific book overview."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/book/{id}/overview", params=params, data=None
        )

    def put_book_id(self, id: str, data: dict) -> Any:
        """Update book id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/book/{id}", params=params, data=data)

    def delete_book_id(
        self,
        id: int,
        deleteFiles: bool | None = None,
        addImportListExclusion: bool | None = None,
    ) -> Any:
        """Delete book id."""
        params: dict[str, Any] = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/book/{id}", params=params, data=None)

    def get_book_id(self, id: int) -> Any:
        """Get specific book."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/book/{id}", params=params, data=None)

    def put_book_monitor(self, data: dict) -> Any:
        """Update book monitor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/book/monitor", params=params, data=data)

    def put_book_editor(self, data: dict) -> Any:
        """Update book editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/book/editor", params=params, data=data)

    def delete_book_editor(self, data: dict) -> Any:
        """Delete book editor."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v1/book/editor", params=params, data=data)

    def get_bookfile(
        self,
        authorId: int | None = None,
        bookFileIds: list | None = None,
        bookId: list | None = None,
        unmapped: bool | None = None,
    ) -> Any:
        """Get bookfile."""
        params: dict[str, Any] = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookFileIds is not None:
            params["bookFileIds"] = bookFileIds
        if bookId is not None:
            params["bookId"] = bookId
        if unmapped is not None:
            params["unmapped"] = unmapped
        return self.request("GET", "/api/v1/bookfile", params=params, data=None)

    def put_bookfile_id(self, id: str, data: dict) -> Any:
        """Update bookfile id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/bookfile/{id}", params=params, data=data)

    def delete_bookfile_id(self, id: int) -> Any:
        """Delete bookfile id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/bookfile/{id}", params=params, data=None
        )

    def get_bookfile_id(self, id: int) -> Any:
        """Get specific bookfile."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/bookfile/{id}", params=params, data=None)

    def put_bookfile_editor(self, data: dict) -> Any:
        """Update bookfile editor."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/bookfile/editor", params=params, data=data)

    def delete_bookfile_bulk(self, data: dict) -> Any:
        """Delete bookfile bulk."""
        params: dict[str, Any] = {}
        return self.request("DELETE", "/api/v1/bookfile/bulk", params=params, data=data)

    def get_book_lookup(self, term: str | None = None) -> Any:
        """Get book lookup."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/book/lookup", params=params, data=None)

    def post_bookshelf(self, data: dict) -> Any:
        """Add a new bookshelf."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/bookshelf", params=params, data=data)

    def get_calendar(
        self,
        start: str | None = None,
        end: str | None = None,
        unmonitored: bool | None = None,
        includeAuthor: bool | None = None,
    ) -> Any:
        """Get calendar."""
        params: dict[str, Any] = {}
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
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/calendar/{id}", params=params, data=None)

    def get_feed_v1_calendar_readarrics(
        self,
        pastDays: int | None = None,
        futureDays: int | None = None,
        tagList: str | None = None,
        unmonitored: bool | None = None,
    ) -> Any:
        """Get feed v1 calendar readarrics."""
        params: dict[str, Any] = {}
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

    def post_command(self, data: dict) -> Any:
        """Add a new command."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/command", params=params, data=data)

    def get_command(self) -> Any:
        """Get command."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/command", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """Delete command id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/command/{id}", params=params, data=None)

    def get_command_id(self, id: int) -> Any:
        """Get specific command."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/command/{id}", params=params, data=None)

    def get_customfilter(self) -> Any:
        """Get customfilter."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/customfilter", params=params, data=None)

    def post_customfilter(self, data: dict) -> Any:
        """Add a new customfilter."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/customfilter", params=params, data=data)

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

    def get_customfilter_id(self, id: int) -> Any:
        """Get specific customfilter."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def post_customformat(self, data: dict) -> Any:
        """Add a new customformat."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/customformat", params=params, data=data)

    def get_customformat(self) -> Any:
        """Get customformat."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/customformat", params=params, data=None)

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

    def get_customformat_id(self, id: int) -> Any:
        """Get specific customformat."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/customformat/{id}", params=params, data=None
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
        includeAuthor: bool | None = None,
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
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
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

    def get_config_development(self) -> Any:
        """Get config development."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/development", params=params, data=None
        )

    def put_config_development_id(self, id: str, data: dict) -> Any:
        """Update config development id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/development/{id}", params=params, data=data
        )

    def get_config_development_id(self, id: int) -> Any:
        """Get specific config development."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/development/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """Get diskspace."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/diskspace", params=params, data=None)

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

    def put_downloadclient_id(
        self, id: str, data: dict, forceSave: bool | None = None
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

    def get_downloadclient_id(self, id: int) -> Any:
        """Get specific downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

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

    def get_config_downloadclient(self) -> Any:
        """Get config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/downloadclient", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: dict) -> Any:
        """Update config downloadclient id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """Get specific config downloadclient."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/downloadclient/{id}", params=params, data=None
        )

    def get_edition(self, bookId: list | None = None) -> Any:
        """Get edition."""
        params: dict[str, Any] = {}
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/edition", params=params, data=None)

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
        includeAuthor: bool | None = None,
        includeBook: bool | None = None,
        eventType: list | None = None,
        bookId: int | None = None,
        downloadId: str | None = None,
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
        date: str | None = None,
        eventType: str | None = None,
        includeAuthor: bool | None = None,
        includeBook: bool | None = None,
    ) -> Any:
        """Get history since."""
        params: dict[str, Any] = {}
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
        authorId: int | None = None,
        bookId: int | None = None,
        eventType: str | None = None,
        includeAuthor: bool | None = None,
        includeBook: bool | None = None,
    ) -> Any:
        """Get history author."""
        params: dict[str, Any] = {}
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
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/history/failed/{id}", params=params, data=None
        )

    def get_config_host(self) -> Any:
        """Get config host."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/host", params=params, data=None)

    def put_config_host_id(self, id: str, data: dict) -> Any:
        """Update config host id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/host/{id}", params=params, data=data
        )

    def get_config_host_id(self, id: int) -> Any:
        """Get specific config host."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/host/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """Get importlist."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/importlist", params=params, data=None)

    def post_importlist(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new importlist."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/importlist", params=params, data=data)

    def put_importlist_id(
        self, id: str, data: dict, forceSave: bool | None = None
    ) -> Any:
        """Update importlist id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """Delete importlist id."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", f"/api/v1/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """Get specific importlist."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/importlist/{id}", params=params, data=None)

    def put_importlist_bulk(self, data: dict) -> Any:
        """Update importlist bulk."""
        params: dict[str, Any] = {}
        return self.request("PUT", "/api/v1/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: dict) -> Any:
        """Delete importlist bulk."""
        params: dict[str, Any] = {}
        return self.request(
            "DELETE", "/api/v1/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """Get importlist schema."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: dict, forceTest: bool | None = None) -> Any:
        """Test importlist."""
        params: dict[str, Any] = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """Add a new importlist testall."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", "/api/v1/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: dict) -> Any:
        """Add a new importlist action name."""
        params: dict[str, Any] = {}
        return self.request(
            "POST", f"/api/v1/importlist/action/{name}", params=params, data=data
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

    def get_importlistexclusion_id(self, id: int) -> Any:
        """Get specific importlistexclusion."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def get_indexer(self) -> Any:
        """Get indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/indexer", params=params, data=None)

    def post_indexer(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new indexer."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/indexer", params=params, data=data)

    def put_indexer_id(self, id: str, data: dict, forceSave: bool | None = None) -> Any:
        """Update indexer id."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """Delete indexer id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/indexer/{id}", params=params, data=None)

    def get_indexer_id(self, id: int) -> Any:
        """Get specific indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/indexer/{id}", params=params, data=None)

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

    def get_config_indexer(self) -> Any:
        """Get config indexer."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/indexer", params=params, data=None)

    def put_config_indexer_id(self, id: str, data: dict) -> Any:
        """Update config indexer id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """Get specific config indexer."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/indexer/{id}", params=params, data=None
        )

    def get_indexerflag(self) -> Any:
        """Get indexerflag."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/indexerflag", params=params, data=None)

    def get_language(self) -> Any:
        """Get language."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/language", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """Get specific language."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/language/{id}", params=params, data=None)

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
        authorId: int | None = None,
        filterExistingFiles: bool | None = None,
        replaceExistingFiles: bool | None = None,
    ) -> Any:
        """Get manualimport."""
        params: dict[str, Any] = {}
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
        params: dict[str, Any] = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/author/{authorId}/{filename}",
            params=params,
            data=None,
        )

    def get_mediacover_book_book_id_filename(self, bookId: int, filename: str) -> Any:
        """Get specific mediacover book book filename."""
        params: dict[str, Any] = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/book/{bookId}/{filename}",
            params=params,
            data=None,
        )

    def get_config_mediamanagement(self) -> Any:
        """Get config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/mediamanagement", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: dict) -> Any:
        """Update config mediamanagement id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """Get specific config mediamanagement."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/mediamanagement/{id}", params=params, data=None
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

    def put_metadata_id(
        self, id: str, data: dict, forceSave: bool | None = None
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

    def get_metadata_id(self, id: int) -> Any:
        """Get specific metadata."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/metadata/{id}", params=params, data=None)

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

    def get_config_metadataprovider(self) -> Any:
        """Get config metadataprovider."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", "/api/v1/config/metadataprovider", params=params, data=None
        )

    def put_config_metadataprovider_id(self, id: str, data: dict) -> Any:
        """Update config metadataprovider id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/metadataprovider/{id}", params=params, data=data
        )

    def get_config_metadataprovider_id(self, id: int) -> Any:
        """Get specific config metadataprovider."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/metadataprovider/{id}", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int | None = None,
        pageSize: int | None = None,
        sortKey: str | None = None,
        sortDirection: str | None = None,
        includeAuthor: bool | None = None,
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
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/missing", params=params, data=None)

    def get_wanted_missing_id(self, id: int) -> Any:
        """Get specific wanted missing."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/wanted/missing/{id}", params=params, data=None
        )

    def get_config_naming(self) -> Any:
        """Get config naming."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/config/naming", params=params, data=None)

    def put_config_naming_id(self, id: str, data: dict) -> Any:
        """Update config naming id."""
        params: dict[str, Any] = {}
        return self.request(
            "PUT", f"/api/v1/config/naming/{id}", params=params, data=data
        )

    def get_config_naming_id(self, id: int) -> Any:
        """Get specific config naming."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/config/naming/{id}", params=params, data=None
        )

    def get_config_naming_examples(
        self,
        renameBooks: bool | None = None,
        replaceIllegalCharacters: bool | None = None,
        colonReplacementFormat: int | None = None,
        standardBookFormat: str | None = None,
        authorFolderFormat: str | None = None,
        includeAuthorName: bool | None = None,
        includeBookTitle: bool | None = None,
        includeQuality: bool | None = None,
        replaceSpaces: bool | None = None,
        separator: str | None = None,
        numberStyle: str | None = None,
        id: int | None = None,
        resourceName: str | None = None,
    ) -> Any:
        """Get config naming examples."""
        params: dict[str, Any] = {}
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
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/notification", params=params, data=None)

    def post_notification(self, data: dict, forceSave: bool | None = None) -> Any:
        """Add a new notification."""
        params: dict[str, Any] = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/notification", params=params, data=data)

    def put_notification_id(
        self, id: str, data: dict, forceSave: bool | None = None
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

    def get_notification_id(self, id: int) -> Any:
        """Get specific notification."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/notification/{id}", params=params, data=None
        )

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
        includeUnknownAuthorItems: bool | None = None,
        includeAuthor: bool | None = None,
        includeBook: bool | None = None,
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
        if includeUnknownAuthorItems is not None:
            params["includeUnknownAuthorItems"] = includeUnknownAuthorItems
        if includeAuthor is not None:
            params["includeAuthor"] = includeAuthor
        if includeBook is not None:
            params["includeBook"] = includeBook
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
        authorId: int | None = None,
        bookIds: list | None = None,
        includeAuthor: bool | None = None,
        includeBook: bool | None = None,
    ) -> Any:
        """Get queue details."""
        params: dict[str, Any] = {}
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
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/queue/status", params=params, data=None)

    def post_release(self, data: dict) -> Any:
        """Add a new release."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/release", params=params, data=data)

    def get_release(
        self, bookId: int | None = None, authorId: int | None = None
    ) -> Any:
        """Get release."""
        params: dict[str, Any] = {}
        if bookId is not None:
            params["bookId"] = bookId
        if authorId is not None:
            params["authorId"] = authorId
        return self.request("GET", "/api/v1/release", params=params, data=None)

    def get_releaseprofile(self) -> Any:
        """Get releaseprofile."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/releaseprofile", params=params, data=None)

    def post_releaseprofile(self, data: dict) -> Any:
        """Add a new releaseprofile."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/releaseprofile", params=params, data=data)

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

    def get_releaseprofile_id(self, id: int) -> Any:
        """Get specific releaseprofile."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def post_release_push(self, data: dict) -> Any:
        """Add a new release push."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/release/push", params=params, data=data)

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

    def get_remotepathmapping_id(self, id: int) -> Any:
        """Get specific remotepathmapping."""
        params: dict[str, Any] = {}
        return self.request(
            "GET", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def get_rename(self, authorId: int | None = None, bookId: int | None = None) -> Any:
        """Get rename."""
        params: dict[str, Any] = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/rename", params=params, data=None)

    def get_retag(self, authorId: int | None = None, bookId: int | None = None) -> Any:
        """Get retag."""
        params: dict[str, Any] = {}
        if authorId is not None:
            params["authorId"] = authorId
        if bookId is not None:
            params["bookId"] = bookId
        return self.request("GET", "/api/v1/retag", params=params, data=None)

    def post_rootfolder(self, data: dict) -> Any:
        """Add a new rootfolder."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """Get rootfolder."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/rootfolder", params=params, data=None)

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

    def get_rootfolder_id(self, id: int) -> Any:
        """Get specific rootfolder."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/rootfolder/{id}", params=params, data=None)

    def get_search(self, term: str | None = None) -> Any:
        """Get search."""
        params: dict[str, Any] = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/search", params=params, data=None)

    def get_series(self, authorId: int | None = None) -> Any:
        """Get series."""
        params: dict[str, Any] = {}
        if authorId is not None:
            params["authorId"] = authorId
        return self.request("GET", "/api/v1/series", params=params, data=None)

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

    def get_tag(self) -> Any:
        """Get tag."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/tag", params=params, data=None)

    def post_tag(self, data: dict) -> Any:
        """Add a new tag."""
        params: dict[str, Any] = {}
        return self.request("POST", "/api/v1/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: dict) -> Any:
        """Update tag id."""
        params: dict[str, Any] = {}
        return self.request("PUT", f"/api/v1/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """Delete tag id."""
        params: dict[str, Any] = {}
        return self.request("DELETE", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """Get specific tag."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """Get tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", "/api/v1/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """Get specific tag detail."""
        params: dict[str, Any] = {}
        return self.request("GET", f"/api/v1/tag/detail/{id}", params=params, data=None)

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
