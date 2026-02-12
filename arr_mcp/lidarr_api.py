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
            self._session.headers.update({"X-Api-Key": token})

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

    def get_album(
        self,
        artistId: int = None,
        albumIds: List = None,
        foreignAlbumId: str = None,
        includeAllArtistAlbums: bool = None,
    ) -> Any:
        """No description"""
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumIds is not None:
            params["albumIds"] = albumIds
        if foreignAlbumId is not None:
            params["foreignAlbumId"] = foreignAlbumId
        if includeAllArtistAlbums is not None:
            params["includeAllArtistAlbums"] = includeAllArtistAlbums
        return self.request("GET", "/api/v1/album", params=params, data=None)

    def post_album(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/album", params=params, data=data)

    def put_album_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v1/album/{id}", params=params, data=data)

    def delete_album_id(
        self, id: int, deleteFiles: bool = None, addImportListExclusion: bool = None
    ) -> Any:
        """No description"""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/album/{id}", params=params, data=None)

    def get_album_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/album/{id}", params=params, data=None)

    def put_album_monitor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v1/album/monitor", params=params, data=data)

    def get_album_lookup(self, term: str = None) -> Any:
        """No description"""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/album/lookup", params=params, data=None)

    def post_albumstudio(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/albumstudio", params=params, data=data)

    def get_api(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api", params=params, data=None)

    def get_artist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/artist/{id}", params=params, data=None)

    def put_artist_id(self, id: str, data: Dict, moveFiles: bool = None) -> Any:
        """No description"""
        params = {}
        if moveFiles is not None:
            params["moveFiles"] = moveFiles
        return self.request("PUT", f"/api/v1/artist/{id}", params=params, data=data)

    def delete_artist_id(
        self, id: int, deleteFiles: bool = None, addImportListExclusion: bool = None
    ) -> Any:
        """No description"""
        params = {}
        if deleteFiles is not None:
            params["deleteFiles"] = deleteFiles
        if addImportListExclusion is not None:
            params["addImportListExclusion"] = addImportListExclusion
        return self.request("DELETE", f"/api/v1/artist/{id}", params=params, data=None)

    def get_artist(self, mbId: str = None) -> Any:
        """No description"""
        params = {}
        if mbId is not None:
            params["mbId"] = mbId
        return self.request("GET", "/api/v1/artist", params=params, data=None)

    def post_artist(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/artist", params=params, data=data)

    def put_artist_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v1/artist/editor", params=params, data=data)

    def delete_artist_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", "/api/v1/artist/editor", params=params, data=data)

    def get_artist_lookup(self, term: str = None) -> Any:
        """No description"""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/artist/lookup", params=params, data=None)

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

    def get_autotagging_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/autotagging/{id}", params=params, data=None
        )

    def put_autotagging_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/autotagging/{id}", params=params, data=data
        )

    def delete_autotagging_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/autotagging/{id}", params=params, data=None
        )

    def post_autotagging(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/autotagging", params=params, data=data)

    def get_autotagging(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/autotagging", params=params, data=None)

    def get_autotagging_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/autotagging/schema", params=params, data=None
        )

    def get_system_backup(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/system/backup", params=params, data=None)

    def delete_system_backup_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/system/backup/{id}", params=params, data=None
        )

    def post_system_backup_restore_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/system/backup/restore/{id}", params=params, data=None
        )

    def post_system_backup_restore_upload(self) -> Any:
        """No description"""
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
        return self.request("GET", "/api/v1/blocklist", params=params, data=None)

    def delete_blocklist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/blocklist/{id}", params=params, data=None
        )

    def delete_blocklist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v1/blocklist/bulk", params=params, data=data
        )

    def get_calendar(
        self,
        start: str = None,
        end: str = None,
        unmonitored: bool = None,
        includeArtist: bool = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if tags is not None:
            params["tags"] = tags
        return self.request("GET", "/api/v1/calendar", params=params, data=None)

    def get_calendar_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/calendar/{id}", params=params, data=None)

    def get_feed_v1_calendar_lidarrics(
        self,
        pastDays: int = None,
        futureDays: int = None,
        tags: str = None,
        unmonitored: bool = None,
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
        return self.request(
            "GET", "/feed/v1/calendar/lidarr.ics", params=params, data=None
        )

    def get_command_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/command/{id}", params=params, data=None)

    def delete_command_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v1/command/{id}", params=params, data=None)

    def post_command(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/command", params=params, data=data)

    def get_command(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/command", params=params, data=None)

    def get_customfilter_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def put_customfilter_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/customfilter/{id}", params=params, data=data
        )

    def delete_customfilter_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/customfilter/{id}", params=params, data=None
        )

    def get_customfilter(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/customfilter", params=params, data=None)

    def post_customfilter(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/customfilter", params=params, data=data)

    def get_customformat_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def put_customformat_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/customformat/{id}", params=params, data=data
        )

    def delete_customformat_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/customformat/{id}", params=params, data=None
        )

    def get_customformat(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/customformat", params=params, data=None)

    def post_customformat(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/customformat", params=params, data=data)

    def put_customformat_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v1/customformat/bulk", params=params, data=data
        )

    def delete_customformat_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v1/customformat/bulk", params=params, data=data
        )

    def get_customformat_schema(self) -> Any:
        """No description"""
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
        includeArtist: bool = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/cutoff", params=params, data=None)

    def get_wanted_cutoff_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/wanted/cutoff/{id}", params=params, data=None
        )

    def post_delayprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/delayprofile", params=params, data=data)

    def get_delayprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/delayprofile", params=params, data=None)

    def delete_delayprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/delayprofile/{id}", params=params, data=data
        )

    def get_delayprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/delayprofile/{id}", params=params, data=None
        )

    def put_delayprofile_reorder_id(self, id: int, afterId: int = None) -> Any:
        """No description"""
        params = {}
        if afterId is not None:
            params["afterId"] = afterId
        return self.request(
            "PUT", f"/api/v1/delayprofile/reorder/{id}", params=params, data=None
        )

    def get_diskspace(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/diskspace", params=params, data=None)

    def get_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def put_downloadclient_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/downloadclient/{id}", params=params, data=data
        )

    def delete_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/downloadclient/{id}", params=params, data=None
        )

    def get_downloadclient(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/downloadclient", params=params, data=None)

    def post_downloadclient(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/downloadclient", params=params, data=data)

    def put_downloadclient_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def delete_downloadclient_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v1/downloadclient/bulk", params=params, data=data
        )

    def get_downloadclient_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/downloadclient/schema", params=params, data=None
        )

    def post_downloadclient_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/downloadclient/test", params=params, data=data
        )

    def post_downloadclient_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/downloadclient/testall", params=params, data=None
        )

    def post_downloadclient_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/downloadclient/action/{name}", params=params, data=data
        )

    def get_config_downloadclient_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/downloadclient/{id}", params=params, data=None
        )

    def put_config_downloadclient_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/downloadclient/{id}", params=params, data=data
        )

    def get_config_downloadclient(self) -> Any:
        """No description"""
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
        return self.request("GET", "/api/v1/filesystem", params=params, data=None)

    def get_filesystem_type(self, path: str = None) -> Any:
        """No description"""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request("GET", "/api/v1/filesystem/type", params=params, data=None)

    def get_filesystem_mediafiles(self, path: str = None) -> Any:
        """No description"""
        params = {}
        if path is not None:
            params["path"] = path
        return self.request(
            "GET", "/api/v1/filesystem/mediafiles", params=params, data=None
        )

    def get_health(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/health", params=params, data=None)

    def get_history(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeArtist: bool = None,
        includeAlbum: bool = None,
        includeTrack: bool = None,
        eventType: List = None,
        albumId: int = None,
        downloadId: str = None,
        artistIds: List = None,
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
        date: str = None,
        eventType: str = None,
        includeArtist: bool = None,
        includeAlbum: bool = None,
        includeTrack: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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
        artistId: int = None,
        albumId: int = None,
        eventType: str = None,
        includeArtist: bool = None,
        includeAlbum: bool = None,
        includeTrack: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/history/failed/{id}", params=params, data=None
        )

    def get_config_host_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/host/{id}", params=params, data=None
        )

    def put_config_host_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/host/{id}", params=params, data=data
        )

    def get_config_host(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/config/host", params=params, data=None)

    def get_importlist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/importlist/{id}", params=params, data=None)

    def put_importlist_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/importlist/{id}", params=params, data=data)

    def delete_importlist_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/importlist/{id}", params=params, data=None
        )

    def get_importlist(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/importlist", params=params, data=None)

    def post_importlist(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/importlist", params=params, data=data)

    def put_importlist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v1/importlist/bulk", params=params, data=data)

    def delete_importlist_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v1/importlist/bulk", params=params, data=data
        )

    def get_importlist_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/importlist/schema", params=params, data=None
        )

    def post_importlist_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/importlist/test", params=params, data=data)

    def post_importlist_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/importlist/testall", params=params, data=None
        )

    def post_importlist_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/importlist/action/{name}", params=params, data=data
        )

    def get_importlistexclusion_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def put_importlistexclusion_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/importlistexclusion/{id}", params=params, data=data
        )

    def delete_importlistexclusion_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/importlistexclusion/{id}", params=params, data=None
        )

    def get_importlistexclusion(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/importlistexclusion", params=params, data=None
        )

    def post_importlistexclusion(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/importlistexclusion", params=params, data=data
        )

    def get_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/indexer/{id}", params=params, data=None)

    def put_indexer_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/indexer/{id}", params=params, data=data)

    def delete_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v1/indexer/{id}", params=params, data=None)

    def get_indexer(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/indexer", params=params, data=None)

    def post_indexer(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/indexer", params=params, data=data)

    def put_indexer_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v1/indexer/bulk", params=params, data=data)

    def delete_indexer_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", "/api/v1/indexer/bulk", params=params, data=data)

    def get_indexer_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/indexer/schema", params=params, data=None)

    def post_indexer_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/indexer/test", params=params, data=data)

    def post_indexer_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/indexer/testall", params=params, data=None)

    def post_indexer_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/indexer/action/{name}", params=params, data=data
        )

    def get_config_indexer_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/indexer/{id}", params=params, data=None
        )

    def put_config_indexer_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/indexer/{id}", params=params, data=data
        )

    def get_config_indexer(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/config/indexer", params=params, data=None)

    def get_indexerflag(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/indexerflag", params=params, data=None)

    def get_language_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/language/{id}", params=params, data=None)

    def get_language(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/language", params=params, data=None)

    def get_localization(self) -> Any:
        """No description"""
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
        return self.request("GET", "/api/v1/log", params=params, data=None)

    def get_log_file(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/log/file", params=params, data=None)

    def get_log_file_filename(self, filename: str) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/log/file/{filename}", params=params, data=None
        )

    def post_manualimport(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/manualimport", params=params, data=data)

    def get_manualimport(
        self,
        folder: str = None,
        downloadId: str = None,
        artistId: int = None,
        filterExistingFiles: bool = None,
        replaceExistingFiles: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/artist/{artistId}/{filename}",
            params=params,
            data=None,
        )

    def get_mediacover_album_album_id_filename(
        self, albumId: int, filename: str
    ) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET",
            f"/api/v1/mediacover/album/{albumId}/{filename}",
            params=params,
            data=None,
        )

    def get_config_mediamanagement_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/mediamanagement/{id}", params=params, data=None
        )

    def put_config_mediamanagement_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/mediamanagement/{id}", params=params, data=data
        )

    def get_config_mediamanagement(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/config/mediamanagement", params=params, data=None
        )

    def get_metadata_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/metadata/{id}", params=params, data=None)

    def put_metadata_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("PUT", f"/api/v1/metadata/{id}", params=params, data=data)

    def delete_metadata_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/metadata/{id}", params=params, data=None
        )

    def get_metadata(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/metadata", params=params, data=None)

    def post_metadata(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/metadata", params=params, data=data)

    def get_metadata_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/metadata/schema", params=params, data=None)

    def post_metadata_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request("POST", "/api/v1/metadata/test", params=params, data=data)

    def post_metadata_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/metadata/testall", params=params, data=None
        )

    def post_metadata_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/metadata/action/{name}", params=params, data=data
        )

    def post_metadataprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/metadataprofile", params=params, data=data)

    def get_metadataprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/metadataprofile", params=params, data=None)

    def delete_metadataprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def put_metadataprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/metadataprofile/{id}", params=params, data=data
        )

    def get_metadataprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/metadataprofile/{id}", params=params, data=None
        )

    def get_metadataprofile_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/metadataprofile/schema", params=params, data=None
        )

    def get_config_metadataprovider_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/metadataprovider/{id}", params=params, data=None
        )

    def put_config_metadataprovider_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/metadataprovider/{id}", params=params, data=data
        )

    def get_config_metadataprovider(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/config/metadataprovider", params=params, data=None
        )

    def get_wanted_missing(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeArtist: bool = None,
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
        if includeArtist is not None:
            params["includeArtist"] = includeArtist
        if monitored is not None:
            params["monitored"] = monitored
        return self.request("GET", "/api/v1/wanted/missing", params=params, data=None)

    def get_wanted_missing_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/wanted/missing/{id}", params=params, data=None
        )

    def get_config_naming_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/config/naming/{id}", params=params, data=None
        )

    def put_config_naming_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/config/naming/{id}", params=params, data=data
        )

    def get_config_naming(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/config/naming", params=params, data=None)

    def get_config_naming_examples(
        self,
        renameTracks: bool = None,
        replaceIllegalCharacters: bool = None,
        colonReplacementFormat: int = None,
        standardTrackFormat: str = None,
        multiDiscTrackFormat: str = None,
        artistFolderFormat: str = None,
        includeArtistName: bool = None,
        includeAlbumTitle: bool = None,
        includeQuality: bool = None,
        replaceSpaces: bool = None,
        separator: str = None,
        numberStyle: str = None,
        id: int = None,
        resourceName: str = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/notification/{id}", params=params, data=None
        )

    def put_notification_id(self, id: int, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request(
            "PUT", f"/api/v1/notification/{id}", params=params, data=data
        )

    def delete_notification_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/notification/{id}", params=params, data=None
        )

    def get_notification(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/notification", params=params, data=None)

    def post_notification(self, data: Dict, forceSave: bool = None) -> Any:
        """No description"""
        params = {}
        if forceSave is not None:
            params["forceSave"] = forceSave
        return self.request("POST", "/api/v1/notification", params=params, data=data)

    def get_notification_schema(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/notification/schema", params=params, data=None
        )

    def post_notification_test(self, data: Dict, forceTest: bool = None) -> Any:
        """No description"""
        params = {}
        if forceTest is not None:
            params["forceTest"] = forceTest
        return self.request(
            "POST", "/api/v1/notification/test", params=params, data=data
        )

    def post_notification_testall(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/notification/testall", params=params, data=None
        )

    def post_notification_action_name(self, name: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/notification/action/{name}", params=params, data=data
        )

    def get_parse(self, title: str = None) -> Any:
        """No description"""
        params = {}
        if title is not None:
            params["title"] = title
        return self.request("GET", "/api/v1/parse", params=params, data=None)

    def get_ping(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/ping", params=params, data=None)

    def put_qualitydefinition_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/qualitydefinition/{id}", params=params, data=data
        )

    def get_qualitydefinition_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/qualitydefinition/{id}", params=params, data=None
        )

    def get_qualitydefinition(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/qualitydefinition", params=params, data=None
        )

    def put_qualitydefinition_update(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", "/api/v1/qualitydefinition/update", params=params, data=data
        )

    def post_qualityprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/qualityprofile", params=params, data=data)

    def get_qualityprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/qualityprofile", params=params, data=None)

    def delete_qualityprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def put_qualityprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/qualityprofile/{id}", params=params, data=data
        )

    def get_qualityprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/qualityprofile/{id}", params=params, data=None
        )

    def get_qualityprofile_schema(self) -> Any:
        """No description"""
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
        return self.request("DELETE", f"/api/v1/queue/{id}", params=params, data=None)

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
        return self.request("DELETE", "/api/v1/queue/bulk", params=params, data=data)

    def get_queue(
        self,
        page: int = None,
        pageSize: int = None,
        sortKey: str = None,
        sortDirection: str = None,
        includeUnknownArtistItems: bool = None,
        includeArtist: bool = None,
        includeAlbum: bool = None,
        artistIds: List = None,
        protocol: str = None,
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
        """No description"""
        params = {}
        return self.request(
            "POST", f"/api/v1/queue/grab/{id}", params=params, data=None
        )

    def post_queue_grab_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/queue/grab/bulk", params=params, data=data)

    def get_queue_details(
        self,
        artistId: int = None,
        albumIds: List = None,
        includeArtist: bool = None,
        includeAlbum: bool = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/queue/status", params=params, data=None)

    def post_release(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/release", params=params, data=data)

    def get_release(self, albumId: int = None, artistId: int = None) -> Any:
        """No description"""
        params = {}
        if albumId is not None:
            params["albumId"] = albumId
        if artistId is not None:
            params["artistId"] = artistId
        return self.request("GET", "/api/v1/release", params=params, data=None)

    def get_releaseprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def put_releaseprofile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/releaseprofile/{id}", params=params, data=data
        )

    def delete_releaseprofile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/releaseprofile/{id}", params=params, data=None
        )

    def get_releaseprofile(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/releaseprofile", params=params, data=None)

    def post_releaseprofile(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/releaseprofile", params=params, data=data)

    def post_release_push(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/release/push", params=params, data=data)

    def get_remotepathmapping_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def delete_remotepathmapping_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/remotepathmapping/{id}", params=params, data=None
        )

    def put_remotepathmapping_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "PUT", f"/api/v1/remotepathmapping/{id}", params=params, data=data
        )

    def post_remotepathmapping(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "POST", "/api/v1/remotepathmapping", params=params, data=data
        )

    def get_remotepathmapping(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/remotepathmapping", params=params, data=None
        )

    def get_rename(self, artistId: int = None, albumId: int = None) -> Any:
        """No description"""
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        return self.request("GET", "/api/v1/rename", params=params, data=None)

    def get_retag(self, artistId: int = None, albumId: int = None) -> Any:
        """No description"""
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        return self.request("GET", "/api/v1/retag", params=params, data=None)

    def get_rootfolder_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/rootfolder/{id}", params=params, data=None)

    def put_rootfolder_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v1/rootfolder/{id}", params=params, data=data)

    def delete_rootfolder_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/rootfolder/{id}", params=params, data=None
        )

    def post_rootfolder(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/rootfolder", params=params, data=data)

    def get_rootfolder(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/rootfolder", params=params, data=None)

    def get_search(self, term: str = None) -> Any:
        """No description"""
        params = {}
        if term is not None:
            params["term"] = term
        return self.request("GET", "/api/v1/search", params=params, data=None)

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
        return self.request("GET", "/api/v1/system/status", params=params, data=None)

    def get_system_routes(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/system/routes", params=params, data=None)

    def get_system_routes_duplicate(self) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", "/api/v1/system/routes/duplicate", params=params, data=None
        )

    def post_system_shutdown(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/system/shutdown", params=params, data=None)

    def post_system_restart(self) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/system/restart", params=params, data=None)

    def get_tag_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/tag/{id}", params=params, data=None)

    def put_tag_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v1/tag/{id}", params=params, data=data)

    def delete_tag_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("DELETE", f"/api/v1/tag/{id}", params=params, data=None)

    def get_tag(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/tag", params=params, data=None)

    def post_tag(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("POST", "/api/v1/tag", params=params, data=data)

    def get_tag_detail_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/tag/detail/{id}", params=params, data=None)

    def get_tag_detail(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/tag/detail", params=params, data=None)

    def get_system_task(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/system/task", params=params, data=None)

    def get_system_task_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/system/task/{id}", params=params, data=None
        )

    def get_track(
        self,
        artistId: int = None,
        albumId: int = None,
        albumReleaseId: int = None,
        trackIds: List = None,
    ) -> Any:
        """No description"""
        params = {}
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
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/track/{id}", params=params, data=None)

    def get_trackfile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/trackfile/{id}", params=params, data=None)

    def put_trackfile_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v1/trackfile/{id}", params=params, data=data)

    def delete_trackfile_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", f"/api/v1/trackfile/{id}", params=params, data=None
        )

    def get_trackfile(
        self,
        artistId: int = None,
        trackFileIds: List = None,
        albumId: List = None,
        unmapped: bool = None,
    ) -> Any:
        """No description"""
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if trackFileIds is not None:
            params["trackFileIds"] = trackFileIds
        if albumId is not None:
            params["albumId"] = albumId
        if unmapped is not None:
            params["unmapped"] = unmapped
        return self.request("GET", "/api/v1/trackfile", params=params, data=None)

    def put_trackfile_editor(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", "/api/v1/trackfile/editor", params=params, data=data)

    def delete_trackfile_bulk(self, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request(
            "DELETE", "/api/v1/trackfile/bulk", params=params, data=data
        )

    def put_config_ui_id(self, id: str, data: Dict) -> Any:
        """No description"""
        params = {}
        return self.request("PUT", f"/api/v1/config/ui/{id}", params=params, data=data)

    def get_config_ui_id(self, id: int) -> Any:
        """No description"""
        params = {}
        return self.request("GET", f"/api/v1/config/ui/{id}", params=params, data=None)

    def get_config_ui(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/config/ui", params=params, data=None)

    def get_update(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/update", params=params, data=None)

    def get_log_file_update(self) -> Any:
        """No description"""
        params = {}
        return self.request("GET", "/api/v1/log/file/update", params=params, data=None)

    def get_log_file_update_filename(self, filename: str) -> Any:
        """No description"""
        params = {}
        return self.request(
            "GET", f"/api/v1/log/file/update/{filename}", params=params, data=None
        )
