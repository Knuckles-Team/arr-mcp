#!/usr/bin/env python
# coding: utf-8

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib3


class Api:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        verify: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if token:
            # Some arr apps accept key in header X-Api-Key
            self._session.headers.update({"X-Api-Key": token})
            # Also support query param in requests if needed, but header is cleaner

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

    def get_alttitle(self, movieId: int = None, movieMetadataId: int = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieMetadataId is not None:
            params["movieMetadataId"] = movieMetadataId
        return self.request("GET", "/api/v3/alttitle", params=params, data=None)

    def get_alttitle_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/alttitle/{id}", params=params, data=None)

    def get_api(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api", params=params, data=None)

    def post_login(self, returnUrl: str = None) -> Any:
        """No description"""
        params = {}
        if returnUrl is not None:
            params["returnUrl"] = returnUrl
        return self.request("POST", "/login", params=params, data=None)

    def get_login(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/login", params=params, data=None)

    def get_logout(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/logout", params=params, data=None)

    def post_autotagging(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/autotagging", params=params, data=None)

    def put_autotagging_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/autotagging/{id}", params=params, data=None
        )

    def get_autotagging_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """No description"""
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
        movieIds: List = None,
        protocols: List = None,
    ) -> Any:
        """No description"""
        params = {}
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

    def get_blocklist_movie(self, movieId: int = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/blocklist/movie", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/blocklist/bulk", params=params, data=data
        )

    def get_calendar(
        self,
        start: str = None,
        end: str = None,
        unmonitored: bool = None,
        tags: str = None,
    ) -> Any:
        """No description"""
        params = {}
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
        pastDays: int = None,
        futureDays: int = None,
        tags: str = None,
        unmonitored: bool = None,
        releaseTypes: List = None,
    ) -> Any:
        """No description"""
        params = {}
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

    def get_collection(self, tmdbId: int = None) -> Any:
        """No description"""
        params = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        return self.request("GET", "/api/v3/collection", params=params, data=None)

    def put_collection(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/collection", params=params, data=data)

    def put_collection_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v3/collection/{id}", params=params, data=data)

    def get_collection_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/collection/{id}", params=params, data=None)

    def post_command(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/command", params=params, data=data)

    def get_command(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/command", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v3/command/{id}", params=params, data=None)

    def get_command_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/command/{id}", params=params, data=None)

    def get_credit(self, movieId: int = None, movieMetadataId: int = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieMetadataId is not None:
            params["movieMetadataId"] = movieMetadataId
        return self.request("GET", "/api/v3/credit", params=params, data=None)

    def get_credit_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/credit/{id}", params=params, data=None)

    def get_customfilter(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/customfilter", params=params, data=None)

    def post_customfilter(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/customfilter", params=params, data=data)

    def put_customfilter_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customfilter_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/customfilter/{id}", params=params, data=None
        )

    def get_customformat(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/customformat", params=params, data=None)

    def post_customformat(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/customformat", params=params, data=data)

    def put_customformat_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def get_customformat_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/customformat/{id}", params=params, data=None
        )

    def put_customformat_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v3/customformat/bulk", params=params, data=data
        )

    def delete_customformat_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/customformat/bulk", params=params, data=data
        )

    def get_customformat_schema(self) -> Any:
        """No description"""
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
        monitored: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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

    def post_delayprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, after: int = None) -> Any:
        """No description"""
        params = {}
        if after is not None:
            params["after"] = after
        return self.request(
            "PUT", f"/api/v3/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/diskspace", params=params, data=None)

    def get_downloadclient(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/downloadclient", params=params, data=data)

    def put_downloadclient_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/config/downloadclient", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/downloadclient/{id}", params=params, data=None
        )

    def get_extrafile(self, movieId: int = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/extrafile", params=params, data=None)

    def get_filesystem(
        self,
        path: str = None,
        includeFiles: bool = None,
        allowFoldersWithoutTrailingSlashes: bool = None,
    ) -> Any:
        """No description"""
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
        """No description"""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v3/filesystem/type", params=params, data=None)

    def get_filesystem_mediafiles(self, path: str = None) -> Any:
        """No description"""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v3/filesystem/mediafiles", params=params, data=None
        )

    def get_health(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/health", params=params, data=None)

    def get_history(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeMovie: bool = None,
        eventType: List = None,
        downloadId: str = None,
        movieIds: List = None,
        languages: List = None,
        quality: List = None,
    ) -> Any:
        """No description"""
        params = {}
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
        self, date: str = None, eventType: str = None, includeMovie: bool = None
    ) -> Any:
        """No description"""
        params = {}
        if date is not None:
            params["date"] = date
        if eventType is not None:
            params["eventType"] = eventType
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/history/since", params=params, data=None)

    def get_history_movie(
        self, movieId: int = None, eventType: str = None, includeMovie: bool = None
    ) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        if eventType is not None:
            params["eventType"] = eventType
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/history/movie", params=params, data=None)

    def post_history_failed_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/history/failed/{id}", params=params, data=None
        )

    def get_config_host(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/config/host", params=params, data=None)

    def put_config_host_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/host/{id}", params=params, data=data
        )

    def get_config_host_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/host/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/importlist", params=params, data=None)

    def post_importlist(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/importlist", params=params, data=data)

    def put_importlist_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/importlist/{id}", params=params, data=None
        )

    def get_importlist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/importlist/{id}", params=params, data=None)

    def put_importlist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/importlist/action/{name}", params=params, data=data
        )

    def get_config_importlist(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/config/importlist", params=params, data=None
        )

    def put_config_importlist_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/importlist/{id}", params=params, data=data
        )

    def get_config_importlist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/importlist/{id}", params=params, data=None
        )

    def get_exclusions(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/exclusions", params=params, data=None)

    def post_exclusions(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/exclusions", params=params, data=data)

    def get_exclusions_paged(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
    ) -> Any:
        """No description"""
        params = {}
        if page is not None:
            params["page"] = page
        if pageSize is not None:
            params["pageSize"] = pageSize
        if sortKey is not None:
            params["sortKey"] = sortKey
        if sortDirection is not None:
            params["sortDirection"] = sortDirection
        return self.request("GET", "/api/v3/exclusions/paged", params=params, data=None)

    def put_exclusions_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v3/exclusions/{id}", params=params, data=data)

    def delete_exclusions_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/exclusions/{id}", params=params, data=None
        )

    def get_exclusions_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/exclusions/{id}", params=params, data=None)

    def post_exclusions_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/exclusions/bulk", params=params, data=data)

    def delete_exclusions_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/exclusions/bulk", params=params, data=data
        )

    def get_importlist_movie(
        self,
        includeRecommendations: bool = None,
        includeTrending: bool = None,
        includePopular: bool = None,
    ) -> Any:
        """No description"""
        params = {}
        if includeRecommendations is not None:
            params["includeRecommendations"] = includeRecommendations
        if includeTrending is not None:
            params["includeTrending"] = includeTrending
        if includePopular is not None:
            params["includePopular"] = includePopular
        return self.request("GET", "/api/v3/importlist/movie", params=params, data=None)

    def post_importlist_movie(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/importlist/movie", params=params, data=data
        )

    def get_indexer(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/indexer", params=params, data=None)

    def post_indexer(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/indexer", params=params, data=data)

    def put_indexer_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v3/indexer/{id}", params=params, data=None)

    def get_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/indexer/{id}", params=params, data=None)

    def put_indexer_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", "/api/v3/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/indexer/action/{name}", params=params, data=data
        )

    def get_config_indexer(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/config/indexer", params=params, data=None)

    def put_config_indexer_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/indexer/{id}", params=params, data=None
        )

    def get_indexerflag(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/indexerflag", params=params, data=None)

    def get_language(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/language", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/language/{id}", params=params, data=None)

    def get_localization(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/localization", params=params, data=None)

    def get_localization_language(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/localization/language", params=params, data=None
        )

    def get_log(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        level: str = None,
    ) -> Any:
        """No description"""
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
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/log/file/{filename}", params=params, data=None
        )

    def get_manualimport(
        self,
        folder: str = None,
        downloadId: str = None,
        movieId: int = None,
        filterExistingFiles: bool = None,
    ) -> Any:
        """No description"""
        params = {}
        if folder is not None:
            params["folder"] = folder
        if downloadId is not None:
            params["downloadId"] = downloadId
        if movieId is not None:
            params["movieId"] = movieId
        if filterExistingFiles is not None:
            params["filterExistingFiles"] = filterExistingFiles
        return self.request("GET", "/api/v3/manualimport", params=params, data=None)

    def post_manualimport(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/manualimport", params=params, data=data)

    def get_mediacover_movie_id_filename(self, movieId: int, filename: str) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/mediacover/{movieId}/{filename}", params=params, data=None
        )

    def get_config_mediamanagement(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/config/mediamanagement", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/mediamanagement/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/metadata", params=params, data=None)

    def post_metadata(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/metadata", params=params, data=data)

    def put_metadata_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v3/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/metadata/{id}", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/metadata/{id}", params=params, data=None)

    def get_metadata_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v3/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/metadata/action/{name}", params=params, data=data
        )

    def get_config_metadata(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/config/metadata", params=params, data=None)

    def put_config_metadata_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/metadata/{id}", params=params, data=data
        )

    def get_config_metadata_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/metadata/{id}", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        monitored: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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
        tmdbId: int = None,
        excludeLocalCovers: bool = None,
        languageId: int = None,
    ) -> Any:
        """No description"""
        params = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        if excludeLocalCovers is not None:
            params["excludeLocalCovers"] = excludeLocalCovers
        if languageId is not None:
            params["languageId"] = languageId
        return self.request("GET", "/api/v3/movie", params=params, data=None)

    def post_movie(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/movie", params=params, data=data)

    def put_movie_id(self, id: str, data: Dict, moveFiles: bool = None) -> Any:
        """No description"""
        params = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v3/movie/{id}", params=params, data=data)

    def delete_movie_id(
        self, id: int, deleteFiles: bool = None, addImportExclusion: bool = None
    ) -> Any:
        """No description"""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportExclusion is not None:
            params["addImportExclusion"] = addImportExclusion
        return self.request("DELETE", f"/api/v3/movie/{id}", params=params, data=None)

    def get_movie_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/movie/{id}", params=params, data=None)

    def put_movie_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/movie/editor", params=params, data=data)

    def delete_movie_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", "/api/v3/movie/editor", params=params, data=data)

    def get_moviefile(self, movieId: List = None, movieFileIds: List = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        if movieFileIds is not None:
            params["movieFileIds"] = movieFileIds
        return self.request("GET", "/api/v3/moviefile", params=params, data=None)

    def put_moviefile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v3/moviefile/{id}", params=params, data=data)

    def delete_moviefile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/moviefile/{id}", params=params, data=None
        )

    def get_moviefile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/moviefile/{id}", params=params, data=None)

    def put_moviefile_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/moviefile/editor", params=params, data=data)

    def delete_moviefile_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v3/moviefile/bulk", params=params, data=data
        )

    def put_moviefile_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v3/moviefile/bulk", params=params, data=data)

    def get_movie_id_folder(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/movie/{id}/folder", params=params, data=None
        )

    def post_movie_import(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/movie/import", params=params, data=data)

    def get_movie_lookup_tmdb(self, tmdbId: int = None) -> Any:
        """No description"""
        params = {}
        if tmdbId is not None:
            params["tmdbId"] = tmdbId
        return self.request(
            "GET", "/api/v3/movie/lookup/tmdb", params=params, data=None
        )

    def get_movie_lookup_imdb(self, imdbId: str = None) -> Any:
        """No description"""
        params = {}
        if imdbId is not None:
            params["imdbId"] = imdbId
        return self.request(
            "GET", "/api/v3/movie/lookup/imdb", params=params, data=None
        )

    def get_movie_lookup(self, term: str = None) -> Any:
        """No description"""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v3/movie/lookup", params=params, data=None)

    def get_config_naming(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/config/naming", params=params, data=None)

    def put_config_naming_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/config/naming/{id}", params=params, data=data
        )

    def get_config_naming_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/config/naming/{id}", params=params, data=None
        )

    def get_config_naming_examples(
        self,
        renameMovies: bool = None,
        replaceIllegalCharacters: bool = None,
        colonReplacementFormat: str = None,
        standardMovieFormat: str = None,
        movieFolderFormat: str = None,
        id: int = None,
        resourceName: str = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/notification", params=params, data=None)

    def post_notification(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v3/notification", params=params, data=data)

    def put_notification_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v3/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/notification/{id}", params=params, data=None
        )

    def get_notification_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v3/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/notification/action/{name}", params=params, data=data
        )

    def get_parse(self, title: str = None) -> Any:
        """No description"""
        params = {}
        if title is not None:
            params["title"] = title
        return self.request("GET", "/api/v3/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v3/qualitydefinition/update", params=params, data=data
        )

    def get_qualitydefinition_limits(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/qualitydefinition/limits", params=params, data=None
        )

    def post_qualityprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """No description"""
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
        """No description"""
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
        """No description"""
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
        includeUnknownMovieItems: bool = None,
        includeMovie: bool = None,
        movieIds: List = None,
        protocol: str = None,
        languages: List = None,
        quality: List = None,
        status: List = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v3/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/queue/grab/bulk", params=params, data=data)

    def get_queue_details(self, movieId: int = None, includeMovie: bool = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        if includeMovie is not None:
            params["includeMovie"] = includeMovie
        return self.request("GET", "/api/v3/queue/details", params=params, data=None)

    def get_queue_status(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/queue/status", params=params, data=None)

    def post_release(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/release", params=params, data=data)

    def get_release(self, movieId: int = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/release", params=params, data=None)

    def post_releaseprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/releaseprofile", params=params, data=data)

    def get_releaseprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/releaseprofile", params=params, data=None)

    def delete_releaseprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def put_releaseprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/releaseprofile/{id}", params=params, data=data
        )

    def get_releaseprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/releaseprofile/{id}", params=params, data=None
        )

    def post_release_push(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/release/push", params=params, data=data)

    def post_remotepathmapping(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v3/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/remotepathmapping", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v3/remotepathmapping/{id}", params=params, data=data
        )

    def get_remotepathmapping_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/remotepathmapping/{id}", params=params, data=None
        )

    def get_rename(self, movieId: List = None) -> Any:
        """No description"""
        params = {}
        if movieId is not None:
            params["movieId"] = movieId
        return self.request("GET", "/api/v3/rename", params=params, data=None)

    def post_rootfolder(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/rootfolder", params=params, data=None)

    def delete_rootfolder_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v3/rootfolder/{id}", params=params, data=None
        )

    def get_rootfolder_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/rootfolder/{id}", params=params, data=None)

    def get_content_path(self, path: str) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/content/{path}", params=params, data=None)

    def get_(self, path: str) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/", params=params, data=None)

    def get_path(self, path: str) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/{path}", params=params, data=None)

    def get_system_status(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v3/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/system/restart", params=params, data=None)

    def get_tag(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/tag", params=params, data=None)

    def post_tag(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v3/tag", params=params, data=data)

    def put_tag_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v3/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/tag/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/tag/detail", params=params, data=None)

    def get_tag_detail_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/tag/detail/{id}", params=params, data=None)

    def get_system_task(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/system/task/{id}", params=params, data=None
        )

    def put_config_ui_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v3/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v3/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v3/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v3/log/file/update/{filename}", params=params, data=None
        )
