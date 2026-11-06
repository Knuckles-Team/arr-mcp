"""Bazarr API client: one method per upstream operation.

Written by ``scripts/generate_api_client.py`` from the Bazarr API description
(bazarr_swagger.json 1.6.2); every method is served as one typed MCP tool
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
    """API client for Bazarr."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url, self._origin = validate_base_url(base_url)
        self.api_key = api_key
        self._tls_profile = tls_profile or resolve_tls_profile("bazarr")
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

    def get_badges(self) -> Any:
        """Get badges count to update the UI

        GET /api/badges
        """
        return self._request("GET", "/api/badges")

    def get_episodes(
        self,
        *,
        seriesid: Annotated[
            list[int] | None, Field(description="Series IDs to list episodes for")
        ] = None,
        episodeid: Annotated[
            list[int] | None, Field(description="Episodes ID to list")
        ] = None,
    ) -> Any:
        """List episodes metadata for specific series or episodes

        GET /api/episodes
        """
        return self._request(
            "GET",
            "/api/episodes",
            params={"seriesid[]": seriesid, "episodeid[]": episodeid},
        )

    def get_episodes_blacklist(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
    ) -> Any:
        """List blacklisted episodes subtitles

        GET /api/episodes/blacklist
        """
        return self._request(
            "GET", "/api/episodes/blacklist", params={"start": start, "length": length}
        )

    def post_episodes_blacklist(
        self,
        *,
        seriesid: Annotated[int, Field(description="Series ID")],
        episodeid: Annotated[int, Field(description="Episode ID")],
        provider: Annotated[str, Field(description="Provider name")],
        subs_id: Annotated[str, Field(description="Subtitles ID")],
        language: Annotated[str, Field(description="Subtitles language")],
        subtitles_path: Annotated[str, Field(description="Subtitles file path")],
    ) -> Any:
        """Add an episodes subtitles to blacklist

        POST /api/episodes/blacklist
        """
        return self._request(
            "POST",
            "/api/episodes/blacklist",
            params={
                "seriesid": seriesid,
                "episodeid": episodeid,
                "provider": provider,
                "subs_id": subs_id,
                "language": language,
                "subtitles_path": subtitles_path,
            },
        )

    def delete_episodes_blacklist(
        self,
        *,
        all: Annotated[
            str | None, Field(description="Empty episodes subtitles blacklist")
        ] = None,
        provider: Annotated[str | None, Field(description="Provider name")] = None,
        subs_id: Annotated[str | None, Field(description="Subtitles ID")] = None,
    ) -> Any:
        """Delete an episodes subtitles from blacklist

        DELETE /api/episodes/blacklist
        """
        return self._request(
            "DELETE",
            "/api/episodes/blacklist",
            params={"all": all, "provider": provider, "subs_id": subs_id},
        )

    def get_episodes_history(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        episodeid: Annotated[int | None, Field(description="Episode ID")] = None,
    ) -> Any:
        """List episodes history events

        GET /api/episodes/history
        """
        return self._request(
            "GET",
            "/api/episodes/history",
            params={"start": start, "length": length, "episodeid": episodeid},
        )

    def post_episodes_subtitles(
        self,
        *,
        seriesid: Annotated[int, Field(description="Series ID")],
        episodeid: Annotated[int, Field(description="Episode ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
        file: Annotated[Any, Field(description="Subtitles file as file upload object")],
    ) -> Any:
        """Upload an episode subtitles

        POST /api/episodes/subtitles
        """
        return self._request(
            "POST",
            "/api/episodes/subtitles",
            params={
                "seriesid": seriesid,
                "episodeid": episodeid,
                "language": language,
                "forced": forced,
                "hi": hi,
            },
            form={"file": file},
        )

    def patch_episodes_subtitles(
        self,
        *,
        seriesid: Annotated[int, Field(description="Series ID")],
        episodeid: Annotated[int, Field(description="Episode ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
    ) -> Any:
        """Download an episode subtitles

        PATCH /api/episodes/subtitles
        """
        return self._request(
            "PATCH",
            "/api/episodes/subtitles",
            params={
                "seriesid": seriesid,
                "episodeid": episodeid,
                "language": language,
                "forced": forced,
                "hi": hi,
            },
        )

    def delete_episodes_subtitles(
        self,
        *,
        seriesid: Annotated[int, Field(description="Series ID")],
        episodeid: Annotated[int, Field(description="Episode ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
        path: Annotated[str, Field(description="Path of the subtitles file")],
    ) -> Any:
        """Delete an episode subtitles

        DELETE /api/episodes/subtitles
        """
        return self._request(
            "DELETE",
            "/api/episodes/subtitles",
            params={
                "seriesid": seriesid,
                "episodeid": episodeid,
                "language": language,
                "forced": forced,
                "hi": hi,
                "path": path,
            },
        )

    def get_episodes_wanted(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        episodeid: Annotated[
            list[int] | None, Field(description="Episodes ID to list")
        ] = None,
    ) -> Any:
        """List episodes wanted subtitles

        GET /api/episodes/wanted
        """
        return self._request(
            "GET",
            "/api/episodes/wanted",
            params={"start": start, "length": length, "episodeid[]": episodeid},
        )

    def get_browse_bazarr_fs(
        self, *, path: Annotated[str | None, Field(description="Path to browse")] = None
    ) -> Any:
        """List Bazarr file system content

        GET /api/files
        """
        return self._request("GET", "/api/files", params={"path": path})

    def get_browse_radarr_fs(
        self, *, path: Annotated[str | None, Field(description="Path to browse")] = None
    ) -> Any:
        """List Radarr file system content

        GET /api/files/radarr
        """
        return self._request("GET", "/api/files/radarr", params={"path": path})

    def get_browse_sonarr_fs(
        self, *, path: Annotated[str | None, Field(description="Path to browse")] = None
    ) -> Any:
        """List Sonarr file system content

        GET /api/files/sonarr
        """
        return self._request("GET", "/api/files/sonarr", params={"path": path})

    def get_history_stats(
        self,
        *,
        time_frame: Annotated[
            str | None,
            Field(
                description='Timeframe to get stats for. Must be in ["week", "month", "trimester", "year"]'
            ),
        ] = None,
        action: Annotated[
            str | None, Field(description="Action type to filter for.")
        ] = None,
        provider: Annotated[
            str | None, Field(description="Provider name to filter for.")
        ] = None,
        language: Annotated[
            str | None, Field(description="Language name to filter for")
        ] = None,
    ) -> Any:
        """Get history statistics

        GET /api/history/stats
        """
        return self._request(
            "GET",
            "/api/history/stats",
            params={
                "timeFrame": time_frame,
                "action": action,
                "provider": provider,
                "language": language,
            },
        )

    def get_jellyfin_libraries(
        self,
        *,
        url: Annotated[str | None, Field(description="Jellyfin server URL")] = None,
        apikey: Annotated[str | None, Field(description="Jellyfin API key")] = None,
    ) -> Any:
        """List available movie and series libraries from the Jellyfin server

        GET /api/jellyfin/libraries
        """
        return self._request(
            "GET", "/api/jellyfin/libraries", params={"url": url, "apikey": apikey}
        )

    def post_jellyfin_test_connection(
        self,
        *,
        url: Annotated[str, Field(description="Jellyfin server URL")],
        apikey: Annotated[str, Field(description="Jellyfin API key")],
    ) -> Any:
        """Test connection to a Jellyfin server with provided credentials

        POST /api/jellyfin/test-connection
        """
        return self._request(
            "POST",
            "/api/jellyfin/test-connection",
            params={"url": url, "apikey": apikey},
        )

    def get_movies(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        radarrid: Annotated[
            list[int] | None, Field(description="Movies IDs to get metadata for")
        ] = None,
        sort_by: Annotated[str | None, Field(description="Column to sort by")] = None,
        sort_order: Annotated[str | None, Field(description="Sort direction")] = None,
        monitored: Annotated[
            str | None, Field(description="Filter by monitored status")
        ] = None,
        profileid: Annotated[
            str | None, Field(description='Filter by languages profile ID or "none"')
        ] = None,
        missing: Annotated[
            str | None, Field(description="Filter by missing subtitles")
        ] = None,
        audio_language: Annotated[
            str | None, Field(description="Filter by audio language name")
        ] = None,
        tags: Annotated[
            list[str] | None, Field(description="Tags to filter by")
        ] = None,
    ) -> Any:
        """List movies metadata for specific movies

        GET /api/movies
        """
        return self._request(
            "GET",
            "/api/movies",
            params={
                "start": start,
                "length": length,
                "radarrid[]": radarrid,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "monitored": monitored,
                "profileid": profileid,
                "missing": missing,
                "audio_language": audio_language,
                "tags[]": tags,
            },
        )

    def post_movies(
        self,
        *,
        radarrid: Annotated[
            list[int] | None, Field(description="Radarr movie(s) ID")
        ] = None,
        profileid: Annotated[
            list[str] | None, Field(description='Languages profile(s) ID or "none"')
        ] = None,
    ) -> Any:
        """Update specific movies languages profile

        POST /api/movies
        """
        return self._request(
            "POST", "/api/movies", params={"radarrid": radarrid, "profileid": profileid}
        )

    def patch_movies(
        self,
        *,
        radarrid: Annotated[int | None, Field(description="Radarr movie ID")] = None,
        action: Annotated[
            str | None,
            Field(
                description='Action to perform from ["scan-disk", "search-missing", "search-wanted", "sync"]'
            ),
        ] = None,
    ) -> Any:
        """Run actions on specific movies

        PATCH /api/movies
        """
        return self._request(
            "PATCH", "/api/movies", params={"radarrid": radarrid, "action": action}
        )

    def get_movies_blacklist(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
    ) -> Any:
        """List blacklisted movies subtitles

        GET /api/movies/blacklist
        """
        return self._request(
            "GET", "/api/movies/blacklist", params={"start": start, "length": length}
        )

    def post_movies_blacklist(
        self,
        *,
        radarrid: Annotated[int, Field(description="Radarr ID")],
        provider: Annotated[str, Field(description="Provider name")],
        subs_id: Annotated[str, Field(description="Subtitles ID")],
        language: Annotated[str, Field(description="Subtitles language")],
        subtitles_path: Annotated[str, Field(description="Subtitles file path")],
    ) -> Any:
        """Add a movies subtitles to blacklist

        POST /api/movies/blacklist
        """
        return self._request(
            "POST",
            "/api/movies/blacklist",
            params={
                "radarrid": radarrid,
                "provider": provider,
                "subs_id": subs_id,
                "language": language,
                "subtitles_path": subtitles_path,
            },
        )

    def delete_movies_blacklist(
        self,
        *,
        all: Annotated[
            str | None, Field(description="Empty movies subtitles blacklist")
        ] = None,
        provider: Annotated[str | None, Field(description="Provider name")] = None,
        subs_id: Annotated[str | None, Field(description="Subtitles ID")] = None,
    ) -> Any:
        """Delete a movies subtitles from blacklist

        DELETE /api/movies/blacklist
        """
        return self._request(
            "DELETE",
            "/api/movies/blacklist",
            params={"all": all, "provider": provider, "subs_id": subs_id},
        )

    def get_movies_history(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        radarrid: Annotated[int | None, Field(description="Movie ID")] = None,
    ) -> Any:
        """List movies history events

        GET /api/movies/history
        """
        return self._request(
            "GET",
            "/api/movies/history",
            params={"start": start, "length": length, "radarrid": radarrid},
        )

    def post_movies_subtitles(
        self,
        *,
        radarrid: Annotated[int, Field(description="Movie ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
        file: Annotated[Any, Field(description="Subtitles file as file upload object")],
    ) -> Any:
        """Upload a movie subtitles

        POST /api/movies/subtitles
        """
        return self._request(
            "POST",
            "/api/movies/subtitles",
            params={
                "radarrid": radarrid,
                "language": language,
                "forced": forced,
                "hi": hi,
            },
            form={"file": file},
        )

    def patch_movies_subtitles(
        self,
        *,
        radarrid: Annotated[int, Field(description="Movie ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
    ) -> Any:
        """Download a movie subtitles

        PATCH /api/movies/subtitles
        """
        return self._request(
            "PATCH",
            "/api/movies/subtitles",
            params={
                "radarrid": radarrid,
                "language": language,
                "forced": forced,
                "hi": hi,
            },
        )

    def delete_movies_subtitles(
        self,
        *,
        radarrid: Annotated[int, Field(description="Movie ID")],
        language: Annotated[str, Field(description="Language code2")],
        forced: Annotated[str, Field(description="Forced true/false as string")],
        hi: Annotated[str, Field(description="HI true/false as string")],
        path: Annotated[str, Field(description="Path of the subtitles file")],
    ) -> Any:
        """Delete a movie subtitles

        DELETE /api/movies/subtitles
        """
        return self._request(
            "DELETE",
            "/api/movies/subtitles",
            params={
                "radarrid": radarrid,
                "language": language,
                "forced": forced,
                "hi": hi,
                "path": path,
            },
        )

    def get_movies_tags(self) -> Any:
        """List all distinct tags assigned to any movie

        GET /api/movies/tags
        """
        return self._request("GET", "/api/movies/tags")

    def get_movies_wanted(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        radarrid: Annotated[
            list[int] | None, Field(description="Movies ID to list")
        ] = None,
    ) -> Any:
        """List movies wanted subtitles

        GET /api/movies/wanted
        """
        return self._request(
            "GET",
            "/api/movies/wanted",
            params={"start": start, "length": length, "radarrid[]": radarrid},
        )

    def post_plex_api_key(
        self, *, apikey: Annotated[str, Field(description="API key")]
    ) -> Any:
        """post /plex/apikey

        POST /api/plex/apikey
        """
        return self._request("POST", "/api/plex/apikey", params={"apikey": apikey})

    def get_plex_autopulse_config(self) -> Any:
        """get /plex/autopulse/config

        GET /api/plex/autopulse/config
        """
        return self._request("GET", "/api/plex/autopulse/config")

    def post_plex_encrypt_api_key(self) -> Any:
        """post /plex/encrypt-apikey

        POST /api/plex/encrypt-apikey
        """
        return self._request("POST", "/api/plex/encrypt-apikey")

    def get_plex_libraries(self) -> Any:
        """get /plex/oauth/libraries

        GET /api/plex/oauth/libraries
        """
        return self._request("GET", "/api/plex/oauth/libraries")

    def post_plex_logout(self) -> Any:
        """post /plex/oauth/logout

        POST /api/plex/oauth/logout
        """
        return self._request("POST", "/api/plex/oauth/logout")

    def get_plex_pin(self) -> Any:
        """get /plex/oauth/pin

        GET /api/plex/oauth/pin
        """
        return self._request("GET", "/api/plex/oauth/pin")

    def post_plex_pin(
        self, *, client_id: Annotated[str | None, Field(description="Client ID")] = None
    ) -> Any:
        """post /plex/oauth/pin

        POST /api/plex/oauth/pin
        """
        return self._request(
            "POST", "/api/plex/oauth/pin", params={"clientId": client_id}
        )

    def get_plex_pin_check(
        self, *, pin_id: Annotated[str, Field(description="pin_id")]
    ) -> Any:
        """get /plex/oauth/pin/{pin_id}/check

        GET /api/plex/oauth/pin/{pin_id}/check
        """
        return self._request("GET", f"/api/plex/oauth/pin/{pin_id}/check")

    def get_plex_servers(self) -> Any:
        """get /plex/oauth/servers

        GET /api/plex/oauth/servers
        """
        return self._request("GET", "/api/plex/oauth/servers")

    def get_plex_validate(self) -> Any:
        """get /plex/oauth/validate

        GET /api/plex/oauth/validate
        """
        return self._request("GET", "/api/plex/oauth/validate")

    def get_plex_select_server(self) -> Any:
        """get /plex/select-server

        GET /api/plex/select-server
        """
        return self._request("GET", "/api/plex/select-server")

    def post_plex_select_server(
        self,
        *,
        machine_identifier: Annotated[str, Field(description="Machine identifier")],
        name: Annotated[str, Field(description="Server name")],
        uri: Annotated[str, Field(description="Connection URI")],
        local: Annotated[str | None, Field(description="Is local connection")] = None,
        connections: Annotated[str | None, Field(description="connections")] = None,
    ) -> Any:
        """post /plex/select-server

        POST /api/plex/select-server
        """
        return self._request(
            "POST",
            "/api/plex/select-server",
            params={
                "machineIdentifier": machine_identifier,
                "name": name,
                "uri": uri,
                "local": local,
            },
            data=_clean({"connections": connections}),
        )

    def get_plex_test_connection(self) -> Any:
        """get /plex/test-connection

        GET /api/plex/test-connection
        """
        return self._request("GET", "/api/plex/test-connection")

    def post_plex_test_connection(
        self, *, uri: Annotated[str, Field(description="Server URI")]
    ) -> Any:
        """post /plex/test-connection

        POST /api/plex/test-connection
        """
        return self._request("POST", "/api/plex/test-connection", params={"uri": uri})

    def post_plex_webhook_create(self) -> Any:
        """post /plex/webhook/create

        POST /api/plex/webhook/create
        """
        return self._request("POST", "/api/plex/webhook/create")

    def post_plex_webhook_delete(
        self, *, webhook_url: Annotated[str, Field(description="Webhook URL to delete")]
    ) -> Any:
        """post /plex/webhook/delete

        POST /api/plex/webhook/delete
        """
        return self._request(
            "POST", "/api/plex/webhook/delete", params={"webhook_url": webhook_url}
        )

    def get_plex_webhook_list(self) -> Any:
        """get /plex/webhook/list

        GET /api/plex/webhook/list
        """
        return self._request("GET", "/api/plex/webhook/list")

    def get_providers(
        self,
        *,
        history: Annotated[
            str | None, Field(description="Provider name for history stats")
        ] = None,
    ) -> Any:
        """Get providers status

        GET /api/providers
        """
        return self._request("GET", "/api/providers", params={"history": history})

    def post_providers(
        self,
        *,
        action: Annotated[str, Field(description='Action to perform from ["reset"]')],
    ) -> Any:
        """Reset providers status

        POST /api/providers
        """
        return self._request("POST", "/api/providers", params={"action": action})

    def get_provider_episodes(
        self, *, episodeid: Annotated[int, Field(description="Episode ID")]
    ) -> Any:
        """Search manually for an episode subtitles

        GET /api/providers/episodes
        """
        return self._request(
            "GET", "/api/providers/episodes", params={"episodeid": episodeid}
        )

    def post_provider_episodes(
        self,
        *,
        seriesid: Annotated[int, Field(description="Series ID")],
        episodeid: Annotated[int, Field(description="Episode ID")],
        hi: Annotated[str, Field(description='HI subtitles from ["True", "False"]')],
        forced: Annotated[
            str, Field(description='Forced subtitles from ["True", "False"]')
        ],
        original_format: Annotated[
            str,
            Field(description='Use original subtitles format from ["True", "False"]'),
        ],
        provider: Annotated[str, Field(description="Provider name")],
        subtitle: Annotated[str, Field(description="Subtitle ID as returned by GET")],
    ) -> Any:
        """Manually download an episode subtitles

        POST /api/providers/episodes
        """
        return self._request(
            "POST",
            "/api/providers/episodes",
            params={
                "seriesid": seriesid,
                "episodeid": episodeid,
                "hi": hi,
                "forced": forced,
                "original_format": original_format,
                "provider": provider,
                "subtitle": subtitle,
            },
        )

    def get_provider_movies(
        self, *, radarrid: Annotated[int, Field(description="Movie ID")]
    ) -> Any:
        """Search manually for a movie subtitles

        GET /api/providers/movies
        """
        return self._request(
            "GET", "/api/providers/movies", params={"radarrid": radarrid}
        )

    def post_provider_movies(
        self,
        *,
        radarrid: Annotated[int, Field(description="Movie ID")],
        hi: Annotated[str, Field(description='HI subtitles from ["True", "False"]')],
        forced: Annotated[
            str, Field(description='Forced subtitles from ["True", "False"]')
        ],
        original_format: Annotated[
            str,
            Field(description='Use original subtitles format from ["True", "False"]'),
        ],
        provider: Annotated[str, Field(description="Provider name")],
        subtitle: Annotated[str, Field(description="Subtitle ID as returned by GET")],
    ) -> Any:
        """Manually download a movie subtitles

        POST /api/providers/movies
        """
        return self._request(
            "POST",
            "/api/providers/movies",
            params={
                "radarrid": radarrid,
                "hi": hi,
                "forced": forced,
                "original_format": original_format,
                "provider": provider,
                "subtitle": subtitle,
            },
        )

    def get_series(
        self,
        *,
        start: Annotated[int | None, Field(description="Paging start integer")] = None,
        length: Annotated[
            int | None, Field(description="Paging length integer")
        ] = None,
        seriesid: Annotated[
            list[int] | None, Field(description="Series IDs to get metadata for")
        ] = None,
        sort_by: Annotated[str | None, Field(description="Column to sort by")] = None,
        sort_order: Annotated[str | None, Field(description="Sort direction")] = None,
        monitored: Annotated[
            str | None, Field(description="Filter by monitored status")
        ] = None,
        profileid: Annotated[
            str | None, Field(description='Filter by languages profile ID or "none"')
        ] = None,
        missing: Annotated[
            str | None, Field(description="Filter by missing subtitles")
        ] = None,
        audio_language: Annotated[
            str | None, Field(description="Filter by audio language name")
        ] = None,
        tags: Annotated[
            list[str] | None, Field(description="Tags to filter by")
        ] = None,
    ) -> Any:
        """List series metadata for specific series

        GET /api/series
        """
        return self._request(
            "GET",
            "/api/series",
            params={
                "start": start,
                "length": length,
                "seriesid[]": seriesid,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "monitored": monitored,
                "profileid": profileid,
                "missing": missing,
                "audio_language": audio_language,
                "tags[]": tags,
            },
        )

    def post_series(
        self,
        *,
        seriesid: Annotated[
            list[int] | None, Field(description="Sonarr series ID")
        ] = None,
        profileid: Annotated[
            list[str] | None, Field(description='Languages profile(s) ID or "none"')
        ] = None,
    ) -> Any:
        """Update specific series languages profile

        POST /api/series
        """
        return self._request(
            "POST", "/api/series", params={"seriesid": seriesid, "profileid": profileid}
        )

    def patch_series(
        self,
        *,
        seriesid: Annotated[int | None, Field(description="Sonarr series ID")] = None,
        action: Annotated[
            str | None,
            Field(
                description='Action to perform from ["scan-disk", "search-missing", "search-wanted", "sync"]'
            ),
        ] = None,
    ) -> Any:
        """Run actions on specific series

        PATCH /api/series
        """
        return self._request(
            "PATCH", "/api/series", params={"seriesid": seriesid, "action": action}
        )

    def get_series_tags(self) -> Any:
        """List all distinct tags assigned to any series

        GET /api/series/tags
        """
        return self._request("GET", "/api/series/tags")

    def get_subtitles(
        self,
        *,
        subtitles_path: Annotated[
            str, Field(description="External subtitles file path")
        ],
        sonarr_episode_id: Annotated[
            int | None, Field(description="Sonarr Episode ID")
        ] = None,
        radarr_movie_id: Annotated[
            int | None, Field(description="Radarr Movie ID")
        ] = None,
    ) -> Any:
        """Return available audio and embedded subtitles tracks with external subtitles

        GET /api/subtitles
        """
        return self._request(
            "GET",
            "/api/subtitles",
            params={
                "subtitlesPath": subtitles_path,
                "sonarrEpisodeId": sonarr_episode_id,
                "radarrMovieId": radarr_movie_id,
            },
        )

    def patch_subtitles(
        self,
        *,
        action: Annotated[
            str,
            Field(
                description='Action from ["sync", "translate", "extract" or mods name]'
            ),
        ],
        language: Annotated[str, Field(description="Language code2")],
        type: Annotated[str, Field(description='Media type from ["episode", "movie"]')],
        id: Annotated[int, Field(description="Media ID (episodeId, radarrId)")],
        path: Annotated[str | None, Field(description="Subtitles file path")] = None,
        forced: Annotated[
            str | None, Field(description='Forced subtitles from ["True", "False"]')
        ] = None,
        hi: Annotated[
            str | None, Field(description='HI subtitles from ["True", "False"]')
        ] = None,
        original_format: Annotated[
            str | None,
            Field(description='Use original subtitles format from ["True", "False"]'),
        ] = None,
        reference: Annotated[
            str | None,
            Field(
                description="Reference to use for sync from video file track number (a:0) or some subtitles file path"
            ),
        ] = None,
        max_offset_seconds: Annotated[
            str | None, Field(description="Maximum offset seconds to allow")
        ] = None,
        no_fix_framerate: Annotated[
            str | None,
            Field(description='Don\'t try to fix framerate from ["True", "False"]'),
        ] = None,
        gss: Annotated[
            str | None,
            Field(description='Use Golden-Section Search from ["True", "False"]'),
        ] = None,
        quality_min_score: Annotated[
            str | None, Field(description="Minimum quality score for sync (0.0-1.0)")
        ] = None,
        quality_max_offset_seconds: Annotated[
            str | None,
            Field(description="Maximum offset in seconds for quality checks"),
        ] = None,
        quality_max_framerate_deviation: Annotated[
            str | None, Field(description="Maximum framerate deviation (0.0-1.0)")
        ] = None,
        subtitles_id: Annotated[
            int | None,
            Field(
                description='Subtitles database ID (required for the "extract" action)'
            ),
        ] = None,
    ) -> Any:
        """Apply mods/tools on external subtitles

        PATCH /api/subtitles
        """
        return self._request(
            "PATCH",
            "/api/subtitles",
            params={
                "action": action,
                "language": language,
                "path": path,
                "type": type,
                "id": id,
                "forced": forced,
                "hi": hi,
                "original_format": original_format,
                "reference": reference,
                "max_offset_seconds": max_offset_seconds,
                "no_fix_framerate": no_fix_framerate,
                "gss": gss,
                "quality_min_score": quality_min_score,
                "quality_max_offset_seconds": quality_max_offset_seconds,
                "quality_max_framerate_deviation": quality_max_framerate_deviation,
                "subtitles_id": subtitles_id,
            },
        )

    def get_subtitle_name_contents(
        self, *, subtitle_path: Annotated[str, Field(description="Subtitle filepath")]
    ) -> Any:
        """Retrieve subtitle file contents

        GET /api/subtitles/contents
        """
        return self._request(
            "GET", "/api/subtitles/contents", params={"subtitlePath": subtitle_path}
        )

    def get_subtitle_name_info(
        self,
        *,
        filenames: Annotated[list[str], Field(description="Subtitles filenames")],
    ) -> Any:
        """Guessit over subtitles filename

        GET /api/subtitles/info
        """
        return self._request(
            "GET", "/api/subtitles/info", params={"filenames[]": filenames}
        )

    def get_system_announcements(self) -> Any:
        """List announcements relative to Bazarr

        GET /api/system/announcements
        """
        return self._request("GET", "/api/system/announcements")

    def post_system_announcements(
        self,
        *,
        hash: Annotated[str, Field(description="hash of the announcement to dismiss")],
    ) -> Any:
        """Mark announcement as dismissed

        POST /api/system/announcements
        """
        return self._request("POST", "/api/system/announcements", params={"hash": hash})

    def get_system_backups(self) -> Any:
        """List backup files

        GET /api/system/backups
        """
        return self._request("GET", "/api/system/backups")

    def post_system_backups(self) -> Any:
        """Create a new backup

        POST /api/system/backups
        """
        return self._request("POST", "/api/system/backups")

    def patch_system_backups(
        self,
        *,
        filename: Annotated[str, Field(description="Backups to restore filename")],
    ) -> Any:
        """Restore a backup file

        PATCH /api/system/backups
        """
        return self._request(
            "PATCH", "/api/system/backups", params={"filename": filename}
        )

    def delete_system_backups(
        self,
        *,
        filename: Annotated[str, Field(description="Backups to delete filename")],
    ) -> Any:
        """Delete a backup file

        DELETE /api/system/backups
        """
        return self._request(
            "DELETE", "/api/system/backups", params={"filename": filename}
        )

    def get_system_health(self) -> Any:
        """List health issues

        GET /api/system/health
        """
        return self._request("GET", "/api/system/health")

    def get_system_jobs(
        self,
        *,
        id: Annotated[int | None, Field(description="Job ID to return")] = None,
        status: Annotated[str | None, Field(description="Job status to return")] = None,
    ) -> Any:
        """List jobs from the queue

        GET /api/system/jobs
        """
        return self._request(
            "GET", "/api/system/jobs", params={"id": id, "status": status}
        )

    def post_system_jobs(
        self,
        *,
        id: Annotated[int, Field(description="Job ID act onto")],
        action: Annotated[
            str,
            Field(
                description='Action to perform from ["force_start", "move_top", "move_bottom"]'
            ),
        ],
    ) -> Any:
        """Force start, move to top or move to bottom of the queue a specific job

        POST /api/system/jobs
        """
        return self._request(
            "POST", "/api/system/jobs", params={"id": id, "action": action}
        )

    def patch_system_jobs(
        self,
        *,
        queue_name: Annotated[str, Field(description="Jobs queue name to empty")],
    ) -> Any:
        """Empty a specific jobs queue

        PATCH /api/system/jobs
        """
        return self._request(
            "PATCH", "/api/system/jobs", params={"queueName": queue_name}
        )

    def delete_system_jobs(
        self, *, id: Annotated[int, Field(description="Job ID to delete from queue")]
    ) -> Any:
        """Delete a job from the queue

        DELETE /api/system/jobs
        """
        return self._request("DELETE", "/api/system/jobs", params={"id": id})

    def get_languages(
        self,
        *,
        history: Annotated[
            str | None, Field(description="Language name for history stats")
        ] = None,
    ) -> Any:
        """List languages for history filter or for language filter menu

        GET /api/system/languages
        """
        return self._request(
            "GET", "/api/system/languages", params={"history": history}
        )

    def get_languages_profiles(self) -> Any:
        """List languages profiles

        GET /api/system/languages/profiles
        """
        return self._request("GET", "/api/system/languages/profiles")

    def get_system_logs(self) -> Any:
        """List log entries

        GET /api/system/logs
        """
        return self._request("GET", "/api/system/logs")

    def delete_system_logs(self) -> Any:
        """Force log rotation and create a new log file

        DELETE /api/system/logs
        """
        return self._request("DELETE", "/api/system/logs")

    def get_system_ping(self) -> Any:
        """Return status and http 200

        GET /api/system/ping
        """
        return self._request("GET", "/api/system/ping")

    def get_system_releases(self) -> Any:
        """Get Bazarr releases

        GET /api/system/releases
        """
        return self._request("GET", "/api/system/releases")

    def get_searches(
        self,
        *,
        query: Annotated[str, Field(description="Series or movie name to search for")],
    ) -> Any:
        """List results from query

        GET /api/system/searches
        """
        return self._request("GET", "/api/system/searches", params={"query": query})

    def get_system_status(self) -> Any:
        """Return environment information and versions

        GET /api/system/status
        """
        return self._request("GET", "/api/system/status")

    def get_system_tasks(self) -> Any:
        """List tasks

        GET /api/system/tasks
        """
        return self._request("GET", "/api/system/tasks")

    def post_system_tasks(
        self, *, taskid: Annotated[str, Field(description="Task id of the task to run")]
    ) -> Any:
        """Run task

        POST /api/system/tasks
        """
        return self._request("POST", "/api/system/tasks", params={"taskid": taskid})

    def post_system_webhook_test(self) -> Any:
        """Test external webhook connection

        POST /api/system/webhooks/test
        """
        return self._request("POST", "/api/system/webhooks/test")

    def post_web_hooks_plex(
        self, *, payload: Annotated[str, Field(description="Webhook payload")]
    ) -> Any:
        """Trigger subtitles search on play media event in Plex

        POST /api/webhooks/plex
        """
        return self._request("POST", "/api/webhooks/plex", params={"payload": payload})

    def post_web_hooks_radarr(
        self,
        *,
        event_type: Annotated[
            str, Field(description="Type of Radarr event (e.g. MovieAdded, Test, etc)")
        ],
        movie_file: Annotated[
            dict[str, Any] | None,
            Field(
                description="Radarr movie file payload. Required for anything other than test hooks"
            ),
        ] = None,
        movie: Annotated[
            dict[str, Any] | None,
            Field(
                description="Radarr movie payload. Can be used to sync movies from Radarr if not found in Bazarr"
            ),
        ] = None,
    ) -> Any:
        """Search for missing subtitles based on Radarr webhooks

        POST /api/webhooks/radarr
        """
        return self._request(
            "POST",
            "/api/webhooks/radarr",
            data=_clean(
                {"eventType": event_type, "movieFile": movie_file, "movie": movie}
            ),
        )

    def post_web_hooks_sonarr(
        self,
        *,
        event_type: Annotated[
            str, Field(description="Type of Sonarr event (e.g. Test, Download, etc.)")
        ],
        episodes: Annotated[
            list[dict[str, Any]] | None,
            Field(
                description="List of episodes. Can be used to sync episodes from Sonarr if not found in Bazarr."
            ),
        ] = None,
        episode_files: Annotated[
            list[dict[str, Any]] | None,
            Field(
                description="List of episode files; required for anything other than test hooks"
            ),
        ] = None,
    ) -> Any:
        """Search for missing subtitles based on Sonarr webhooks

        POST /api/webhooks/sonarr
        """
        return self._request(
            "POST",
            "/api/webhooks/sonarr",
            data=_clean(
                {
                    "episodes": episodes,
                    "episodeFiles": episode_files,
                    "eventType": event_type,
                }
            ),
        )
