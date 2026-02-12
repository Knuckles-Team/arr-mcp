#!/usr/bin/python
import sys

# coding: utf-8
import json
import os
import argparse
import logging
import uvicorn
import httpx
from typing import Optional, Any, List
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import (
    load_mcp_servers,
    MCPServerStreamableHTTP,
    MCPServerSSE,
)
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from arr_mcp.utils import (
    to_integer,
    to_boolean,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    tool_in_tag,
    prune_large_messages,
)

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "0.2.7"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-coder-next")
DEFAULT_LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:1234/v1")
DEFAULT_LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_SKILLS_DIRECTORY = os.getenv("SKILLS_DIRECTORY", get_skills_path())
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))
DEFAULT_SSL_VERIFY = to_boolean(os.getenv("SSL_VERIFY", "True"))

DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "16384"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_SEED = to_integer(os.getenv("SEED", None))
DEFAULT_PRESENCE_PENALTY = to_float(os.getenv("PRESENCE_PENALTY", "0.0"))
DEFAULT_FREQUENCY_PENALTY = to_float(os.getenv("FREQUENCY_PENALTY", "0.0"))
DEFAULT_LOGIT_BIAS = to_dict(os.getenv("LOGIT_BIAS", None))
DEFAULT_STOP_SEQUENCES = to_list(os.getenv("STOP_SEQUENCES", None))
DEFAULT_EXTRA_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))
DEFAULT_EXTRA_BODY = to_dict(os.getenv("EXTRA_BODY", None))

AGENT_NAME = "SonarrAgent"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing Sonarr resources via delegated specialists."
)


SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the Sonarr Supervisor Agent.\n"
        "Your goal is to assist the user by assigning tasks to specialized child agents through your available toolset.\n"
        "Analyze the user's request and determine which domain(s) it falls into.\n"
        "Then, call the appropriate tool(s) to delegate the task.\n"
        "Synthesize the results from the child agents into a final helpful response.\n"
        "Always be warm, professional, and helpful."
        "Note: The final response should contain all the relevant information from the tool executions. Never leave out any relevant information or leave it to the user to find it. "
        "You are the final authority on the user's request and the final communicator to the user. Present information as logically and concisely as possible. "
        "Explore using organized output with headers, sections, lists, and tables to make the information easy to navigate. "
        "If there are gaps in the information, clearly state that information is missing. Do not make assumptions or invent placeholder information, only use the information which is available."
    ),
)

