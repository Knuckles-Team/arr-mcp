"""Seerr API client: one method per upstream operation.

Written by ``scripts/generate_api_client.py`` from the Seerr API description
(seerr-team_seerr-api.yml 1.0.0); every method is served as one typed MCP tool
(CONN-ARR-MCP-SUITE-R001).
"""

# ruff: noqa: E501

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field
from scion_sdk.tls.profile import ResolvedTLSProfile
from scion_sdk.tls.resolve import resolve_tls_profile

from arr_mcp.api._security import (
    build_client,
    decode_response,
    request_url,
    send_request,
    validate_base_url,
)


def _clean(values: dict[str, Any] | None) -> dict[str, Any] | None:
    if values is None:
        return None
    kept = {key: value for key, value in values.items() if value is not None}
    return kept or None


class Api:
    """API client for Seerr."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url, self._origin = validate_base_url(base_url)
        self.api_key = api_key
        self._tls_profile = tls_profile or resolve_tls_profile("seerr")
        self._session = build_client(self.base_url, self._tls_profile, api_key)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any = None,
        form: dict[str, Any] | None = None,
    ) -> Any:
        """Send one request; an error status or an HTML page raises."""
        url = request_url(self.base_url, self._origin, endpoint)
        response = send_request(
            self._session, method, url, _clean(params), data, form=_clean(form)
        )
        try:
            if response.status_code >= 400:
                raise RuntimeError(f"API error: HTTP {response.status_code}")
            if response.status_code == 204:
                return {"status": "success"}
            result = decode_response(response)
            if isinstance(result, list):
                return {"result": result}
            return result
        finally:
            response.close()

    def get_status(
        self,
        *,
        check_update_available: Annotated[
            bool | None,
            Field(
                description="If false, updateAvailable and commitsBehind will be omitted from the response. Defaults to the versionCheck setting."
            ),
        ] = None,
    ) -> Any:
        """Get Seerr status

        GET /api/v1/status
        """
        return self._request(
            "GET",
            "/api/v1/status",
            params={"checkUpdateAvailable": check_update_available},
        )

    def get_status_appdata(self) -> Any:
        """Get application data volume status

        GET /api/v1/status/appdata
        """
        return self._request("GET", "/api/v1/status/appdata")

    def get_settings_main(self) -> Any:
        """Get main settings

        GET /api/v1/settings/main
        """
        return self._request("GET", "/api/v1/settings/main")

    def post_settings_main(
        self,
        *,
        api_key: Annotated[str | None, Field(description="apiKey")] = None,
        app_language: Annotated[str | None, Field(description="appLanguage")] = None,
        application_title: Annotated[
            str | None, Field(description="applicationTitle")
        ] = None,
        application_url: Annotated[
            str | None, Field(description="applicationUrl")
        ] = None,
        hide_available: Annotated[
            bool | None, Field(description="hideAvailable")
        ] = None,
        hide_requested: Annotated[
            bool | None, Field(description="hideRequested")
        ] = None,
        partial_requests_enabled: Annotated[
            bool | None, Field(description="partialRequestsEnabled")
        ] = None,
        local_login: Annotated[bool | None, Field(description="localLogin")] = None,
        media_server_type: Annotated[
            float | None, Field(description="mediaServerType")
        ] = None,
        new_plex_login: Annotated[
            bool | None, Field(description="newPlexLogin")
        ] = None,
        default_permissions: Annotated[
            float | None, Field(description="defaultPermissions")
        ] = None,
        enable_special_episodes: Annotated[
            bool | None, Field(description="enableSpecialEpisodes")
        ] = None,
        version_check: Annotated[bool | None, Field(description="versionCheck")] = None,
    ) -> Any:
        """Update main settings

        POST /api/v1/settings/main
        """
        return self._request(
            "POST",
            "/api/v1/settings/main",
            data=_clean(
                {
                    "apiKey": api_key,
                    "appLanguage": app_language,
                    "applicationTitle": application_title,
                    "applicationUrl": application_url,
                    "hideAvailable": hide_available,
                    "hideRequested": hide_requested,
                    "partialRequestsEnabled": partial_requests_enabled,
                    "localLogin": local_login,
                    "mediaServerType": media_server_type,
                    "newPlexLogin": new_plex_login,
                    "defaultPermissions": default_permissions,
                    "enableSpecialEpisodes": enable_special_episodes,
                    "versionCheck": version_check,
                }
            ),
        )

    def get_settings_network(self) -> Any:
        """Get network settings

        GET /api/v1/settings/network
        """
        return self._request("GET", "/api/v1/settings/network")

    def post_settings_network(
        self,
        *,
        csrf_protection: Annotated[
            bool | None, Field(description="csrfProtection")
        ] = None,
        force_ipv4_first: Annotated[
            bool | None, Field(description="forceIpv4First")
        ] = None,
        trust_proxy: Annotated[bool | None, Field(description="trustProxy")] = None,
        proxy: Annotated[dict[str, Any] | None, Field(description="proxy")] = None,
        dns_cache: Annotated[
            dict[str, Any] | None, Field(description="dnsCache")
        ] = None,
    ) -> Any:
        """Update network settings

        POST /api/v1/settings/network
        """
        return self._request(
            "POST",
            "/api/v1/settings/network",
            data=_clean(
                {
                    "csrfProtection": csrf_protection,
                    "forceIpv4First": force_ipv4_first,
                    "trustProxy": trust_proxy,
                    "proxy": proxy,
                    "dnsCache": dns_cache,
                }
            ),
        )

    def post_settings_main_regenerate(self) -> Any:
        """Get main settings with newly-generated API key

        POST /api/v1/settings/main/regenerate
        """
        return self._request("POST", "/api/v1/settings/main/regenerate")

    def get_settings_jellyfin(self) -> Any:
        """Get Jellyfin settings

        GET /api/v1/settings/jellyfin
        """
        return self._request("GET", "/api/v1/settings/jellyfin")

    def post_settings_jellyfin(
        self,
        *,
        name: Annotated[str | None, Field(description="name")] = None,
        hostname: Annotated[str | None, Field(description="hostname")] = None,
        external_hostname: Annotated[
            str | None, Field(description="externalHostname")
        ] = None,
        jellyfin_forgot_password_url: Annotated[
            str | None, Field(description="jellyfinForgotPasswordUrl")
        ] = None,
        admin_user: Annotated[str | None, Field(description="adminUser")] = None,
        admin_pass: Annotated[str | None, Field(description="adminPass")] = None,
        libraries: Annotated[
            list[dict[str, Any]] | None, Field(description="libraries")
        ] = None,
        server_id: Annotated[str | None, Field(description="serverID")] = None,
    ) -> Any:
        """Update Jellyfin settings

        POST /api/v1/settings/jellyfin
        """
        return self._request(
            "POST",
            "/api/v1/settings/jellyfin",
            data=_clean(
                {
                    "name": name,
                    "hostname": hostname,
                    "externalHostname": external_hostname,
                    "jellyfinForgotPasswordUrl": jellyfin_forgot_password_url,
                    "adminUser": admin_user,
                    "adminPass": admin_pass,
                    "libraries": libraries,
                    "serverID": server_id,
                }
            ),
        )

    def get_settings_jellyfin_library(self) -> Any:
        """Get Jellyfin libraries

        GET /api/v1/settings/jellyfin/library
        """
        return self._request("GET", "/api/v1/settings/jellyfin/library")

    def put_settings_jellyfin_library_id(
        self,
        *,
        library_id: Annotated[str, Field(description="libraryId")],
        enabled: Annotated[bool, Field(description="enabled")],
    ) -> Any:
        """Update a single Jellyfin library

        PUT /api/v1/settings/jellyfin/library/{libraryId}
        """
        return self._request(
            "PUT",
            f"/api/v1/settings/jellyfin/library/{library_id}",
            data=_clean({"enabled": enabled}),
        )

    def post_settings_jellyfin_library_sync(self) -> Any:
        """Sync Jellyfin libraries

        POST /api/v1/settings/jellyfin/library/sync
        """
        return self._request("POST", "/api/v1/settings/jellyfin/library/sync")

    def get_settings_jellyfin_users(self) -> Any:
        """Get Jellyfin Users

        GET /api/v1/settings/jellyfin/users
        """
        return self._request("GET", "/api/v1/settings/jellyfin/users")

    def get_settings_jellyfin_sync(self) -> Any:
        """Get status of full Jellyfin library sync

        GET /api/v1/settings/jellyfin/sync
        """
        return self._request("GET", "/api/v1/settings/jellyfin/sync")

    def post_settings_jellyfin_sync(
        self,
        *,
        cancel: Annotated[bool | None, Field(description="cancel")] = None,
        start: Annotated[bool | None, Field(description="start")] = None,
    ) -> Any:
        """Start full Jellyfin library sync

        POST /api/v1/settings/jellyfin/sync
        """
        return self._request(
            "POST",
            "/api/v1/settings/jellyfin/sync",
            data=_clean({"cancel": cancel, "start": start}),
        )

    def get_settings_plex(self) -> Any:
        """Get Plex settings

        GET /api/v1/settings/plex
        """
        return self._request("GET", "/api/v1/settings/plex")

    def post_settings_plex(
        self,
        *,
        name: Annotated[str, Field(description="name")],
        machine_id: Annotated[str, Field(description="machineId")],
        ip: Annotated[str, Field(description="ip")],
        port: Annotated[float, Field(description="port")],
        use_ssl: Annotated[bool | None, Field(description="useSsl")] = None,
        libraries: Annotated[
            list[dict[str, Any]] | None, Field(description="libraries")
        ] = None,
        web_app_url: Annotated[str | None, Field(description="webAppUrl")] = None,
    ) -> Any:
        """Update Plex settings

        POST /api/v1/settings/plex
        """
        return self._request(
            "POST",
            "/api/v1/settings/plex",
            data=_clean(
                {
                    "name": name,
                    "machineId": machine_id,
                    "ip": ip,
                    "port": port,
                    "useSsl": use_ssl,
                    "libraries": libraries,
                    "webAppUrl": web_app_url,
                }
            ),
        )

    def get_settings_plex_library(self) -> Any:
        """Get Plex libraries

        GET /api/v1/settings/plex/library
        """
        return self._request("GET", "/api/v1/settings/plex/library")

    def put_settings_plex_library_id(
        self,
        *,
        library_id: Annotated[str, Field(description="libraryId")],
        enabled: Annotated[bool, Field(description="enabled")],
    ) -> Any:
        """Update a single Plex library

        PUT /api/v1/settings/plex/library/{libraryId}
        """
        return self._request(
            "PUT",
            f"/api/v1/settings/plex/library/{library_id}",
            data=_clean({"enabled": enabled}),
        )

    def post_settings_plex_library_sync(self) -> Any:
        """Sync Plex libraries

        POST /api/v1/settings/plex/library/sync
        """
        return self._request("POST", "/api/v1/settings/plex/library/sync")

    def get_settings_plex_sync(self) -> Any:
        """Get status of full Plex library scan

        GET /api/v1/settings/plex/sync
        """
        return self._request("GET", "/api/v1/settings/plex/sync")

    def post_settings_plex_sync(
        self,
        *,
        cancel: Annotated[bool | None, Field(description="cancel")] = None,
        start: Annotated[bool | None, Field(description="start")] = None,
    ) -> Any:
        """Start full Plex library scan

        POST /api/v1/settings/plex/sync
        """
        return self._request(
            "POST",
            "/api/v1/settings/plex/sync",
            data=_clean({"cancel": cancel, "start": start}),
        )

    def get_settings_plex_devices_servers(self) -> Any:
        """Gets the user's available Plex servers

        GET /api/v1/settings/plex/devices/servers
        """
        return self._request("GET", "/api/v1/settings/plex/devices/servers")

    def get_settings_plex_users(self) -> Any:
        """Get Plex users

        GET /api/v1/settings/plex/users
        """
        return self._request("GET", "/api/v1/settings/plex/users")

    def get_settings_metadatas(self) -> Any:
        """Get Metadata settings

        GET /api/v1/settings/metadatas
        """
        return self._request("GET", "/api/v1/settings/metadatas")

    def put_settings_metadatas(
        self,
        *,
        settings: Annotated[
            dict[str, Any] | None, Field(description="settings")
        ] = None,
    ) -> Any:
        """Update Metadata settings

        PUT /api/v1/settings/metadatas
        """
        return self._request(
            "PUT", "/api/v1/settings/metadatas", data=_clean({"settings": settings})
        )

    def post_settings_metadatas_test(
        self,
        *,
        tmdb: Annotated[bool | None, Field(description="tmdb")] = None,
        tvdb: Annotated[bool | None, Field(description="tvdb")] = None,
    ) -> Any:
        """Test Provider configuration

        POST /api/v1/settings/metadatas/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/metadatas/test",
            data=_clean({"tmdb": tmdb, "tvdb": tvdb}),
        )

    def get_settings_tautulli(self) -> Any:
        """Get Tautulli settings

        GET /api/v1/settings/tautulli
        """
        return self._request("GET", "/api/v1/settings/tautulli")

    def post_settings_tautulli(
        self,
        *,
        hostname: Annotated[str | None, Field(description="hostname")] = None,
        port: Annotated[float | None, Field(description="port")] = None,
        use_ssl: Annotated[bool | None, Field(description="useSsl")] = None,
        api_key: Annotated[str | None, Field(description="apiKey")] = None,
        external_url: Annotated[str | None, Field(description="externalUrl")] = None,
    ) -> Any:
        """Update Tautulli settings

        POST /api/v1/settings/tautulli
        """
        return self._request(
            "POST",
            "/api/v1/settings/tautulli",
            data=_clean(
                {
                    "hostname": hostname,
                    "port": port,
                    "useSsl": use_ssl,
                    "apiKey": api_key,
                    "externalUrl": external_url,
                }
            ),
        )

    def get_settings_radarr(self) -> Any:
        """Get Radarr settings

        GET /api/v1/settings/radarr
        """
        return self._request("GET", "/api/v1/settings/radarr")

    def post_settings_radarr(
        self,
        *,
        name: Annotated[str, Field(description="name")],
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        active_profile_id: Annotated[float, Field(description="activeProfileId")],
        active_profile_name: Annotated[str, Field(description="activeProfileName")],
        active_directory: Annotated[str, Field(description="activeDirectory")],
        is4k: Annotated[bool, Field(description="is4k")],
        minimum_availability: Annotated[str, Field(description="minimumAvailability")],
        is_default: Annotated[bool, Field(description="isDefault")],
        id: Annotated[float | None, Field(description="id")] = None,
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
        external_url: Annotated[str | None, Field(description="externalUrl")] = None,
        sync_enabled: Annotated[bool | None, Field(description="syncEnabled")] = None,
        prevent_search: Annotated[
            bool | None, Field(description="preventSearch")
        ] = None,
    ) -> Any:
        """Create Radarr instance

        POST /api/v1/settings/radarr
        """
        return self._request(
            "POST",
            "/api/v1/settings/radarr",
            data=_clean(
                {
                    "id": id,
                    "name": name,
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                    "activeProfileId": active_profile_id,
                    "activeProfileName": active_profile_name,
                    "activeDirectory": active_directory,
                    "is4k": is4k,
                    "minimumAvailability": minimum_availability,
                    "isDefault": is_default,
                    "externalUrl": external_url,
                    "syncEnabled": sync_enabled,
                    "preventSearch": prevent_search,
                }
            ),
        )

    def post_settings_radarr_test(
        self,
        *,
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
    ) -> Any:
        """Test Radarr configuration

        POST /api/v1/settings/radarr/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/radarr/test",
            data=_clean(
                {
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                }
            ),
        )

    def put_settings_radarr_id(
        self,
        *,
        radarr_id: Annotated[int, Field(description="Radarr instance ID")],
        name: Annotated[str, Field(description="name")],
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        active_profile_id: Annotated[float, Field(description="activeProfileId")],
        active_profile_name: Annotated[str, Field(description="activeProfileName")],
        active_directory: Annotated[str, Field(description="activeDirectory")],
        is4k: Annotated[bool, Field(description="is4k")],
        minimum_availability: Annotated[str, Field(description="minimumAvailability")],
        is_default: Annotated[bool, Field(description="isDefault")],
        id: Annotated[float | None, Field(description="id")] = None,
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
        external_url: Annotated[str | None, Field(description="externalUrl")] = None,
        sync_enabled: Annotated[bool | None, Field(description="syncEnabled")] = None,
        prevent_search: Annotated[
            bool | None, Field(description="preventSearch")
        ] = None,
    ) -> Any:
        """Update Radarr instance

        PUT /api/v1/settings/radarr/{radarrId}
        """
        return self._request(
            "PUT",
            f"/api/v1/settings/radarr/{radarr_id}",
            data=_clean(
                {
                    "id": id,
                    "name": name,
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                    "activeProfileId": active_profile_id,
                    "activeProfileName": active_profile_name,
                    "activeDirectory": active_directory,
                    "is4k": is4k,
                    "minimumAvailability": minimum_availability,
                    "isDefault": is_default,
                    "externalUrl": external_url,
                    "syncEnabled": sync_enabled,
                    "preventSearch": prevent_search,
                }
            ),
        )

    def delete_settings_radarr_id(
        self, *, radarr_id: Annotated[int, Field(description="Radarr instance ID")]
    ) -> Any:
        """Delete Radarr instance

        DELETE /api/v1/settings/radarr/{radarrId}
        """
        return self._request("DELETE", f"/api/v1/settings/radarr/{radarr_id}")

    def get_settings_radarr_id_profiles(
        self, *, radarr_id: Annotated[int, Field(description="Radarr instance ID")]
    ) -> Any:
        """Get available Radarr profiles

        GET /api/v1/settings/radarr/{radarrId}/profiles
        """
        return self._request("GET", f"/api/v1/settings/radarr/{radarr_id}/profiles")

    def get_settings_sonarr(self) -> Any:
        """Get Sonarr settings

        GET /api/v1/settings/sonarr
        """
        return self._request("GET", "/api/v1/settings/sonarr")

    def post_settings_sonarr(
        self,
        *,
        name: Annotated[str, Field(description="name")],
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        active_profile_id: Annotated[float, Field(description="activeProfileId")],
        active_profile_name: Annotated[str, Field(description="activeProfileName")],
        active_directory: Annotated[str, Field(description="activeDirectory")],
        is4k: Annotated[bool, Field(description="is4k")],
        enable_season_folders: Annotated[
            bool, Field(description="enableSeasonFolders")
        ],
        is_default: Annotated[bool, Field(description="isDefault")],
        id: Annotated[float | None, Field(description="id")] = None,
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
        active_language_profile_id: Annotated[
            float | None, Field(description="activeLanguageProfileId")
        ] = None,
        active_anime_profile_id: Annotated[
            float | None, Field(description="activeAnimeProfileId")
        ] = None,
        active_anime_language_profile_id: Annotated[
            float | None, Field(description="activeAnimeLanguageProfileId")
        ] = None,
        active_anime_profile_name: Annotated[
            str | None, Field(description="activeAnimeProfileName")
        ] = None,
        active_anime_directory: Annotated[
            str | None, Field(description="activeAnimeDirectory")
        ] = None,
        external_url: Annotated[str | None, Field(description="externalUrl")] = None,
        sync_enabled: Annotated[bool | None, Field(description="syncEnabled")] = None,
        prevent_search: Annotated[
            bool | None, Field(description="preventSearch")
        ] = None,
    ) -> Any:
        """Create Sonarr instance

        POST /api/v1/settings/sonarr
        """
        return self._request(
            "POST",
            "/api/v1/settings/sonarr",
            data=_clean(
                {
                    "id": id,
                    "name": name,
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                    "activeProfileId": active_profile_id,
                    "activeProfileName": active_profile_name,
                    "activeDirectory": active_directory,
                    "activeLanguageProfileId": active_language_profile_id,
                    "activeAnimeProfileId": active_anime_profile_id,
                    "activeAnimeLanguageProfileId": active_anime_language_profile_id,
                    "activeAnimeProfileName": active_anime_profile_name,
                    "activeAnimeDirectory": active_anime_directory,
                    "is4k": is4k,
                    "enableSeasonFolders": enable_season_folders,
                    "isDefault": is_default,
                    "externalUrl": external_url,
                    "syncEnabled": sync_enabled,
                    "preventSearch": prevent_search,
                }
            ),
        )

    def post_settings_sonarr_test(
        self,
        *,
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
    ) -> Any:
        """Test Sonarr configuration

        POST /api/v1/settings/sonarr/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/sonarr/test",
            data=_clean(
                {
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                }
            ),
        )

    def put_settings_sonarr_id(
        self,
        *,
        sonarr_id: Annotated[int, Field(description="Sonarr instance ID")],
        name: Annotated[str, Field(description="name")],
        hostname: Annotated[str, Field(description="hostname")],
        port: Annotated[float, Field(description="port")],
        api_key: Annotated[str, Field(description="apiKey")],
        use_ssl: Annotated[bool, Field(description="useSsl")],
        active_profile_id: Annotated[float, Field(description="activeProfileId")],
        active_profile_name: Annotated[str, Field(description="activeProfileName")],
        active_directory: Annotated[str, Field(description="activeDirectory")],
        is4k: Annotated[bool, Field(description="is4k")],
        enable_season_folders: Annotated[
            bool, Field(description="enableSeasonFolders")
        ],
        is_default: Annotated[bool, Field(description="isDefault")],
        id: Annotated[float | None, Field(description="id")] = None,
        base_url: Annotated[str | None, Field(description="baseUrl")] = None,
        active_language_profile_id: Annotated[
            float | None, Field(description="activeLanguageProfileId")
        ] = None,
        active_anime_profile_id: Annotated[
            float | None, Field(description="activeAnimeProfileId")
        ] = None,
        active_anime_language_profile_id: Annotated[
            float | None, Field(description="activeAnimeLanguageProfileId")
        ] = None,
        active_anime_profile_name: Annotated[
            str | None, Field(description="activeAnimeProfileName")
        ] = None,
        active_anime_directory: Annotated[
            str | None, Field(description="activeAnimeDirectory")
        ] = None,
        external_url: Annotated[str | None, Field(description="externalUrl")] = None,
        sync_enabled: Annotated[bool | None, Field(description="syncEnabled")] = None,
        prevent_search: Annotated[
            bool | None, Field(description="preventSearch")
        ] = None,
    ) -> Any:
        """Update Sonarr instance

        PUT /api/v1/settings/sonarr/{sonarrId}
        """
        return self._request(
            "PUT",
            f"/api/v1/settings/sonarr/{sonarr_id}",
            data=_clean(
                {
                    "id": id,
                    "name": name,
                    "hostname": hostname,
                    "port": port,
                    "apiKey": api_key,
                    "useSsl": use_ssl,
                    "baseUrl": base_url,
                    "activeProfileId": active_profile_id,
                    "activeProfileName": active_profile_name,
                    "activeDirectory": active_directory,
                    "activeLanguageProfileId": active_language_profile_id,
                    "activeAnimeProfileId": active_anime_profile_id,
                    "activeAnimeLanguageProfileId": active_anime_language_profile_id,
                    "activeAnimeProfileName": active_anime_profile_name,
                    "activeAnimeDirectory": active_anime_directory,
                    "is4k": is4k,
                    "enableSeasonFolders": enable_season_folders,
                    "isDefault": is_default,
                    "externalUrl": external_url,
                    "syncEnabled": sync_enabled,
                    "preventSearch": prevent_search,
                }
            ),
        )

    def delete_settings_sonarr_id(
        self, *, sonarr_id: Annotated[int, Field(description="Sonarr instance ID")]
    ) -> Any:
        """Delete Sonarr instance

        DELETE /api/v1/settings/sonarr/{sonarrId}
        """
        return self._request("DELETE", f"/api/v1/settings/sonarr/{sonarr_id}")

    def get_settings_public(self) -> Any:
        """Get public settings

        GET /api/v1/settings/public
        """
        return self._request("GET", "/api/v1/settings/public")

    def post_settings_initialize(self) -> Any:
        """Initialize application

        POST /api/v1/settings/initialize
        """
        return self._request("POST", "/api/v1/settings/initialize")

    def get_settings_jobs(self) -> Any:
        """Get scheduled jobs

        GET /api/v1/settings/jobs
        """
        return self._request("GET", "/api/v1/settings/jobs")

    def post_settings_jobs_job_id_run(
        self, *, job_id: Annotated[str, Field(description="jobId")]
    ) -> Any:
        """Invoke a specific job

        POST /api/v1/settings/jobs/{jobId}/run
        """
        return self._request("POST", f"/api/v1/settings/jobs/{job_id}/run")

    def post_settings_jobs_job_id_cancel(
        self, *, job_id: Annotated[str, Field(description="jobId")]
    ) -> Any:
        """Cancel a specific job

        POST /api/v1/settings/jobs/{jobId}/cancel
        """
        return self._request("POST", f"/api/v1/settings/jobs/{job_id}/cancel")

    def post_settings_jobs_job_id_schedule(
        self,
        *,
        job_id: Annotated[str, Field(description="jobId")],
        schedule: Annotated[str | None, Field(description="schedule")] = None,
    ) -> Any:
        """Modify job schedule

        POST /api/v1/settings/jobs/{jobId}/schedule
        """
        return self._request(
            "POST",
            f"/api/v1/settings/jobs/{job_id}/schedule",
            data=_clean({"schedule": schedule}),
        )

    def get_settings_cache(self) -> Any:
        """Get a list of active caches

        GET /api/v1/settings/cache
        """
        return self._request("GET", "/api/v1/settings/cache")

    def post_settings_cache_id_flush(
        self, *, cache_id: Annotated[str, Field(description="cacheId")]
    ) -> Any:
        """Flush a specific cache

        POST /api/v1/settings/cache/{cacheId}/flush
        """
        return self._request("POST", f"/api/v1/settings/cache/{cache_id}/flush")

    def post_settings_cache_dns_entry_flush(
        self, *, dns_entry: Annotated[str, Field(description="dnsEntry")]
    ) -> Any:
        """Flush a specific DNS cache entry

        POST /api/v1/settings/cache/dns/{dnsEntry}/flush
        """
        return self._request("POST", f"/api/v1/settings/cache/dns/{dns_entry}/flush")

    def get_settings_logs(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
        search: Annotated[str | None, Field(description="search")] = None,
    ) -> Any:
        """Returns logs

        GET /api/v1/settings/logs
        """
        return self._request(
            "GET",
            "/api/v1/settings/logs",
            params={"take": take, "skip": skip, "filter": filter, "search": search},
        )

    def get_settings_notifications_email(self) -> Any:
        """Get email notification settings

        GET /api/v1/settings/notifications/email
        """
        return self._request("GET", "/api/v1/settings/notifications/email")

    def post_settings_notifications_email(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update email notification settings

        POST /api/v1/settings/notifications/email
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/email",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_email_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test email settings

        POST /api/v1/settings/notifications/email/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/email/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_discord(self) -> Any:
        """Get Discord notification settings

        GET /api/v1/settings/notifications/discord
        """
        return self._request("GET", "/api/v1/settings/notifications/discord")

    def post_settings_notifications_discord(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Discord notification settings

        POST /api/v1/settings/notifications/discord
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/discord",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_discord_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Discord settings

        POST /api/v1/settings/notifications/discord/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/discord/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_pushbullet(self) -> Any:
        """Get Pushbullet notification settings

        GET /api/v1/settings/notifications/pushbullet
        """
        return self._request("GET", "/api/v1/settings/notifications/pushbullet")

    def post_settings_notifications_pushbullet(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Pushbullet notification settings

        POST /api/v1/settings/notifications/pushbullet
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/pushbullet",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_pushbullet_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Pushbullet settings

        POST /api/v1/settings/notifications/pushbullet/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/pushbullet/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_pushover(self) -> Any:
        """Get Pushover notification settings

        GET /api/v1/settings/notifications/pushover
        """
        return self._request("GET", "/api/v1/settings/notifications/pushover")

    def post_settings_notifications_pushover(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Pushover notification settings

        POST /api/v1/settings/notifications/pushover
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/pushover",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_pushover_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Pushover settings

        POST /api/v1/settings/notifications/pushover/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/pushover/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_pushover_sounds(
        self, *, token: Annotated[str, Field(description="token")]
    ) -> Any:
        """Get Pushover sounds

        GET /api/v1/settings/notifications/pushover/sounds
        """
        return self._request(
            "GET",
            "/api/v1/settings/notifications/pushover/sounds",
            params={"token": token},
        )

    def get_settings_notifications_gotify(self) -> Any:
        """Get Gotify notification settings

        GET /api/v1/settings/notifications/gotify
        """
        return self._request("GET", "/api/v1/settings/notifications/gotify")

    def post_settings_notifications_gotify(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Gotify notification settings

        POST /api/v1/settings/notifications/gotify
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/gotify",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_gotify_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Gotify settings

        POST /api/v1/settings/notifications/gotify/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/gotify/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_ntfy(self) -> Any:
        """Get ntfy.sh notification settings

        GET /api/v1/settings/notifications/ntfy
        """
        return self._request("GET", "/api/v1/settings/notifications/ntfy")

    def post_settings_notifications_ntfy(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update ntfy.sh notification settings

        POST /api/v1/settings/notifications/ntfy
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/ntfy",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_ntfy_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test ntfy.sh settings

        POST /api/v1/settings/notifications/ntfy/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/ntfy/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_slack(self) -> Any:
        """Get Slack notification settings

        GET /api/v1/settings/notifications/slack
        """
        return self._request("GET", "/api/v1/settings/notifications/slack")

    def post_settings_notifications_slack(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Slack notification settings

        POST /api/v1/settings/notifications/slack
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/slack",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_slack_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Slack settings

        POST /api/v1/settings/notifications/slack/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/slack/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_telegram(self) -> Any:
        """Get Telegram notification settings

        GET /api/v1/settings/notifications/telegram
        """
        return self._request("GET", "/api/v1/settings/notifications/telegram")

    def post_settings_notifications_telegram(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update Telegram notification settings

        POST /api/v1/settings/notifications/telegram
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/telegram",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_telegram_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test Telegram settings

        POST /api/v1/settings/notifications/telegram/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/telegram/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_notifications_webpush(self) -> Any:
        """Get Web Push notification settings

        GET /api/v1/settings/notifications/webpush
        """
        return self._request("GET", "/api/v1/settings/notifications/webpush")

    def post_settings_notifications_webpush(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
    ) -> Any:
        """Update Web Push notification settings

        POST /api/v1/settings/notifications/webpush
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/webpush",
            data=_clean({"enabled": enabled, "types": types}),
        )

    def post_settings_notifications_webpush_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
    ) -> Any:
        """Test Web Push settings

        POST /api/v1/settings/notifications/webpush/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/webpush/test",
            data=_clean({"enabled": enabled, "types": types}),
        )

    def get_settings_notifications_webhook(self) -> Any:
        """Get webhook notification settings

        GET /api/v1/settings/notifications/webhook
        """
        return self._request("GET", "/api/v1/settings/notifications/webhook")

    def post_settings_notifications_webhook(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Update webhook notification settings

        POST /api/v1/settings/notifications/webhook
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/webhook",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def post_settings_notifications_webhook_test(
        self,
        *,
        enabled: Annotated[bool | None, Field(description="enabled")] = None,
        types: Annotated[float | None, Field(description="types")] = None,
        options: Annotated[dict[str, Any] | None, Field(description="options")] = None,
    ) -> Any:
        """Test webhook settings

        POST /api/v1/settings/notifications/webhook/test
        """
        return self._request(
            "POST",
            "/api/v1/settings/notifications/webhook/test",
            data=_clean({"enabled": enabled, "types": types, "options": options}),
        )

    def get_settings_discover(self) -> Any:
        """Get all discover sliders

        GET /api/v1/settings/discover
        """
        return self._request("GET", "/api/v1/settings/discover")

    def post_settings_discover(
        self,
        *,
        body: Annotated[
            list[dict[str, Any]], Field(description="The request body as JSON.")
        ],
    ) -> Any:
        """Batch update all sliders.

        POST /api/v1/settings/discover
        """
        return self._request("POST", "/api/v1/settings/discover", data=body)

    def put_settings_discover_slider_id(
        self,
        *,
        slider_id: Annotated[float, Field(description="sliderId")],
        title: Annotated[str | None, Field(description="title")] = None,
        type: Annotated[float | None, Field(description="type")] = None,
        data_: Annotated[str | None, Field(description="data")] = None,
    ) -> Any:
        """Update a single slider

        PUT /api/v1/settings/discover/{sliderId}
        """
        return self._request(
            "PUT",
            f"/api/v1/settings/discover/{slider_id}",
            data=_clean({"title": title, "type": type, "data": data_}),
        )

    def delete_settings_discover_slider_id(
        self, *, slider_id: Annotated[float, Field(description="sliderId")]
    ) -> Any:
        """Delete slider by ID

        DELETE /api/v1/settings/discover/{sliderId}
        """
        return self._request("DELETE", f"/api/v1/settings/discover/{slider_id}")

    def post_settings_discover_add(
        self,
        *,
        title: Annotated[str | None, Field(description="title")] = None,
        type: Annotated[float | None, Field(description="type")] = None,
        data_: Annotated[str | None, Field(description="data")] = None,
    ) -> Any:
        """Add a new slider

        POST /api/v1/settings/discover/add
        """
        return self._request(
            "POST",
            "/api/v1/settings/discover/add",
            data=_clean({"title": title, "type": type, "data": data_}),
        )

    def get_settings_discover_reset(self) -> Any:
        """Reset all discover sliders

        GET /api/v1/settings/discover/reset
        """
        return self._request("GET", "/api/v1/settings/discover/reset")

    def get_settings_about(self) -> Any:
        """Get server stats

        GET /api/v1/settings/about
        """
        return self._request("GET", "/api/v1/settings/about")

    def get_auth_me(self) -> Any:
        """Get logged-in user

        GET /api/v1/auth/me
        """
        return self._request("GET", "/api/v1/auth/me")

    def post_auth_plex(
        self, *, auth_token: Annotated[str, Field(description="authToken")]
    ) -> Any:
        """Sign in using a Plex token

        POST /api/v1/auth/plex
        """
        return self._request(
            "POST", "/api/v1/auth/plex", data=_clean({"authToken": auth_token})
        )

    def post_auth_jellyfin(
        self,
        *,
        username: Annotated[str, Field(description="username")],
        password: Annotated[str, Field(description="password")],
        hostname: Annotated[str | None, Field(description="hostname")] = None,
        email: Annotated[str | None, Field(description="email")] = None,
        server_type: Annotated[float | None, Field(description="serverType")] = None,
    ) -> Any:
        """Sign in using a Jellyfin username and password

        POST /api/v1/auth/jellyfin
        """
        return self._request(
            "POST",
            "/api/v1/auth/jellyfin",
            data=_clean(
                {
                    "username": username,
                    "password": password,
                    "hostname": hostname,
                    "email": email,
                    "serverType": server_type,
                }
            ),
        )

    def post_auth_jellyfin_quickconnect_initiate(self) -> Any:
        """Initiate Jellyfin Quick Connect

        POST /api/v1/auth/jellyfin/quickconnect/initiate
        """
        return self._request("POST", "/api/v1/auth/jellyfin/quickconnect/initiate")

    def get_auth_jellyfin_quickconnect_check(
        self,
        *,
        secret: Annotated[
            str, Field(description="The secret returned from the initiate endpoint")
        ],
    ) -> Any:
        """Check Quick Connect authorization status

        GET /api/v1/auth/jellyfin/quickconnect/check
        """
        return self._request(
            "GET", "/api/v1/auth/jellyfin/quickconnect/check", params={"secret": secret}
        )

    def post_auth_jellyfin_quickconnect_authenticate(
        self, *, secret: Annotated[str, Field(description="secret")]
    ) -> Any:
        """Authenticate with Quick Connect

        POST /api/v1/auth/jellyfin/quickconnect/authenticate
        """
        return self._request(
            "POST",
            "/api/v1/auth/jellyfin/quickconnect/authenticate",
            data=_clean({"secret": secret}),
        )

    def post_auth_local(
        self,
        *,
        email: Annotated[str, Field(description="email")],
        password: Annotated[str, Field(description="password")],
    ) -> Any:
        """Sign in using a local account

        POST /api/v1/auth/local
        """
        return self._request(
            "POST",
            "/api/v1/auth/local",
            data=_clean({"email": email, "password": password}),
        )

    def post_auth_logout(self) -> Any:
        """Sign out and clear session cookie

        POST /api/v1/auth/logout
        """
        return self._request("POST", "/api/v1/auth/logout")

    def post_auth_reset_password(
        self, *, email: Annotated[str, Field(description="email")]
    ) -> Any:
        """Send a reset password email

        POST /api/v1/auth/reset-password
        """
        return self._request(
            "POST", "/api/v1/auth/reset-password", data=_clean({"email": email})
        )

    def post_auth_reset_password_guid(
        self,
        *,
        guid: Annotated[str, Field(description="guid")],
        password: Annotated[str, Field(description="password")],
    ) -> Any:
        """Reset the password for a user

        POST /api/v1/auth/reset-password/{guid}
        """
        return self._request(
            "POST",
            f"/api/v1/auth/reset-password/{guid}",
            data=_clean({"password": password}),
        )

    def get_user(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        sort: Annotated[str | None, Field(description="sort")] = None,
        sort_direction: Annotated[
            str | None,
            Field(
                description="Sort direction. When omitted, the server chooses the direction per sort field (e.g. displayname defaults to asc, requests/updated to desc)."
            ),
        ] = None,
        q: Annotated[str | None, Field(description="q")] = None,
        include_ids: Annotated[str | None, Field(description="includeIds")] = None,
    ) -> Any:
        """Get all users

        GET /api/v1/user
        """
        return self._request(
            "GET",
            "/api/v1/user",
            params={
                "take": take,
                "skip": skip,
                "sort": sort,
                "sortDirection": sort_direction,
                "q": q,
                "includeIds": include_ids,
            },
        )

    def post_user(
        self,
        *,
        email: Annotated[str | None, Field(description="email")] = None,
        username: Annotated[str | None, Field(description="username")] = None,
        permissions: Annotated[float | None, Field(description="permissions")] = None,
    ) -> Any:
        """Create new user

        POST /api/v1/user
        """
        return self._request(
            "POST",
            "/api/v1/user",
            data=_clean(
                {"email": email, "username": username, "permissions": permissions}
            ),
        )

    def put_user(
        self,
        *,
        ids: Annotated[list[int] | None, Field(description="ids")] = None,
        permissions: Annotated[int | None, Field(description="permissions")] = None,
    ) -> Any:
        """Update batch of users

        PUT /api/v1/user
        """
        return self._request(
            "PUT", "/api/v1/user", data=_clean({"ids": ids, "permissions": permissions})
        )

    def post_user_import_from_plex(
        self,
        *,
        plex_ids: Annotated[list[str] | None, Field(description="plexIds")] = None,
    ) -> Any:
        """Import all users from Plex

        POST /api/v1/user/import-from-plex
        """
        return self._request(
            "POST", "/api/v1/user/import-from-plex", data=_clean({"plexIds": plex_ids})
        )

    def post_user_import_from_jellyfin(
        self,
        *,
        jellyfin_user_ids: Annotated[
            list[str] | None, Field(description="jellyfinUserIds")
        ] = None,
    ) -> Any:
        """Import all users from Jellyfin

        POST /api/v1/user/import-from-jellyfin
        """
        return self._request(
            "POST",
            "/api/v1/user/import-from-jellyfin",
            data=_clean({"jellyfinUserIds": jellyfin_user_ids}),
        )

    def post_user_register_push_subscription(
        self,
        *,
        endpoint: Annotated[str, Field(description="endpoint")],
        auth: Annotated[str, Field(description="auth")],
        p256dh: Annotated[str, Field(description="p256dh")],
        user_agent: Annotated[str | None, Field(description="userAgent")] = None,
    ) -> Any:
        """Register a web push /user/registerPushSubscription

        POST /api/v1/user/registerPushSubscription
        """
        return self._request(
            "POST",
            "/api/v1/user/registerPushSubscription",
            data=_clean(
                {
                    "endpoint": endpoint,
                    "auth": auth,
                    "p256dh": p256dh,
                    "userAgent": user_agent,
                }
            ),
        )

    def get_user_id_push_subscriptions(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get all web push notification settings for a user

        GET /api/v1/user/{userId}/pushSubscriptions
        """
        return self._request("GET", f"/api/v1/user/{user_id}/pushSubscriptions")

    def get_user_id_push_subscription_endpoint(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        endpoint: Annotated[str, Field(description="endpoint")],
    ) -> Any:
        """Get web push notification settings for a user

        GET /api/v1/user/{userId}/pushSubscription/{endpoint}
        """
        return self._request(
            "GET", f"/api/v1/user/{user_id}/pushSubscription/{endpoint}"
        )

    def delete_user_id_push_subscription_endpoint(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        endpoint: Annotated[str, Field(description="endpoint")],
    ) -> Any:
        """Delete user push subscription by key

        DELETE /api/v1/user/{userId}/pushSubscription/{endpoint}
        """
        return self._request(
            "DELETE", f"/api/v1/user/{user_id}/pushSubscription/{endpoint}"
        )

    def get_user_id(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get user by ID

        GET /api/v1/user/{userId}
        """
        return self._request("GET", f"/api/v1/user/{user_id}")

    def put_user_id(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        id: Annotated[int, Field(description="id")],
        email: Annotated[str, Field(description="email")],
        created_at: Annotated[str, Field(description="createdAt")],
        updated_at: Annotated[str, Field(description="updatedAt")],
        username: Annotated[str | None, Field(description="username")] = None,
        plex_username: Annotated[str | None, Field(description="plexUsername")] = None,
        plex_token: Annotated[str | None, Field(description="plexToken")] = None,
        jellyfin_auth_token: Annotated[
            str | None, Field(description="jellyfinAuthToken")
        ] = None,
        user_type: Annotated[int | None, Field(description="userType")] = None,
        permissions: Annotated[float | None, Field(description="permissions")] = None,
        avatar: Annotated[str | None, Field(description="avatar")] = None,
        request_count: Annotated[
            float | None, Field(description="requestCount")
        ] = None,
    ) -> Any:
        """Update a user by user ID

        PUT /api/v1/user/{userId}
        """
        return self._request(
            "PUT",
            f"/api/v1/user/{user_id}",
            data=_clean(
                {
                    "id": id,
                    "email": email,
                    "username": username,
                    "plexUsername": plex_username,
                    "plexToken": plex_token,
                    "jellyfinAuthToken": jellyfin_auth_token,
                    "userType": user_type,
                    "permissions": permissions,
                    "avatar": avatar,
                    "createdAt": created_at,
                    "updatedAt": updated_at,
                    "requestCount": request_count,
                }
            ),
        )

    def delete_user_id(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Delete user by ID

        DELETE /api/v1/user/{userId}
        """
        return self._request("DELETE", f"/api/v1/user/{user_id}")

    def get_user_jellyfin_user_id(
        self,
        *,
        jellyfin_user_id: Annotated[
            str,
            Field(description="The Jellyfin user ID (32-character hexadecimal string)"),
        ],
    ) -> Any:
        """Get user by Jellyfin user ID

        GET /api/v1/user/jellyfin/{jellyfinUserId}
        """
        return self._request("GET", f"/api/v1/user/jellyfin/{jellyfin_user_id}")

    def get_user_id_requests(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
    ) -> Any:
        """Get requests for a specific user

        GET /api/v1/user/{userId}/requests
        """
        return self._request(
            "GET",
            f"/api/v1/user/{user_id}/requests",
            params={"take": take, "skip": skip},
        )

    def get_user_id_quota(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get quotas for a specific user

        GET /api/v1/user/{userId}/quota
        """
        return self._request("GET", f"/api/v1/user/{user_id}/quota")

    def get_blocklist(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        search: Annotated[str | None, Field(description="search")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
    ) -> Any:
        """Returns blocklisted items

        GET /api/v1/blocklist
        """
        return self._request(
            "GET",
            "/api/v1/blocklist",
            params={"take": take, "skip": skip, "search": search, "filter": filter},
        )

    def post_blocklist(
        self,
        *,
        tmdb_id: Annotated[float | None, Field(description="tmdbId")] = None,
        title: Annotated[str | None, Field(description="title")] = None,
        media: Annotated[dict[str, Any] | None, Field(description="media")] = None,
        user_id: Annotated[float | None, Field(description="userId")] = None,
    ) -> Any:
        """Add media to blocklist

        POST /api/v1/blocklist
        """
        return self._request(
            "POST",
            "/api/v1/blocklist",
            data=_clean(
                {"tmdbId": tmdb_id, "title": title, "media": media, "userId": user_id}
            ),
        )

    def get_blocklist_tmdb_id(
        self,
        *,
        tmdb_id: Annotated[str, Field(description="tmdbId ID")],
        media_type: Annotated[str, Field(description="mediaType")],
    ) -> Any:
        """Get media from blocklist

        GET /api/v1/blocklist/{tmdbId}
        """
        return self._request(
            "GET", f"/api/v1/blocklist/{tmdb_id}", params={"mediaType": media_type}
        )

    def delete_blocklist_tmdb_id(
        self,
        *,
        tmdb_id: Annotated[str, Field(description="tmdbId ID")],
        media_type: Annotated[str, Field(description="mediaType")],
    ) -> Any:
        """Remove media from blocklist

        DELETE /api/v1/blocklist/{tmdbId}
        """
        return self._request(
            "DELETE", f"/api/v1/blocklist/{tmdb_id}", params={"mediaType": media_type}
        )

    def get_blacklist(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        search: Annotated[str | None, Field(description="search")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
    ) -> Any:
        """Returns blocklisted items

        GET /api/v1/blacklist
        """
        return self._request(
            "GET",
            "/api/v1/blacklist",
            params={"take": take, "skip": skip, "search": search, "filter": filter},
        )

    def post_blacklist(
        self,
        *,
        tmdb_id: Annotated[float | None, Field(description="tmdbId")] = None,
        title: Annotated[str | None, Field(description="title")] = None,
        media: Annotated[dict[str, Any] | None, Field(description="media")] = None,
        user_id: Annotated[float | None, Field(description="userId")] = None,
    ) -> Any:
        """Add media to blocklist

        POST /api/v1/blacklist
        """
        return self._request(
            "POST",
            "/api/v1/blacklist",
            data=_clean(
                {"tmdbId": tmdb_id, "title": title, "media": media, "userId": user_id}
            ),
        )

    def get_blacklist_tmdb_id(
        self,
        *,
        tmdb_id: Annotated[str, Field(description="tmdbId ID")],
        media_type: Annotated[str, Field(description="mediaType")],
    ) -> Any:
        """Get media from blocklist

        GET /api/v1/blacklist/{tmdbId}
        """
        return self._request(
            "GET", f"/api/v1/blacklist/{tmdb_id}", params={"mediaType": media_type}
        )

    def delete_blacklist_tmdb_id(
        self,
        *,
        tmdb_id: Annotated[str, Field(description="tmdbId ID")],
        media_type: Annotated[str, Field(description="mediaType")],
    ) -> Any:
        """Remove media from blocklist

        DELETE /api/v1/blacklist/{tmdbId}
        """
        return self._request(
            "DELETE", f"/api/v1/blacklist/{tmdb_id}", params={"mediaType": media_type}
        )

    def post_blocklist_collection_id(
        self,
        *,
        collection_id: Annotated[str, Field(description="Collection ID")],
        body: Annotated[
            dict[str, Any] | None, Field(description="The request body as JSON.")
        ] = None,
    ) -> Any:
        """Add collection to blocklist

        POST /api/v1/blocklist/collection/{collectionId}
        """
        return self._request(
            "POST", f"/api/v1/blocklist/collection/{collection_id}", data=body
        )

    def delete_blocklist_collection_id(
        self, *, collection_id: Annotated[str, Field(description="Collection ID")]
    ) -> Any:
        """Remove collection from blocklist

        DELETE /api/v1/blocklist/collection/{collectionId}
        """
        return self._request("DELETE", f"/api/v1/blocklist/collection/{collection_id}")

    def post_watchlist(
        self,
        *,
        tmdb_id: Annotated[float, Field(description="tmdbId")],
        media_type: Annotated[str, Field(description="mediaType")],
        rating_key: Annotated[str | None, Field(description="ratingKey")] = None,
        title: Annotated[str | None, Field(description="title")] = None,
    ) -> Any:
        """Add media to watchlist

        POST /api/v1/watchlist
        """
        return self._request(
            "POST",
            "/api/v1/watchlist",
            data=_clean(
                {
                    "tmdbId": tmdb_id,
                    "mediaType": media_type,
                    "ratingKey": rating_key,
                    "title": title,
                }
            ),
        )

    def delete_watchlist_tmdb_id(
        self,
        *,
        tmdb_id: Annotated[str, Field(description="tmdbId ID")],
        media_type: Annotated[str, Field(description="mediaType")],
    ) -> Any:
        """Delete watchlist item

        DELETE /api/v1/watchlist/{tmdbId}
        """
        return self._request(
            "DELETE", f"/api/v1/watchlist/{tmdb_id}", params={"mediaType": media_type}
        )

    def get_user_id_watchlist(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        page: Annotated[float | None, Field(description="page")] = None,
    ) -> Any:
        """Get the Plex watchlist for a specific user

        GET /api/v1/user/{userId}/watchlist
        """
        return self._request(
            "GET", f"/api/v1/user/{user_id}/watchlist", params={"page": page}
        )

    def get_user_id_settings_main(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get general settings for a user

        GET /api/v1/user/{userId}/settings/main
        """
        return self._request("GET", f"/api/v1/user/{user_id}/settings/main")

    def post_user_id_settings_main(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        username: Annotated[str | None, Field(description="username")] = None,
        email: Annotated[str | None, Field(description="email")] = None,
        locale: Annotated[str | None, Field(description="locale")] = None,
        discover_region: Annotated[
            str | None, Field(description="discoverRegion")
        ] = None,
        streaming_region: Annotated[
            str | None, Field(description="streamingRegion")
        ] = None,
        original_language: Annotated[
            str | None, Field(description="originalLanguage")
        ] = None,
        movie_quota_limit: Annotated[
            float | None, Field(description="Maximum number of movie requests allowed")
        ] = None,
        movie_quota_days: Annotated[
            float | None, Field(description="Time period in days for movie quota")
        ] = None,
        tv_quota_limit: Annotated[
            float | None, Field(description="Maximum number of TV requests allowed")
        ] = None,
        tv_quota_days: Annotated[
            float | None, Field(description="Time period in days for TV quota")
        ] = None,
        global_movie_quota_days: Annotated[
            float | None, Field(description="Global movie quota days setting")
        ] = None,
        global_movie_quota_limit: Annotated[
            float | None, Field(description="Global movie quota limit setting")
        ] = None,
        global_tv_quota_limit: Annotated[
            float | None, Field(description="Global TV quota limit setting")
        ] = None,
        global_tv_quota_days: Annotated[
            float | None, Field(description="Global TV quota days setting")
        ] = None,
        watchlist_sync_movies: Annotated[
            bool | None, Field(description="Enable watchlist sync for movies")
        ] = None,
        watchlist_sync_tv: Annotated[
            bool | None, Field(description="Enable watchlist sync for TV")
        ] = None,
    ) -> Any:
        """Update general settings for a user

        POST /api/v1/user/{userId}/settings/main
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/main",
            data=_clean(
                {
                    "username": username,
                    "email": email,
                    "locale": locale,
                    "discoverRegion": discover_region,
                    "streamingRegion": streaming_region,
                    "originalLanguage": original_language,
                    "movieQuotaLimit": movie_quota_limit,
                    "movieQuotaDays": movie_quota_days,
                    "tvQuotaLimit": tv_quota_limit,
                    "tvQuotaDays": tv_quota_days,
                    "globalMovieQuotaDays": global_movie_quota_days,
                    "globalMovieQuotaLimit": global_movie_quota_limit,
                    "globalTvQuotaLimit": global_tv_quota_limit,
                    "globalTvQuotaDays": global_tv_quota_days,
                    "watchlistSyncMovies": watchlist_sync_movies,
                    "watchlistSyncTv": watchlist_sync_tv,
                }
            ),
        )

    def get_user_id_settings_password(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get password page information

        GET /api/v1/user/{userId}/settings/password
        """
        return self._request("GET", f"/api/v1/user/{user_id}/settings/password")

    def post_user_id_settings_password(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        new_password: Annotated[str, Field(description="newPassword")],
        current_password: Annotated[
            str | None, Field(description="currentPassword")
        ] = None,
    ) -> Any:
        """Update password for a user

        POST /api/v1/user/{userId}/settings/password
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/password",
            data=_clean(
                {"currentPassword": current_password, "newPassword": new_password}
            ),
        )

    def post_user_id_settings_linked_accounts_plex(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        auth_token: Annotated[str, Field(description="authToken")],
    ) -> Any:
        """Link the provided Plex account to the current user

        POST /api/v1/user/{userId}/settings/linked-accounts/plex
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/linked-accounts/plex",
            data=_clean({"authToken": auth_token}),
        )

    def delete_user_id_settings_linked_accounts_plex(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Remove the linked Plex account for a user

        DELETE /api/v1/user/{userId}/settings/linked-accounts/plex
        """
        return self._request(
            "DELETE", f"/api/v1/user/{user_id}/settings/linked-accounts/plex"
        )

    def post_user_id_settings_linked_accounts_jellyfin(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        username: Annotated[str | None, Field(description="username")] = None,
        password: Annotated[str | None, Field(description="password")] = None,
    ) -> Any:
        """Link the provided Jellyfin account to the current user

        POST /api/v1/user/{userId}/settings/linked-accounts/jellyfin
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/linked-accounts/jellyfin",
            data=_clean({"username": username, "password": password}),
        )

    def delete_user_id_settings_linked_accounts_jellyfin(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Remove the linked Jellyfin account for a user

        DELETE /api/v1/user/{userId}/settings/linked-accounts/jellyfin
        """
        return self._request(
            "DELETE", f"/api/v1/user/{user_id}/settings/linked-accounts/jellyfin"
        )

    def post_user_id_settings_linked_accounts_jellyfin_quickconnect(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        secret: Annotated[str, Field(description="secret")],
    ) -> Any:
        """Link Jellyfin/Emby account with Quick Connect

        POST /api/v1/user/{userId}/settings/linked-accounts/jellyfin/quickconnect
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/linked-accounts/jellyfin/quickconnect",
            data=_clean({"secret": secret}),
        )

    def get_user_id_settings_notifications(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get notification settings for a user

        GET /api/v1/user/{userId}/settings/notifications
        """
        return self._request("GET", f"/api/v1/user/{user_id}/settings/notifications")

    def post_user_id_settings_notifications(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        notification_types: Annotated[
            dict[str, Any] | None, Field(description="notificationTypes")
        ] = None,
        email_enabled: Annotated[bool | None, Field(description="emailEnabled")] = None,
        pgp_key: Annotated[str | None, Field(description="pgpKey")] = None,
        discord_enabled: Annotated[
            bool | None, Field(description="discordEnabled")
        ] = None,
        discord_enabled_types: Annotated[
            float | None, Field(description="discordEnabledTypes")
        ] = None,
        discord_ids: Annotated[
            list[str] | None, Field(description="discordIds")
        ] = None,
        pushbullet_access_token: Annotated[
            str | None, Field(description="pushbulletAccessToken")
        ] = None,
        pushover_application_token: Annotated[
            str | None, Field(description="pushoverApplicationToken")
        ] = None,
        pushover_user_key: Annotated[
            str | None, Field(description="pushoverUserKey")
        ] = None,
        pushover_sound: Annotated[
            str | None, Field(description="pushoverSound")
        ] = None,
        telegram_enabled: Annotated[
            bool | None, Field(description="telegramEnabled")
        ] = None,
        telegram_bot_username: Annotated[
            str | None, Field(description="telegramBotUsername")
        ] = None,
        telegram_chat_id: Annotated[
            str | None, Field(description="telegramChatId")
        ] = None,
        telegram_message_thread_id: Annotated[
            str | None, Field(description="telegramMessageThreadId")
        ] = None,
        telegram_send_silently: Annotated[
            bool | None, Field(description="telegramSendSilently")
        ] = None,
    ) -> Any:
        """Update notification settings for a user

        POST /api/v1/user/{userId}/settings/notifications
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/notifications",
            data=_clean(
                {
                    "notificationTypes": notification_types,
                    "emailEnabled": email_enabled,
                    "pgpKey": pgp_key,
                    "discordEnabled": discord_enabled,
                    "discordEnabledTypes": discord_enabled_types,
                    "discordIds": discord_ids,
                    "pushbulletAccessToken": pushbullet_access_token,
                    "pushoverApplicationToken": pushover_application_token,
                    "pushoverUserKey": pushover_user_key,
                    "pushoverSound": pushover_sound,
                    "telegramEnabled": telegram_enabled,
                    "telegramBotUsername": telegram_bot_username,
                    "telegramChatId": telegram_chat_id,
                    "telegramMessageThreadId": telegram_message_thread_id,
                    "telegramSendSilently": telegram_send_silently,
                }
            ),
        )

    def get_user_id_settings_permissions(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get permission settings for a user

        GET /api/v1/user/{userId}/settings/permissions
        """
        return self._request("GET", f"/api/v1/user/{user_id}/settings/permissions")

    def post_user_id_settings_permissions(
        self,
        *,
        user_id: Annotated[float, Field(description="userId")],
        permissions: Annotated[float, Field(description="permissions")],
    ) -> Any:
        """Update permission settings for a user

        POST /api/v1/user/{userId}/settings/permissions
        """
        return self._request(
            "POST",
            f"/api/v1/user/{user_id}/settings/permissions",
            data=_clean({"permissions": permissions}),
        )

    def get_user_id_watch_data(
        self, *, user_id: Annotated[float, Field(description="userId")]
    ) -> Any:
        """Get watch data

        GET /api/v1/user/{userId}/watch_data
        """
        return self._request("GET", f"/api/v1/user/{user_id}/watch_data")

    def get_search(
        self,
        *,
        query: Annotated[str, Field(description="query")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Search for movies, TV shows, or people

        GET /api/v1/search
        """
        return self._request(
            "GET",
            "/api/v1/search",
            params={"query": query, "page": page, "language": language},
        )

    def get_search_keyword(
        self,
        *,
        query: Annotated[str, Field(description="query")],
        page: Annotated[float | None, Field(description="page")] = None,
    ) -> Any:
        """Search for keywords

        GET /api/v1/search/keyword
        """
        return self._request(
            "GET", "/api/v1/search/keyword", params={"query": query, "page": page}
        )

    def get_search_company(
        self,
        *,
        query: Annotated[str, Field(description="query")],
        page: Annotated[float | None, Field(description="page")] = None,
    ) -> Any:
        """Search for companies

        GET /api/v1/search/company
        """
        return self._request(
            "GET", "/api/v1/search/company", params={"query": query, "page": page}
        )

    def get_discover_movies(
        self,
        *,
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
        genre: Annotated[str | None, Field(description="genre")] = None,
        studio: Annotated[float | None, Field(description="studio")] = None,
        keywords: Annotated[str | None, Field(description="keywords")] = None,
        exclude_keywords: Annotated[
            str | None,
            Field(
                description="Comma-separated list of keyword IDs to exclude from results"
            ),
        ] = None,
        sort_by: Annotated[str | None, Field(description="sortBy")] = None,
        primary_release_date_gte: Annotated[
            str | None, Field(description="primaryReleaseDateGte")
        ] = None,
        primary_release_date_lte: Annotated[
            str | None, Field(description="primaryReleaseDateLte")
        ] = None,
        with_runtime_gte: Annotated[
            float | None, Field(description="withRuntimeGte")
        ] = None,
        with_runtime_lte: Annotated[
            float | None, Field(description="withRuntimeLte")
        ] = None,
        vote_average_gte: Annotated[
            float | None, Field(description="voteAverageGte")
        ] = None,
        vote_average_lte: Annotated[
            float | None, Field(description="voteAverageLte")
        ] = None,
        vote_count_gte: Annotated[
            float | None, Field(description="voteCountGte")
        ] = None,
        vote_count_lte: Annotated[
            float | None, Field(description="voteCountLte")
        ] = None,
        watch_region: Annotated[str | None, Field(description="watchRegion")] = None,
        watch_providers: Annotated[
            str | None, Field(description="watchProviders")
        ] = None,
        certification: Annotated[
            str | None,
            Field(
                description="Exact certification to filter by (used when certificationMode is 'exact')"
            ),
        ] = None,
        certification_gte: Annotated[
            str | None,
            Field(
                description="Minimum certification to filter by (used when certificationMode is 'range')"
            ),
        ] = None,
        certification_lte: Annotated[
            str | None,
            Field(
                description="Maximum certification to filter by (used when certificationMode is 'range')"
            ),
        ] = None,
        certification_country: Annotated[
            str | None,
            Field(
                description="Country code for the certification system (e.g., US, GB, CA)"
            ),
        ] = None,
        certification_mode: Annotated[
            str | None,
            Field(
                description="Determines whether to use exact certification matching or a certification range (internal use only, not sent to TMDB API)"
            ),
        ] = None,
    ) -> Any:
        """Discover movies

        GET /api/v1/discover/movies
        """
        return self._request(
            "GET",
            "/api/v1/discover/movies",
            params={
                "page": page,
                "language": language,
                "genre": genre,
                "studio": studio,
                "keywords": keywords,
                "excludeKeywords": exclude_keywords,
                "sortBy": sort_by,
                "primaryReleaseDateGte": primary_release_date_gte,
                "primaryReleaseDateLte": primary_release_date_lte,
                "withRuntimeGte": with_runtime_gte,
                "withRuntimeLte": with_runtime_lte,
                "voteAverageGte": vote_average_gte,
                "voteAverageLte": vote_average_lte,
                "voteCountGte": vote_count_gte,
                "voteCountLte": vote_count_lte,
                "watchRegion": watch_region,
                "watchProviders": watch_providers,
                "certification": certification,
                "certificationGte": certification_gte,
                "certificationLte": certification_lte,
                "certificationCountry": certification_country,
                "certificationMode": certification_mode,
            },
        )

    def get_discover_movies_genre_id(
        self,
        *,
        genre_id: Annotated[str, Field(description="genreId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover movies by genre

        GET /api/v1/discover/movies/genre/{genreId}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/movies/genre/{genre_id}",
            params={"page": page, "language": language},
        )

    def get_discover_movies_language_language(
        self,
        *,
        language: Annotated[str, Field(description="language")],
        page: Annotated[float | None, Field(description="page")] = None,
        body_language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover movies by original language

        GET /api/v1/discover/movies/language/{language}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/movies/language/{language}",
            params={"page": page, "language": body_language},
        )

    def get_discover_movies_studio_id(
        self,
        *,
        studio_id: Annotated[str, Field(description="studioId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover movies by studio

        GET /api/v1/discover/movies/studio/{studioId}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/movies/studio/{studio_id}",
            params={"page": page, "language": language},
        )

    def get_discover_movies_upcoming(
        self,
        *,
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Upcoming movies

        GET /api/v1/discover/movies/upcoming
        """
        return self._request(
            "GET",
            "/api/v1/discover/movies/upcoming",
            params={"page": page, "language": language},
        )

    def get_discover_tv(
        self,
        *,
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
        genre: Annotated[str | None, Field(description="genre")] = None,
        network: Annotated[float | None, Field(description="network")] = None,
        keywords: Annotated[str | None, Field(description="keywords")] = None,
        exclude_keywords: Annotated[
            str | None,
            Field(
                description="Comma-separated list of keyword IDs to exclude from results"
            ),
        ] = None,
        sort_by: Annotated[str | None, Field(description="sortBy")] = None,
        first_air_date_gte: Annotated[
            str | None, Field(description="firstAirDateGte")
        ] = None,
        first_air_date_lte: Annotated[
            str | None, Field(description="firstAirDateLte")
        ] = None,
        with_runtime_gte: Annotated[
            float | None, Field(description="withRuntimeGte")
        ] = None,
        with_runtime_lte: Annotated[
            float | None, Field(description="withRuntimeLte")
        ] = None,
        vote_average_gte: Annotated[
            float | None, Field(description="voteAverageGte")
        ] = None,
        vote_average_lte: Annotated[
            float | None, Field(description="voteAverageLte")
        ] = None,
        vote_count_gte: Annotated[
            float | None, Field(description="voteCountGte")
        ] = None,
        vote_count_lte: Annotated[
            float | None, Field(description="voteCountLte")
        ] = None,
        watch_region: Annotated[str | None, Field(description="watchRegion")] = None,
        watch_providers: Annotated[
            str | None, Field(description="watchProviders")
        ] = None,
        status: Annotated[str | None, Field(description="status")] = None,
        certification: Annotated[
            str | None,
            Field(
                description="Exact certification to filter by (used when certificationMode is 'exact')"
            ),
        ] = None,
        certification_gte: Annotated[
            str | None,
            Field(
                description="Minimum certification to filter by (used when certificationMode is 'range')"
            ),
        ] = None,
        certification_lte: Annotated[
            str | None,
            Field(
                description="Maximum certification to filter by (used when certificationMode is 'range')"
            ),
        ] = None,
        certification_country: Annotated[
            str | None,
            Field(
                description="Country code for the certification system (e.g., US, GB, CA)"
            ),
        ] = None,
        certification_mode: Annotated[
            str | None,
            Field(
                description="Determines whether to use exact certification matching or a certification range (internal use only, not sent to TMDB API)"
            ),
        ] = None,
    ) -> Any:
        """Discover TV shows

        GET /api/v1/discover/tv
        """
        return self._request(
            "GET",
            "/api/v1/discover/tv",
            params={
                "page": page,
                "language": language,
                "genre": genre,
                "network": network,
                "keywords": keywords,
                "excludeKeywords": exclude_keywords,
                "sortBy": sort_by,
                "firstAirDateGte": first_air_date_gte,
                "firstAirDateLte": first_air_date_lte,
                "withRuntimeGte": with_runtime_gte,
                "withRuntimeLte": with_runtime_lte,
                "voteAverageGte": vote_average_gte,
                "voteAverageLte": vote_average_lte,
                "voteCountGte": vote_count_gte,
                "voteCountLte": vote_count_lte,
                "watchRegion": watch_region,
                "watchProviders": watch_providers,
                "status": status,
                "certification": certification,
                "certificationGte": certification_gte,
                "certificationLte": certification_lte,
                "certificationCountry": certification_country,
                "certificationMode": certification_mode,
            },
        )

    def get_discover_tv_language_language(
        self,
        *,
        language: Annotated[str, Field(description="language")],
        page: Annotated[float | None, Field(description="page")] = None,
        body_language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover TV shows by original language

        GET /api/v1/discover/tv/language/{language}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/tv/language/{language}",
            params={"page": page, "language": body_language},
        )

    def get_discover_tv_genre_id(
        self,
        *,
        genre_id: Annotated[str, Field(description="genreId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover TV shows by genre

        GET /api/v1/discover/tv/genre/{genreId}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/tv/genre/{genre_id}",
            params={"page": page, "language": language},
        )

    def get_discover_tv_network_id(
        self,
        *,
        network_id: Annotated[str, Field(description="networkId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover TV shows by network

        GET /api/v1/discover/tv/network/{networkId}
        """
        return self._request(
            "GET",
            f"/api/v1/discover/tv/network/{network_id}",
            params={"page": page, "language": language},
        )

    def get_discover_tv_upcoming(
        self,
        *,
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Discover Upcoming TV shows

        GET /api/v1/discover/tv/upcoming
        """
        return self._request(
            "GET",
            "/api/v1/discover/tv/upcoming",
            params={"page": page, "language": language},
        )

    def get_discover_trending(
        self,
        *,
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
        media_type: Annotated[str | None, Field(description="mediaType")] = None,
        time_window: Annotated[str | None, Field(description="timeWindow")] = None,
    ) -> Any:
        """Trending movies and TV

        GET /api/v1/discover/trending
        """
        return self._request(
            "GET",
            "/api/v1/discover/trending",
            params={
                "page": page,
                "language": language,
                "mediaType": media_type,
                "timeWindow": time_window,
            },
        )

    def get_discover_keyword_id_movies(
        self,
        *,
        keyword_id: Annotated[float, Field(description="keywordId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get movies from keyword

        GET /api/v1/discover/keyword/{keywordId}/movies
        """
        return self._request(
            "GET",
            f"/api/v1/discover/keyword/{keyword_id}/movies",
            params={"page": page, "language": language},
        )

    def get_discover_genreslider_movie(
        self, *, language: Annotated[str | None, Field(description="language")] = None
    ) -> Any:
        """Get genre slider data for movies

        GET /api/v1/discover/genreslider/movie
        """
        return self._request(
            "GET", "/api/v1/discover/genreslider/movie", params={"language": language}
        )

    def get_discover_genreslider_tv(
        self, *, language: Annotated[str | None, Field(description="language")] = None
    ) -> Any:
        """Get genre slider data for TV series

        GET /api/v1/discover/genreslider/tv
        """
        return self._request(
            "GET", "/api/v1/discover/genreslider/tv", params={"language": language}
        )

    def get_discover_watchlist(
        self, *, page: Annotated[float | None, Field(description="page")] = None
    ) -> Any:
        """Get the Plex watchlist.

        GET /api/v1/discover/watchlist
        """
        return self._request("GET", "/api/v1/discover/watchlist", params={"page": page})

    def get_request(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
        sort: Annotated[str | None, Field(description="sort")] = None,
        sort_direction: Annotated[
            str | None, Field(description="sortDirection")
        ] = None,
        requested_by: Annotated[float | None, Field(description="requestedBy")] = None,
        media_type: Annotated[str | None, Field(description="mediaType")] = None,
    ) -> Any:
        """Get all requests

        GET /api/v1/request
        """
        return self._request(
            "GET",
            "/api/v1/request",
            params={
                "take": take,
                "skip": skip,
                "filter": filter,
                "sort": sort,
                "sortDirection": sort_direction,
                "requestedBy": requested_by,
                "mediaType": media_type,
            },
        )

    def post_request(
        self,
        *,
        media_type: Annotated[str, Field(description="mediaType")],
        media_id: Annotated[float, Field(description="mediaId")],
        tvdb_id: Annotated[float | None, Field(description="tvdbId")] = None,
        seasons: Annotated[Any | None, Field(description="seasons")] = None,
        is4k: Annotated[bool | None, Field(description="is4k")] = None,
        server_id: Annotated[float | None, Field(description="serverId")] = None,
        profile_id: Annotated[float | None, Field(description="profileId")] = None,
        root_folder: Annotated[str | None, Field(description="rootFolder")] = None,
        language_profile_id: Annotated[
            float | None, Field(description="languageProfileId")
        ] = None,
        user_id: Annotated[float | None, Field(description="userId")] = None,
        ignore_quota: Annotated[
            bool | None,
            Field(
                description="If true, this request will not count against the user's quota. Requires MANAGE_REQUESTS permission."
            ),
        ] = None,
    ) -> Any:
        """Create new request

        POST /api/v1/request
        """
        return self._request(
            "POST",
            "/api/v1/request",
            data=_clean(
                {
                    "mediaType": media_type,
                    "mediaId": media_id,
                    "tvdbId": tvdb_id,
                    "seasons": seasons,
                    "is4k": is4k,
                    "serverId": server_id,
                    "profileId": profile_id,
                    "rootFolder": root_folder,
                    "languageProfileId": language_profile_id,
                    "userId": user_id,
                    "ignoreQuota": ignore_quota,
                }
            ),
        )

    def get_request_count(self) -> Any:
        """Gets request counts

        GET /api/v1/request/count
        """
        return self._request("GET", "/api/v1/request/count")

    def get_request_id(
        self, *, request_id: Annotated[str, Field(description="Request ID")]
    ) -> Any:
        """Get MediaRequest

        GET /api/v1/request/{requestId}
        """
        return self._request("GET", f"/api/v1/request/{request_id}")

    def put_request_id(
        self,
        *,
        request_id: Annotated[str, Field(description="Request ID")],
        media_type: Annotated[str, Field(description="mediaType")],
        seasons: Annotated[list[float] | None, Field(description="seasons")] = None,
        is4k: Annotated[bool | None, Field(description="is4k")] = None,
        server_id: Annotated[float | None, Field(description="serverId")] = None,
        profile_id: Annotated[float | None, Field(description="profileId")] = None,
        root_folder: Annotated[str | None, Field(description="rootFolder")] = None,
        language_profile_id: Annotated[
            float | None, Field(description="languageProfileId")
        ] = None,
        user_id: Annotated[float | None, Field(description="userId")] = None,
    ) -> Any:
        """Update MediaRequest

        PUT /api/v1/request/{requestId}
        """
        return self._request(
            "PUT",
            f"/api/v1/request/{request_id}",
            data=_clean(
                {
                    "mediaType": media_type,
                    "seasons": seasons,
                    "is4k": is4k,
                    "serverId": server_id,
                    "profileId": profile_id,
                    "rootFolder": root_folder,
                    "languageProfileId": language_profile_id,
                    "userId": user_id,
                }
            ),
        )

    def delete_request_id(
        self, *, request_id: Annotated[str, Field(description="Request ID")]
    ) -> Any:
        """Delete request

        DELETE /api/v1/request/{requestId}
        """
        return self._request("DELETE", f"/api/v1/request/{request_id}")

    def post_request_id_retry(
        self, *, request_id: Annotated[str, Field(description="Request ID")]
    ) -> Any:
        """Retry failed request

        POST /api/v1/request/{requestId}/retry
        """
        return self._request("POST", f"/api/v1/request/{request_id}/retry")

    def post_request_id_status(
        self,
        *,
        request_id: Annotated[str, Field(description="Request ID")],
        status: Annotated[str, Field(description="New status")],
    ) -> Any:
        """Update a request's status

        POST /api/v1/request/{requestId}/{status}
        """
        return self._request("POST", f"/api/v1/request/{request_id}/{status}")

    def get_movie_id(
        self,
        *,
        movie_id: Annotated[float, Field(description="movieId")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get movie details

        GET /api/v1/movie/{movieId}
        """
        return self._request(
            "GET", f"/api/v1/movie/{movie_id}", params={"language": language}
        )

    def get_movie_id_recommendations(
        self,
        *,
        movie_id: Annotated[float, Field(description="movieId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get recommended movies

        GET /api/v1/movie/{movieId}/recommendations
        """
        return self._request(
            "GET",
            f"/api/v1/movie/{movie_id}/recommendations",
            params={"page": page, "language": language},
        )

    def get_movie_id_similar(
        self,
        *,
        movie_id: Annotated[float, Field(description="movieId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get similar movies

        GET /api/v1/movie/{movieId}/similar
        """
        return self._request(
            "GET",
            f"/api/v1/movie/{movie_id}/similar",
            params={"page": page, "language": language},
        )

    def get_movie_id_ratings(
        self, *, movie_id: Annotated[float, Field(description="movieId")]
    ) -> Any:
        """Get movie ratings

        GET /api/v1/movie/{movieId}/ratings
        """
        return self._request("GET", f"/api/v1/movie/{movie_id}/ratings")

    def get_movie_id_ratingscombined(
        self, *, movie_id: Annotated[float, Field(description="movieId")]
    ) -> Any:
        """Get RT and IMDB movie ratings combined

        GET /api/v1/movie/{movieId}/ratingscombined
        """
        return self._request("GET", f"/api/v1/movie/{movie_id}/ratingscombined")

    def get_tv_id(
        self,
        *,
        tv_id: Annotated[float, Field(description="tvId")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get TV details

        GET /api/v1/tv/{tvId}
        """
        return self._request(
            "GET", f"/api/v1/tv/{tv_id}", params={"language": language}
        )

    def get_tv_id_season_number(
        self,
        *,
        tv_id: Annotated[float, Field(description="tvId")],
        season_number: Annotated[float, Field(description="seasonNumber")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get season details and episode list

        GET /api/v1/tv/{tvId}/season/{seasonNumber}
        """
        return self._request(
            "GET",
            f"/api/v1/tv/{tv_id}/season/{season_number}",
            params={"language": language},
        )

    def get_tv_id_recommendations(
        self,
        *,
        tv_id: Annotated[float, Field(description="tvId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get recommended TV series

        GET /api/v1/tv/{tvId}/recommendations
        """
        return self._request(
            "GET",
            f"/api/v1/tv/{tv_id}/recommendations",
            params={"page": page, "language": language},
        )

    def get_tv_id_similar(
        self,
        *,
        tv_id: Annotated[float, Field(description="tvId")],
        page: Annotated[float | None, Field(description="page")] = None,
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get similar TV series

        GET /api/v1/tv/{tvId}/similar
        """
        return self._request(
            "GET",
            f"/api/v1/tv/{tv_id}/similar",
            params={"page": page, "language": language},
        )

    def get_tv_id_ratings(
        self, *, tv_id: Annotated[float, Field(description="tvId")]
    ) -> Any:
        """Get TV ratings

        GET /api/v1/tv/{tvId}/ratings
        """
        return self._request("GET", f"/api/v1/tv/{tv_id}/ratings")

    def get_person_id(
        self,
        *,
        person_id: Annotated[float, Field(description="personId")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get person details

        GET /api/v1/person/{personId}
        """
        return self._request(
            "GET", f"/api/v1/person/{person_id}", params={"language": language}
        )

    def get_person_id_combined_credits(
        self,
        *,
        person_id: Annotated[float, Field(description="personId")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get combined credits

        GET /api/v1/person/{personId}/combined_credits
        """
        return self._request(
            "GET",
            f"/api/v1/person/{person_id}/combined_credits",
            params={"language": language},
        )

    def get_media(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
        sort: Annotated[str | None, Field(description="sort")] = None,
    ) -> Any:
        """Get media

        GET /api/v1/media
        """
        return self._request(
            "GET",
            "/api/v1/media",
            params={"take": take, "skip": skip, "filter": filter, "sort": sort},
        )

    def delete_media_id(
        self, *, media_id: Annotated[str, Field(description="Media ID")]
    ) -> Any:
        """Delete media item

        DELETE /api/v1/media/{mediaId}
        """
        return self._request("DELETE", f"/api/v1/media/{media_id}")

    def delete_media_id_file(
        self,
        *,
        media_id: Annotated[str, Field(description="Media ID")],
        is4k: Annotated[
            bool | None,
            Field(
                description="Whether to remove from 4K service instance (true) or regular service instance (false)"
            ),
        ] = None,
    ) -> Any:
        """Delete media file

        DELETE /api/v1/media/{mediaId}/file
        """
        return self._request(
            "DELETE", f"/api/v1/media/{media_id}/file", params={"is4k": is4k}
        )

    def post_media_id_status(
        self,
        *,
        media_id: Annotated[str, Field(description="Media ID")],
        status: Annotated[str, Field(description="New status")],
        is4k: Annotated[
            bool | None,
            Field(
                description="When true, updates the 4K status field (status4k). When false or not provided, updates the regular status field (status). This applies to all status values (available, partial, processing, pending, unknown)."
            ),
        ] = None,
    ) -> Any:
        """Update media status

        POST /api/v1/media/{mediaId}/{status}
        """
        return self._request(
            "POST", f"/api/v1/media/{media_id}/{status}", data=_clean({"is4k": is4k})
        )

    def get_media_id_watch_data(
        self, *, media_id: Annotated[str, Field(description="Media ID")]
    ) -> Any:
        """Get watch data

        GET /api/v1/media/{mediaId}/watch_data
        """
        return self._request("GET", f"/api/v1/media/{media_id}/watch_data")

    def get_collection_id(
        self,
        *,
        collection_id: Annotated[float, Field(description="collectionId")],
        language: Annotated[str | None, Field(description="language")] = None,
    ) -> Any:
        """Get collection details

        GET /api/v1/collection/{collectionId}
        """
        return self._request(
            "GET", f"/api/v1/collection/{collection_id}", params={"language": language}
        )

    def get_service_radarr(self) -> Any:
        """Get non-sensitive Radarr server list

        GET /api/v1/service/radarr
        """
        return self._request("GET", "/api/v1/service/radarr")

    def get_service_radarr_id(
        self, *, radarr_id: Annotated[float, Field(description="radarrId")]
    ) -> Any:
        """Get Radarr server quality profiles and root folders

        GET /api/v1/service/radarr/{radarrId}
        """
        return self._request("GET", f"/api/v1/service/radarr/{radarr_id}")

    def get_service_sonarr(self) -> Any:
        """Get non-sensitive Sonarr server list

        GET /api/v1/service/sonarr
        """
        return self._request("GET", "/api/v1/service/sonarr")

    def get_service_sonarr_id(
        self, *, sonarr_id: Annotated[float, Field(description="sonarrId")]
    ) -> Any:
        """Get Sonarr server quality profiles and root folders

        GET /api/v1/service/sonarr/{sonarrId}
        """
        return self._request("GET", f"/api/v1/service/sonarr/{sonarr_id}")

    def get_service_sonarr_lookup_tmdb_id(
        self, *, tmdb_id: Annotated[float, Field(description="tmdbId")]
    ) -> Any:
        """Get series from Sonarr

        GET /api/v1/service/sonarr/lookup/{tmdbId}
        """
        return self._request("GET", f"/api/v1/service/sonarr/lookup/{tmdb_id}")

    def get_regions(self) -> Any:
        """Regions supported by TMDB

        GET /api/v1/regions
        """
        return self._request("GET", "/api/v1/regions")

    def get_languages(self) -> Any:
        """Languages supported by TMDB

        GET /api/v1/languages
        """
        return self._request("GET", "/api/v1/languages")

    def get_studio_id(
        self, *, studio_id: Annotated[float, Field(description="studioId")]
    ) -> Any:
        """Get movie studio details

        GET /api/v1/studio/{studioId}
        """
        return self._request("GET", f"/api/v1/studio/{studio_id}")

    def get_network_id(
        self, *, network_id: Annotated[float, Field(description="networkId")]
    ) -> Any:
        """Get TV network details

        GET /api/v1/network/{networkId}
        """
        return self._request("GET", f"/api/v1/network/{network_id}")

    def get_genres_movie(
        self, *, language: Annotated[str | None, Field(description="language")] = None
    ) -> Any:
        """Get list of official TMDB movie genres

        GET /api/v1/genres/movie
        """
        return self._request(
            "GET", "/api/v1/genres/movie", params={"language": language}
        )

    def get_genres_tv(
        self, *, language: Annotated[str | None, Field(description="language")] = None
    ) -> Any:
        """Get list of official TMDB movie genres

        GET /api/v1/genres/tv
        """
        return self._request("GET", "/api/v1/genres/tv", params={"language": language})

    def get_backdrops(self) -> Any:
        """Get backdrops of trending items

        GET /api/v1/backdrops
        """
        return self._request("GET", "/api/v1/backdrops")

    def get_issue(
        self,
        *,
        take: Annotated[float | None, Field(description="take")] = None,
        skip: Annotated[float | None, Field(description="skip")] = None,
        sort: Annotated[str | None, Field(description="sort")] = None,
        filter: Annotated[str | None, Field(description="filter")] = None,
        requested_by: Annotated[float | None, Field(description="requestedBy")] = None,
    ) -> Any:
        """Get all issues

        GET /api/v1/issue
        """
        return self._request(
            "GET",
            "/api/v1/issue",
            params={
                "take": take,
                "skip": skip,
                "sort": sort,
                "filter": filter,
                "requestedBy": requested_by,
            },
        )

    def post_issue(
        self,
        *,
        issue_type: Annotated[float | None, Field(description="issueType")] = None,
        message: Annotated[str | None, Field(description="message")] = None,
        media_id: Annotated[float | None, Field(description="mediaId")] = None,
        user_id: Annotated[float | None, Field(description="userId")] = None,
    ) -> Any:
        """Create new issue

        POST /api/v1/issue
        """
        return self._request(
            "POST",
            "/api/v1/issue",
            data=_clean(
                {
                    "issueType": issue_type,
                    "message": message,
                    "mediaId": media_id,
                    "userId": user_id,
                }
            ),
        )

    def get_issue_count(self) -> Any:
        """Gets issue counts

        GET /api/v1/issue/count
        """
        return self._request("GET", "/api/v1/issue/count")

    def get_issue_id(
        self, *, issue_id: Annotated[float, Field(description="issueId")]
    ) -> Any:
        """Get issue

        GET /api/v1/issue/{issueId}
        """
        return self._request("GET", f"/api/v1/issue/{issue_id}")

    def delete_issue_id(
        self, *, issue_id: Annotated[str, Field(description="Issue ID")]
    ) -> Any:
        """Delete issue

        DELETE /api/v1/issue/{issueId}
        """
        return self._request("DELETE", f"/api/v1/issue/{issue_id}")

    def post_issue_id_comment(
        self,
        *,
        issue_id: Annotated[float, Field(description="issueId")],
        message: Annotated[str, Field(description="message")],
    ) -> Any:
        """Create a comment

        POST /api/v1/issue/{issueId}/comment
        """
        return self._request(
            "POST",
            f"/api/v1/issue/{issue_id}/comment",
            data=_clean({"message": message}),
        )

    def get_issue_comment_comment_id(
        self, *, comment_id: Annotated[str, Field(description="commentId")]
    ) -> Any:
        """Get issue comment

        GET /api/v1/issueComment/{commentId}
        """
        return self._request("GET", f"/api/v1/issueComment/{comment_id}")

    def put_issue_comment_comment_id(
        self,
        *,
        comment_id: Annotated[str, Field(description="commentId")],
        message: Annotated[str | None, Field(description="message")] = None,
    ) -> Any:
        """Update issue comment

        PUT /api/v1/issueComment/{commentId}
        """
        return self._request(
            "PUT",
            f"/api/v1/issueComment/{comment_id}",
            data=_clean({"message": message}),
        )

    def delete_issue_comment_comment_id(
        self, *, comment_id: Annotated[str, Field(description="Issue Comment ID")]
    ) -> Any:
        """Delete issue comment

        DELETE /api/v1/issueComment/{commentId}
        """
        return self._request("DELETE", f"/api/v1/issueComment/{comment_id}")

    def post_issue_id_status(
        self,
        *,
        issue_id: Annotated[str, Field(description="Issue ID")],
        status: Annotated[str, Field(description="New status")],
    ) -> Any:
        """Update an issue's status

        POST /api/v1/issue/{issueId}/{status}
        """
        return self._request("POST", f"/api/v1/issue/{issue_id}/{status}")

    def get_keyword_id(
        self, *, keyword_id: Annotated[float, Field(description="keywordId")]
    ) -> Any:
        """Get keyword

        GET /api/v1/keyword/{keywordId}
        """
        return self._request("GET", f"/api/v1/keyword/{keyword_id}")

    def get_watchproviders_regions(self) -> Any:
        """Get watch provider regions

        GET /api/v1/watchproviders/regions
        """
        return self._request("GET", "/api/v1/watchproviders/regions")

    def get_watchproviders_movies(
        self, *, watch_region: Annotated[str, Field(description="watchRegion")]
    ) -> Any:
        """Get watch provider movies

        GET /api/v1/watchproviders/movies
        """
        return self._request(
            "GET", "/api/v1/watchproviders/movies", params={"watchRegion": watch_region}
        )

    def get_watchproviders_tv(
        self, *, watch_region: Annotated[str, Field(description="watchRegion")]
    ) -> Any:
        """Get watch provider series

        GET /api/v1/watchproviders/tv
        """
        return self._request(
            "GET", "/api/v1/watchproviders/tv", params={"watchRegion": watch_region}
        )

    def get_certifications_movie(self) -> Any:
        """Get movie certifications

        GET /api/v1/certifications/movie
        """
        return self._request("GET", "/api/v1/certifications/movie")

    def get_certifications_tv(self) -> Any:
        """Get TV certifications

        GET /api/v1/certifications/tv
        """
        return self._request("GET", "/api/v1/certifications/tv")

    def get_override_rule(self) -> Any:
        """Get override rules

        GET /api/v1/overrideRule
        """
        return self._request("GET", "/api/v1/overrideRule")

    def post_override_rule(self) -> Any:
        """Create override rule

        POST /api/v1/overrideRule
        """
        return self._request("POST", "/api/v1/overrideRule")

    def put_override_rule_rule_id(
        self, *, rule_id: Annotated[float, Field(description="ruleId")]
    ) -> Any:
        """Update override rule

        PUT /api/v1/overrideRule/{ruleId}
        """
        return self._request("PUT", f"/api/v1/overrideRule/{rule_id}")

    def delete_override_rule_rule_id(
        self, *, rule_id: Annotated[float, Field(description="ruleId")]
    ) -> Any:
        """Delete override rule by ID

        DELETE /api/v1/overrideRule/{ruleId}
        """
        return self._request("DELETE", f"/api/v1/overrideRule/{rule_id}")

    def post_override_rule_advanced_request(
        self,
        *,
        media_type: Annotated[str, Field(description="mediaType")],
        tmdb_id: Annotated[float, Field(description="tmdbId")],
        is4k: Annotated[bool | None, Field(description="is4k")] = None,
        request_id: Annotated[float | None, Field(description="requestId")] = None,
        request_user: Annotated[float | None, Field(description="requestUser")] = None,
        tags: Annotated[list[float] | None, Field(description="tags")] = None,
        service_id: Annotated[float | None, Field(description="serviceId")] = None,
    ) -> Any:
        """Advanced override rule request

        POST /api/v1/overrideRule/advancedRequest
        """
        return self._request(
            "POST",
            "/api/v1/overrideRule/advancedRequest",
            data=_clean(
                {
                    "mediaType": media_type,
                    "tmdbId": tmdb_id,
                    "is4k": is4k,
                    "requestId": request_id,
                    "requestUser": request_user,
                    "tags": tags,
                    "serviceId": service_id,
                }
            ),
        )
