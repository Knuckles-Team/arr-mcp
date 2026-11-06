"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "arr-check-download-queue",
        (
            ToolStep(
                "radarr_get_queue_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_queue",
                params=("page", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_queue_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_queue",
                params=("page", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_queue_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_queue",
                params=("page", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_queue_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read every app's queue summary and items to find stalled, failed or warning downloads.",
    ),
    ToolUseContract(
        "arr-ingest-library",
        (
            ToolStep(
                "arr_ingest_library",
                params=("services",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Ingest movies, series and indexers as typed graph nodes (Film, Series, MediaIndexer, QualityProfile).",
    ),
    ToolUseContract(
        "arr-remove-stalled-download",
        (
            ToolStep(
                "radarr_get_queue",
                params=("status", "includeMovie"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_queue_id",
                params=("id", "removeFromClient", "blocklist", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Remove one stalled or failed queue item, blocklist the release so it is not grabbed again, and search again.",
    ),
    ToolUseContract(
        "arr-repair-download-client",
        (
            ToolStep(
                "radarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_downloadclient",
                params=(),
                result=("id",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_downloadclient_test",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_downloadclient_id",
                params=("id", "data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_downloadclient_test",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="When an app reports every download client unavailable, read the client's own failure reason, fix the setting with approval and confirm the test passes.",
    ),
    ToolUseContract(
        "arr-suite-health-check",
        (
            ToolStep(
                "radarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read every app's status and health, and report versions, connectivity and open health issues.",
    ),
    ToolUseContract(
        "bazarr-connect-sonarr-radarr",
        (
            ToolStep(
                "bazarr_get_system_settings",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_settings",
                params=("settings",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_tasks",
                params=("taskid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_badges",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Point Bazarr at the Sonarr and Radarr instances, sync their series and movies, and confirm both links are live.",
    ),
    ToolUseContract(
        "bazarr-download-wanted-subtitles",
        (
            ToolStep(
                "bazarr_get_system_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_providers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_episodes_wanted",
                params=("length",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_episodes_subtitles",
                params=("seriesid", "episodeid", "language", "forced", "hi"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_movies_wanted",
                params=("length",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_movies_subtitles",
                params=("radarrid", "language", "forced", "hi"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Check that Bazarr is connected to Sonarr and Radarr, list the episodes and movies missing subtitles, and download one for each.",
    ),
    ToolUseContract(
        "bazarr-enable-free-providers",
        (
            ToolStep(
                "bazarr_get_system_settings",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_languages_profiles",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_settings",
                params=("settings",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_providers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_movies_wanted",
                params=("length",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_provider_movies",
                params=("radarrid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_episodes_wanted",
                params=("length",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_provider_episodes",
                params=("episodeid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Enable the subtitle providers that need no account, create the default language profile, and prove a search returns subtitles for one movie and one episode.",
    ),
    ToolUseContract(
        "bazarr-reset-providers",
        (
            ToolStep(
                "bazarr_get_providers",
                params=("history",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_providers_reset",
                params=("action",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read the provider status and reset throttled providers with approval.",
    ),
    ToolUseContract(
        "chaptarr-add-author-and-search",
        (
            ToolStep(
                "chaptarr_get_rootfolder",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_qualityprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_metadataprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_author_lookup",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_author",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Resolve the book library location and profiles, look the author up and add them with a missing-book search. Stops when no root folder is configured.",
    ),
    ToolUseContract(
        "chaptarr-provision-book-library",
        (
            ToolStep(
                "chaptarr_get_rootfolder",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_qualityprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_metadataprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_rootfolder",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_downloadclient_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_downloadclient_test",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_downloadclient",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_applications_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_applications_test",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_applications",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Give Chaptarr its book root folder, qBittorrent as download client, and a Prowlarr link for book indexers.",
    ),
    ToolUseContract(
        "chaptarr-search-missing",
        (
            ToolStep(
                "chaptarr_get_wanted_missing",
                params=("monitored",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List monitored books with no file and start one book search.",
    ),
    ToolUseContract(
        "lidarr-add-artist-and-search",
        (
            ToolStep(
                "lidarr_get_rootfolder",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_qualityprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_metadataprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_artist_lookup",
                params=("term",),
                result=("foreignArtistId",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_artist",
                params=("mbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_artist",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Resolve the music library location, quality and metadata profiles, look the artist up and add them with a missing-album search.",
    ),
    ToolUseContract(
        "lidarr-search-missing",
        (
            ToolStep(
                "lidarr_get_wanted_missing",
                params=("monitored", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List monitored albums with no files and start one album search.",
    ),
    ToolUseContract(
        "prowlarr-fix-failing-indexer",
        (
            ToolStep(
                "prowlarr_get_indexerstatus",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_health",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_indexerproxy",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_indexer_id",
                params=("id", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Find indexers Prowlarr has disabled after failures, read the failure, retest, and change the indexer settings only with approval.",
    ),
    ToolUseContract(
        "prowlarr-replace-dead-indexer",
        (
            ToolStep(
                "prowlarr_get_indexer_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_delete_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="After the fix-a-failing-indexer workflow shows an indexer cannot work (domain gone, TLS broken on every mirror, Cloudflare the proxy cannot solve), add a tested public replacement, remove the dead one and sync the apps.",
    ),
    ToolUseContract(
        "prowlarr-search-releases",
        (
            ToolStep(
                "prowlarr_get_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_search",
                params=("query", "type", "limit"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Run one manual search across the enabled indexers.",
    ),
    ToolUseContract(
        "prowlarr-sync-indexers",
        (
            ToolStep(
                "prowlarr_get_applications",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Push the Prowlarr indexer pool to every connected app (Radarr, Sonarr, Lidarr).",
    ),
    ToolUseContract(
        "radarr-add-and-search",
        (
            ToolStep(
                "radarr_get_rootfolder",
                params=(),
                result=("path",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_qualityprofile",
                params=(),
                result=("id",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_movie_lookup",
                params=("term",),
                result=("tmdbId",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_movie",
                params=("tmdbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_add_movie",
                params=(
                    "term",
                    "root_folder_path",
                    "quality_profile_id",
                    "monitored",
                    "search_for_movie",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_queue",
                params=("page", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Resolve the movie library location and quality profile, look the title up, add it monitored and start a search, then confirm it reached the download queue.",
    ),
    ToolUseContract(
        "radarr-search-missing",
        (
            ToolStep(
                "radarr_get_wanted_missing",
                params=("monitored", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List the monitored items that have no file and start one search command for them.",
    ),
    ToolUseContract(
        "radarr-tag-roundtrip",
        (
            ToolStep(
                "radarr_get_tag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_tag",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_tag_id",
                params=("id", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Create a tag to group items, verify it, and delete it again when it was only a test.",
    ),
    ToolUseContract(
        "seerr-request-title",
        (
            ToolStep(
                "seerr_get_search",
                params=("query",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_movie_id",
                params=("movie_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_request",
                params=("media_type", "media_id", "is4k"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_request",
                params=("filter", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Search the catalogue and file a request that Seerr routes to Radarr or Sonarr.",
    ),
    ToolUseContract(
        "seerr-retry-failed",
        (
            ToolStep(
                "seerr_get_request",
                params=("filter",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_radarr",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_request_id_retry",
                params=("request_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List failed requests and retry each one after the routing problem is fixed.",
    ),
    ToolUseContract(
        "seerr-route-requests-by-quality",
        (
            ToolStep(
                "seerr_get_settings_radarr",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_qualityprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_radarr_test",
                params=("hostname", "port", "api_key", "use_ssl"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_radarr",
                params=("is4k", "is_default", "active_profile_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_settings_radarr_id",
                params=("radarr_id", "active_profile_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_sonarr",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_sonarr",
                params=("is4k", "is_default"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_settings_sonarr_id",
                params=("sonarr_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Give Seerr a default non-4K Radarr and Sonarr server with the 1080p profile, and keep the 4K servers for 4K requests with the 4K profile.",
    ),
    ToolUseContract(
        "seerr-triage-requests",
        (
            ToolStep(
                "seerr_get_request_count",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_request",
                params=("filter", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_request_id",
                params=("request_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_service_radarr",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_service_sonarr",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_request_id_status",
                params=("request_id", "status"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Count and list pending requests, read each one, check where it will route, and approve or decline it with approval.",
    ),
    ToolUseContract(
        "sonarr-add-and-search",
        (
            ToolStep(
                "sonarr_get_rootfolder",
                params=(),
                result=("path",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_qualityprofile",
                params=(),
                result=("id",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_series_lookup",
                params=("term",),
                result=("tvdbId",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_series",
                params=("tvdbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_add_series",
                params=(
                    "term",
                    "root_folder_path",
                    "quality_profile_id",
                    "monitored",
                    "search_for_missing_episodes",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_queue",
                params=("page", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Resolve the TV library location and quality profile, look the title up, add it monitored and start a search, then confirm it reached the download queue.",
    ),
    ToolUseContract(
        "sonarr-search-missing",
        (
            ToolStep(
                "sonarr_get_wanted_missing",
                params=("monitored", "pageSize"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_command",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_queue",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="List the monitored items that have no file and start one search command for them.",
    ),
    ToolUseContract(
        "sonarr-tag-roundtrip",
        (
            ToolStep(
                "sonarr_get_tag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_tag",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_tag_id",
                params=("id", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Create a tag to group items, verify it, and delete it again when it was only a test.",
    ),
    ToolUseContract(
        "bazarr-manage-browse",
        (
            ToolStep(
                "bazarr_get_browse_bazarr_fs",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_browse_radarr_fs",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_browse_sonarr_fs",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change browse on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-episodes",
        (
            ToolStep(
                "bazarr_get_episodes",
                params=("episodeid", "seriesid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_episodes_blacklist",
                params=("length", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_episodes_history",
                params=("episodeid", "length", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_episodes_blacklist",
                params=(
                    "episodeid",
                    "language",
                    "provider",
                    "seriesid",
                    "subs_id",
                    "subtitles_path",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_episodes_subtitles",
                params=("episodeid", "file", "forced", "hi", "language", "seriesid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_episodes_blacklist",
                params=("all", "confirm", "provider", "subs_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_episodes_subtitles",
                params=(
                    "confirm",
                    "episodeid",
                    "forced",
                    "hi",
                    "language",
                    "path",
                    "seriesid",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change episodes on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-history",
        (
            ToolStep(
                "bazarr_get_history_stats",
                params=("action_type", "language", "provider", "time_frame"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change history on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-jellyfin",
        (
            ToolStep(
                "bazarr_get_jellyfin_libraries",
                params=("apikey", "url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_jellyfin_test_connection",
                params=("apikey", "url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change jellyfin on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-languages",
        (
            ToolStep(
                "bazarr_get_languages",
                params=("history",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change languages on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-movies",
        (
            ToolStep(
                "bazarr_get_movies",
                params=(
                    "audio_language",
                    "length",
                    "missing",
                    "monitored",
                    "profileid",
                    "radarrid",
                    "sort_by",
                    "sort_order",
                    "start",
                    "tags",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_movies_blacklist",
                params=("length", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_movies_history",
                params=("length", "radarrid", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_movies_tags",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_movies",
                params=("profileid", "radarrid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_movies_blacklist",
                params=(
                    "language",
                    "provider",
                    "radarrid",
                    "subs_id",
                    "subtitles_path",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_movies_subtitles",
                params=("file", "forced", "hi", "language", "radarrid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_movies_scan_disk",
                params=("radarrid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_movies_search_missing",
                params=("radarrid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_movies_search_wanted",
                params=("radarrid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_movies_sync",
                params=("radarrid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_movies_blacklist",
                params=("all", "confirm", "provider", "subs_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_movies_subtitles",
                params=("confirm", "forced", "hi", "language", "path", "radarrid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change movies on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-plex",
        (
            ToolStep(
                "bazarr_get_plex_autopulse_config",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_libraries",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_pin",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_pin_check",
                params=("pin_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_select_server",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_servers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_test_connection",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_validate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_plex_webhook_list",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_api_key",
                params=("apikey",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_encrypt_api_key",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_pin",
                params=("client_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_select_server",
                params=("connections", "local", "machine_identifier", "name", "uri"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_test_connection",
                params=("uri",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_webhook_create",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_plex_webhook_delete",
                params=("confirm", "webhook_url"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change plex on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-provider",
        (
            ToolStep(
                "bazarr_post_provider_episodes",
                params=(
                    "episodeid",
                    "forced",
                    "hi",
                    "original_format",
                    "provider",
                    "seriesid",
                    "subtitle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_provider_movies",
                params=(
                    "forced",
                    "hi",
                    "original_format",
                    "provider",
                    "radarrid",
                    "subtitle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change provider on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-searches",
        (
            ToolStep(
                "bazarr_get_searches",
                params=("query",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change searches on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-series",
        (
            ToolStep(
                "bazarr_get_series",
                params=(
                    "audio_language",
                    "length",
                    "missing",
                    "monitored",
                    "profileid",
                    "seriesid",
                    "sort_by",
                    "sort_order",
                    "start",
                    "tags",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_series_tags",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_series",
                params=("profileid", "seriesid"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_series_scan_disk",
                params=("seriesid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_series_search_missing",
                params=("seriesid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_series_search_wanted",
                params=("seriesid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_series_sync",
                params=("seriesid",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change series on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-subtitle",
        (
            ToolStep(
                "bazarr_get_subtitle_name_contents",
                params=("subtitle_path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_subtitle_name_info",
                params=("filenames",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change subtitle on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-subtitles",
        (
            ToolStep(
                "bazarr_get_subtitles",
                params=("radarr_movie_id", "sonarr_episode_id", "subtitles_path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_subtitles_extract",
                params=(
                    "forced",
                    "gss",
                    "hi",
                    "id",
                    "language",
                    "max_offset_seconds",
                    "no_fix_framerate",
                    "original_format",
                    "path",
                    "quality_max_framerate_deviation",
                    "quality_max_offset_seconds",
                    "quality_min_score",
                    "reference",
                    "subtitles_id",
                    "type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_subtitles_mod",
                params=(
                    "forced",
                    "gss",
                    "hi",
                    "id",
                    "language",
                    "max_offset_seconds",
                    "mod",
                    "no_fix_framerate",
                    "original_format",
                    "path",
                    "quality_max_framerate_deviation",
                    "quality_max_offset_seconds",
                    "quality_min_score",
                    "reference",
                    "subtitles_id",
                    "type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_subtitles_sync",
                params=(
                    "forced",
                    "gss",
                    "hi",
                    "id",
                    "language",
                    "max_offset_seconds",
                    "no_fix_framerate",
                    "original_format",
                    "path",
                    "quality_max_framerate_deviation",
                    "quality_max_offset_seconds",
                    "quality_min_score",
                    "reference",
                    "subtitles_id",
                    "type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_subtitles_translate",
                params=(
                    "forced",
                    "gss",
                    "hi",
                    "id",
                    "language",
                    "max_offset_seconds",
                    "no_fix_framerate",
                    "original_format",
                    "path",
                    "quality_max_framerate_deviation",
                    "quality_max_offset_seconds",
                    "quality_min_score",
                    "reference",
                    "subtitles_id",
                    "type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change subtitles on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-system",
        (
            ToolStep(
                "bazarr_get_system_announcements",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_backups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_jobs",
                params=("id", "status"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_logs",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_releases",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_get_system_tasks",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_announcements",
                params=("hash",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_backups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_jobs_force_start",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_jobs_move_bottom",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_jobs_move_top",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_system_webhook_test",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_system_backups",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_system_jobs",
                params=("queue_name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_patch_system_notifications",
                params=("url",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_system_backups",
                params=("confirm", "filename"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_system_jobs",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "bazarr_delete_system_logs",
                params=("confirm",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "bazarr-manage-web",
        (
            ToolStep(
                "bazarr_post_web_hooks_plex",
                params=("payload",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_web_hooks_radarr",
                params=("event_type", "movie", "movie_file"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "bazarr_post_web_hooks_sonarr",
                params=("episode_files", "episodes", "event_type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change web on bazarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-",
        (
            ToolStep(
                "chaptarr_get_",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change  on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-api",
        (
            ToolStep(
                "chaptarr_get_api",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change api on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-author",
        (
            ToolStep(
                "chaptarr_get_author",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_author_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_author_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_author_id",
                params=("data", "id", "moveFiles"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_author_editor",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_author_id",
                params=("addImportListExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change author on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-blocklist",
        (
            ToolStep(
                "chaptarr_get_blocklist",
                params=("page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_blocklist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_blocklist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blocklist on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-book",
        (
            ToolStep(
                "chaptarr_get_book",
                params=("authorId", "bookIds", "includeAllAuthorBooks", "titleSlug"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_book_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_book_id_overview",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_book_lookup",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_book",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_book_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_book_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_book_monitor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_book_editor",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_book_id",
                params=("addImportListExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change book on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-bookfile",
        (
            ToolStep(
                "chaptarr_get_bookfile",
                params=("authorId", "bookFileIds", "bookId", "unmapped"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_bookfile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_bookfile_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_bookfile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_bookfile_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_bookfile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change bookfile on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-bookshelf",
        (
            ToolStep(
                "chaptarr_post_bookshelf",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change bookshelf on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-calendar",
        (
            ToolStep(
                "chaptarr_get_calendar",
                params=("end", "includeAuthor", "start", "unmonitored"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_calendar_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change calendar on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-command",
        (
            ToolStep(
                "chaptarr_get_command",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_command_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_command_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change command on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-config",
        (
            ToolStep(
                "chaptarr_get_config_development",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_development_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_host",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_host_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_mediamanagement",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_mediamanagement_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_metadataprovider",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_metadataprovider_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_naming",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_naming_examples",
                params=(
                    "authorFolderFormat",
                    "colonReplacementFormat",
                    "id",
                    "includeAuthorName",
                    "includeBookTitle",
                    "includeQuality",
                    "numberStyle",
                    "renameBooks",
                    "replaceIllegalCharacters",
                    "replaceSpaces",
                    "resourceName",
                    "separator",
                    "standardBookFormat",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_naming_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_ui",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_config_ui_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_development_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_downloadclient_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_host_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_indexer_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_mediamanagement_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_metadataprovider_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_naming_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_config_ui_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change config on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-content",
        (
            ToolStep(
                "chaptarr_get_content_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change content on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-customfilter",
        (
            ToolStep(
                "chaptarr_get_customfilter",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_customfilter_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_customfilter",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_customfilter_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_customfilter_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customfilter on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-customformat",
        (
            ToolStep(
                "chaptarr_get_customformat",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_customformat_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_customformat_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_customformat",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_customformat_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_customformat_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customformat on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-delayprofile",
        (
            ToolStep(
                "chaptarr_get_delayprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_delayprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_delayprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_delayprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_delayprofile_reorder_id",
                params=("afterId", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_delayprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change delayprofile on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-diskspace",
        (
            ToolStep(
                "chaptarr_get_diskspace",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change diskspace on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-downloadclient",
        (
            ToolStep(
                "chaptarr_get_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_downloadclient_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_downloadclient_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_downloadclient_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_downloadclient_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_downloadclient_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_downloadclient_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change downloadclient on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-edition",
        (
            ToolStep(
                "chaptarr_get_edition",
                params=("bookId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change edition on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-feed",
        (
            ToolStep(
                "chaptarr_get_feed_v1_calendar_readarrics",
                params=("futureDays", "pastDays", "tagList", "unmonitored"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change feed on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-filesystem",
        (
            ToolStep(
                "chaptarr_get_filesystem",
                params=("allowFoldersWithoutTrailingSlashes", "includeFiles", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_filesystem_mediafiles",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_filesystem_type",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change filesystem on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-history",
        (
            ToolStep(
                "chaptarr_get_history",
                params=(
                    "bookId",
                    "downloadId",
                    "eventType",
                    "includeAuthor",
                    "includeBook",
                    "page",
                    "pageSize",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_history_author",
                params=(
                    "authorId",
                    "bookId",
                    "eventType",
                    "includeAuthor",
                    "includeBook",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_history_since",
                params=("date", "eventType", "includeAuthor", "includeBook"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_history_failed_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change history on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-importlist",
        (
            ToolStep(
                "chaptarr_get_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_importlist_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_importlist",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_importlist_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_importlist_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_importlist_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_importlist_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_importlist_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_importlist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_importlist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlist on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-importlistexclusion",
        (
            ToolStep(
                "chaptarr_get_importlistexclusion",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_importlistexclusion_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_importlistexclusion",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_importlistexclusion_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_importlistexclusion_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlistexclusion on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-indexer",
        (
            ToolStep(
                "chaptarr_get_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_indexer_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_indexer",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_indexer_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_indexer_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_indexer_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_indexer_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_indexer_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_indexer_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexer on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-indexerflag",
        (
            ToolStep(
                "chaptarr_get_indexerflag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change indexerflag on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-language",
        (
            ToolStep(
                "chaptarr_get_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_language_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change language on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-localization",
        (
            ToolStep(
                "chaptarr_get_localization",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change localization on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-log",
        (
            ToolStep(
                "chaptarr_get_log",
                params=("level", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_log_file",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_log_file_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_log_file_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_log_file_update_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-login",
        (
            ToolStep(
                "chaptarr_get_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_login",
                params=("returnUrl",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change login on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-logout",
        (
            ToolStep(
                "chaptarr_get_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change logout on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-manualimport",
        (
            ToolStep(
                "chaptarr_get_manualimport",
                params=(
                    "authorId",
                    "downloadId",
                    "filterExistingFiles",
                    "folder",
                    "replaceExistingFiles",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_manualimport",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change manualimport on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-mediacover",
        (
            ToolStep(
                "chaptarr_get_mediacover_author_author_id_filename",
                params=("authorId", "filename"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_mediacover_book_book_id_filename",
                params=("bookId", "filename"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change mediacover on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-metadata",
        (
            ToolStep(
                "chaptarr_get_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_metadata_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_metadata_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_metadata",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_metadata_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_metadata_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_metadata_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_metadata_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_metadata_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadata on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-metadataprofile",
        (
            ToolStep(
                "chaptarr_get_metadataprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_metadataprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_metadataprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_metadataprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_metadataprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadataprofile on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-notification",
        (
            ToolStep(
                "chaptarr_get_notification",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_notification_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_notification_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_notification",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_notification_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_notification_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_notification_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_notification_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_notification_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change notification on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-parse",
        (
            ToolStep(
                "chaptarr_get_parse",
                params=("title",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change parse on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-path",
        (
            ToolStep(
                "chaptarr_get_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change path on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-ping",
        (
            ToolStep(
                "chaptarr_get_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change ping on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-qualitydefinition",
        (
            ToolStep(
                "chaptarr_get_qualitydefinition",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_qualitydefinition_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_qualitydefinition_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_qualitydefinition_update",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change qualitydefinition on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-qualityprofile",
        (
            ToolStep(
                "chaptarr_get_qualityprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_qualityprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_qualityprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_qualityprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_qualityprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change qualityprofile on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-queue",
        (
            ToolStep(
                "chaptarr_get_queue_details",
                params=("authorId", "bookIds", "includeAuthor", "includeBook"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_queue_grab_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_queue_grab_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_queue_bulk",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "data",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_queue_id",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "id",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change queue on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-release",
        (
            ToolStep(
                "chaptarr_get_release",
                params=("authorId", "bookId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_release",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_release_push",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change release on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-releaseprofile",
        (
            ToolStep(
                "chaptarr_get_releaseprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_releaseprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_releaseprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_releaseprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_releaseprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change releaseprofile on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-remotepathmapping",
        (
            ToolStep(
                "chaptarr_get_remotepathmapping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_remotepathmapping_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_remotepathmapping",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_remotepathmapping_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_remotepathmapping_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change remotepathmapping on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-rename",
        (
            ToolStep(
                "chaptarr_get_rename",
                params=("authorId", "bookId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change rename on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-retag",
        (
            ToolStep(
                "chaptarr_get_retag",
                params=("authorId", "bookId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change retag on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-rootfolder",
        (
            ToolStep(
                "chaptarr_get_rootfolder_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_put_rootfolder_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_rootfolder_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change rootfolder on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-search",
        (
            ToolStep(
                "chaptarr_get_search",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change search on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-series",
        (
            ToolStep(
                "chaptarr_get_series",
                params=("authorId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change series on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-system",
        (
            ToolStep(
                "chaptarr_get_system_backup",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_system_routes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_system_routes_duplicate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_system_task",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_system_task_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_system_backup_restore_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_system_backup_restore_upload",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_delete_system_backup_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-tag",
        (
            ToolStep(
                "chaptarr_get_tag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_tag_detail",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_tag_detail_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_tag_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_post_tag",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_put_tag_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_delete_tag_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change tag on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-update",
        (
            ToolStep(
                "chaptarr_get_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change update on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "chaptarr-manage-wanted",
        (
            ToolStep(
                "chaptarr_get_wanted_cutoff",
                params=(
                    "includeAuthor",
                    "monitored",
                    "page",
                    "pageSize",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "chaptarr_get_wanted_cutoff_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "chaptarr_get_wanted_missing_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change wanted on chaptarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-",
        (
            ToolStep(
                "lidarr_get_",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change  on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-album",
        (
            ToolStep(
                "lidarr_get_album",
                params=(
                    "albumIds",
                    "artistId",
                    "foreignAlbumId",
                    "includeAllArtistAlbums",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_album_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_album_lookup",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_album",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_album_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_album_monitor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_album_id",
                params=("addImportListExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change album on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-albumstudio",
        (
            ToolStep(
                "lidarr_post_albumstudio",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change albumstudio on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-api",
        (
            ToolStep(
                "lidarr_get_api",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change api on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-artist",
        (
            ToolStep(
                "lidarr_get_artist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_artist_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_artist_id",
                params=("data", "id", "moveFiles"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_artist_editor",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_artist_id",
                params=("addImportListExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change artist on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-autotagging",
        (
            ToolStep(
                "lidarr_get_autotagging",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_autotagging_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_autotagging_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_autotagging",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_autotagging_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_autotagging_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change autotagging on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-blocklist",
        (
            ToolStep(
                "lidarr_get_blocklist",
                params=("page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_blocklist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_blocklist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blocklist on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-calendar",
        (
            ToolStep(
                "lidarr_get_calendar",
                params=("end", "includeArtist", "start", "tags", "unmonitored"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_calendar_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change calendar on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-command",
        (
            ToolStep(
                "lidarr_get_command",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_command_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_command_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change command on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-config",
        (
            ToolStep(
                "lidarr_get_config_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_host",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_host_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_mediamanagement",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_mediamanagement_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_metadataprovider",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_metadataprovider_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_naming",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_naming_examples",
                params=(
                    "artistFolderFormat",
                    "colonReplacementFormat",
                    "id",
                    "includeAlbumTitle",
                    "includeArtistName",
                    "includeQuality",
                    "multiDiscTrackFormat",
                    "numberStyle",
                    "renameTracks",
                    "replaceIllegalCharacters",
                    "replaceSpaces",
                    "resourceName",
                    "separator",
                    "standardTrackFormat",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_naming_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_config_ui",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_config_ui_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_downloadclient_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_host_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_indexer_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_mediamanagement_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_metadataprovider_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_naming_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_config_ui_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change config on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-content",
        (
            ToolStep(
                "lidarr_get_content_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change content on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-customfilter",
        (
            ToolStep(
                "lidarr_get_customfilter",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_customfilter_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_customfilter",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_customfilter_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_customfilter_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customfilter on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-customformat",
        (
            ToolStep(
                "lidarr_get_customformat",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_customformat_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_customformat_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_customformat",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_customformat_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_customformat_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_customformat_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_customformat_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customformat on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-delayprofile",
        (
            ToolStep(
                "lidarr_get_delayprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_delayprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_delayprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_delayprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_delayprofile_reorder_id",
                params=("afterId", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_delayprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change delayprofile on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-diskspace",
        (
            ToolStep(
                "lidarr_get_diskspace",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change diskspace on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-downloadclient",
        (
            ToolStep(
                "lidarr_get_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_downloadclient_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_downloadclient",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_downloadclient_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_downloadclient_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_downloadclient_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_downloadclient_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_downloadclient_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_downloadclient_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_downloadclient_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change downloadclient on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-feed",
        (
            ToolStep(
                "lidarr_get_feed_v1_calendar_lidarrics",
                params=("futureDays", "pastDays", "tags", "unmonitored"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change feed on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-filesystem",
        (
            ToolStep(
                "lidarr_get_filesystem",
                params=("allowFoldersWithoutTrailingSlashes", "includeFiles", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_filesystem_mediafiles",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_filesystem_type",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change filesystem on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-history",
        (
            ToolStep(
                "lidarr_get_history",
                params=(
                    "albumId",
                    "artistIds",
                    "downloadId",
                    "eventType",
                    "includeAlbum",
                    "includeArtist",
                    "includeTrack",
                    "page",
                    "pageSize",
                    "quality",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_history_artist",
                params=(
                    "albumId",
                    "artistId",
                    "eventType",
                    "includeAlbum",
                    "includeArtist",
                    "includeTrack",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_history_since",
                params=(
                    "date",
                    "eventType",
                    "includeAlbum",
                    "includeArtist",
                    "includeTrack",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_history_failed_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change history on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-importlist",
        (
            ToolStep(
                "lidarr_get_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_importlist_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_importlist",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_importlist_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_importlist_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_importlist_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_importlist_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_importlist_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_importlist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_importlist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlist on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-importlistexclusion",
        (
            ToolStep(
                "lidarr_get_importlistexclusion",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_importlistexclusion_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_importlistexclusion",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_importlistexclusion_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_importlistexclusion_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlistexclusion on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-indexer",
        (
            ToolStep(
                "lidarr_get_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_indexer_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_indexer",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_indexer_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_indexer_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_indexer_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_indexer_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_indexer_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_indexer_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexer on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-indexerflag",
        (
            ToolStep(
                "lidarr_get_indexerflag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change indexerflag on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-language",
        (
            ToolStep(
                "lidarr_get_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_language_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change language on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-localization",
        (
            ToolStep(
                "lidarr_get_localization",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change localization on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-log",
        (
            ToolStep(
                "lidarr_get_log",
                params=("level", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_log_file",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_log_file_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_log_file_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_log_file_update_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-login",
        (
            ToolStep(
                "lidarr_get_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_login",
                params=("returnUrl",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change login on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-logout",
        (
            ToolStep(
                "lidarr_get_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change logout on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-manualimport",
        (
            ToolStep(
                "lidarr_get_manualimport",
                params=(
                    "artistId",
                    "downloadId",
                    "filterExistingFiles",
                    "folder",
                    "replaceExistingFiles",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_manualimport",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change manualimport on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-mediacover",
        (
            ToolStep(
                "lidarr_get_mediacover_album_album_id_filename",
                params=("albumId", "filename"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_mediacover_artist_artist_id_filename",
                params=("artistId", "filename"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change mediacover on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-metadata",
        (
            ToolStep(
                "lidarr_get_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_metadata_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_metadata_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_metadata",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_metadata_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_metadata_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_metadata_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_metadata_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_metadata_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadata on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-metadataprofile",
        (
            ToolStep(
                "lidarr_get_metadataprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_metadataprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_metadataprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_metadataprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_metadataprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadataprofile on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-notification",
        (
            ToolStep(
                "lidarr_get_notification",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_notification_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_notification_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_notification",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_notification_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_notification_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_notification_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_notification_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_notification_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change notification on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-parse",
        (
            ToolStep(
                "lidarr_get_parse",
                params=("title",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change parse on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-path",
        (
            ToolStep(
                "lidarr_get_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change path on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-ping",
        (
            ToolStep(
                "lidarr_get_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change ping on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-qualitydefinition",
        (
            ToolStep(
                "lidarr_get_qualitydefinition",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_qualitydefinition_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_qualitydefinition_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_qualitydefinition_update",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change qualitydefinition on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-qualityprofile",
        (
            ToolStep(
                "lidarr_get_qualityprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_qualityprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_qualityprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_qualityprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_qualityprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change qualityprofile on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-queue",
        (
            ToolStep(
                "lidarr_get_queue_details",
                params=("albumIds", "artistId", "includeAlbum", "includeArtist"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_queue_grab_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_queue_grab_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_queue_bulk",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "data",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_queue_id",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "id",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change queue on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-release",
        (
            ToolStep(
                "lidarr_get_release",
                params=("albumId", "artistId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_release",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_release_push",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change release on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-releaseprofile",
        (
            ToolStep(
                "lidarr_get_releaseprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_releaseprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_releaseprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_releaseprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_releaseprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change releaseprofile on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-remotepathmapping",
        (
            ToolStep(
                "lidarr_get_remotepathmapping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_remotepathmapping_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_remotepathmapping",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_remotepathmapping_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_remotepathmapping_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change remotepathmapping on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-rename",
        (
            ToolStep(
                "lidarr_get_rename",
                params=("albumId", "artistId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change rename on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-retag",
        (
            ToolStep(
                "lidarr_get_retag",
                params=("albumId", "artistId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change retag on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-rootfolder",
        (
            ToolStep(
                "lidarr_get_rootfolder_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_rootfolder",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_rootfolder_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_rootfolder_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change rootfolder on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-search",
        (
            ToolStep(
                "lidarr_get_search",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change search on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-system",
        (
            ToolStep(
                "lidarr_get_system_backup",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_system_routes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_system_routes_duplicate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_system_task",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_system_task_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_system_backup_restore_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_system_backup_restore_upload",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_system_backup_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-tag",
        (
            ToolStep(
                "lidarr_get_tag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_tag_detail",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_tag_detail_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_tag_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_post_tag",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_tag_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_tag_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change tag on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-track",
        (
            ToolStep(
                "lidarr_get_track",
                params=("albumId", "albumReleaseId", "artistId", "trackIds"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_track_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change track on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-trackfile",
        (
            ToolStep(
                "lidarr_get_trackfile",
                params=("albumId", "artistId", "trackFileIds", "unmapped"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_trackfile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_put_trackfile_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_put_trackfile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_delete_trackfile_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "lidarr_delete_trackfile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change trackfile on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-update",
        (
            ToolStep(
                "lidarr_get_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change update on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "lidarr-manage-wanted",
        (
            ToolStep(
                "lidarr_get_wanted_cutoff",
                params=(
                    "includeArtist",
                    "monitored",
                    "page",
                    "pageSize",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "lidarr_get_wanted_cutoff_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "lidarr_get_wanted_missing_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change wanted on lidarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-",
        (
            ToolStep(
                "prowlarr_get_",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change  on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-api",
        (
            ToolStep(
                "prowlarr_get_api",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change api on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-applications",
        (
            ToolStep(
                "prowlarr_get_applications_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_applications_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_applications_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_applications_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_applications_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_applications_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_delete_applications_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change applications on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-appprofile",
        (
            ToolStep(
                "prowlarr_get_appprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_appprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_appprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_appprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_appprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_appprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change appprofile on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-command",
        (
            ToolStep(
                "prowlarr_get_command",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_command_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_command_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change command on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-config",
        (
            ToolStep(
                "prowlarr_get_config_development",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_development_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_host",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_host_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_ui",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_config_ui_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_put_config_development_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_put_config_downloadclient_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_put_config_host_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_put_config_ui_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change config on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-content",
        (
            ToolStep(
                "prowlarr_get_content_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change content on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-customfilter",
        (
            ToolStep(
                "prowlarr_get_customfilter",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_customfilter_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_customfilter",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_customfilter_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_customfilter_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customfilter on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-downloadclient",
        (
            ToolStep(
                "prowlarr_get_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_downloadclient_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_downloadclient",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_downloadclient_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_downloadclient_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_downloadclient_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_downloadclient_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_downloadclient_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_downloadclient_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_delete_downloadclient_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change downloadclient on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-filesystem",
        (
            ToolStep(
                "prowlarr_get_filesystem",
                params=("allowFoldersWithoutTrailingSlashes", "includeFiles", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_filesystem_type",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change filesystem on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-history",
        (
            ToolStep(
                "prowlarr_get_history",
                params=(
                    "downloadId",
                    "eventType",
                    "indexerIds",
                    "page",
                    "pageSize",
                    "sortDirection",
                    "sortKey",
                    "successful",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_history_indexer",
                params=("eventType", "indexerId", "limit"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_history_since",
                params=("date", "eventType"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change history on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-id",
        (
            ToolStep(
                "prowlarr_get_id_api",
                params=(
                    "album",
                    "artist",
                    "author",
                    "cat",
                    "configured",
                    "doubanid",
                    "ep",
                    "extended",
                    "genre",
                    "host",
                    "id",
                    "imdbid",
                    "label",
                    "limit",
                    "maxage",
                    "maxsize",
                    "minage",
                    "minsize",
                    "offset",
                    "publisher",
                    "q",
                    "rid",
                    "season",
                    "server",
                    "source",
                    "t",
                    "title",
                    "tmdbid",
                    "track",
                    "traktid",
                    "tvdbid",
                    "tvmazeid",
                    "year",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_id_download",
                params=("file", "id", "link"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change id on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-indexer",
        (
            ToolStep(
                "prowlarr_get_indexer_categories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_indexer_id_download",
                params=("file", "id", "link"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_indexer_id_newznab",
                params=(
                    "album",
                    "artist",
                    "author",
                    "cat",
                    "configured",
                    "doubanid",
                    "ep",
                    "extended",
                    "genre",
                    "host",
                    "id",
                    "imdbid",
                    "label",
                    "limit",
                    "maxage",
                    "maxsize",
                    "minage",
                    "minsize",
                    "offset",
                    "publisher",
                    "q",
                    "rid",
                    "season",
                    "server",
                    "source",
                    "t",
                    "title",
                    "tmdbid",
                    "track",
                    "traktid",
                    "tvdbid",
                    "tvmazeid",
                    "year",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexer_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_indexer_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_delete_indexer_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexer on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-indexerproxy",
        (
            ToolStep(
                "prowlarr_get_indexerproxy_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_indexerproxy_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexerproxy",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexerproxy_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexerproxy_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_indexerproxy_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_indexerproxy_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_indexerproxy_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexerproxy on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-indexerstats",
        (
            ToolStep(
                "prowlarr_get_indexerstats",
                params=("endDate", "indexers", "protocols", "startDate", "tags"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change indexerstats on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-localization",
        (
            ToolStep(
                "prowlarr_get_localization",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_localization_options",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change localization on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-log",
        (
            ToolStep(
                "prowlarr_get_log",
                params=("level", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_log_file",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_log_file_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_log_file_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_log_file_update_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-login",
        (
            ToolStep(
                "prowlarr_get_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_login",
                params=("returnUrl",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change login on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-logout",
        (
            ToolStep(
                "prowlarr_get_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change logout on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-notification",
        (
            ToolStep(
                "prowlarr_get_notification",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_notification_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_notification_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_notification",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_notification_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_notification_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_notification_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_notification_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_notification_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change notification on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-path",
        (
            ToolStep(
                "prowlarr_get_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change path on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-ping",
        (
            ToolStep(
                "prowlarr_get_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change ping on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-search",
        (
            ToolStep(
                "prowlarr_search",
                params=("query",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_search",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_search_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change search on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-system",
        (
            ToolStep(
                "prowlarr_get_system_backup",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_system_routes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_system_routes_duplicate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_system_task",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_system_task_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_system_backup_restore_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_system_backup_restore_upload",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_delete_system_backup_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-tag",
        (
            ToolStep(
                "prowlarr_get_tag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_tag_detail",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_get_tag_detail_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_get_tag_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_post_tag",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "prowlarr_put_tag_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "prowlarr_delete_tag_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change tag on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "prowlarr-manage-update",
        (
            ToolStep(
                "prowlarr_get_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change update on prowlarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-",
        (
            ToolStep(
                "radarr_get_",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change  on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-alttitle",
        (
            ToolStep(
                "radarr_get_alttitle",
                params=("movieId", "movieMetadataId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_alttitle_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change alttitle on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-api",
        (
            ToolStep(
                "radarr_get_api",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change api on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-autotagging",
        (
            ToolStep(
                "radarr_get_autotagging",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_autotagging_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_autotagging_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_autotagging",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_autotagging_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_autotagging_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change autotagging on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-blocklist",
        (
            ToolStep(
                "radarr_get_blocklist",
                params=(
                    "movieIds",
                    "page",
                    "pageSize",
                    "protocols",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_blocklist_movie",
                params=("movieId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_blocklist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_blocklist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blocklist on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-calendar",
        (
            ToolStep(
                "radarr_get_calendar",
                params=("end", "start", "tags", "unmonitored"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change calendar on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-collection",
        (
            ToolStep(
                "radarr_get_collection",
                params=("tmdbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_collection_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_collection",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_collection_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change collection on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-command",
        (
            ToolStep(
                "radarr_get_command",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_command_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_command_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change command on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-config",
        (
            ToolStep(
                "radarr_get_config_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_host",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_host_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_mediamanagement",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_mediamanagement_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_metadata_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_naming",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_naming_examples",
                params=(
                    "colonReplacementFormat",
                    "id",
                    "movieFolderFormat",
                    "renameMovies",
                    "replaceIllegalCharacters",
                    "resourceName",
                    "standardMovieFormat",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_naming_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_config_ui",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_config_ui_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_downloadclient_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_host_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_importlist_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_indexer_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_mediamanagement_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_metadata_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_naming_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_config_ui_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change config on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-content",
        (
            ToolStep(
                "radarr_get_content_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change content on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-credit",
        (
            ToolStep(
                "radarr_get_credit",
                params=("movieId", "movieMetadataId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_credit_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change credit on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-customfilter",
        (
            ToolStep(
                "radarr_get_customfilter",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_customfilter_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_customfilter",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_customfilter_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_customfilter_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customfilter on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-customformat",
        (
            ToolStep(
                "radarr_get_customformat",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_customformat_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_customformat_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_customformat",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_customformat_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_customformat_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_customformat_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_customformat_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customformat on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-delayprofile",
        (
            ToolStep(
                "radarr_get_delayprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_delayprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_delayprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_delayprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_delayprofile_reorder_id",
                params=("after", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_delayprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change delayprofile on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-diskspace",
        (
            ToolStep(
                "radarr_get_diskspace",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change diskspace on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-downloadclient",
        (
            ToolStep(
                "radarr_get_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_downloadclient_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_downloadclient",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_downloadclient_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_downloadclient_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_downloadclient_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_downloadclient_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_downloadclient_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change downloadclient on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-exclusions",
        (
            ToolStep(
                "radarr_get_exclusions",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_exclusions_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_exclusions_paged",
                params=("page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_exclusions",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_exclusions_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_exclusions_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_exclusions_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_exclusions_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change exclusions on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-extrafile",
        (
            ToolStep(
                "radarr_get_extrafile",
                params=("movieId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change extrafile on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-feed",
        (
            ToolStep(
                "radarr_get_feed_v3_calendar_radarrics",
                params=(
                    "futureDays",
                    "pastDays",
                    "releaseTypes",
                    "tags",
                    "unmonitored",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change feed on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-filesystem",
        (
            ToolStep(
                "radarr_get_filesystem",
                params=("allowFoldersWithoutTrailingSlashes", "includeFiles", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_filesystem_mediafiles",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_filesystem_type",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change filesystem on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-history",
        (
            ToolStep(
                "radarr_get_history",
                params=(
                    "downloadId",
                    "eventType",
                    "includeMovie",
                    "languages",
                    "movieIds",
                    "page",
                    "pageSize",
                    "quality",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_history_movie",
                params=("eventType", "includeMovie", "movieId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_history_since",
                params=("date", "eventType", "includeMovie"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_history_failed_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change history on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-importlist",
        (
            ToolStep(
                "radarr_get_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_importlist_movie",
                params=("includePopular", "includeRecommendations", "includeTrending"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_importlist_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_importlist",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_importlist_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_importlist_movie",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_importlist_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_importlist_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_importlist_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_importlist_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_importlist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_importlist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlist on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-indexer",
        (
            ToolStep(
                "radarr_get_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_indexer_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_indexer",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_indexer_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_indexer_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_indexer_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_indexer_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_indexer_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_indexer_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexer on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-indexerflag",
        (
            ToolStep(
                "radarr_get_indexerflag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change indexerflag on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-language",
        (
            ToolStep(
                "radarr_get_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_language_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change language on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-localization",
        (
            ToolStep(
                "radarr_get_localization",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_localization_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change localization on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-log",
        (
            ToolStep(
                "radarr_get_log",
                params=("level", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_log_file",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_log_file_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_log_file_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_log_file_update_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-login",
        (
            ToolStep(
                "radarr_get_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_login",
                params=("returnUrl",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change login on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-logout",
        (
            ToolStep(
                "radarr_get_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change logout on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-manualimport",
        (
            ToolStep(
                "radarr_get_manualimport",
                params=("downloadId", "filterExistingFiles", "folder", "movieId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_manualimport",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change manualimport on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-mediacover",
        (
            ToolStep(
                "radarr_get_mediacover_movie_id_filename",
                params=("filename", "movieId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change mediacover on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-metadata",
        (
            ToolStep(
                "radarr_get_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_metadata_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_metadata_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_metadata",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_metadata_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_metadata_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_metadata_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_metadata_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_metadata_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadata on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-movie",
        (
            ToolStep(
                "radarr_get_movie_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_movie_id_folder",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_movie_lookup_imdb",
                params=("imdbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_movie_lookup_tmdb",
                params=("tmdbId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_movie",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_movie_import",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_movie_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_movie_id",
                params=("data", "id", "moveFiles"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_movie_editor",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_movie_id",
                params=("addImportExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_lookup_movie",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change movie on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-moviefile",
        (
            ToolStep(
                "radarr_get_moviefile",
                params=("movieFileIds", "movieId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_moviefile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_moviefile_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_moviefile_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_moviefile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_moviefile_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_moviefile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change moviefile on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-notification",
        (
            ToolStep(
                "radarr_get_notification",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_notification_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_notification_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_notification",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_notification_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_notification_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_notification_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_notification_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_notification_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change notification on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-parse",
        (
            ToolStep(
                "radarr_get_parse",
                params=("title",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change parse on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-path",
        (
            ToolStep(
                "radarr_get_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change path on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-ping",
        (
            ToolStep(
                "radarr_get_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change ping on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-qualitydefinition",
        (
            ToolStep(
                "radarr_get_qualitydefinition",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_qualitydefinition_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_qualitydefinition_limits",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_qualitydefinition_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_qualitydefinition_update",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change qualitydefinition on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-qualityprofile",
        (
            ToolStep(
                "radarr_get_qualityprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_qualityprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_qualityprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_qualityprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_qualityprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change qualityprofile on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-queue",
        (
            ToolStep(
                "radarr_get_queue_details",
                params=("includeMovie", "movieId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_queue_grab_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_queue_grab_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_queue_bulk",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "data",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change queue on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-release",
        (
            ToolStep(
                "radarr_get_release",
                params=("movieId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_release",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_release_push",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change release on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-releaseprofile",
        (
            ToolStep(
                "radarr_get_releaseprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_releaseprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_releaseprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_releaseprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_releaseprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change releaseprofile on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-remotepathmapping",
        (
            ToolStep(
                "radarr_get_remotepathmapping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_remotepathmapping_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_remotepathmapping",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_put_remotepathmapping_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_delete_remotepathmapping_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change remotepathmapping on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-rename",
        (
            ToolStep(
                "radarr_get_rename",
                params=("movieId",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change rename on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-rootfolder",
        (
            ToolStep(
                "radarr_get_rootfolder_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_rootfolder",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_rootfolder_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change rootfolder on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-system",
        (
            ToolStep(
                "radarr_get_system_backup",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_system_routes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_system_routes_duplicate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_system_task",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_system_task_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_system_backup_restore_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_post_system_backup_restore_upload",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_delete_system_backup_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-tag",
        (
            ToolStep(
                "radarr_get_tag_detail",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "radarr_get_tag_detail_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_get_tag_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "radarr_put_tag_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change tag on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-update",
        (
            ToolStep(
                "radarr_get_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change update on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "radarr-manage-wanted",
        (
            ToolStep(
                "radarr_get_wanted_cutoff",
                params=("monitored", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change wanted on radarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-auth",
        (
            ToolStep(
                "seerr_get_auth_jellyfin_quickconnect_check",
                params=("secret",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_auth_me",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_jellyfin",
                params=("email", "hostname", "password", "server_type", "username"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_jellyfin_quickconnect_authenticate",
                params=("secret",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_jellyfin_quickconnect_initiate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_local",
                params=("email", "password"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_plex",
                params=("auth_token",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_reset_password",
                params=("email",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_auth_reset_password_guid",
                params=("guid", "password"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change auth on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-backdrops",
        (
            ToolStep(
                "seerr_get_backdrops",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change backdrops on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-blacklist",
        (
            ToolStep(
                "seerr_get_blacklist",
                params=("filter", "search", "skip", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_blacklist_tmdb_id",
                params=("media_type", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_blacklist",
                params=("media", "title", "tmdb_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_blacklist_tmdb_id",
                params=("confirm", "media_type", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blacklist on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-blocklist",
        (
            ToolStep(
                "seerr_get_blocklist",
                params=("filter", "search", "skip", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_blocklist_tmdb_id",
                params=("media_type", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_blocklist",
                params=("media", "title", "tmdb_id", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_blocklist_collection_id",
                params=("body", "collection_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_blocklist_collection_id",
                params=("collection_id", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_blocklist_tmdb_id",
                params=("confirm", "media_type", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blocklist on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-certifications",
        (
            ToolStep(
                "seerr_get_certifications_movie",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_certifications_tv",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change certifications on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-collection",
        (
            ToolStep(
                "seerr_get_collection_id",
                params=("collection_id", "language"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change collection on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-discover",
        (
            ToolStep(
                "seerr_get_discover_genreslider_movie",
                params=("language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_genreslider_tv",
                params=("language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_keyword_id_movies",
                params=("keyword_id", "language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_discover_movies",
                params=(
                    "certification",
                    "certification_country",
                    "certification_gte",
                    "certification_lte",
                    "certification_mode",
                    "exclude_keywords",
                    "genre",
                    "keywords",
                    "language",
                    "page",
                    "primary_release_date_gte",
                    "primary_release_date_lte",
                    "sort_by",
                    "studio",
                    "vote_average_gte",
                    "vote_average_lte",
                    "vote_count_gte",
                    "vote_count_lte",
                    "watch_providers",
                    "watch_region",
                    "with_runtime_gte",
                    "with_runtime_lte",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_movies_genre_id",
                params=("genre_id", "language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_discover_movies_language_language",
                params=("body_language", "language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_movies_studio_id",
                params=("language", "page", "studio_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_discover_movies_upcoming",
                params=("language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_trending",
                params=("language", "media_type", "page", "time_window"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_tv",
                params=(
                    "certification",
                    "certification_country",
                    "certification_gte",
                    "certification_lte",
                    "certification_mode",
                    "exclude_keywords",
                    "first_air_date_gte",
                    "first_air_date_lte",
                    "genre",
                    "keywords",
                    "language",
                    "network",
                    "page",
                    "sort_by",
                    "status",
                    "vote_average_gte",
                    "vote_average_lte",
                    "vote_count_gte",
                    "vote_count_lte",
                    "watch_providers",
                    "watch_region",
                    "with_runtime_gte",
                    "with_runtime_lte",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_tv_genre_id",
                params=("genre_id", "language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_discover_tv_language_language",
                params=("body_language", "language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_tv_network_id",
                params=("language", "network_id", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_discover_tv_upcoming",
                params=("language", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_discover_watchlist",
                params=("page",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change discover on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-genres",
        (
            ToolStep(
                "seerr_get_genres_movie",
                params=("language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_genres_tv",
                params=("language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change genres on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-issue",
        (
            ToolStep(
                "seerr_get_issue",
                params=("filter", "requested_by", "skip", "sort", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_issue_comment_comment_id",
                params=("comment_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_issue_count",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_issue_id",
                params=("issue_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_issue",
                params=("issue_type", "media_id", "message", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_issue_id_comment",
                params=("issue_id", "message"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_issue_id_status",
                params=("issue_id", "status"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_put_issue_comment_comment_id",
                params=("comment_id", "message"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_issue_comment_comment_id",
                params=("comment_id", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_issue_id",
                params=("confirm", "issue_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change issue on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-keyword",
        (
            ToolStep(
                "seerr_get_keyword_id",
                params=("keyword_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change keyword on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-languages",
        (
            ToolStep(
                "seerr_get_languages",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change languages on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-media",
        (
            ToolStep(
                "seerr_get_media",
                params=("filter", "skip", "sort", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_media_id_watch_data",
                params=("media_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_media_id_status",
                params=("is4k", "media_id", "status"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_media_id",
                params=("confirm", "media_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_media_id_file",
                params=("confirm", "is4k", "media_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change media on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-movie",
        (
            ToolStep(
                "seerr_get_movie_id_ratings",
                params=("movie_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_movie_id_ratingscombined",
                params=("movie_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_movie_id_recommendations",
                params=("language", "movie_id", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_movie_id_similar",
                params=("language", "movie_id", "page"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change movie on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-network",
        (
            ToolStep(
                "seerr_get_network_id",
                params=("network_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change network on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-override",
        (
            ToolStep(
                "seerr_get_override_rule",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_override_rule",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_override_rule_advanced_request",
                params=(
                    "is4k",
                    "media_type",
                    "request_id",
                    "request_user",
                    "service_id",
                    "tags",
                    "tmdb_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_override_rule_rule_id",
                params=("rule_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_override_rule_rule_id",
                params=("confirm", "rule_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change override on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-person",
        (
            ToolStep(
                "seerr_get_person_id",
                params=("language", "person_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_person_id_combined_credits",
                params=("language", "person_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change person on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-regions",
        (
            ToolStep(
                "seerr_get_regions",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change regions on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-request",
        (
            ToolStep(
                "seerr_put_request_id",
                params=(
                    "is4k",
                    "language_profile_id",
                    "media_type",
                    "profile_id",
                    "request_id",
                    "root_folder",
                    "seasons",
                    "server_id",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_request_id",
                params=("confirm", "request_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change request on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-search",
        (
            ToolStep(
                "seerr_get_search_company",
                params=("page", "query"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_search_keyword",
                params=("page", "query"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change search on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-service",
        (
            ToolStep(
                "seerr_get_service_radarr_id",
                params=("radarr_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_service_sonarr_id",
                params=("sonarr_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_service_sonarr_lookup_tmdb_id",
                params=("tmdb_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change service on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-settings",
        (
            ToolStep(
                "seerr_get_settings_about",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_cache",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_discover",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_discover_reset",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_jellyfin",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_jellyfin_library",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_jellyfin_sync",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_jellyfin_users",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_jobs",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_logs",
                params=("filter", "search", "skip", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_main",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_metadatas",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_network",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_discord",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_email",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_gotify",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_ntfy",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_pushbullet",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_pushover",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_pushover_sounds",
                params=("token",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_slack",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_telegram",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_webhook",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_notifications_webpush",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_plex",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_plex_devices_servers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_plex_library",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_plex_sync",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_plex_users",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_public",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_settings_radarr_id_profiles",
                params=("radarr_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_settings_tautulli",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_cache_dns_entry_flush",
                params=("dns_entry",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_cache_id_flush",
                params=("cache_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_settings_discover",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_discover_add",
                params=("data_", "title", "type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_initialize",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jellyfin",
                params=(
                    "admin_pass",
                    "admin_user",
                    "external_hostname",
                    "hostname",
                    "jellyfin_forgot_password_url",
                    "libraries",
                    "name",
                    "server_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jellyfin_library_sync",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jellyfin_sync",
                params=("cancel", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jobs_job_id_cancel",
                params=("job_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jobs_job_id_run",
                params=("job_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_settings_jobs_job_id_schedule",
                params=("job_id", "schedule"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_settings_main",
                params=(
                    "api_key",
                    "app_language",
                    "application_title",
                    "application_url",
                    "default_permissions",
                    "enable_special_episodes",
                    "hide_available",
                    "hide_requested",
                    "local_login",
                    "media_server_type",
                    "new_plex_login",
                    "partial_requests_enabled",
                    "version_check",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_main_regenerate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_metadatas_test",
                params=("tmdb", "tvdb"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_network",
                params=(
                    "csrf_protection",
                    "dns_cache",
                    "force_ipv4_first",
                    "proxy",
                    "trust_proxy",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_discord",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_discord_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_email",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_email_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_gotify",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_gotify_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_ntfy",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_ntfy_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_pushbullet",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_pushbullet_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_pushover",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_pushover_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_slack",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_slack_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_telegram",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_telegram_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_webhook",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_webhook_test",
                params=("enabled", "options", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_webpush",
                params=("enabled", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_notifications_webpush_test",
                params=("enabled", "types"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_plex",
                params=(
                    "ip",
                    "libraries",
                    "machine_id",
                    "name",
                    "port",
                    "use_ssl",
                    "web_app_url",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_plex_library_sync",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_plex_sync",
                params=("cancel", "start"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_sonarr_test",
                params=("api_key", "base_url", "hostname", "port", "use_ssl"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_settings_tautulli",
                params=("api_key", "external_url", "hostname", "port", "use_ssl"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_settings_discover_slider_id",
                params=("data_", "slider_id", "title", "type"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_put_settings_jellyfin_library_id",
                params=("enabled", "library_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_put_settings_metadatas",
                params=("settings",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_settings_plex_library_id",
                params=("enabled", "library_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_settings_discover_slider_id",
                params=("confirm", "slider_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_settings_radarr_id",
                params=("confirm", "radarr_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_settings_sonarr_id",
                params=("confirm", "sonarr_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change settings on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-status",
        (
            ToolStep(
                "seerr_get_status_appdata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change status on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-studio",
        (
            ToolStep(
                "seerr_get_studio_id",
                params=("studio_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change studio on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-tv",
        (
            ToolStep(
                "seerr_get_tv_id",
                params=("language", "tv_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_tv_id_ratings",
                params=("tv_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_tv_id_recommendations",
                params=("language", "page", "tv_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_tv_id_season_number",
                params=("language", "season_number", "tv_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_tv_id_similar",
                params=("language", "page", "tv_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change tv on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-user",
        (
            ToolStep(
                "seerr_get_user",
                params=("include_ids", "q", "skip", "sort", "sort_direction", "take"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_user_id",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_push_subscription_endpoint",
                params=("endpoint", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_push_subscriptions",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_quota",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_requests",
                params=("skip", "take", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_settings_main",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_settings_notifications",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_settings_password",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_settings_permissions",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_watch_data",
                params=("user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_id_watchlist",
                params=("page", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_get_user_jellyfin_user_id",
                params=("jellyfin_user_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user",
                params=("email", "permissions", "username"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_linked_accounts_jellyfin",
                params=("password", "user_id", "username"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_linked_accounts_jellyfin_quickconnect",
                params=("secret", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_linked_accounts_plex",
                params=("auth_token", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_main",
                params=(
                    "discover_region",
                    "email",
                    "global_movie_quota_days",
                    "global_movie_quota_limit",
                    "global_tv_quota_days",
                    "global_tv_quota_limit",
                    "locale",
                    "movie_quota_days",
                    "movie_quota_limit",
                    "original_language",
                    "streaming_region",
                    "tv_quota_days",
                    "tv_quota_limit",
                    "user_id",
                    "username",
                    "watchlist_sync_movies",
                    "watchlist_sync_tv",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_notifications",
                params=(
                    "discord_enabled",
                    "discord_enabled_types",
                    "discord_ids",
                    "email_enabled",
                    "notification_types",
                    "pgp_key",
                    "pushbullet_access_token",
                    "pushover_application_token",
                    "pushover_sound",
                    "pushover_user_key",
                    "telegram_bot_username",
                    "telegram_chat_id",
                    "telegram_enabled",
                    "telegram_message_thread_id",
                    "telegram_send_silently",
                    "user_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_password",
                params=("current_password", "new_password", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_id_settings_permissions",
                params=("permissions", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_post_user_import_from_jellyfin",
                params=("jellyfin_user_ids",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_user_import_from_plex",
                params=("plex_ids",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_post_user_register_push_subscription",
                params=("auth", "endpoint", "p256dh", "user_agent"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_user",
                params=("ids", "permissions"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_put_user_id",
                params=(
                    "avatar",
                    "created_at",
                    "email",
                    "id",
                    "jellyfin_auth_token",
                    "permissions",
                    "plex_token",
                    "plex_username",
                    "request_count",
                    "updated_at",
                    "user_id",
                    "user_type",
                    "username",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "seerr_delete_user_id",
                params=("confirm", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_user_id_push_subscription_endpoint",
                params=("confirm", "endpoint", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_user_id_settings_linked_accounts_jellyfin",
                params=("confirm", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_user_id_settings_linked_accounts_plex",
                params=("confirm", "user_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change user on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-watchlist",
        (
            ToolStep(
                "seerr_post_watchlist",
                params=("media_type", "rating_key", "title", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_delete_watchlist_tmdb_id",
                params=("confirm", "media_type", "tmdb_id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change watchlist on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "seerr-manage-watchproviders",
        (
            ToolStep(
                "seerr_get_watchproviders_movies",
                params=("watch_region",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_watchproviders_regions",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "seerr_get_watchproviders_tv",
                params=("watch_region",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change watchproviders on seerr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-",
        (
            ToolStep(
                "sonarr_get_",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change  on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-api",
        (
            ToolStep(
                "sonarr_get_api",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change api on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-autotagging",
        (
            ToolStep(
                "sonarr_get_autotagging",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_autotagging_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_autotagging_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_autotagging",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_autotagging_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_autotagging_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change autotagging on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-blocklist",
        (
            ToolStep(
                "sonarr_get_blocklist",
                params=(
                    "page",
                    "pageSize",
                    "protocols",
                    "seriesIds",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_blocklist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_blocklist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change blocklist on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-calendar",
        (
            ToolStep(
                "sonarr_get_calendar",
                params=(
                    "end",
                    "includeEpisodeFile",
                    "includeEpisodeImages",
                    "includeSeries",
                    "start",
                    "tags",
                    "unmonitored",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_calendar_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change calendar on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-command",
        (
            ToolStep(
                "sonarr_get_command",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_command_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_command_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change command on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-config",
        (
            ToolStep(
                "sonarr_get_config_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_host",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_host_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_mediamanagement",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_mediamanagement_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_naming",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_naming_examples",
                params=(
                    "animeEpisodeFormat",
                    "colonReplacementFormat",
                    "customColonReplacementFormat",
                    "dailyEpisodeFormat",
                    "id",
                    "multiEpisodeStyle",
                    "renameEpisodes",
                    "replaceIllegalCharacters",
                    "resourceName",
                    "seasonFolderFormat",
                    "seriesFolderFormat",
                    "specialsFolderFormat",
                    "standardEpisodeFormat",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_naming_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_config_ui",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_config_ui_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_downloadclient_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_host_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_importlist_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_indexer_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_mediamanagement_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_naming_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_config_ui_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change config on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-content",
        (
            ToolStep(
                "sonarr_get_content_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change content on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-customfilter",
        (
            ToolStep(
                "sonarr_get_customfilter",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_customfilter_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_customfilter",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_customfilter_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_customfilter_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customfilter on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-customformat",
        (
            ToolStep(
                "sonarr_get_customformat",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_customformat_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_customformat_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_customformat",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_customformat_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_customformat_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_customformat_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_customformat_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change customformat on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-delayprofile",
        (
            ToolStep(
                "sonarr_get_delayprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_delayprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_delayprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_delayprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_delayprofile_reorder_id",
                params=("after", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_delayprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change delayprofile on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-diskspace",
        (
            ToolStep(
                "sonarr_get_diskspace",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change diskspace on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-downloadclient",
        (
            ToolStep(
                "sonarr_get_downloadclient",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_downloadclient_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_downloadclient_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_downloadclient",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_downloadclient_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_downloadclient_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_downloadclient_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_downloadclient_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_downloadclient_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_downloadclient_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_downloadclient_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change downloadclient on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-episode",
        (
            ToolStep(
                "sonarr_get_episode",
                params=(
                    "episodeFileId",
                    "episodeIds",
                    "includeEpisodeFile",
                    "includeImages",
                    "includeSeries",
                    "seasonNumber",
                    "seriesId",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_episode_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_episode_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_episode_monitor",
                params=("data", "includeImages"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change episode on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-episodefile",
        (
            ToolStep(
                "sonarr_get_episodefile",
                params=("episodeFileIds", "seriesId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_episodefile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_episodefile_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_episodefile_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_episodefile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_episodefile_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_episodefile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change episodefile on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-feed",
        (
            ToolStep(
                "sonarr_get_feed_v3_calendar_sonarrics",
                params=(
                    "asAllDay",
                    "futureDays",
                    "pastDays",
                    "premieresOnly",
                    "tags",
                    "unmonitored",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change feed on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-filesystem",
        (
            ToolStep(
                "sonarr_get_filesystem",
                params=("allowFoldersWithoutTrailingSlashes", "includeFiles", "path"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_filesystem_mediafiles",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_filesystem_type",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change filesystem on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-history",
        (
            ToolStep(
                "sonarr_get_history",
                params=(
                    "downloadId",
                    "episodeId",
                    "eventType",
                    "includeEpisode",
                    "includeSeries",
                    "languages",
                    "page",
                    "pageSize",
                    "quality",
                    "seriesIds",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_history_series",
                params=(
                    "eventType",
                    "includeEpisode",
                    "includeSeries",
                    "seasonNumber",
                    "seriesId",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_history_since",
                params=("date", "eventType", "includeEpisode", "includeSeries"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_history_failed_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change history on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-importlist",
        (
            ToolStep(
                "sonarr_get_importlist",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_importlist_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_importlist_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_importlist",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_importlist_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_importlist_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_importlist_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_importlist_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_importlist_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_importlist_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_importlist_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlist on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-importlistexclusion",
        (
            ToolStep(
                "sonarr_get_importlistexclusion",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_importlistexclusion_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_importlistexclusion_paged",
                params=("page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_importlistexclusion",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_importlistexclusion_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_importlistexclusion_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_importlistexclusion_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change importlistexclusion on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-indexer",
        (
            ToolStep(
                "sonarr_get_indexer",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_indexer_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_indexer_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_indexer",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_indexer_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_indexer_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_indexer_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_indexer_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_indexer_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_indexer_bulk",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_indexer_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change indexer on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-indexerflag",
        (
            ToolStep(
                "sonarr_get_indexerflag",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change indexerflag on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-language",
        (
            ToolStep(
                "sonarr_get_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_language_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change language on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-languageprofile",
        (
            ToolStep(
                "sonarr_get_languageprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_languageprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_languageprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_languageprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_languageprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_languageprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change languageprofile on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-localization",
        (
            ToolStep(
                "sonarr_get_localization",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_localization_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_localization_language",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change localization on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-log",
        (
            ToolStep(
                "sonarr_get_log",
                params=("level", "page", "pageSize", "sortDirection", "sortKey"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_log_file",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_log_file_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_log_file_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_log_file_update_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change log on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-login",
        (
            ToolStep(
                "sonarr_get_login",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_login",
                params=("returnUrl",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change login on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-logout",
        (
            ToolStep(
                "sonarr_get_logout",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change logout on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-manualimport",
        (
            ToolStep(
                "sonarr_get_manualimport",
                params=(
                    "downloadId",
                    "filterExistingFiles",
                    "folder",
                    "seasonNumber",
                    "seriesId",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_manualimport",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change manualimport on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-mediacover",
        (
            ToolStep(
                "sonarr_get_mediacover_series_id_filename",
                params=("filename", "seriesId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change mediacover on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-metadata",
        (
            ToolStep(
                "sonarr_get_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_metadata_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_metadata_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_metadata",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_metadata_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_metadata_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_metadata_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_metadata_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_metadata_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change metadata on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-notification",
        (
            ToolStep(
                "sonarr_get_notification",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_notification_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_notification_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_notification",
                params=("data", "forceSave"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_notification_action_name",
                params=("data", "name"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_notification_test",
                params=("data", "forceTest"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_notification_testall",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_notification_id",
                params=("data", "forceSave", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_notification_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change notification on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-parse",
        (
            ToolStep(
                "sonarr_get_parse",
                params=("path", "title"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change parse on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-path",
        (
            ToolStep(
                "sonarr_get_path",
                params=("path",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change path on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-ping",
        (
            ToolStep(
                "sonarr_get_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change ping on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-qualitydefinition",
        (
            ToolStep(
                "sonarr_get_qualitydefinition",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_qualitydefinition_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_qualitydefinition_limits",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_qualitydefinition_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_qualitydefinition_update",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change qualitydefinition on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-qualityprofile",
        (
            ToolStep(
                "sonarr_get_qualityprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_qualityprofile_schema",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_qualityprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_qualityprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_qualityprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change qualityprofile on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-queue",
        (
            ToolStep(
                "sonarr_get_queue_details",
                params=("episodeIds", "includeEpisode", "includeSeries", "seriesId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_queue_grab_bulk",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_queue_grab_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_queue_bulk",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "data",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_queue_id",
                params=(
                    "blocklist",
                    "changeCategory",
                    "confirm",
                    "id",
                    "removeFromClient",
                    "skipRedownload",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change queue on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-release",
        (
            ToolStep(
                "sonarr_get_release",
                params=("episodeId", "seasonNumber", "seriesId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_release",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_release_push",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change release on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-releaseprofile",
        (
            ToolStep(
                "sonarr_get_releaseprofile",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_releaseprofile_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_releaseprofile",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_releaseprofile_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_releaseprofile_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change releaseprofile on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-remotepathmapping",
        (
            ToolStep(
                "sonarr_get_remotepathmapping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_remotepathmapping_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_remotepathmapping",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_remotepathmapping_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_remotepathmapping_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change remotepathmapping on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-rename",
        (
            ToolStep(
                "sonarr_get_rename",
                params=("seasonNumber", "seriesId"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_rename_bulk",
                params=("seriesIds",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change rename on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-rootfolder",
        (
            ToolStep(
                "sonarr_get_rootfolder_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_rootfolder",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_rootfolder_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change rootfolder on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-seasonpass",
        (
            ToolStep(
                "sonarr_post_seasonpass",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change seasonpass on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-series",
        (
            ToolStep(
                "sonarr_get_series_id",
                params=("id", "includeSeasonImages"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_series_id_folder",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_series",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_series_import",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_series_editor",
                params=("data",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_put_series_id",
                params=("data", "id", "moveFiles"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_delete_series_editor",
                params=("confirm", "data"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_series_id",
                params=("addImportListExclusion", "confirm", "deleteFiles", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "sonarr_lookup_series",
                params=("term",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change series on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-system",
        (
            ToolStep(
                "sonarr_get_system_backup",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_routes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_routes_duplicate",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_task",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_system_task_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_system_backup_restore_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_post_system_backup_restore_upload",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_system_restart",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_post_system_shutdown",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_delete_system_backup_id",
                params=("confirm", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
        description="Read and change system on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-tag",
        (
            ToolStep(
                "sonarr_get_tag_detail",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_tag_detail_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_tag_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_put_tag_id",
                params=("data", "id"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change tag on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-update",
        (
            ToolStep(
                "sonarr_get_update",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
        description="Read and change update on sonarr through its typed tools, reading before any write.",
    ),
    ToolUseContract(
        "sonarr-manage-wanted",
        (
            ToolStep(
                "sonarr_get_wanted_cutoff",
                params=(
                    "includeEpisodeFile",
                    "includeImages",
                    "includeSeries",
                    "monitored",
                    "page",
                    "pageSize",
                    "sortDirection",
                    "sortKey",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "sonarr_get_wanted_cutoff_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
            ToolStep(
                "sonarr_get_wanted_missing_id",
                params=("id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("NOT_FOUND", "no object has the given id"),
                ),
            ),
        ),
        description="Read and change wanted on sonarr through its typed tools, reading before any write.",
    ),
)

LINKS = (
    SurfaceLink(
        "arr-check-download-queue",
        tools=(
            "chaptarr_get_queue",
            "chaptarr_get_queue_status",
            "lidarr_get_queue",
            "lidarr_get_queue_status",
            "radarr_get_queue",
            "radarr_get_queue_status",
            "sonarr_get_queue",
            "sonarr_get_queue_status",
        ),
        prompts=(
            "arr_operator",
            "download_monitor",
            "media_librarian",
            "request_manager",
        ),
        skills=("arr-download-queue",),
    ),
    SurfaceLink(
        "arr-ingest-library",
        tools=("arr_ingest_library",),
        prompts=("arr_operator", "download_monitor"),
        skills=("arr-mcp-operations",),
    ),
    SurfaceLink(
        "arr-remove-stalled-download",
        tools=(
            "radarr_delete_queue_id",
            "radarr_get_queue",
            "radarr_post_command",
        ),
        prompts=(
            "arr_operator",
            "download_monitor",
            "media_librarian",
            "request_manager",
        ),
        skills=("arr-download-queue",),
    ),
    SurfaceLink(
        "arr-repair-download-client",
        tools=(
            "radarr_get_downloadclient",
            "radarr_get_health",
            "radarr_post_downloadclient_test",
            "radarr_put_downloadclient_id",
        ),
        prompts=("arr_operator", "download_monitor"),
        skills=("arr-download-queue",),
    ),
    SurfaceLink(
        "arr-suite-health-check",
        tools=(
            "bazarr_get_system_health",
            "bazarr_get_system_status",
            "chaptarr_get_health",
            "chaptarr_get_system_status",
            "lidarr_get_health",
            "lidarr_get_system_status",
            "prowlarr_get_health",
            "prowlarr_get_system_status",
            "radarr_get_health",
            "radarr_get_system_status",
            "seerr_get_status",
            "sonarr_get_health",
            "sonarr_get_system_status",
        ),
        prompts=("arr_operator", "download_monitor"),
        skills=("arr-mcp-operations",),
    ),
    SurfaceLink(
        "bazarr-connect-sonarr-radarr",
        tools=(
            "bazarr_get_badges",
            "bazarr_get_system_settings",
            "bazarr_post_system_settings",
            "bazarr_post_system_tasks",
            "radarr_get_system_status",
            "sonarr_get_system_status",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-download-wanted-subtitles",
        tools=(
            "bazarr_get_episodes_wanted",
            "bazarr_get_movies_wanted",
            "bazarr_get_providers",
            "bazarr_get_system_status",
            "bazarr_patch_episodes_subtitles",
            "bazarr_patch_movies_subtitles",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-enable-free-providers",
        tools=(
            "bazarr_get_episodes_wanted",
            "bazarr_get_languages_profiles",
            "bazarr_get_movies_wanted",
            "bazarr_get_provider_episodes",
            "bazarr_get_provider_movies",
            "bazarr_get_providers",
            "bazarr_get_system_settings",
            "bazarr_post_system_settings",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-reset-providers",
        tools=(
            "bazarr_get_providers",
            "bazarr_post_providers_reset",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "chaptarr-add-author-and-search",
        tools=(
            "chaptarr_get_author_lookup",
            "chaptarr_get_metadataprofile",
            "chaptarr_get_qualityprofile",
            "chaptarr_get_queue",
            "chaptarr_get_rootfolder",
            "chaptarr_post_author",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-provision-book-library",
        tools=(
            "chaptarr_get_downloadclient_schema",
            "chaptarr_get_metadataprofile",
            "chaptarr_get_qualityprofile",
            "chaptarr_get_rootfolder",
            "chaptarr_post_downloadclient",
            "chaptarr_post_downloadclient_test",
            "chaptarr_post_rootfolder",
            "prowlarr_get_applications_schema",
            "prowlarr_post_applications",
            "prowlarr_post_applications_test",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-search-missing",
        tools=(
            "chaptarr_get_wanted_missing",
            "chaptarr_post_command",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "lidarr-add-artist-and-search",
        tools=(
            "lidarr_get_artist",
            "lidarr_get_artist_lookup",
            "lidarr_get_metadataprofile",
            "lidarr_get_qualityprofile",
            "lidarr_get_queue",
            "lidarr_get_rootfolder",
            "lidarr_post_artist",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-search-missing",
        tools=(
            "lidarr_get_queue",
            "lidarr_get_wanted_missing",
            "lidarr_post_command",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "prowlarr-fix-failing-indexer",
        tools=(
            "prowlarr_get_health",
            "prowlarr_get_indexer_id",
            "prowlarr_get_indexerproxy",
            "prowlarr_get_indexerstatus",
            "prowlarr_post_indexer_test",
            "prowlarr_put_indexer_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-replace-dead-indexer",
        tools=(
            "prowlarr_delete_indexer_id",
            "prowlarr_get_indexer_schema",
            "prowlarr_post_command",
            "prowlarr_post_indexer",
            "prowlarr_post_indexer_test",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-search-releases",
        tools=(
            "prowlarr_get_indexer",
            "prowlarr_get_search",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-sync-indexers",
        tools=(
            "prowlarr_get_applications",
            "prowlarr_post_command",
            "radarr_get_indexer",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "radarr-add-and-search",
        tools=(
            "radarr_add_movie",
            "radarr_get_movie",
            "radarr_get_movie_lookup",
            "radarr_get_qualityprofile",
            "radarr_get_queue",
            "radarr_get_rootfolder",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-search-missing",
        tools=(
            "radarr_get_queue",
            "radarr_get_wanted_missing",
            "radarr_post_command",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-tag-roundtrip",
        tools=(
            "radarr_delete_tag_id",
            "radarr_get_tag",
            "radarr_post_tag",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "seerr-request-title",
        tools=(
            "seerr_get_movie_id",
            "seerr_get_request",
            "seerr_get_search",
            "seerr_post_request",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-retry-failed",
        tools=(
            "seerr_get_request",
            "seerr_get_settings_radarr",
            "seerr_post_request_id_retry",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-route-requests-by-quality",
        tools=(
            "radarr_get_qualityprofile",
            "seerr_get_settings_radarr",
            "seerr_get_settings_sonarr",
            "seerr_post_settings_radarr",
            "seerr_post_settings_radarr_test",
            "seerr_post_settings_sonarr",
            "seerr_put_settings_radarr_id",
            "seerr_put_settings_sonarr_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-triage-requests",
        tools=(
            "seerr_get_request",
            "seerr_get_request_count",
            "seerr_get_request_id",
            "seerr_get_service_radarr",
            "seerr_get_service_sonarr",
            "seerr_post_request_id_status",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "sonarr-add-and-search",
        tools=(
            "sonarr_add_series",
            "sonarr_get_qualityprofile",
            "sonarr_get_queue",
            "sonarr_get_rootfolder",
            "sonarr_get_series",
            "sonarr_get_series_lookup",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-search-missing",
        tools=(
            "sonarr_get_queue",
            "sonarr_get_wanted_missing",
            "sonarr_post_command",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-tag-roundtrip",
        tools=(
            "sonarr_delete_tag_id",
            "sonarr_get_tag",
            "sonarr_post_tag",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "bazarr-manage-browse",
        tools=(
            "bazarr_get_browse_bazarr_fs",
            "bazarr_get_browse_radarr_fs",
            "bazarr_get_browse_sonarr_fs",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-episodes",
        tools=(
            "bazarr_delete_episodes_blacklist",
            "bazarr_delete_episodes_subtitles",
            "bazarr_get_episodes",
            "bazarr_get_episodes_blacklist",
            "bazarr_get_episodes_history",
            "bazarr_post_episodes_blacklist",
            "bazarr_post_episodes_subtitles",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-history",
        tools=("bazarr_get_history_stats",),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-jellyfin",
        tools=(
            "bazarr_get_jellyfin_libraries",
            "bazarr_post_jellyfin_test_connection",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-languages",
        tools=("bazarr_get_languages",),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-movies",
        tools=(
            "bazarr_delete_movies_blacklist",
            "bazarr_delete_movies_subtitles",
            "bazarr_get_movies",
            "bazarr_get_movies_blacklist",
            "bazarr_get_movies_history",
            "bazarr_get_movies_tags",
            "bazarr_patch_movies_scan_disk",
            "bazarr_patch_movies_search_missing",
            "bazarr_patch_movies_search_wanted",
            "bazarr_patch_movies_sync",
            "bazarr_post_movies",
            "bazarr_post_movies_blacklist",
            "bazarr_post_movies_subtitles",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-plex",
        tools=(
            "bazarr_get_plex_autopulse_config",
            "bazarr_get_plex_libraries",
            "bazarr_get_plex_pin",
            "bazarr_get_plex_pin_check",
            "bazarr_get_plex_select_server",
            "bazarr_get_plex_servers",
            "bazarr_get_plex_test_connection",
            "bazarr_get_plex_validate",
            "bazarr_get_plex_webhook_list",
            "bazarr_post_plex_api_key",
            "bazarr_post_plex_encrypt_api_key",
            "bazarr_post_plex_logout",
            "bazarr_post_plex_pin",
            "bazarr_post_plex_select_server",
            "bazarr_post_plex_test_connection",
            "bazarr_post_plex_webhook_create",
            "bazarr_post_plex_webhook_delete",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-provider",
        tools=(
            "bazarr_post_provider_episodes",
            "bazarr_post_provider_movies",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-searches",
        tools=("bazarr_get_searches",),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-series",
        tools=(
            "bazarr_get_series",
            "bazarr_get_series_tags",
            "bazarr_patch_series_scan_disk",
            "bazarr_patch_series_search_missing",
            "bazarr_patch_series_search_wanted",
            "bazarr_patch_series_sync",
            "bazarr_post_series",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-subtitle",
        tools=(
            "bazarr_get_subtitle_name_contents",
            "bazarr_get_subtitle_name_info",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-subtitles",
        tools=(
            "bazarr_get_subtitles",
            "bazarr_patch_subtitles_extract",
            "bazarr_patch_subtitles_mod",
            "bazarr_patch_subtitles_sync",
            "bazarr_patch_subtitles_translate",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-system",
        tools=(
            "bazarr_delete_system_backups",
            "bazarr_delete_system_jobs",
            "bazarr_delete_system_logs",
            "bazarr_get_system_announcements",
            "bazarr_get_system_backups",
            "bazarr_get_system_jobs",
            "bazarr_get_system_logs",
            "bazarr_get_system_ping",
            "bazarr_get_system_releases",
            "bazarr_get_system_tasks",
            "bazarr_patch_system_backups",
            "bazarr_patch_system_jobs",
            "bazarr_patch_system_notifications",
            "bazarr_post_system_announcements",
            "bazarr_post_system_backups",
            "bazarr_post_system_jobs_force_start",
            "bazarr_post_system_jobs_move_bottom",
            "bazarr_post_system_jobs_move_top",
            "bazarr_post_system_restart",
            "bazarr_post_system_shutdown",
            "bazarr_post_system_webhook_test",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "bazarr-manage-web",
        tools=(
            "bazarr_post_web_hooks_plex",
            "bazarr_post_web_hooks_radarr",
            "bazarr_post_web_hooks_sonarr",
        ),
        prompts=("arr_operator", "subtitle_curator"),
        skills=("arr-subtitle-management",),
    ),
    SurfaceLink(
        "chaptarr-manage-",
        tools=("chaptarr_get_",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-api",
        tools=("chaptarr_get_api",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-author",
        tools=(
            "chaptarr_delete_author_editor",
            "chaptarr_delete_author_id",
            "chaptarr_get_author",
            "chaptarr_get_author_id",
            "chaptarr_put_author_editor",
            "chaptarr_put_author_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-blocklist",
        tools=(
            "chaptarr_delete_blocklist_bulk",
            "chaptarr_delete_blocklist_id",
            "chaptarr_get_blocklist",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-book",
        tools=(
            "chaptarr_delete_book_editor",
            "chaptarr_delete_book_id",
            "chaptarr_get_book",
            "chaptarr_get_book_id",
            "chaptarr_get_book_id_overview",
            "chaptarr_get_book_lookup",
            "chaptarr_post_book",
            "chaptarr_put_book_editor",
            "chaptarr_put_book_id",
            "chaptarr_put_book_monitor",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-bookfile",
        tools=(
            "chaptarr_delete_bookfile_bulk",
            "chaptarr_delete_bookfile_id",
            "chaptarr_get_bookfile",
            "chaptarr_get_bookfile_id",
            "chaptarr_put_bookfile_editor",
            "chaptarr_put_bookfile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-bookshelf",
        tools=("chaptarr_post_bookshelf",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-calendar",
        tools=(
            "chaptarr_get_calendar",
            "chaptarr_get_calendar_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-command",
        tools=(
            "chaptarr_delete_command_id",
            "chaptarr_get_command",
            "chaptarr_get_command_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-config",
        tools=(
            "chaptarr_get_config_development",
            "chaptarr_get_config_development_id",
            "chaptarr_get_config_downloadclient",
            "chaptarr_get_config_downloadclient_id",
            "chaptarr_get_config_host",
            "chaptarr_get_config_host_id",
            "chaptarr_get_config_indexer",
            "chaptarr_get_config_indexer_id",
            "chaptarr_get_config_mediamanagement",
            "chaptarr_get_config_mediamanagement_id",
            "chaptarr_get_config_metadataprovider",
            "chaptarr_get_config_metadataprovider_id",
            "chaptarr_get_config_naming",
            "chaptarr_get_config_naming_examples",
            "chaptarr_get_config_naming_id",
            "chaptarr_get_config_ui",
            "chaptarr_get_config_ui_id",
            "chaptarr_put_config_development_id",
            "chaptarr_put_config_downloadclient_id",
            "chaptarr_put_config_host_id",
            "chaptarr_put_config_indexer_id",
            "chaptarr_put_config_mediamanagement_id",
            "chaptarr_put_config_metadataprovider_id",
            "chaptarr_put_config_naming_id",
            "chaptarr_put_config_ui_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-content",
        tools=("chaptarr_get_content_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-customfilter",
        tools=(
            "chaptarr_delete_customfilter_id",
            "chaptarr_get_customfilter",
            "chaptarr_get_customfilter_id",
            "chaptarr_post_customfilter",
            "chaptarr_put_customfilter_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-customformat",
        tools=(
            "chaptarr_delete_customformat_id",
            "chaptarr_get_customformat",
            "chaptarr_get_customformat_id",
            "chaptarr_get_customformat_schema",
            "chaptarr_post_customformat",
            "chaptarr_put_customformat_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-delayprofile",
        tools=(
            "chaptarr_delete_delayprofile_id",
            "chaptarr_get_delayprofile",
            "chaptarr_get_delayprofile_id",
            "chaptarr_post_delayprofile",
            "chaptarr_put_delayprofile_id",
            "chaptarr_put_delayprofile_reorder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-diskspace",
        tools=("chaptarr_get_diskspace",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-downloadclient",
        tools=(
            "chaptarr_delete_downloadclient_bulk",
            "chaptarr_delete_downloadclient_id",
            "chaptarr_get_downloadclient",
            "chaptarr_get_downloadclient_id",
            "chaptarr_post_downloadclient_action_name",
            "chaptarr_post_downloadclient_testall",
            "chaptarr_put_downloadclient_bulk",
            "chaptarr_put_downloadclient_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-edition",
        tools=("chaptarr_get_edition",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-feed",
        tools=("chaptarr_get_feed_v1_calendar_readarrics",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-filesystem",
        tools=(
            "chaptarr_get_filesystem",
            "chaptarr_get_filesystem_mediafiles",
            "chaptarr_get_filesystem_type",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-history",
        tools=(
            "chaptarr_get_history",
            "chaptarr_get_history_author",
            "chaptarr_get_history_since",
            "chaptarr_post_history_failed_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-importlist",
        tools=(
            "chaptarr_delete_importlist_bulk",
            "chaptarr_delete_importlist_id",
            "chaptarr_get_importlist",
            "chaptarr_get_importlist_id",
            "chaptarr_get_importlist_schema",
            "chaptarr_post_importlist",
            "chaptarr_post_importlist_action_name",
            "chaptarr_post_importlist_test",
            "chaptarr_post_importlist_testall",
            "chaptarr_put_importlist_bulk",
            "chaptarr_put_importlist_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-importlistexclusion",
        tools=(
            "chaptarr_delete_importlistexclusion_id",
            "chaptarr_get_importlistexclusion",
            "chaptarr_get_importlistexclusion_id",
            "chaptarr_post_importlistexclusion",
            "chaptarr_put_importlistexclusion_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-indexer",
        tools=(
            "chaptarr_delete_indexer_bulk",
            "chaptarr_delete_indexer_id",
            "chaptarr_get_indexer",
            "chaptarr_get_indexer_id",
            "chaptarr_get_indexer_schema",
            "chaptarr_post_indexer",
            "chaptarr_post_indexer_action_name",
            "chaptarr_post_indexer_test",
            "chaptarr_post_indexer_testall",
            "chaptarr_put_indexer_bulk",
            "chaptarr_put_indexer_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-indexerflag",
        tools=("chaptarr_get_indexerflag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-language",
        tools=(
            "chaptarr_get_language",
            "chaptarr_get_language_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-localization",
        tools=("chaptarr_get_localization",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-log",
        tools=(
            "chaptarr_get_log",
            "chaptarr_get_log_file",
            "chaptarr_get_log_file_filename",
            "chaptarr_get_log_file_update",
            "chaptarr_get_log_file_update_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-login",
        tools=(
            "chaptarr_get_login",
            "chaptarr_post_login",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-logout",
        tools=("chaptarr_get_logout",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-manualimport",
        tools=(
            "chaptarr_get_manualimport",
            "chaptarr_post_manualimport",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-mediacover",
        tools=(
            "chaptarr_get_mediacover_author_author_id_filename",
            "chaptarr_get_mediacover_book_book_id_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-metadata",
        tools=(
            "chaptarr_delete_metadata_id",
            "chaptarr_get_metadata",
            "chaptarr_get_metadata_id",
            "chaptarr_get_metadata_schema",
            "chaptarr_post_metadata",
            "chaptarr_post_metadata_action_name",
            "chaptarr_post_metadata_test",
            "chaptarr_post_metadata_testall",
            "chaptarr_put_metadata_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-metadataprofile",
        tools=(
            "chaptarr_delete_metadataprofile_id",
            "chaptarr_get_metadataprofile_id",
            "chaptarr_get_metadataprofile_schema",
            "chaptarr_post_metadataprofile",
            "chaptarr_put_metadataprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-notification",
        tools=(
            "chaptarr_delete_notification_id",
            "chaptarr_get_notification",
            "chaptarr_get_notification_id",
            "chaptarr_get_notification_schema",
            "chaptarr_post_notification",
            "chaptarr_post_notification_action_name",
            "chaptarr_post_notification_test",
            "chaptarr_post_notification_testall",
            "chaptarr_put_notification_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-parse",
        tools=("chaptarr_get_parse",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-path",
        tools=("chaptarr_get_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-ping",
        tools=("chaptarr_get_ping",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-qualitydefinition",
        tools=(
            "chaptarr_get_qualitydefinition",
            "chaptarr_get_qualitydefinition_id",
            "chaptarr_put_qualitydefinition_id",
            "chaptarr_put_qualitydefinition_update",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-qualityprofile",
        tools=(
            "chaptarr_delete_qualityprofile_id",
            "chaptarr_get_qualityprofile_id",
            "chaptarr_get_qualityprofile_schema",
            "chaptarr_post_qualityprofile",
            "chaptarr_put_qualityprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-queue",
        tools=(
            "chaptarr_delete_queue_bulk",
            "chaptarr_delete_queue_id",
            "chaptarr_get_queue_details",
            "chaptarr_post_queue_grab_bulk",
            "chaptarr_post_queue_grab_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-release",
        tools=(
            "chaptarr_get_release",
            "chaptarr_post_release",
            "chaptarr_post_release_push",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-releaseprofile",
        tools=(
            "chaptarr_delete_releaseprofile_id",
            "chaptarr_get_releaseprofile",
            "chaptarr_get_releaseprofile_id",
            "chaptarr_post_releaseprofile",
            "chaptarr_put_releaseprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-remotepathmapping",
        tools=(
            "chaptarr_delete_remotepathmapping_id",
            "chaptarr_get_remotepathmapping",
            "chaptarr_get_remotepathmapping_id",
            "chaptarr_post_remotepathmapping",
            "chaptarr_put_remotepathmapping_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-rename",
        tools=("chaptarr_get_rename",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-retag",
        tools=("chaptarr_get_retag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-rootfolder",
        tools=(
            "chaptarr_delete_rootfolder_id",
            "chaptarr_get_rootfolder_id",
            "chaptarr_put_rootfolder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-search",
        tools=("chaptarr_get_search",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-series",
        tools=("chaptarr_get_series",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-system",
        tools=(
            "chaptarr_delete_system_backup_id",
            "chaptarr_get_system_backup",
            "chaptarr_get_system_routes",
            "chaptarr_get_system_routes_duplicate",
            "chaptarr_get_system_task",
            "chaptarr_get_system_task_id",
            "chaptarr_post_system_backup_restore_id",
            "chaptarr_post_system_backup_restore_upload",
            "chaptarr_post_system_restart",
            "chaptarr_post_system_shutdown",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-tag",
        tools=(
            "chaptarr_delete_tag_id",
            "chaptarr_get_tag",
            "chaptarr_get_tag_detail",
            "chaptarr_get_tag_detail_id",
            "chaptarr_get_tag_id",
            "chaptarr_post_tag",
            "chaptarr_put_tag_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-update",
        tools=("chaptarr_get_update",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "chaptarr-manage-wanted",
        tools=(
            "chaptarr_get_wanted_cutoff",
            "chaptarr_get_wanted_cutoff_id",
            "chaptarr_get_wanted_missing_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-book-library",),
    ),
    SurfaceLink(
        "lidarr-manage-",
        tools=("lidarr_get_",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-album",
        tools=(
            "lidarr_delete_album_id",
            "lidarr_get_album",
            "lidarr_get_album_id",
            "lidarr_get_album_lookup",
            "lidarr_post_album",
            "lidarr_put_album_id",
            "lidarr_put_album_monitor",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-albumstudio",
        tools=("lidarr_post_albumstudio",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-api",
        tools=("lidarr_get_api",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-artist",
        tools=(
            "lidarr_delete_artist_editor",
            "lidarr_delete_artist_id",
            "lidarr_get_artist_id",
            "lidarr_put_artist_editor",
            "lidarr_put_artist_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-autotagging",
        tools=(
            "lidarr_delete_autotagging_id",
            "lidarr_get_autotagging",
            "lidarr_get_autotagging_id",
            "lidarr_get_autotagging_schema",
            "lidarr_post_autotagging",
            "lidarr_put_autotagging_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-blocklist",
        tools=(
            "lidarr_delete_blocklist_bulk",
            "lidarr_delete_blocklist_id",
            "lidarr_get_blocklist",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-calendar",
        tools=(
            "lidarr_get_calendar",
            "lidarr_get_calendar_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-command",
        tools=(
            "lidarr_delete_command_id",
            "lidarr_get_command",
            "lidarr_get_command_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-config",
        tools=(
            "lidarr_get_config_downloadclient",
            "lidarr_get_config_downloadclient_id",
            "lidarr_get_config_host",
            "lidarr_get_config_host_id",
            "lidarr_get_config_indexer",
            "lidarr_get_config_indexer_id",
            "lidarr_get_config_mediamanagement",
            "lidarr_get_config_mediamanagement_id",
            "lidarr_get_config_metadataprovider",
            "lidarr_get_config_metadataprovider_id",
            "lidarr_get_config_naming",
            "lidarr_get_config_naming_examples",
            "lidarr_get_config_naming_id",
            "lidarr_get_config_ui",
            "lidarr_get_config_ui_id",
            "lidarr_put_config_downloadclient_id",
            "lidarr_put_config_host_id",
            "lidarr_put_config_indexer_id",
            "lidarr_put_config_mediamanagement_id",
            "lidarr_put_config_metadataprovider_id",
            "lidarr_put_config_naming_id",
            "lidarr_put_config_ui_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-content",
        tools=("lidarr_get_content_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-customfilter",
        tools=(
            "lidarr_delete_customfilter_id",
            "lidarr_get_customfilter",
            "lidarr_get_customfilter_id",
            "lidarr_post_customfilter",
            "lidarr_put_customfilter_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-customformat",
        tools=(
            "lidarr_delete_customformat_bulk",
            "lidarr_delete_customformat_id",
            "lidarr_get_customformat",
            "lidarr_get_customformat_id",
            "lidarr_get_customformat_schema",
            "lidarr_post_customformat",
            "lidarr_put_customformat_bulk",
            "lidarr_put_customformat_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-delayprofile",
        tools=(
            "lidarr_delete_delayprofile_id",
            "lidarr_get_delayprofile",
            "lidarr_get_delayprofile_id",
            "lidarr_post_delayprofile",
            "lidarr_put_delayprofile_id",
            "lidarr_put_delayprofile_reorder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-diskspace",
        tools=("lidarr_get_diskspace",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-downloadclient",
        tools=(
            "lidarr_delete_downloadclient_bulk",
            "lidarr_delete_downloadclient_id",
            "lidarr_get_downloadclient",
            "lidarr_get_downloadclient_id",
            "lidarr_get_downloadclient_schema",
            "lidarr_post_downloadclient",
            "lidarr_post_downloadclient_action_name",
            "lidarr_post_downloadclient_test",
            "lidarr_post_downloadclient_testall",
            "lidarr_put_downloadclient_bulk",
            "lidarr_put_downloadclient_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-feed",
        tools=("lidarr_get_feed_v1_calendar_lidarrics",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-filesystem",
        tools=(
            "lidarr_get_filesystem",
            "lidarr_get_filesystem_mediafiles",
            "lidarr_get_filesystem_type",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-history",
        tools=(
            "lidarr_get_history",
            "lidarr_get_history_artist",
            "lidarr_get_history_since",
            "lidarr_post_history_failed_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-importlist",
        tools=(
            "lidarr_delete_importlist_bulk",
            "lidarr_delete_importlist_id",
            "lidarr_get_importlist",
            "lidarr_get_importlist_id",
            "lidarr_get_importlist_schema",
            "lidarr_post_importlist",
            "lidarr_post_importlist_action_name",
            "lidarr_post_importlist_test",
            "lidarr_post_importlist_testall",
            "lidarr_put_importlist_bulk",
            "lidarr_put_importlist_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-importlistexclusion",
        tools=(
            "lidarr_delete_importlistexclusion_id",
            "lidarr_get_importlistexclusion",
            "lidarr_get_importlistexclusion_id",
            "lidarr_post_importlistexclusion",
            "lidarr_put_importlistexclusion_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-indexer",
        tools=(
            "lidarr_delete_indexer_bulk",
            "lidarr_delete_indexer_id",
            "lidarr_get_indexer",
            "lidarr_get_indexer_id",
            "lidarr_get_indexer_schema",
            "lidarr_post_indexer",
            "lidarr_post_indexer_action_name",
            "lidarr_post_indexer_test",
            "lidarr_post_indexer_testall",
            "lidarr_put_indexer_bulk",
            "lidarr_put_indexer_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-indexerflag",
        tools=("lidarr_get_indexerflag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-language",
        tools=(
            "lidarr_get_language",
            "lidarr_get_language_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-localization",
        tools=("lidarr_get_localization",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-log",
        tools=(
            "lidarr_get_log",
            "lidarr_get_log_file",
            "lidarr_get_log_file_filename",
            "lidarr_get_log_file_update",
            "lidarr_get_log_file_update_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-login",
        tools=(
            "lidarr_get_login",
            "lidarr_post_login",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-logout",
        tools=("lidarr_get_logout",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-manualimport",
        tools=(
            "lidarr_get_manualimport",
            "lidarr_post_manualimport",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-mediacover",
        tools=(
            "lidarr_get_mediacover_album_album_id_filename",
            "lidarr_get_mediacover_artist_artist_id_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-metadata",
        tools=(
            "lidarr_delete_metadata_id",
            "lidarr_get_metadata",
            "lidarr_get_metadata_id",
            "lidarr_get_metadata_schema",
            "lidarr_post_metadata",
            "lidarr_post_metadata_action_name",
            "lidarr_post_metadata_test",
            "lidarr_post_metadata_testall",
            "lidarr_put_metadata_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-metadataprofile",
        tools=(
            "lidarr_delete_metadataprofile_id",
            "lidarr_get_metadataprofile_id",
            "lidarr_get_metadataprofile_schema",
            "lidarr_post_metadataprofile",
            "lidarr_put_metadataprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-notification",
        tools=(
            "lidarr_delete_notification_id",
            "lidarr_get_notification",
            "lidarr_get_notification_id",
            "lidarr_get_notification_schema",
            "lidarr_post_notification",
            "lidarr_post_notification_action_name",
            "lidarr_post_notification_test",
            "lidarr_post_notification_testall",
            "lidarr_put_notification_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-parse",
        tools=("lidarr_get_parse",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-path",
        tools=("lidarr_get_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-ping",
        tools=("lidarr_get_ping",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-qualitydefinition",
        tools=(
            "lidarr_get_qualitydefinition",
            "lidarr_get_qualitydefinition_id",
            "lidarr_put_qualitydefinition_id",
            "lidarr_put_qualitydefinition_update",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-qualityprofile",
        tools=(
            "lidarr_delete_qualityprofile_id",
            "lidarr_get_qualityprofile_id",
            "lidarr_get_qualityprofile_schema",
            "lidarr_post_qualityprofile",
            "lidarr_put_qualityprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-queue",
        tools=(
            "lidarr_delete_queue_bulk",
            "lidarr_delete_queue_id",
            "lidarr_get_queue_details",
            "lidarr_post_queue_grab_bulk",
            "lidarr_post_queue_grab_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-release",
        tools=(
            "lidarr_get_release",
            "lidarr_post_release",
            "lidarr_post_release_push",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-releaseprofile",
        tools=(
            "lidarr_delete_releaseprofile_id",
            "lidarr_get_releaseprofile",
            "lidarr_get_releaseprofile_id",
            "lidarr_post_releaseprofile",
            "lidarr_put_releaseprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-remotepathmapping",
        tools=(
            "lidarr_delete_remotepathmapping_id",
            "lidarr_get_remotepathmapping",
            "lidarr_get_remotepathmapping_id",
            "lidarr_post_remotepathmapping",
            "lidarr_put_remotepathmapping_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-rename",
        tools=("lidarr_get_rename",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-retag",
        tools=("lidarr_get_retag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-rootfolder",
        tools=(
            "lidarr_delete_rootfolder_id",
            "lidarr_get_rootfolder_id",
            "lidarr_post_rootfolder",
            "lidarr_put_rootfolder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-search",
        tools=("lidarr_get_search",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-system",
        tools=(
            "lidarr_delete_system_backup_id",
            "lidarr_get_system_backup",
            "lidarr_get_system_routes",
            "lidarr_get_system_routes_duplicate",
            "lidarr_get_system_task",
            "lidarr_get_system_task_id",
            "lidarr_post_system_backup_restore_id",
            "lidarr_post_system_backup_restore_upload",
            "lidarr_post_system_restart",
            "lidarr_post_system_shutdown",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-tag",
        tools=(
            "lidarr_delete_tag_id",
            "lidarr_get_tag",
            "lidarr_get_tag_detail",
            "lidarr_get_tag_detail_id",
            "lidarr_get_tag_id",
            "lidarr_post_tag",
            "lidarr_put_tag_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-track",
        tools=(
            "lidarr_get_track",
            "lidarr_get_track_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-trackfile",
        tools=(
            "lidarr_delete_trackfile_bulk",
            "lidarr_delete_trackfile_id",
            "lidarr_get_trackfile",
            "lidarr_get_trackfile_id",
            "lidarr_put_trackfile_editor",
            "lidarr_put_trackfile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-update",
        tools=("lidarr_get_update",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "lidarr-manage-wanted",
        tools=(
            "lidarr_get_wanted_cutoff",
            "lidarr_get_wanted_cutoff_id",
            "lidarr_get_wanted_missing_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-music-library",),
    ),
    SurfaceLink(
        "prowlarr-manage-",
        tools=("prowlarr_get_",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-api",
        tools=("prowlarr_get_api",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-applications",
        tools=(
            "prowlarr_delete_applications_bulk",
            "prowlarr_delete_applications_id",
            "prowlarr_get_applications_id",
            "prowlarr_post_applications_action_name",
            "prowlarr_post_applications_testall",
            "prowlarr_put_applications_bulk",
            "prowlarr_put_applications_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-appprofile",
        tools=(
            "prowlarr_delete_appprofile_id",
            "prowlarr_get_appprofile",
            "prowlarr_get_appprofile_id",
            "prowlarr_get_appprofile_schema",
            "prowlarr_post_appprofile",
            "prowlarr_put_appprofile_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-command",
        tools=(
            "prowlarr_delete_command_id",
            "prowlarr_get_command",
            "prowlarr_get_command_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-config",
        tools=(
            "prowlarr_get_config_development",
            "prowlarr_get_config_development_id",
            "prowlarr_get_config_downloadclient",
            "prowlarr_get_config_downloadclient_id",
            "prowlarr_get_config_host",
            "prowlarr_get_config_host_id",
            "prowlarr_get_config_ui",
            "prowlarr_get_config_ui_id",
            "prowlarr_put_config_development_id",
            "prowlarr_put_config_downloadclient_id",
            "prowlarr_put_config_host_id",
            "prowlarr_put_config_ui_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-content",
        tools=("prowlarr_get_content_path",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-customfilter",
        tools=(
            "prowlarr_delete_customfilter_id",
            "prowlarr_get_customfilter",
            "prowlarr_get_customfilter_id",
            "prowlarr_post_customfilter",
            "prowlarr_put_customfilter_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-downloadclient",
        tools=(
            "prowlarr_delete_downloadclient_bulk",
            "prowlarr_delete_downloadclient_id",
            "prowlarr_get_downloadclient",
            "prowlarr_get_downloadclient_id",
            "prowlarr_get_downloadclient_schema",
            "prowlarr_post_downloadclient",
            "prowlarr_post_downloadclient_action_name",
            "prowlarr_post_downloadclient_test",
            "prowlarr_post_downloadclient_testall",
            "prowlarr_put_downloadclient_bulk",
            "prowlarr_put_downloadclient_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-filesystem",
        tools=(
            "prowlarr_get_filesystem",
            "prowlarr_get_filesystem_type",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-history",
        tools=(
            "prowlarr_get_history",
            "prowlarr_get_history_indexer",
            "prowlarr_get_history_since",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-id",
        tools=(
            "prowlarr_get_id_api",
            "prowlarr_get_id_download",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-indexer",
        tools=(
            "prowlarr_delete_indexer_bulk",
            "prowlarr_get_indexer_categories",
            "prowlarr_get_indexer_id_download",
            "prowlarr_get_indexer_id_newznab",
            "prowlarr_post_indexer_action_name",
            "prowlarr_post_indexer_testall",
            "prowlarr_put_indexer_bulk",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-indexerproxy",
        tools=(
            "prowlarr_delete_indexerproxy_id",
            "prowlarr_get_indexerproxy_id",
            "prowlarr_get_indexerproxy_schema",
            "prowlarr_post_indexerproxy",
            "prowlarr_post_indexerproxy_action_name",
            "prowlarr_post_indexerproxy_test",
            "prowlarr_post_indexerproxy_testall",
            "prowlarr_put_indexerproxy_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-indexerstats",
        tools=("prowlarr_get_indexerstats",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-localization",
        tools=(
            "prowlarr_get_localization",
            "prowlarr_get_localization_options",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-log",
        tools=(
            "prowlarr_get_log",
            "prowlarr_get_log_file",
            "prowlarr_get_log_file_filename",
            "prowlarr_get_log_file_update",
            "prowlarr_get_log_file_update_filename",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-login",
        tools=(
            "prowlarr_get_login",
            "prowlarr_post_login",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-logout",
        tools=("prowlarr_get_logout",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-notification",
        tools=(
            "prowlarr_delete_notification_id",
            "prowlarr_get_notification",
            "prowlarr_get_notification_id",
            "prowlarr_get_notification_schema",
            "prowlarr_post_notification",
            "prowlarr_post_notification_action_name",
            "prowlarr_post_notification_test",
            "prowlarr_post_notification_testall",
            "prowlarr_put_notification_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-path",
        tools=("prowlarr_get_path",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-ping",
        tools=("prowlarr_get_ping",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-search",
        tools=(
            "prowlarr_post_search",
            "prowlarr_post_search_bulk",
            "prowlarr_search",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-system",
        tools=(
            "prowlarr_delete_system_backup_id",
            "prowlarr_get_system_backup",
            "prowlarr_get_system_routes",
            "prowlarr_get_system_routes_duplicate",
            "prowlarr_get_system_task",
            "prowlarr_get_system_task_id",
            "prowlarr_post_system_backup_restore_id",
            "prowlarr_post_system_backup_restore_upload",
            "prowlarr_post_system_restart",
            "prowlarr_post_system_shutdown",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-tag",
        tools=(
            "prowlarr_delete_tag_id",
            "prowlarr_get_tag",
            "prowlarr_get_tag_detail",
            "prowlarr_get_tag_detail_id",
            "prowlarr_get_tag_id",
            "prowlarr_post_tag",
            "prowlarr_put_tag_id",
        ),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "prowlarr-manage-update",
        tools=("prowlarr_get_update",),
        prompts=("arr_operator", "indexer_maintainer"),
        skills=("arr-indexer-management",),
    ),
    SurfaceLink(
        "radarr-manage-",
        tools=("radarr_get_",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-alttitle",
        tools=(
            "radarr_get_alttitle",
            "radarr_get_alttitle_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-api",
        tools=("radarr_get_api",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-autotagging",
        tools=(
            "radarr_delete_autotagging_id",
            "radarr_get_autotagging",
            "radarr_get_autotagging_id",
            "radarr_get_autotagging_schema",
            "radarr_post_autotagging",
            "radarr_put_autotagging_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-blocklist",
        tools=(
            "radarr_delete_blocklist_bulk",
            "radarr_delete_blocklist_id",
            "radarr_get_blocklist",
            "radarr_get_blocklist_movie",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-calendar",
        tools=("radarr_get_calendar",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-collection",
        tools=(
            "radarr_get_collection",
            "radarr_get_collection_id",
            "radarr_put_collection",
            "radarr_put_collection_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-command",
        tools=(
            "radarr_delete_command_id",
            "radarr_get_command",
            "radarr_get_command_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-config",
        tools=(
            "radarr_get_config_downloadclient",
            "radarr_get_config_downloadclient_id",
            "radarr_get_config_host",
            "radarr_get_config_host_id",
            "radarr_get_config_importlist",
            "radarr_get_config_importlist_id",
            "radarr_get_config_indexer",
            "radarr_get_config_indexer_id",
            "radarr_get_config_mediamanagement",
            "radarr_get_config_mediamanagement_id",
            "radarr_get_config_metadata",
            "radarr_get_config_metadata_id",
            "radarr_get_config_naming",
            "radarr_get_config_naming_examples",
            "radarr_get_config_naming_id",
            "radarr_get_config_ui",
            "radarr_get_config_ui_id",
            "radarr_put_config_downloadclient_id",
            "radarr_put_config_host_id",
            "radarr_put_config_importlist_id",
            "radarr_put_config_indexer_id",
            "radarr_put_config_mediamanagement_id",
            "radarr_put_config_metadata_id",
            "radarr_put_config_naming_id",
            "radarr_put_config_ui_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-content",
        tools=("radarr_get_content_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-credit",
        tools=(
            "radarr_get_credit",
            "radarr_get_credit_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-customfilter",
        tools=(
            "radarr_delete_customfilter_id",
            "radarr_get_customfilter",
            "radarr_get_customfilter_id",
            "radarr_post_customfilter",
            "radarr_put_customfilter_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-customformat",
        tools=(
            "radarr_delete_customformat_bulk",
            "radarr_delete_customformat_id",
            "radarr_get_customformat",
            "radarr_get_customformat_id",
            "radarr_get_customformat_schema",
            "radarr_post_customformat",
            "radarr_put_customformat_bulk",
            "radarr_put_customformat_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-delayprofile",
        tools=(
            "radarr_delete_delayprofile_id",
            "radarr_get_delayprofile",
            "radarr_get_delayprofile_id",
            "radarr_post_delayprofile",
            "radarr_put_delayprofile_id",
            "radarr_put_delayprofile_reorder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-diskspace",
        tools=("radarr_get_diskspace",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-downloadclient",
        tools=(
            "radarr_delete_downloadclient_bulk",
            "radarr_delete_downloadclient_id",
            "radarr_get_downloadclient_id",
            "radarr_get_downloadclient_schema",
            "radarr_post_downloadclient",
            "radarr_post_downloadclient_action_name",
            "radarr_post_downloadclient_testall",
            "radarr_put_downloadclient_bulk",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-exclusions",
        tools=(
            "radarr_delete_exclusions_bulk",
            "radarr_delete_exclusions_id",
            "radarr_get_exclusions",
            "radarr_get_exclusions_id",
            "radarr_get_exclusions_paged",
            "radarr_post_exclusions",
            "radarr_post_exclusions_bulk",
            "radarr_put_exclusions_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-extrafile",
        tools=("radarr_get_extrafile",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-feed",
        tools=("radarr_get_feed_v3_calendar_radarrics",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-filesystem",
        tools=(
            "radarr_get_filesystem",
            "radarr_get_filesystem_mediafiles",
            "radarr_get_filesystem_type",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-history",
        tools=(
            "radarr_get_history",
            "radarr_get_history_movie",
            "radarr_get_history_since",
            "radarr_post_history_failed_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-importlist",
        tools=(
            "radarr_delete_importlist_bulk",
            "radarr_delete_importlist_id",
            "radarr_get_importlist",
            "radarr_get_importlist_id",
            "radarr_get_importlist_movie",
            "radarr_get_importlist_schema",
            "radarr_post_importlist",
            "radarr_post_importlist_action_name",
            "radarr_post_importlist_movie",
            "radarr_post_importlist_test",
            "radarr_post_importlist_testall",
            "radarr_put_importlist_bulk",
            "radarr_put_importlist_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-indexer",
        tools=(
            "radarr_delete_indexer_bulk",
            "radarr_delete_indexer_id",
            "radarr_get_indexer_id",
            "radarr_get_indexer_schema",
            "radarr_post_indexer",
            "radarr_post_indexer_action_name",
            "radarr_post_indexer_test",
            "radarr_post_indexer_testall",
            "radarr_put_indexer_bulk",
            "radarr_put_indexer_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-indexerflag",
        tools=("radarr_get_indexerflag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-language",
        tools=(
            "radarr_get_language",
            "radarr_get_language_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-localization",
        tools=(
            "radarr_get_localization",
            "radarr_get_localization_language",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-log",
        tools=(
            "radarr_get_log",
            "radarr_get_log_file",
            "radarr_get_log_file_filename",
            "radarr_get_log_file_update",
            "radarr_get_log_file_update_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-login",
        tools=(
            "radarr_get_login",
            "radarr_post_login",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-logout",
        tools=("radarr_get_logout",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-manualimport",
        tools=(
            "radarr_get_manualimport",
            "radarr_post_manualimport",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-mediacover",
        tools=("radarr_get_mediacover_movie_id_filename",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-metadata",
        tools=(
            "radarr_delete_metadata_id",
            "radarr_get_metadata",
            "radarr_get_metadata_id",
            "radarr_get_metadata_schema",
            "radarr_post_metadata",
            "radarr_post_metadata_action_name",
            "radarr_post_metadata_test",
            "radarr_post_metadata_testall",
            "radarr_put_metadata_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-movie",
        tools=(
            "radarr_delete_movie_editor",
            "radarr_delete_movie_id",
            "radarr_get_movie_id",
            "radarr_get_movie_id_folder",
            "radarr_get_movie_lookup_imdb",
            "radarr_get_movie_lookup_tmdb",
            "radarr_lookup_movie",
            "radarr_post_movie",
            "radarr_post_movie_import",
            "radarr_put_movie_editor",
            "radarr_put_movie_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-moviefile",
        tools=(
            "radarr_delete_moviefile_bulk",
            "radarr_delete_moviefile_id",
            "radarr_get_moviefile",
            "radarr_get_moviefile_id",
            "radarr_put_moviefile_bulk",
            "radarr_put_moviefile_editor",
            "radarr_put_moviefile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-notification",
        tools=(
            "radarr_delete_notification_id",
            "radarr_get_notification",
            "radarr_get_notification_id",
            "radarr_get_notification_schema",
            "radarr_post_notification",
            "radarr_post_notification_action_name",
            "radarr_post_notification_test",
            "radarr_post_notification_testall",
            "radarr_put_notification_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-parse",
        tools=("radarr_get_parse",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-path",
        tools=("radarr_get_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-ping",
        tools=("radarr_get_ping",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-qualitydefinition",
        tools=(
            "radarr_get_qualitydefinition",
            "radarr_get_qualitydefinition_id",
            "radarr_get_qualitydefinition_limits",
            "radarr_put_qualitydefinition_id",
            "radarr_put_qualitydefinition_update",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-qualityprofile",
        tools=(
            "radarr_delete_qualityprofile_id",
            "radarr_get_qualityprofile_id",
            "radarr_get_qualityprofile_schema",
            "radarr_post_qualityprofile",
            "radarr_put_qualityprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-queue",
        tools=(
            "radarr_delete_queue_bulk",
            "radarr_get_queue_details",
            "radarr_post_queue_grab_bulk",
            "radarr_post_queue_grab_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-release",
        tools=(
            "radarr_get_release",
            "radarr_post_release",
            "radarr_post_release_push",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-releaseprofile",
        tools=(
            "radarr_delete_releaseprofile_id",
            "radarr_get_releaseprofile",
            "radarr_get_releaseprofile_id",
            "radarr_post_releaseprofile",
            "radarr_put_releaseprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-remotepathmapping",
        tools=(
            "radarr_delete_remotepathmapping_id",
            "radarr_get_remotepathmapping",
            "radarr_get_remotepathmapping_id",
            "radarr_post_remotepathmapping",
            "radarr_put_remotepathmapping_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-rename",
        tools=("radarr_get_rename",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-rootfolder",
        tools=(
            "radarr_delete_rootfolder_id",
            "radarr_get_rootfolder_id",
            "radarr_post_rootfolder",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-system",
        tools=(
            "radarr_delete_system_backup_id",
            "radarr_get_system_backup",
            "radarr_get_system_routes",
            "radarr_get_system_routes_duplicate",
            "radarr_get_system_task",
            "radarr_get_system_task_id",
            "radarr_post_system_backup_restore_id",
            "radarr_post_system_backup_restore_upload",
            "radarr_post_system_restart",
            "radarr_post_system_shutdown",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-tag",
        tools=(
            "radarr_get_tag_detail",
            "radarr_get_tag_detail_id",
            "radarr_get_tag_id",
            "radarr_put_tag_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-update",
        tools=("radarr_get_update",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "radarr-manage-wanted",
        tools=("radarr_get_wanted_cutoff",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-movie-library",),
    ),
    SurfaceLink(
        "seerr-manage-auth",
        tools=(
            "seerr_get_auth_jellyfin_quickconnect_check",
            "seerr_get_auth_me",
            "seerr_post_auth_jellyfin",
            "seerr_post_auth_jellyfin_quickconnect_authenticate",
            "seerr_post_auth_jellyfin_quickconnect_initiate",
            "seerr_post_auth_local",
            "seerr_post_auth_logout",
            "seerr_post_auth_plex",
            "seerr_post_auth_reset_password",
            "seerr_post_auth_reset_password_guid",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-backdrops",
        tools=("seerr_get_backdrops",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-blacklist",
        tools=(
            "seerr_delete_blacklist_tmdb_id",
            "seerr_get_blacklist",
            "seerr_get_blacklist_tmdb_id",
            "seerr_post_blacklist",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-blocklist",
        tools=(
            "seerr_delete_blocklist_collection_id",
            "seerr_delete_blocklist_tmdb_id",
            "seerr_get_blocklist",
            "seerr_get_blocklist_tmdb_id",
            "seerr_post_blocklist",
            "seerr_post_blocklist_collection_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-certifications",
        tools=(
            "seerr_get_certifications_movie",
            "seerr_get_certifications_tv",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-collection",
        tools=("seerr_get_collection_id",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-discover",
        tools=(
            "seerr_get_discover_genreslider_movie",
            "seerr_get_discover_genreslider_tv",
            "seerr_get_discover_keyword_id_movies",
            "seerr_get_discover_movies",
            "seerr_get_discover_movies_genre_id",
            "seerr_get_discover_movies_language_language",
            "seerr_get_discover_movies_studio_id",
            "seerr_get_discover_movies_upcoming",
            "seerr_get_discover_trending",
            "seerr_get_discover_tv",
            "seerr_get_discover_tv_genre_id",
            "seerr_get_discover_tv_language_language",
            "seerr_get_discover_tv_network_id",
            "seerr_get_discover_tv_upcoming",
            "seerr_get_discover_watchlist",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-genres",
        tools=(
            "seerr_get_genres_movie",
            "seerr_get_genres_tv",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-issue",
        tools=(
            "seerr_delete_issue_comment_comment_id",
            "seerr_delete_issue_id",
            "seerr_get_issue",
            "seerr_get_issue_comment_comment_id",
            "seerr_get_issue_count",
            "seerr_get_issue_id",
            "seerr_post_issue",
            "seerr_post_issue_id_comment",
            "seerr_post_issue_id_status",
            "seerr_put_issue_comment_comment_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-keyword",
        tools=("seerr_get_keyword_id",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-languages",
        tools=("seerr_get_languages",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-media",
        tools=(
            "seerr_delete_media_id",
            "seerr_delete_media_id_file",
            "seerr_get_media",
            "seerr_get_media_id_watch_data",
            "seerr_post_media_id_status",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-movie",
        tools=(
            "seerr_get_movie_id_ratings",
            "seerr_get_movie_id_ratingscombined",
            "seerr_get_movie_id_recommendations",
            "seerr_get_movie_id_similar",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-network",
        tools=("seerr_get_network_id",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-override",
        tools=(
            "seerr_delete_override_rule_rule_id",
            "seerr_get_override_rule",
            "seerr_post_override_rule",
            "seerr_post_override_rule_advanced_request",
            "seerr_put_override_rule_rule_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-person",
        tools=(
            "seerr_get_person_id",
            "seerr_get_person_id_combined_credits",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-regions",
        tools=("seerr_get_regions",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-request",
        tools=(
            "seerr_delete_request_id",
            "seerr_put_request_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-search",
        tools=(
            "seerr_get_search_company",
            "seerr_get_search_keyword",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-service",
        tools=(
            "seerr_get_service_radarr_id",
            "seerr_get_service_sonarr_id",
            "seerr_get_service_sonarr_lookup_tmdb_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-settings",
        tools=(
            "seerr_delete_settings_discover_slider_id",
            "seerr_delete_settings_radarr_id",
            "seerr_delete_settings_sonarr_id",
            "seerr_get_settings_about",
            "seerr_get_settings_cache",
            "seerr_get_settings_discover",
            "seerr_get_settings_discover_reset",
            "seerr_get_settings_jellyfin",
            "seerr_get_settings_jellyfin_library",
            "seerr_get_settings_jellyfin_sync",
            "seerr_get_settings_jellyfin_users",
            "seerr_get_settings_jobs",
            "seerr_get_settings_logs",
            "seerr_get_settings_main",
            "seerr_get_settings_metadatas",
            "seerr_get_settings_network",
            "seerr_get_settings_notifications_discord",
            "seerr_get_settings_notifications_email",
            "seerr_get_settings_notifications_gotify",
            "seerr_get_settings_notifications_ntfy",
            "seerr_get_settings_notifications_pushbullet",
            "seerr_get_settings_notifications_pushover",
            "seerr_get_settings_notifications_pushover_sounds",
            "seerr_get_settings_notifications_slack",
            "seerr_get_settings_notifications_telegram",
            "seerr_get_settings_notifications_webhook",
            "seerr_get_settings_notifications_webpush",
            "seerr_get_settings_plex",
            "seerr_get_settings_plex_devices_servers",
            "seerr_get_settings_plex_library",
            "seerr_get_settings_plex_sync",
            "seerr_get_settings_plex_users",
            "seerr_get_settings_public",
            "seerr_get_settings_radarr_id_profiles",
            "seerr_get_settings_tautulli",
            "seerr_post_settings_cache_dns_entry_flush",
            "seerr_post_settings_cache_id_flush",
            "seerr_post_settings_discover",
            "seerr_post_settings_discover_add",
            "seerr_post_settings_initialize",
            "seerr_post_settings_jellyfin",
            "seerr_post_settings_jellyfin_library_sync",
            "seerr_post_settings_jellyfin_sync",
            "seerr_post_settings_jobs_job_id_cancel",
            "seerr_post_settings_jobs_job_id_run",
            "seerr_post_settings_jobs_job_id_schedule",
            "seerr_post_settings_main",
            "seerr_post_settings_main_regenerate",
            "seerr_post_settings_metadatas_test",
            "seerr_post_settings_network",
            "seerr_post_settings_notifications_discord",
            "seerr_post_settings_notifications_discord_test",
            "seerr_post_settings_notifications_email",
            "seerr_post_settings_notifications_email_test",
            "seerr_post_settings_notifications_gotify",
            "seerr_post_settings_notifications_gotify_test",
            "seerr_post_settings_notifications_ntfy",
            "seerr_post_settings_notifications_ntfy_test",
            "seerr_post_settings_notifications_pushbullet",
            "seerr_post_settings_notifications_pushbullet_test",
            "seerr_post_settings_notifications_pushover",
            "seerr_post_settings_notifications_pushover_test",
            "seerr_post_settings_notifications_slack",
            "seerr_post_settings_notifications_slack_test",
            "seerr_post_settings_notifications_telegram",
            "seerr_post_settings_notifications_telegram_test",
            "seerr_post_settings_notifications_webhook",
            "seerr_post_settings_notifications_webhook_test",
            "seerr_post_settings_notifications_webpush",
            "seerr_post_settings_notifications_webpush_test",
            "seerr_post_settings_plex",
            "seerr_post_settings_plex_library_sync",
            "seerr_post_settings_plex_sync",
            "seerr_post_settings_sonarr_test",
            "seerr_post_settings_tautulli",
            "seerr_put_settings_discover_slider_id",
            "seerr_put_settings_jellyfin_library_id",
            "seerr_put_settings_metadatas",
            "seerr_put_settings_plex_library_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-status",
        tools=("seerr_get_status_appdata",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-studio",
        tools=("seerr_get_studio_id",),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-tv",
        tools=(
            "seerr_get_tv_id",
            "seerr_get_tv_id_ratings",
            "seerr_get_tv_id_recommendations",
            "seerr_get_tv_id_season_number",
            "seerr_get_tv_id_similar",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-user",
        tools=(
            "seerr_delete_user_id",
            "seerr_delete_user_id_push_subscription_endpoint",
            "seerr_delete_user_id_settings_linked_accounts_jellyfin",
            "seerr_delete_user_id_settings_linked_accounts_plex",
            "seerr_get_user",
            "seerr_get_user_id",
            "seerr_get_user_id_push_subscription_endpoint",
            "seerr_get_user_id_push_subscriptions",
            "seerr_get_user_id_quota",
            "seerr_get_user_id_requests",
            "seerr_get_user_id_settings_main",
            "seerr_get_user_id_settings_notifications",
            "seerr_get_user_id_settings_password",
            "seerr_get_user_id_settings_permissions",
            "seerr_get_user_id_watch_data",
            "seerr_get_user_id_watchlist",
            "seerr_get_user_jellyfin_user_id",
            "seerr_post_user",
            "seerr_post_user_id_settings_linked_accounts_jellyfin",
            "seerr_post_user_id_settings_linked_accounts_jellyfin_quickconnect",
            "seerr_post_user_id_settings_linked_accounts_plex",
            "seerr_post_user_id_settings_main",
            "seerr_post_user_id_settings_notifications",
            "seerr_post_user_id_settings_password",
            "seerr_post_user_id_settings_permissions",
            "seerr_post_user_import_from_jellyfin",
            "seerr_post_user_import_from_plex",
            "seerr_post_user_register_push_subscription",
            "seerr_put_user",
            "seerr_put_user_id",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-watchlist",
        tools=(
            "seerr_delete_watchlist_tmdb_id",
            "seerr_post_watchlist",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "seerr-manage-watchproviders",
        tools=(
            "seerr_get_watchproviders_movies",
            "seerr_get_watchproviders_regions",
            "seerr_get_watchproviders_tv",
        ),
        prompts=("arr_operator", "request_manager"),
        skills=("arr-media-requests",),
    ),
    SurfaceLink(
        "sonarr-manage-",
        tools=("sonarr_get_",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-api",
        tools=("sonarr_get_api",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-autotagging",
        tools=(
            "sonarr_delete_autotagging_id",
            "sonarr_get_autotagging",
            "sonarr_get_autotagging_id",
            "sonarr_get_autotagging_schema",
            "sonarr_post_autotagging",
            "sonarr_put_autotagging_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-blocklist",
        tools=(
            "sonarr_delete_blocklist_bulk",
            "sonarr_delete_blocklist_id",
            "sonarr_get_blocklist",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-calendar",
        tools=(
            "sonarr_get_calendar",
            "sonarr_get_calendar_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-command",
        tools=(
            "sonarr_delete_command_id",
            "sonarr_get_command",
            "sonarr_get_command_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-config",
        tools=(
            "sonarr_get_config_downloadclient",
            "sonarr_get_config_downloadclient_id",
            "sonarr_get_config_host",
            "sonarr_get_config_host_id",
            "sonarr_get_config_importlist",
            "sonarr_get_config_importlist_id",
            "sonarr_get_config_indexer",
            "sonarr_get_config_indexer_id",
            "sonarr_get_config_mediamanagement",
            "sonarr_get_config_mediamanagement_id",
            "sonarr_get_config_naming",
            "sonarr_get_config_naming_examples",
            "sonarr_get_config_naming_id",
            "sonarr_get_config_ui",
            "sonarr_get_config_ui_id",
            "sonarr_put_config_downloadclient_id",
            "sonarr_put_config_host_id",
            "sonarr_put_config_importlist_id",
            "sonarr_put_config_indexer_id",
            "sonarr_put_config_mediamanagement_id",
            "sonarr_put_config_naming_id",
            "sonarr_put_config_ui_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-content",
        tools=("sonarr_get_content_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-customfilter",
        tools=(
            "sonarr_delete_customfilter_id",
            "sonarr_get_customfilter",
            "sonarr_get_customfilter_id",
            "sonarr_post_customfilter",
            "sonarr_put_customfilter_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-customformat",
        tools=(
            "sonarr_delete_customformat_bulk",
            "sonarr_delete_customformat_id",
            "sonarr_get_customformat",
            "sonarr_get_customformat_id",
            "sonarr_get_customformat_schema",
            "sonarr_post_customformat",
            "sonarr_put_customformat_bulk",
            "sonarr_put_customformat_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-delayprofile",
        tools=(
            "sonarr_delete_delayprofile_id",
            "sonarr_get_delayprofile",
            "sonarr_get_delayprofile_id",
            "sonarr_post_delayprofile",
            "sonarr_put_delayprofile_id",
            "sonarr_put_delayprofile_reorder_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-diskspace",
        tools=("sonarr_get_diskspace",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-downloadclient",
        tools=(
            "sonarr_delete_downloadclient_bulk",
            "sonarr_delete_downloadclient_id",
            "sonarr_get_downloadclient",
            "sonarr_get_downloadclient_id",
            "sonarr_get_downloadclient_schema",
            "sonarr_post_downloadclient",
            "sonarr_post_downloadclient_action_name",
            "sonarr_post_downloadclient_test",
            "sonarr_post_downloadclient_testall",
            "sonarr_put_downloadclient_bulk",
            "sonarr_put_downloadclient_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-episode",
        tools=(
            "sonarr_get_episode",
            "sonarr_get_episode_id",
            "sonarr_put_episode_id",
            "sonarr_put_episode_monitor",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-episodefile",
        tools=(
            "sonarr_delete_episodefile_bulk",
            "sonarr_delete_episodefile_id",
            "sonarr_get_episodefile",
            "sonarr_get_episodefile_id",
            "sonarr_put_episodefile_bulk",
            "sonarr_put_episodefile_editor",
            "sonarr_put_episodefile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-feed",
        tools=("sonarr_get_feed_v3_calendar_sonarrics",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-filesystem",
        tools=(
            "sonarr_get_filesystem",
            "sonarr_get_filesystem_mediafiles",
            "sonarr_get_filesystem_type",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-history",
        tools=(
            "sonarr_get_history",
            "sonarr_get_history_series",
            "sonarr_get_history_since",
            "sonarr_post_history_failed_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-importlist",
        tools=(
            "sonarr_delete_importlist_bulk",
            "sonarr_delete_importlist_id",
            "sonarr_get_importlist",
            "sonarr_get_importlist_id",
            "sonarr_get_importlist_schema",
            "sonarr_post_importlist",
            "sonarr_post_importlist_action_name",
            "sonarr_post_importlist_test",
            "sonarr_post_importlist_testall",
            "sonarr_put_importlist_bulk",
            "sonarr_put_importlist_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-importlistexclusion",
        tools=(
            "sonarr_delete_importlistexclusion_bulk",
            "sonarr_delete_importlistexclusion_id",
            "sonarr_get_importlistexclusion",
            "sonarr_get_importlistexclusion_id",
            "sonarr_get_importlistexclusion_paged",
            "sonarr_post_importlistexclusion",
            "sonarr_put_importlistexclusion_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-indexer",
        tools=(
            "sonarr_delete_indexer_bulk",
            "sonarr_delete_indexer_id",
            "sonarr_get_indexer",
            "sonarr_get_indexer_id",
            "sonarr_get_indexer_schema",
            "sonarr_post_indexer",
            "sonarr_post_indexer_action_name",
            "sonarr_post_indexer_test",
            "sonarr_post_indexer_testall",
            "sonarr_put_indexer_bulk",
            "sonarr_put_indexer_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-indexerflag",
        tools=("sonarr_get_indexerflag",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-language",
        tools=(
            "sonarr_get_language",
            "sonarr_get_language_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-languageprofile",
        tools=(
            "sonarr_delete_languageprofile_id",
            "sonarr_get_languageprofile",
            "sonarr_get_languageprofile_id",
            "sonarr_get_languageprofile_schema",
            "sonarr_post_languageprofile",
            "sonarr_put_languageprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-localization",
        tools=(
            "sonarr_get_localization",
            "sonarr_get_localization_id",
            "sonarr_get_localization_language",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-log",
        tools=(
            "sonarr_get_log",
            "sonarr_get_log_file",
            "sonarr_get_log_file_filename",
            "sonarr_get_log_file_update",
            "sonarr_get_log_file_update_filename",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-login",
        tools=(
            "sonarr_get_login",
            "sonarr_post_login",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-logout",
        tools=("sonarr_get_logout",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-manualimport",
        tools=(
            "sonarr_get_manualimport",
            "sonarr_post_manualimport",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-mediacover",
        tools=("sonarr_get_mediacover_series_id_filename",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-metadata",
        tools=(
            "sonarr_delete_metadata_id",
            "sonarr_get_metadata",
            "sonarr_get_metadata_id",
            "sonarr_get_metadata_schema",
            "sonarr_post_metadata",
            "sonarr_post_metadata_action_name",
            "sonarr_post_metadata_test",
            "sonarr_post_metadata_testall",
            "sonarr_put_metadata_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-notification",
        tools=(
            "sonarr_delete_notification_id",
            "sonarr_get_notification",
            "sonarr_get_notification_id",
            "sonarr_get_notification_schema",
            "sonarr_post_notification",
            "sonarr_post_notification_action_name",
            "sonarr_post_notification_test",
            "sonarr_post_notification_testall",
            "sonarr_put_notification_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-parse",
        tools=("sonarr_get_parse",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-path",
        tools=("sonarr_get_path",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-ping",
        tools=("sonarr_get_ping",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-qualitydefinition",
        tools=(
            "sonarr_get_qualitydefinition",
            "sonarr_get_qualitydefinition_id",
            "sonarr_get_qualitydefinition_limits",
            "sonarr_put_qualitydefinition_id",
            "sonarr_put_qualitydefinition_update",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-qualityprofile",
        tools=(
            "sonarr_delete_qualityprofile_id",
            "sonarr_get_qualityprofile_id",
            "sonarr_get_qualityprofile_schema",
            "sonarr_post_qualityprofile",
            "sonarr_put_qualityprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-queue",
        tools=(
            "sonarr_delete_queue_bulk",
            "sonarr_delete_queue_id",
            "sonarr_get_queue_details",
            "sonarr_post_queue_grab_bulk",
            "sonarr_post_queue_grab_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-release",
        tools=(
            "sonarr_get_release",
            "sonarr_post_release",
            "sonarr_post_release_push",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-releaseprofile",
        tools=(
            "sonarr_delete_releaseprofile_id",
            "sonarr_get_releaseprofile",
            "sonarr_get_releaseprofile_id",
            "sonarr_post_releaseprofile",
            "sonarr_put_releaseprofile_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-remotepathmapping",
        tools=(
            "sonarr_delete_remotepathmapping_id",
            "sonarr_get_remotepathmapping",
            "sonarr_get_remotepathmapping_id",
            "sonarr_post_remotepathmapping",
            "sonarr_put_remotepathmapping_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-rename",
        tools=(
            "sonarr_get_rename",
            "sonarr_get_rename_bulk",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-rootfolder",
        tools=(
            "sonarr_delete_rootfolder_id",
            "sonarr_get_rootfolder_id",
            "sonarr_post_rootfolder",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-seasonpass",
        tools=("sonarr_post_seasonpass",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-series",
        tools=(
            "sonarr_delete_series_editor",
            "sonarr_delete_series_id",
            "sonarr_get_series_id",
            "sonarr_get_series_id_folder",
            "sonarr_lookup_series",
            "sonarr_post_series",
            "sonarr_post_series_import",
            "sonarr_put_series_editor",
            "sonarr_put_series_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-system",
        tools=(
            "sonarr_delete_system_backup_id",
            "sonarr_get_system_backup",
            "sonarr_get_system_routes",
            "sonarr_get_system_routes_duplicate",
            "sonarr_get_system_task",
            "sonarr_get_system_task_id",
            "sonarr_post_system_backup_restore_id",
            "sonarr_post_system_backup_restore_upload",
            "sonarr_post_system_restart",
            "sonarr_post_system_shutdown",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-tag",
        tools=(
            "sonarr_get_tag_detail",
            "sonarr_get_tag_detail_id",
            "sonarr_get_tag_id",
            "sonarr_put_tag_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-update",
        tools=("sonarr_get_update",),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
    SurfaceLink(
        "sonarr-manage-wanted",
        tools=(
            "sonarr_get_wanted_cutoff",
            "sonarr_get_wanted_cutoff_id",
            "sonarr_get_wanted_missing_id",
        ),
        prompts=("arr_operator", "media_librarian"),
        skills=("arr-series-library",),
    ),
)

LOCATIONS = (
    DataLocation("arr-movies", ("Film",), "RADARR_BASE_URL", "radarr_get_movie"),
    DataLocation("arr-series", ("Series",), "SONARR_BASE_URL", "sonarr_get_series"),
    DataLocation("arr-artists", ("Library",), "LIDARR_BASE_URL", "lidarr_get_artist"),
    DataLocation(
        "arr-authors", ("Library",), "CHAPTARR_BASE_URL", "chaptarr_get_author"
    ),
    DataLocation(
        "arr-indexers", ("MediaIndexer",), "PROWLARR_BASE_URL", "prowlarr_get_indexer"
    ),
    DataLocation(
        "arr-subtitles",
        ("SubtitleStore",),
        "BAZARR_BASE_URL",
        "bazarr_get_episodes_wanted",
    ),
    DataLocation(
        "arr-requests", ("RequestQueue",), "SEERR_BASE_URL", "seerr_get_request"
    ),
    DataLocation("arr-queue", ("QueueItem",), "RADARR_BASE_URL", "radarr_get_queue"),
)

ROLES = (
    BusinessRole(
        "download monitor",
        tasks=(
            "arr-check-download-queue",
            "arr-ingest-library",
            "arr-remove-stalled-download",
            "arr-repair-download-client",
            "arr-suite-health-check",
        ),
    ),
    BusinessRole(
        "indexer maintainer",
        tasks=(
            "prowlarr-fix-failing-indexer",
            "prowlarr-manage-",
            "prowlarr-manage-api",
            "prowlarr-manage-applications",
            "prowlarr-manage-appprofile",
            "prowlarr-manage-command",
            "prowlarr-manage-config",
            "prowlarr-manage-content",
            "prowlarr-manage-customfilter",
            "prowlarr-manage-downloadclient",
            "prowlarr-manage-filesystem",
            "prowlarr-manage-history",
            "prowlarr-manage-id",
            "prowlarr-manage-indexer",
            "prowlarr-manage-indexerproxy",
            "prowlarr-manage-indexerstats",
            "prowlarr-manage-localization",
            "prowlarr-manage-log",
            "prowlarr-manage-login",
            "prowlarr-manage-logout",
            "prowlarr-manage-notification",
            "prowlarr-manage-path",
            "prowlarr-manage-ping",
            "prowlarr-manage-search",
            "prowlarr-manage-system",
            "prowlarr-manage-tag",
            "prowlarr-manage-update",
            "prowlarr-replace-dead-indexer",
            "prowlarr-search-releases",
            "prowlarr-sync-indexers",
        ),
    ),
    BusinessRole(
        "media librarian",
        tasks=(
            "arr-check-download-queue",
            "arr-remove-stalled-download",
            "chaptarr-add-author-and-search",
            "chaptarr-manage-",
            "chaptarr-manage-api",
            "chaptarr-manage-author",
            "chaptarr-manage-blocklist",
            "chaptarr-manage-book",
            "chaptarr-manage-bookfile",
            "chaptarr-manage-bookshelf",
            "chaptarr-manage-calendar",
            "chaptarr-manage-command",
            "chaptarr-manage-config",
            "chaptarr-manage-content",
            "chaptarr-manage-customfilter",
            "chaptarr-manage-customformat",
            "chaptarr-manage-delayprofile",
            "chaptarr-manage-diskspace",
            "chaptarr-manage-downloadclient",
            "chaptarr-manage-edition",
            "chaptarr-manage-feed",
            "chaptarr-manage-filesystem",
            "chaptarr-manage-history",
            "chaptarr-manage-importlist",
            "chaptarr-manage-importlistexclusion",
            "chaptarr-manage-indexer",
            "chaptarr-manage-indexerflag",
            "chaptarr-manage-language",
            "chaptarr-manage-localization",
            "chaptarr-manage-log",
            "chaptarr-manage-login",
            "chaptarr-manage-logout",
            "chaptarr-manage-manualimport",
            "chaptarr-manage-mediacover",
            "chaptarr-manage-metadata",
            "chaptarr-manage-metadataprofile",
            "chaptarr-manage-notification",
            "chaptarr-manage-parse",
            "chaptarr-manage-path",
            "chaptarr-manage-ping",
            "chaptarr-manage-qualitydefinition",
            "chaptarr-manage-qualityprofile",
            "chaptarr-manage-queue",
            "chaptarr-manage-release",
            "chaptarr-manage-releaseprofile",
            "chaptarr-manage-remotepathmapping",
            "chaptarr-manage-rename",
            "chaptarr-manage-retag",
            "chaptarr-manage-rootfolder",
            "chaptarr-manage-search",
            "chaptarr-manage-series",
            "chaptarr-manage-system",
            "chaptarr-manage-tag",
            "chaptarr-manage-update",
            "chaptarr-manage-wanted",
            "chaptarr-provision-book-library",
            "chaptarr-search-missing",
            "lidarr-add-artist-and-search",
            "lidarr-manage-",
            "lidarr-manage-album",
            "lidarr-manage-albumstudio",
            "lidarr-manage-api",
            "lidarr-manage-artist",
            "lidarr-manage-autotagging",
            "lidarr-manage-blocklist",
            "lidarr-manage-calendar",
            "lidarr-manage-command",
            "lidarr-manage-config",
            "lidarr-manage-content",
            "lidarr-manage-customfilter",
            "lidarr-manage-customformat",
            "lidarr-manage-delayprofile",
            "lidarr-manage-diskspace",
            "lidarr-manage-downloadclient",
            "lidarr-manage-feed",
            "lidarr-manage-filesystem",
            "lidarr-manage-history",
            "lidarr-manage-importlist",
            "lidarr-manage-importlistexclusion",
            "lidarr-manage-indexer",
            "lidarr-manage-indexerflag",
            "lidarr-manage-language",
            "lidarr-manage-localization",
            "lidarr-manage-log",
            "lidarr-manage-login",
            "lidarr-manage-logout",
            "lidarr-manage-manualimport",
            "lidarr-manage-mediacover",
            "lidarr-manage-metadata",
            "lidarr-manage-metadataprofile",
            "lidarr-manage-notification",
            "lidarr-manage-parse",
            "lidarr-manage-path",
            "lidarr-manage-ping",
            "lidarr-manage-qualitydefinition",
            "lidarr-manage-qualityprofile",
            "lidarr-manage-queue",
            "lidarr-manage-release",
            "lidarr-manage-releaseprofile",
            "lidarr-manage-remotepathmapping",
            "lidarr-manage-rename",
            "lidarr-manage-retag",
            "lidarr-manage-rootfolder",
            "lidarr-manage-search",
            "lidarr-manage-system",
            "lidarr-manage-tag",
            "lidarr-manage-track",
            "lidarr-manage-trackfile",
            "lidarr-manage-update",
            "lidarr-manage-wanted",
            "lidarr-search-missing",
            "radarr-add-and-search",
            "radarr-manage-",
            "radarr-manage-alttitle",
            "radarr-manage-api",
            "radarr-manage-autotagging",
            "radarr-manage-blocklist",
            "radarr-manage-calendar",
            "radarr-manage-collection",
            "radarr-manage-command",
            "radarr-manage-config",
            "radarr-manage-content",
            "radarr-manage-credit",
            "radarr-manage-customfilter",
            "radarr-manage-customformat",
            "radarr-manage-delayprofile",
            "radarr-manage-diskspace",
            "radarr-manage-downloadclient",
            "radarr-manage-exclusions",
            "radarr-manage-extrafile",
            "radarr-manage-feed",
            "radarr-manage-filesystem",
            "radarr-manage-history",
            "radarr-manage-importlist",
            "radarr-manage-indexer",
            "radarr-manage-indexerflag",
            "radarr-manage-language",
            "radarr-manage-localization",
            "radarr-manage-log",
            "radarr-manage-login",
            "radarr-manage-logout",
            "radarr-manage-manualimport",
            "radarr-manage-mediacover",
            "radarr-manage-metadata",
            "radarr-manage-movie",
            "radarr-manage-moviefile",
            "radarr-manage-notification",
            "radarr-manage-parse",
            "radarr-manage-path",
            "radarr-manage-ping",
            "radarr-manage-qualitydefinition",
            "radarr-manage-qualityprofile",
            "radarr-manage-queue",
            "radarr-manage-release",
            "radarr-manage-releaseprofile",
            "radarr-manage-remotepathmapping",
            "radarr-manage-rename",
            "radarr-manage-rootfolder",
            "radarr-manage-system",
            "radarr-manage-tag",
            "radarr-manage-update",
            "radarr-manage-wanted",
            "radarr-search-missing",
            "radarr-tag-roundtrip",
            "sonarr-add-and-search",
            "sonarr-manage-",
            "sonarr-manage-api",
            "sonarr-manage-autotagging",
            "sonarr-manage-blocklist",
            "sonarr-manage-calendar",
            "sonarr-manage-command",
            "sonarr-manage-config",
            "sonarr-manage-content",
            "sonarr-manage-customfilter",
            "sonarr-manage-customformat",
            "sonarr-manage-delayprofile",
            "sonarr-manage-diskspace",
            "sonarr-manage-downloadclient",
            "sonarr-manage-episode",
            "sonarr-manage-episodefile",
            "sonarr-manage-feed",
            "sonarr-manage-filesystem",
            "sonarr-manage-history",
            "sonarr-manage-importlist",
            "sonarr-manage-importlistexclusion",
            "sonarr-manage-indexer",
            "sonarr-manage-indexerflag",
            "sonarr-manage-language",
            "sonarr-manage-languageprofile",
            "sonarr-manage-localization",
            "sonarr-manage-log",
            "sonarr-manage-login",
            "sonarr-manage-logout",
            "sonarr-manage-manualimport",
            "sonarr-manage-mediacover",
            "sonarr-manage-metadata",
            "sonarr-manage-notification",
            "sonarr-manage-parse",
            "sonarr-manage-path",
            "sonarr-manage-ping",
            "sonarr-manage-qualitydefinition",
            "sonarr-manage-qualityprofile",
            "sonarr-manage-queue",
            "sonarr-manage-release",
            "sonarr-manage-releaseprofile",
            "sonarr-manage-remotepathmapping",
            "sonarr-manage-rename",
            "sonarr-manage-rootfolder",
            "sonarr-manage-seasonpass",
            "sonarr-manage-series",
            "sonarr-manage-system",
            "sonarr-manage-tag",
            "sonarr-manage-update",
            "sonarr-manage-wanted",
            "sonarr-search-missing",
            "sonarr-tag-roundtrip",
        ),
    ),
    BusinessRole(
        "request manager",
        tasks=(
            "arr-check-download-queue",
            "arr-remove-stalled-download",
            "seerr-manage-auth",
            "seerr-manage-backdrops",
            "seerr-manage-blacklist",
            "seerr-manage-blocklist",
            "seerr-manage-certifications",
            "seerr-manage-collection",
            "seerr-manage-discover",
            "seerr-manage-genres",
            "seerr-manage-issue",
            "seerr-manage-keyword",
            "seerr-manage-languages",
            "seerr-manage-media",
            "seerr-manage-movie",
            "seerr-manage-network",
            "seerr-manage-override",
            "seerr-manage-person",
            "seerr-manage-regions",
            "seerr-manage-request",
            "seerr-manage-search",
            "seerr-manage-service",
            "seerr-manage-settings",
            "seerr-manage-status",
            "seerr-manage-studio",
            "seerr-manage-tv",
            "seerr-manage-user",
            "seerr-manage-watchlist",
            "seerr-manage-watchproviders",
            "seerr-request-title",
            "seerr-retry-failed",
            "seerr-route-requests-by-quality",
            "seerr-triage-requests",
        ),
    ),
    BusinessRole(
        "subtitle curator",
        tasks=(
            "bazarr-connect-sonarr-radarr",
            "bazarr-download-wanted-subtitles",
            "bazarr-enable-free-providers",
            "bazarr-manage-browse",
            "bazarr-manage-episodes",
            "bazarr-manage-history",
            "bazarr-manage-jellyfin",
            "bazarr-manage-languages",
            "bazarr-manage-movies",
            "bazarr-manage-plex",
            "bazarr-manage-provider",
            "bazarr-manage-searches",
            "bazarr-manage-series",
            "bazarr-manage-subtitle",
            "bazarr-manage-subtitles",
            "bazarr-manage-system",
            "bazarr-manage-web",
            "bazarr-reset-providers",
        ),
    ),
)