APIINFO_AGENT_PROMPT = os.environ.get(
    "APIINFO_AGENT_PROMPT",
    default=(
        "You are the Sonarr ApiInfo Agent.\n"
        "Your goal is to manage api info resources.\n"
        "You have access to tools specifically tagged with 'ApiInfo'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

AUTHENTICATION_AGENT_PROMPT = os.environ.get(
    "AUTHENTICATION_AGENT_PROMPT",
    default=(
        "You are the Sonarr Authentication Agent.\n"
        "Your goal is to manage authentication resources.\n"
        "You have access to tools specifically tagged with 'Authentication'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

AUTOTAGGING_AGENT_PROMPT = os.environ.get(
    "AUTOTAGGING_AGENT_PROMPT",
    default=(
        "You are the Sonarr AutoTagging Agent.\n"
        "Your goal is to manage auto tagging resources.\n"
        "You have access to tools specifically tagged with 'AutoTagging'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BACKUP_AGENT_PROMPT = os.environ.get(
    "BACKUP_AGENT_PROMPT",
    default=(
        "You are the Sonarr Backup Agent.\n"
        "Your goal is to manage backup resources.\n"
        "You have access to tools specifically tagged with 'Backup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BLOCKLIST_AGENT_PROMPT = os.environ.get(
    "BLOCKLIST_AGENT_PROMPT",
    default=(
        "You are the Sonarr Blocklist Agent.\n"
        "Your goal is to manage blocklist resources.\n"
        "You have access to tools specifically tagged with 'Blocklist'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDAR_AGENT_PROMPT = os.environ.get(
    "CALENDAR_AGENT_PROMPT",
    default=(
        "You are the Sonarr Calendar Agent.\n"
        "Your goal is to manage calendar resources.\n"
        "You have access to tools specifically tagged with 'Calendar'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDARFEED_AGENT_PROMPT = os.environ.get(
    "CALENDARFEED_AGENT_PROMPT",
    default=(
        "You are the Sonarr CalendarFeed Agent.\n"
        "Your goal is to manage calendar feed resources.\n"
        "You have access to tools specifically tagged with 'CalendarFeed'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

COMMAND_AGENT_PROMPT = os.environ.get(
    "COMMAND_AGENT_PROMPT",
    default=(
        "You are the Sonarr Command Agent.\n"
        "Your goal is to manage command resources.\n"
        "You have access to tools specifically tagged with 'Command'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFILTER_AGENT_PROMPT = os.environ.get(
    "CUSTOMFILTER_AGENT_PROMPT",
    default=(
        "You are the Sonarr CustomFilter Agent.\n"
        "Your goal is to manage custom filter resources.\n"
        "You have access to tools specifically tagged with 'CustomFilter'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFORMAT_AGENT_PROMPT = os.environ.get(
    "CUSTOMFORMAT_AGENT_PROMPT",
    default=(
        "You are the Sonarr CustomFormat Agent.\n"
        "Your goal is to manage custom format resources.\n"
        "You have access to tools specifically tagged with 'CustomFormat'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUTOFF_AGENT_PROMPT = os.environ.get(
    "CUTOFF_AGENT_PROMPT",
    default=(
        "You are the Sonarr Cutoff Agent.\n"
        "Your goal is to manage cutoff resources.\n"
        "You have access to tools specifically tagged with 'Cutoff'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DELAYPROFILE_AGENT_PROMPT = os.environ.get(
    "DELAYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr DelayProfile Agent.\n"
        "Your goal is to manage delay profile resources.\n"
        "You have access to tools specifically tagged with 'DelayProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DISKSPACE_AGENT_PROMPT = os.environ.get(
    "DISKSPACE_AGENT_PROMPT",
    default=(
        "You are the Sonarr DiskSpace Agent.\n"
        "Your goal is to manage disk space resources.\n"
        "You have access to tools specifically tagged with 'DiskSpace'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENT_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENT_AGENT_PROMPT",
    default=(
        "You are the Sonarr DownloadClient Agent.\n"
        "Your goal is to manage download client resources.\n"
        "You have access to tools specifically tagged with 'DownloadClient'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr DownloadClientConfig Agent.\n"
        "Your goal is to manage download client config resources.\n"
        "You have access to tools specifically tagged with 'DownloadClientConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

EPISODE_AGENT_PROMPT = os.environ.get(
    "EPISODE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Episode Agent.\n"
        "Your goal is to manage episode resources.\n"
        "You have access to tools specifically tagged with 'Episode'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

EPISODEFILE_AGENT_PROMPT = os.environ.get(
    "EPISODEFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr EpisodeFile Agent.\n"
        "Your goal is to manage episode file resources.\n"
        "You have access to tools specifically tagged with 'EpisodeFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

FILESYSTEM_AGENT_PROMPT = os.environ.get(
    "FILESYSTEM_AGENT_PROMPT",
    default=(
        "You are the Sonarr FileSystem Agent.\n"
        "Your goal is to manage file system resources.\n"
        "You have access to tools specifically tagged with 'FileSystem'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HEALTH_AGENT_PROMPT = os.environ.get(
    "HEALTH_AGENT_PROMPT",
    default=(
        "You are the Sonarr Health Agent.\n"
        "Your goal is to manage health resources.\n"
        "You have access to tools specifically tagged with 'Health'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HISTORY_AGENT_PROMPT = os.environ.get(
    "HISTORY_AGENT_PROMPT",
    default=(
        "You are the Sonarr History Agent.\n"
        "Your goal is to manage history resources.\n"
        "You have access to tools specifically tagged with 'History'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HOSTCONFIG_AGENT_PROMPT = os.environ.get(
    "HOSTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr HostConfig Agent.\n"
        "Your goal is to manage host config resources.\n"
        "You have access to tools specifically tagged with 'HostConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLIST_AGENT_PROMPT = os.environ.get(
    "IMPORTLIST_AGENT_PROMPT",
    default=(
        "You are the Sonarr ImportList Agent.\n"
        "Your goal is to manage import list resources.\n"
        "You have access to tools specifically tagged with 'ImportList'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLISTCONFIG_AGENT_PROMPT = os.environ.get(
    "IMPORTLISTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr ImportListConfig Agent.\n"
        "Your goal is to manage import list config resources.\n"
        "You have access to tools specifically tagged with 'ImportListConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLISTEXCLUSION_AGENT_PROMPT = os.environ.get(
    "IMPORTLISTEXCLUSION_AGENT_PROMPT",
    default=(
        "You are the Sonarr ImportListExclusion Agent.\n"
        "Your goal is to manage import list exclusion resources.\n"
        "You have access to tools specifically tagged with 'ImportListExclusion'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXER_AGENT_PROMPT = os.environ.get(
    "INDEXER_AGENT_PROMPT",
    default=(
        "You are the Sonarr Indexer Agent.\n"
        "Your goal is to manage indexer resources.\n"
        "You have access to tools specifically tagged with 'Indexer'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERCONFIG_AGENT_PROMPT = os.environ.get(
    "INDEXERCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr IndexerConfig Agent.\n"
        "Your goal is to manage indexer config resources.\n"
        "You have access to tools specifically tagged with 'IndexerConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERFLAG_AGENT_PROMPT = os.environ.get(
    "INDEXERFLAG_AGENT_PROMPT",
    default=(
        "You are the Sonarr IndexerFlag Agent.\n"
        "Your goal is to manage indexer flag resources.\n"
        "You have access to tools specifically tagged with 'IndexerFlag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LANGUAGE_AGENT_PROMPT = os.environ.get(
    "LANGUAGE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Language Agent.\n"
        "Your goal is to manage language resources.\n"
        "You have access to tools specifically tagged with 'Language'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LANGUAGEPROFILE_AGENT_PROMPT = os.environ.get(
    "LANGUAGEPROFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr LanguageProfile Agent.\n"
        "Your goal is to manage language profile resources.\n"
        "You have access to tools specifically tagged with 'LanguageProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LANGUAGEPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "LANGUAGEPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Sonarr LanguageProfileSchema Agent.\n"
        "Your goal is to manage language profile schema resources.\n"
        "You have access to tools specifically tagged with 'LanguageProfileSchema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOCALIZATION_AGENT_PROMPT = os.environ.get(
    "LOCALIZATION_AGENT_PROMPT",
    default=(
        "You are the Sonarr Localization Agent.\n"
        "Your goal is to manage localization resources.\n"
        "You have access to tools specifically tagged with 'Localization'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOG_AGENT_PROMPT = os.environ.get(
    "LOG_AGENT_PROMPT",
    default=(
        "You are the Sonarr Log Agent.\n"
        "Your goal is to manage log resources.\n"
        "You have access to tools specifically tagged with 'Log'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOGFILE_AGENT_PROMPT = os.environ.get(
    "LOGFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr LogFile Agent.\n"
        "Your goal is to manage log file resources.\n"
        "You have access to tools specifically tagged with 'LogFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MANUALIMPORT_AGENT_PROMPT = os.environ.get(
    "MANUALIMPORT_AGENT_PROMPT",
    default=(
        "You are the Sonarr ManualImport Agent.\n"
        "Your goal is to manage manual import resources.\n"
        "You have access to tools specifically tagged with 'ManualImport'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIACOVER_AGENT_PROMPT = os.environ.get(
    "MEDIACOVER_AGENT_PROMPT",
    default=(
        "You are the Sonarr MediaCover Agent.\n"
        "Your goal is to manage media cover resources.\n"
        "You have access to tools specifically tagged with 'MediaCover'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIAMANAGEMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "MEDIAMANAGEMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr MediaManagementConfig Agent.\n"
        "Your goal is to manage media management config resources.\n"
        "You have access to tools specifically tagged with 'MediaManagementConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATA_AGENT_PROMPT = os.environ.get(
    "METADATA_AGENT_PROMPT",
    default=(
        "You are the Sonarr Metadata Agent.\n"
        "Your goal is to manage metadata resources.\n"
        "You have access to tools specifically tagged with 'Metadata'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MISSING_AGENT_PROMPT = os.environ.get(
    "MISSING_AGENT_PROMPT",
    default=(
        "You are the Sonarr Missing Agent.\n"
        "Your goal is to manage missing resources.\n"
        "You have access to tools specifically tagged with 'Missing'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NAMINGCONFIG_AGENT_PROMPT = os.environ.get(
    "NAMINGCONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr NamingConfig Agent.\n"
        "Your goal is to manage naming config resources.\n"
        "You have access to tools specifically tagged with 'NamingConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NOTIFICATION_AGENT_PROMPT = os.environ.get(
    "NOTIFICATION_AGENT_PROMPT",
    default=(
        "You are the Sonarr Notification Agent.\n"
        "Your goal is to manage notification resources.\n"
        "You have access to tools specifically tagged with 'Notification'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PARSE_AGENT_PROMPT = os.environ.get(
    "PARSE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Parse Agent.\n"
        "Your goal is to manage parse resources.\n"
        "You have access to tools specifically tagged with 'Parse'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PING_AGENT_PROMPT = os.environ.get(
    "PING_AGENT_PROMPT",
    default=(
        "You are the Sonarr Ping Agent.\n"
        "Your goal is to manage ping resources.\n"
        "You have access to tools specifically tagged with 'Ping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYDEFINITION_AGENT_PROMPT = os.environ.get(
    "QUALITYDEFINITION_AGENT_PROMPT",
    default=(
        "You are the Sonarr QualityDefinition Agent.\n"
        "Your goal is to manage quality definition resources.\n"
        "You have access to tools specifically tagged with 'QualityDefinition'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILE_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr QualityProfile Agent.\n"
        "Your goal is to manage quality profile resources.\n"
        "You have access to tools specifically tagged with 'QualityProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Sonarr QualityProfileSchema Agent.\n"
        "Your goal is to manage quality profile schema resources.\n"
        "You have access to tools specifically tagged with 'QualityProfileSchema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUE_AGENT_PROMPT = os.environ.get(
    "QUEUE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Queue Agent.\n"
        "Your goal is to manage queue resources.\n"
        "You have access to tools specifically tagged with 'Queue'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEACTION_AGENT_PROMPT = os.environ.get(
    "QUEUEACTION_AGENT_PROMPT",
    default=(
        "You are the Sonarr QueueAction Agent.\n"
        "Your goal is to manage queue action resources.\n"
        "You have access to tools specifically tagged with 'QueueAction'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEDETAILS_AGENT_PROMPT = os.environ.get(
    "QUEUEDETAILS_AGENT_PROMPT",
    default=(
        "You are the Sonarr QueueDetails Agent.\n"
        "Your goal is to manage queue details resources.\n"
        "You have access to tools specifically tagged with 'QueueDetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUESTATUS_AGENT_PROMPT = os.environ.get(
    "QUEUESTATUS_AGENT_PROMPT",
    default=(
        "You are the Sonarr QueueStatus Agent.\n"
        "Your goal is to manage queue status resources.\n"
        "You have access to tools specifically tagged with 'QueueStatus'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASE_AGENT_PROMPT = os.environ.get(
    "RELEASE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Release Agent.\n"
        "Your goal is to manage release resources.\n"
        "You have access to tools specifically tagged with 'Release'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPROFILE_AGENT_PROMPT = os.environ.get(
    "RELEASEPROFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr ReleaseProfile Agent.\n"
        "Your goal is to manage release profile resources.\n"
        "You have access to tools specifically tagged with 'ReleaseProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPUSH_AGENT_PROMPT = os.environ.get(
    "RELEASEPUSH_AGENT_PROMPT",
    default=(
        "You are the Sonarr ReleasePush Agent.\n"
        "Your goal is to manage release push resources.\n"
        "You have access to tools specifically tagged with 'ReleasePush'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

REMOTEPATHMAPPING_AGENT_PROMPT = os.environ.get(
    "REMOTEPATHMAPPING_AGENT_PROMPT",
    default=(
        "You are the Sonarr RemotePathMapping Agent.\n"
        "Your goal is to manage remote path mapping resources.\n"
        "You have access to tools specifically tagged with 'RemotePathMapping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RENAMEEPISODE_AGENT_PROMPT = os.environ.get(
    "RENAMEEPISODE_AGENT_PROMPT",
    default=(
        "You are the Sonarr RenameEpisode Agent.\n"
        "Your goal is to manage rename episode resources.\n"
        "You have access to tools specifically tagged with 'RenameEpisode'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

ROOTFOLDER_AGENT_PROMPT = os.environ.get(
    "ROOTFOLDER_AGENT_PROMPT",
    default=(
        "You are the Sonarr RootFolder Agent.\n"
        "Your goal is to manage root folder resources.\n"
        "You have access to tools specifically tagged with 'RootFolder'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SEASONPASS_AGENT_PROMPT = os.environ.get(
    "SEASONPASS_AGENT_PROMPT",
    default=(
        "You are the Sonarr SeasonPass Agent.\n"
        "Your goal is to manage season pass resources.\n"
        "You have access to tools specifically tagged with 'SeasonPass'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIES_AGENT_PROMPT = os.environ.get(
    "SERIES_AGENT_PROMPT",
    default=(
        "You are the Sonarr Series Agent.\n"
        "Your goal is to manage series resources.\n"
        "You have access to tools specifically tagged with 'Series'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIESEDITOR_AGENT_PROMPT = os.environ.get(
    "SERIESEDITOR_AGENT_PROMPT",
    default=(
        "You are the Sonarr SeriesEditor Agent.\n"
        "Your goal is to manage series editor resources.\n"
        "You have access to tools specifically tagged with 'SeriesEditor'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIESFOLDER_AGENT_PROMPT = os.environ.get(
    "SERIESFOLDER_AGENT_PROMPT",
    default=(
        "You are the Sonarr SeriesFolder Agent.\n"
        "Your goal is to manage series folder resources.\n"
        "You have access to tools specifically tagged with 'SeriesFolder'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIESIMPORT_AGENT_PROMPT = os.environ.get(
    "SERIESIMPORT_AGENT_PROMPT",
    default=(
        "You are the Sonarr SeriesImport Agent.\n"
        "Your goal is to manage series import resources.\n"
        "You have access to tools specifically tagged with 'SeriesImport'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIESLOOKUP_AGENT_PROMPT = os.environ.get(
    "SERIESLOOKUP_AGENT_PROMPT",
    default=(
        "You are the Sonarr SeriesLookup Agent.\n"
        "Your goal is to manage series lookup resources.\n"
        "You have access to tools specifically tagged with 'SeriesLookup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

STATICRESOURCE_AGENT_PROMPT = os.environ.get(
    "STATICRESOURCE_AGENT_PROMPT",
    default=(
        "You are the Sonarr StaticResource Agent.\n"
        "Your goal is to manage static resource resources.\n"
        "You have access to tools specifically tagged with 'StaticResource'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SYSTEM_AGENT_PROMPT = os.environ.get(
    "SYSTEM_AGENT_PROMPT",
    default=(
        "You are the Sonarr System Agent.\n"
        "Your goal is to manage system resources.\n"
        "You have access to tools specifically tagged with 'System'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAG_AGENT_PROMPT = os.environ.get(
    "TAG_AGENT_PROMPT",
    default=(
        "You are the Sonarr Tag Agent.\n"
        "Your goal is to manage tag resources.\n"
        "You have access to tools specifically tagged with 'Tag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAGDETAILS_AGENT_PROMPT = os.environ.get(
    "TAGDETAILS_AGENT_PROMPT",
    default=(
        "You are the Sonarr TagDetails Agent.\n"
        "Your goal is to manage tag details resources.\n"
        "You have access to tools specifically tagged with 'TagDetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TASK_AGENT_PROMPT = os.environ.get(
    "TASK_AGENT_PROMPT",
    default=(
        "You are the Sonarr Task Agent.\n"
        "Your goal is to manage task resources.\n"
        "You have access to tools specifically tagged with 'Task'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UICONFIG_AGENT_PROMPT = os.environ.get(
    "UICONFIG_AGENT_PROMPT",
    default=(
        "You are the Sonarr UiConfig Agent.\n"
        "Your goal is to manage ui config resources.\n"
        "You have access to tools specifically tagged with 'UiConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATE_AGENT_PROMPT = os.environ.get(
    "UPDATE_AGENT_PROMPT",
    default=(
        "You are the Sonarr Update Agent.\n"
        "Your goal is to manage update resources.\n"
        "You have access to tools specifically tagged with 'Update'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATELOGFILE_AGENT_PROMPT = os.environ.get(
    "UPDATELOGFILE_AGENT_PROMPT",
    default=(
        "You are the Sonarr UpdateLogFile Agent.\n"
        "Your goal is to manage update log file resources.\n"
        "You have access to tools specifically tagged with 'UpdateLogFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for Sonarr...")

    model = create_model(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        ssl_verify=ssl_verify,
        timeout=DEFAULT_TIMEOUT,
    )
    settings = ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        top_p=DEFAULT_TOP_P,
        timeout=DEFAULT_TIMEOUT,
        parallel_tool_calls=DEFAULT_PARALLEL_TOOL_CALLS,
        seed=DEFAULT_SEED,
        presence_penalty=DEFAULT_PRESENCE_PENALTY,
        frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
        logit_bias=DEFAULT_LOGIT_BIAS,
        stop_sequences=DEFAULT_STOP_SEQUENCES,
        extra_headers=DEFAULT_EXTRA_HEADERS,
        extra_body=DEFAULT_EXTRA_BODY,
    )

    agent_toolsets = []
    if mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        else:
            server = MCPServerStreamableHTTP(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        agent_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")
    elif mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        for server in mcp_toolset:
            if hasattr(server, "http_client"):
                server.http_client = httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                )
        agent_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")

    if skills_directory and os.path.exists(skills_directory):
        agent_toolsets.append(SkillsToolset(directories=[str(skills_directory)]))

    agent_defs = {
        "ApiInfo": (APIINFO_AGENT_PROMPT, "Sonarr_ApiInfo_Agent"),
        "Authentication": (AUTHENTICATION_AGENT_PROMPT, "Sonarr_Authentication_Agent"),
        "AutoTagging": (AUTOTAGGING_AGENT_PROMPT, "Sonarr_AutoTagging_Agent"),
        "Backup": (BACKUP_AGENT_PROMPT, "Sonarr_Backup_Agent"),
        "Blocklist": (BLOCKLIST_AGENT_PROMPT, "Sonarr_Blocklist_Agent"),
        "Calendar": (CALENDAR_AGENT_PROMPT, "Sonarr_Calendar_Agent"),
        "CalendarFeed": (CALENDARFEED_AGENT_PROMPT, "Sonarr_CalendarFeed_Agent"),
        "Command": (COMMAND_AGENT_PROMPT, "Sonarr_Command_Agent"),
        "CustomFilter": (CUSTOMFILTER_AGENT_PROMPT, "Sonarr_CustomFilter_Agent"),
        "CustomFormat": (CUSTOMFORMAT_AGENT_PROMPT, "Sonarr_CustomFormat_Agent"),
        "Cutoff": (CUTOFF_AGENT_PROMPT, "Sonarr_Cutoff_Agent"),
        "DelayProfile": (DELAYPROFILE_AGENT_PROMPT, "Sonarr_DelayProfile_Agent"),
        "DiskSpace": (DISKSPACE_AGENT_PROMPT, "Sonarr_DiskSpace_Agent"),
        "DownloadClient": (DOWNLOADCLIENT_AGENT_PROMPT, "Sonarr_DownloadClient_Agent"),
        "DownloadClientConfig": (
            DOWNLOADCLIENTCONFIG_AGENT_PROMPT,
            "Sonarr_DownloadClientConfig_Agent",
        ),
        "Episode": (EPISODE_AGENT_PROMPT, "Sonarr_Episode_Agent"),
        "EpisodeFile": (EPISODEFILE_AGENT_PROMPT, "Sonarr_EpisodeFile_Agent"),
        "FileSystem": (FILESYSTEM_AGENT_PROMPT, "Sonarr_FileSystem_Agent"),
        "Health": (HEALTH_AGENT_PROMPT, "Sonarr_Health_Agent"),
        "History": (HISTORY_AGENT_PROMPT, "Sonarr_History_Agent"),
        "HostConfig": (HOSTCONFIG_AGENT_PROMPT, "Sonarr_HostConfig_Agent"),
        "ImportList": (IMPORTLIST_AGENT_PROMPT, "Sonarr_ImportList_Agent"),
        "ImportListConfig": (
            IMPORTLISTCONFIG_AGENT_PROMPT,
            "Sonarr_ImportListConfig_Agent",
        ),
        "ImportListExclusion": (
            IMPORTLISTEXCLUSION_AGENT_PROMPT,
            "Sonarr_ImportListExclusion_Agent",
        ),
        "Indexer": (INDEXER_AGENT_PROMPT, "Sonarr_Indexer_Agent"),
        "IndexerConfig": (INDEXERCONFIG_AGENT_PROMPT, "Sonarr_IndexerConfig_Agent"),
        "IndexerFlag": (INDEXERFLAG_AGENT_PROMPT, "Sonarr_IndexerFlag_Agent"),
        "Language": (LANGUAGE_AGENT_PROMPT, "Sonarr_Language_Agent"),
        "LanguageProfile": (
            LANGUAGEPROFILE_AGENT_PROMPT,
            "Sonarr_LanguageProfile_Agent",
        ),
        "LanguageProfileSchema": (
            LANGUAGEPROFILESCHEMA_AGENT_PROMPT,
            "Sonarr_LanguageProfileSchema_Agent",
        ),
        "Localization": (LOCALIZATION_AGENT_PROMPT, "Sonarr_Localization_Agent"),
        "Log": (LOG_AGENT_PROMPT, "Sonarr_Log_Agent"),
        "LogFile": (LOGFILE_AGENT_PROMPT, "Sonarr_LogFile_Agent"),
        "ManualImport": (MANUALIMPORT_AGENT_PROMPT, "Sonarr_ManualImport_Agent"),
        "MediaCover": (MEDIACOVER_AGENT_PROMPT, "Sonarr_MediaCover_Agent"),
        "MediaManagementConfig": (
            MEDIAMANAGEMENTCONFIG_AGENT_PROMPT,
            "Sonarr_MediaManagementConfig_Agent",
        ),
        "Metadata": (METADATA_AGENT_PROMPT, "Sonarr_Metadata_Agent"),
        "Missing": (MISSING_AGENT_PROMPT, "Sonarr_Missing_Agent"),
        "NamingConfig": (NAMINGCONFIG_AGENT_PROMPT, "Sonarr_NamingConfig_Agent"),
        "Notification": (NOTIFICATION_AGENT_PROMPT, "Sonarr_Notification_Agent"),
        "Parse": (PARSE_AGENT_PROMPT, "Sonarr_Parse_Agent"),
        "Ping": (PING_AGENT_PROMPT, "Sonarr_Ping_Agent"),
        "QualityDefinition": (
            QUALITYDEFINITION_AGENT_PROMPT,
            "Sonarr_QualityDefinition_Agent",
        ),
        "QualityProfile": (QUALITYPROFILE_AGENT_PROMPT, "Sonarr_QualityProfile_Agent"),
        "QualityProfileSchema": (
            QUALITYPROFILESCHEMA_AGENT_PROMPT,
            "Sonarr_QualityProfileSchema_Agent",
        ),
        "Queue": (QUEUE_AGENT_PROMPT, "Sonarr_Queue_Agent"),
        "QueueAction": (QUEUEACTION_AGENT_PROMPT, "Sonarr_QueueAction_Agent"),
        "QueueDetails": (QUEUEDETAILS_AGENT_PROMPT, "Sonarr_QueueDetails_Agent"),
        "QueueStatus": (QUEUESTATUS_AGENT_PROMPT, "Sonarr_QueueStatus_Agent"),
        "Release": (RELEASE_AGENT_PROMPT, "Sonarr_Release_Agent"),
        "ReleaseProfile": (RELEASEPROFILE_AGENT_PROMPT, "Sonarr_ReleaseProfile_Agent"),
        "ReleasePush": (RELEASEPUSH_AGENT_PROMPT, "Sonarr_ReleasePush_Agent"),
        "RemotePathMapping": (
            REMOTEPATHMAPPING_AGENT_PROMPT,
            "Sonarr_RemotePathMapping_Agent",
        ),
        "RenameEpisode": (RENAMEEPISODE_AGENT_PROMPT, "Sonarr_RenameEpisode_Agent"),
        "RootFolder": (ROOTFOLDER_AGENT_PROMPT, "Sonarr_RootFolder_Agent"),
        "SeasonPass": (SEASONPASS_AGENT_PROMPT, "Sonarr_SeasonPass_Agent"),
        "Series": (SERIES_AGENT_PROMPT, "Sonarr_Series_Agent"),
        "SeriesEditor": (SERIESEDITOR_AGENT_PROMPT, "Sonarr_SeriesEditor_Agent"),
        "SeriesFolder": (SERIESFOLDER_AGENT_PROMPT, "Sonarr_SeriesFolder_Agent"),
        "SeriesImport": (SERIESIMPORT_AGENT_PROMPT, "Sonarr_SeriesImport_Agent"),
        "SeriesLookup": (SERIESLOOKUP_AGENT_PROMPT, "Sonarr_SeriesLookup_Agent"),
        "StaticResource": (STATICRESOURCE_AGENT_PROMPT, "Sonarr_StaticResource_Agent"),
        "System": (SYSTEM_AGENT_PROMPT, "Sonarr_System_Agent"),
        "Tag": (TAG_AGENT_PROMPT, "Sonarr_Tag_Agent"),
        "TagDetails": (TAGDETAILS_AGENT_PROMPT, "Sonarr_TagDetails_Agent"),
        "Task": (TASK_AGENT_PROMPT, "Sonarr_Task_Agent"),
        "UiConfig": (UICONFIG_AGENT_PROMPT, "Sonarr_UiConfig_Agent"),
        "Update": (UPDATE_AGENT_PROMPT, "Sonarr_Update_Agent"),
        "UpdateLogFile": (UPDATELOGFILE_AGENT_PROMPT, "Sonarr_UpdateLogFile_Agent"),
    }

    child_agents = {}

    for tag, (system_prompt, agent_name) in agent_defs.items():
        tag_toolsets = []
        for ts in agent_toolsets:

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)
            else:
                pass

        agent = Agent(
            name=agent_name,
            system_prompt=system_prompt,
            model=model,
            model_settings=settings,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
        )
        child_agents[tag] = agent

    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        deps_type=Any,
    )

    @supervisor.tool
    async def assign_task_to_apiinfo_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ApiInfo to the ApiInfo Agent."""
        return (
            await child_agents["ApiInfo"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_authentication_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to Authentication to the Authentication Agent."""
        return (
            await child_agents["Authentication"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_autotagging_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to AutoTagging to the AutoTagging Agent."""
        return (
            await child_agents["AutoTagging"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_backup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Backup to the Backup Agent."""
        return (
            await child_agents["Backup"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_blocklist_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Blocklist to the Blocklist Agent."""
        return (
            await child_agents["Blocklist"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_calendar_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Calendar to the Calendar Agent."""
        return (
            await child_agents["Calendar"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_calendarfeed_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to CalendarFeed to the CalendarFeed Agent."""
        return (
            await child_agents["CalendarFeed"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_command_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Command to the Command Agent."""
        return (
            await child_agents["Command"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_customfilter_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to CustomFilter to the CustomFilter Agent."""
        return (
            await child_agents["CustomFilter"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_customformat_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to CustomFormat to the CustomFormat Agent."""
        return (
            await child_agents["CustomFormat"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_cutoff_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Cutoff to the Cutoff Agent."""
        return (
            await child_agents["Cutoff"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_delayprofile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to DelayProfile to the DelayProfile Agent."""
        return (
            await child_agents["DelayProfile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_diskspace_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to DiskSpace to the DiskSpace Agent."""
        return (
            await child_agents["DiskSpace"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_downloadclient_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to DownloadClient to the DownloadClient Agent."""
        return (
            await child_agents["DownloadClient"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_downloadclientconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to DownloadClientConfig to the DownloadClientConfig Agent."""
        return (
            await child_agents["DownloadClientConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_episode_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Episode to the Episode Agent."""
        return (
            await child_agents["Episode"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_episodefile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to EpisodeFile to the EpisodeFile Agent."""
        return (
            await child_agents["EpisodeFile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_filesystem_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to FileSystem to the FileSystem Agent."""
        return (
            await child_agents["FileSystem"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_health_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Health to the Health Agent."""
        return (
            await child_agents["Health"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_history_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to History to the History Agent."""
        return (
            await child_agents["History"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_hostconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to HostConfig to the HostConfig Agent."""
        return (
            await child_agents["HostConfig"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_importlist_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ImportList to the ImportList Agent."""
        return (
            await child_agents["ImportList"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_importlistconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to ImportListConfig to the ImportListConfig Agent."""
        return (
            await child_agents["ImportListConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_importlistexclusion_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to ImportListExclusion to the ImportListExclusion Agent."""
        return (
            await child_agents["ImportListExclusion"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_indexer_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Indexer to the Indexer Agent."""
        return (
            await child_agents["Indexer"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_indexerconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to IndexerConfig to the IndexerConfig Agent."""
        return (
            await child_agents["IndexerConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_indexerflag_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to IndexerFlag to the IndexerFlag Agent."""
        return (
            await child_agents["IndexerFlag"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_language_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Language to the Language Agent."""
        return (
            await child_agents["Language"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_languageprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to LanguageProfile to the LanguageProfile Agent."""
        return (
            await child_agents["LanguageProfile"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_languageprofileschema_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to LanguageProfileSchema to the LanguageProfileSchema Agent."""
        return (
            await child_agents["LanguageProfileSchema"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_localization_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Localization to the Localization Agent."""
        return (
            await child_agents["Localization"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_log_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Log to the Log Agent."""
        return (
            await child_agents["Log"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_logfile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to LogFile to the LogFile Agent."""
        return (
            await child_agents["LogFile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_manualimport_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ManualImport to the ManualImport Agent."""
        return (
            await child_agents["ManualImport"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_mediacover_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to MediaCover to the MediaCover Agent."""
        return (
            await child_agents["MediaCover"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_mediamanagementconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to MediaManagementConfig to the MediaManagementConfig Agent."""
        return (
            await child_agents["MediaManagementConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_metadata_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Metadata to the Metadata Agent."""
        return (
            await child_agents["Metadata"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_missing_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Missing to the Missing Agent."""
        return (
            await child_agents["Missing"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_namingconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to NamingConfig to the NamingConfig Agent."""
        return (
            await child_agents["NamingConfig"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_notification_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Notification to the Notification Agent."""
        return (
            await child_agents["Notification"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_parse_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Parse to the Parse Agent."""
        return (
            await child_agents["Parse"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_ping_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Ping to the Ping Agent."""
        return (
            await child_agents["Ping"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_qualitydefinition_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to QualityDefinition to the QualityDefinition Agent."""
        return (
            await child_agents["QualityDefinition"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_qualityprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to QualityProfile to the QualityProfile Agent."""
        return (
            await child_agents["QualityProfile"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_qualityprofileschema_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to QualityProfileSchema to the QualityProfileSchema Agent."""
        return (
            await child_agents["QualityProfileSchema"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_queue_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Queue to the Queue Agent."""
        return (
            await child_agents["Queue"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_queueaction_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to QueueAction to the QueueAction Agent."""
        return (
            await child_agents["QueueAction"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_queuedetails_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to QueueDetails to the QueueDetails Agent."""
        return (
            await child_agents["QueueDetails"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_queuestatus_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to QueueStatus to the QueueStatus Agent."""
        return (
            await child_agents["QueueStatus"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_release_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Release to the Release Agent."""
        return (
            await child_agents["Release"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_releaseprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to ReleaseProfile to the ReleaseProfile Agent."""
        return (
            await child_agents["ReleaseProfile"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_releasepush_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ReleasePush to the ReleasePush Agent."""
        return (
            await child_agents["ReleasePush"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_remotepathmapping_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to RemotePathMapping to the RemotePathMapping Agent."""
        return (
            await child_agents["RemotePathMapping"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_renameepisode_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to RenameEpisode to the RenameEpisode Agent."""
        return (
            await child_agents["RenameEpisode"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_rootfolder_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to RootFolder to the RootFolder Agent."""
        return (
            await child_agents["RootFolder"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_seasonpass_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to SeasonPass to the SeasonPass Agent."""
        return (
            await child_agents["SeasonPass"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_series_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Series to the Series Agent."""
        return (
            await child_agents["Series"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_serieseditor_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to SeriesEditor to the SeriesEditor Agent."""
        return (
            await child_agents["SeriesEditor"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_seriesfolder_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to SeriesFolder to the SeriesFolder Agent."""
        return (
            await child_agents["SeriesFolder"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_seriesimport_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to SeriesImport to the SeriesImport Agent."""
        return (
            await child_agents["SeriesImport"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_serieslookup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to SeriesLookup to the SeriesLookup Agent."""
        return (
            await child_agents["SeriesLookup"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_staticresource_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to StaticResource to the StaticResource Agent."""
        return (
            await child_agents["StaticResource"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_system_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to System to the System Agent."""
        return (
            await child_agents["System"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_tag_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Tag to the Tag Agent."""
        return (
            await child_agents["Tag"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_tagdetails_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to TagDetails to the TagDetails Agent."""
        return (
            await child_agents["TagDetails"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_task_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Task to the Task Agent."""
        return (
            await child_agents["Task"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_uiconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to UiConfig to the UiConfig Agent."""
        return (
            await child_agents["UiConfig"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_update_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Update to the Update Agent."""
        return (
            await child_agents["Update"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_updatelogfile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to UpdateLogFile to the UpdateLogFile Agent."""
        return (
            await child_agents["UpdateLogFile"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    return supervisor


async def chat(agent: Agent, prompt: str):
    result = await agent.run(prompt)
    print(f"Response:\n\n{result.output}")


async def node_chat(agent: Agent, prompt: str) -> List:
    nodes = []
    async with agent.iter(prompt) as agent_run:
        async for node in agent_run:
            nodes.append(node)
            print(node)
    return nodes


async def stream_chat(agent: Agent, prompt: str) -> None:
    async with agent.run_stream(prompt) as result:
        async for text_chunk in result.stream_text(delta=True):
            print(text_chunk, end="", flush=True)
        print("\nDone!")


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
):
    print(
        f"Starting {AGENT_NAME}:"
        f"\tprovider={provider}"
        f"\tmodel={model_id}"
        f"\tbase_url={base_url}"
        f"\tmcp={mcp_url} | {mcp_config}"
        f"\tssl_verify={ssl_verify}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        skills_directory=skills_directory,
        ssl_verify=ssl_verify,
        timeout=DEFAULT_TIMEOUT,
    )

    if skills_directory and os.path.exists(skills_directory):
        skills = load_skills_from_directory(skills_directory)
        logger.info(f"Loaded {len(skills)} skills from {skills_directory}")
    else:
        skills = [
            Skill(
                id="sonarr_agent",
                name="Sonarr Agent",
                description="General access to Sonarr tools",
                tags=["sonarr"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router") and hasattr(a2a_app.router, "lifespan_context"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} - A2A + AG-UI Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "OK"}

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=json.dumps(e.json()),
                media_type="application/json",
                status_code=422,
            )

        if hasattr(run_input, "messages"):
            run_input.messages = prune_large_messages(run_input.messages)

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        sse_stream = adapter.encode_stream(event_stream)

        return StreamingResponse(
            sse_stream,
            media_type=accept,
        )

    if enable_web_ui:
        web_ui = agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT)
        app.mount("/", web_ui)
        logger.info(
            "Starting server on %s:%s (A2A at /a2a, AG-UI at /ag-ui, Web UI: %s)",
            host,
            port,
            "Enabled at /" if enable_web_ui else "Disabled",
        )

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_keep_alive=1800,
        timeout_graceful_shutdown=60,
        log_level="debug" if debug else "info",
    )


def agent_server():
    print(f"sonarr_agent v{__version__}")
    parser = argparse.ArgumentParser(
        add_help=False, description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument("--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["openai", "anthropic", "google", "huggingface"],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_LLM_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_LLM_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--skills-directory",
        default=DEFAULT_SKILLS_DIRECTORY,
        help="Directory containing agent skills",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification for LLM requests (Use with caution)",
    )
    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        usage()

        sys.exit(0)

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        skills_directory=args.skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
        ssl_verify=not args.insecure,
    )


def usage():
    print(
        f"Arr Mcp ({__version__}): Sonarr Agent\n\n"
        "Usage:\n"
        "--host                [ Host to bind the server to ]\n"
        "--port                [ Port to bind the server to ]\n"
        "--debug               [ Debug mode ]\n"
        "--reload              [ Enable auto-reload ]\n"
        "--provider            [ LLM Provider ]\n"
        "--model-id            [ LLM Model ID ]\n"
        "--base-url            [ LLM Base URL (for OpenAI compatible providers) ]\n"
        "--api-key             [ LLM API Key ]\n"
        "--mcp-url             [ MCP Server URL ]\n"
        "--mcp-config          [ MCP Server Config ]\n"
        "--skills-directory    [ Directory containing agent skills ]\n"
        "--web                 [ Enable Pydantic AI Web UI ]\n"
        "\n"
        "Examples:\n"
        "  [Simple]  sonarr-agent \n"
        '  [Complex] sonarr-agent --host "value" --port "value" --debug "value" --reload --provider "value" --model-id "value" --base-url "value" --api-key "value" --mcp-url "value" --mcp-config "value" --skills-directory "value" --web\n'
    )


if __name__ == "__main__":
    agent_server()
