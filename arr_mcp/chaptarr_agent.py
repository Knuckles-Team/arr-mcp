#!/usr/bin/python
import sys

# coding: utf-8
import json
import os
import argparse
import logging
import uvicorn
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

__version__ = "0.2.2"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output to console
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

# Model Settings
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

AGENT_NAME = "ChaptarrAgent"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing Chaptarr resources via delegated specialists."
)

# -------------------------------------------------------------------------
# 1. System Prompts
# -------------------------------------------------------------------------

SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the Chaptarr Supervisor Agent.\n"
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

AUTHORLOOKUP_AGENT_PROMPT = os.environ.get(
    "AUTHORLOOKUP_AGENT_PROMPT",
    default=(
        "You are the Chaptarr AuthorLookup Agent.\n"
        "Your goal is to manage author lookup resources.\n"
        "You have access to tools specifically tagged with 'AuthorLookup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BACKUP_AGENT_PROMPT = os.environ.get(
    "BACKUP_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Backup Agent.\n"
        "Your goal is to manage backup resources.\n"
        "You have access to tools specifically tagged with 'Backup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BLOCKLIST_AGENT_PROMPT = os.environ.get(
    "BLOCKLIST_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Blocklist Agent.\n"
        "Your goal is to manage blocklist resources.\n"
        "You have access to tools specifically tagged with 'Blocklist'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOK_AGENT_PROMPT = os.environ.get(
    "BOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Book Agent.\n"
        "Your goal is to manage book resources.\n"
        "You have access to tools specifically tagged with 'Book'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKEDITOR_AGENT_PROMPT = os.environ.get(
    "BOOKEDITOR_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookEditor Agent.\n"
        "Your goal is to manage book editor resources.\n"
        "You have access to tools specifically tagged with 'BookEditor'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKFILE_AGENT_PROMPT = os.environ.get(
    "BOOKFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookFile Agent.\n"
        "Your goal is to manage book file resources.\n"
        "You have access to tools specifically tagged with 'BookFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKLOOKUP_AGENT_PROMPT = os.environ.get(
    "BOOKLOOKUP_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookLookup Agent.\n"
        "Your goal is to manage book lookup resources.\n"
        "You have access to tools specifically tagged with 'BookLookup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKSHELF_AGENT_PROMPT = os.environ.get(
    "BOOKSHELF_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Bookshelf Agent.\n"
        "Your goal is to manage bookshelf resources.\n"
        "You have access to tools specifically tagged with 'Bookshelf'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDAR_AGENT_PROMPT = os.environ.get(
    "CALENDAR_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Calendar Agent.\n"
        "Your goal is to manage calendar resources.\n"
        "You have access to tools specifically tagged with 'Calendar'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDARFEED_AGENT_PROMPT = os.environ.get(
    "CALENDARFEED_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CalendarFeed Agent.\n"
        "Your goal is to manage calendar feed resources.\n"
        "You have access to tools specifically tagged with 'CalendarFeed'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

COMMAND_AGENT_PROMPT = os.environ.get(
    "COMMAND_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Command Agent.\n"
        "Your goal is to manage command resources.\n"
        "You have access to tools specifically tagged with 'Command'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFILTER_AGENT_PROMPT = os.environ.get(
    "CUSTOMFILTER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CustomFilter Agent.\n"
        "Your goal is to manage custom filter resources.\n"
        "You have access to tools specifically tagged with 'CustomFilter'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFORMAT_AGENT_PROMPT = os.environ.get(
    "CUSTOMFORMAT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CustomFormat Agent.\n"
        "Your goal is to manage custom format resources.\n"
        "You have access to tools specifically tagged with 'CustomFormat'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUTOFF_AGENT_PROMPT = os.environ.get(
    "CUTOFF_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Cutoff Agent.\n"
        "Your goal is to manage cutoff resources.\n"
        "You have access to tools specifically tagged with 'Cutoff'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DELAYPROFILE_AGENT_PROMPT = os.environ.get(
    "DELAYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DelayProfile Agent.\n"
        "Your goal is to manage delay profile resources.\n"
        "You have access to tools specifically tagged with 'DelayProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DEVELOPMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DEVELOPMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DevelopmentConfig Agent.\n"
        "Your goal is to manage development config resources.\n"
        "You have access to tools specifically tagged with 'DevelopmentConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DISKSPACE_AGENT_PROMPT = os.environ.get(
    "DISKSPACE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DiskSpace Agent.\n"
        "Your goal is to manage disk space resources.\n"
        "You have access to tools specifically tagged with 'DiskSpace'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENT_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DownloadClient Agent.\n"
        "Your goal is to manage download client resources.\n"
        "You have access to tools specifically tagged with 'DownloadClient'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DownloadClientConfig Agent.\n"
        "Your goal is to manage download client config resources.\n"
        "You have access to tools specifically tagged with 'DownloadClientConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

EDITION_AGENT_PROMPT = os.environ.get(
    "EDITION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Edition Agent.\n"
        "Your goal is to manage edition resources.\n"
        "You have access to tools specifically tagged with 'Edition'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

FILESYSTEM_AGENT_PROMPT = os.environ.get(
    "FILESYSTEM_AGENT_PROMPT",
    default=(
        "You are the Chaptarr FileSystem Agent.\n"
        "Your goal is to manage file system resources.\n"
        "You have access to tools specifically tagged with 'FileSystem'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HEALTH_AGENT_PROMPT = os.environ.get(
    "HEALTH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Health Agent.\n"
        "Your goal is to manage health resources.\n"
        "You have access to tools specifically tagged with 'Health'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HISTORY_AGENT_PROMPT = os.environ.get(
    "HISTORY_AGENT_PROMPT",
    default=(
        "You are the Chaptarr History Agent.\n"
        "Your goal is to manage history resources.\n"
        "You have access to tools specifically tagged with 'History'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HOSTCONFIG_AGENT_PROMPT = os.environ.get(
    "HOSTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr HostConfig Agent.\n"
        "Your goal is to manage host config resources.\n"
        "You have access to tools specifically tagged with 'HostConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLIST_AGENT_PROMPT = os.environ.get(
    "IMPORTLIST_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ImportList Agent.\n"
        "Your goal is to manage import list resources.\n"
        "You have access to tools specifically tagged with 'ImportList'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLISTEXCLUSION_AGENT_PROMPT = os.environ.get(
    "IMPORTLISTEXCLUSION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ImportListExclusion Agent.\n"
        "Your goal is to manage import list exclusion resources.\n"
        "You have access to tools specifically tagged with 'ImportListExclusion'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXER_AGENT_PROMPT = os.environ.get(
    "INDEXER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Indexer Agent.\n"
        "Your goal is to manage indexer resources.\n"
        "You have access to tools specifically tagged with 'Indexer'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERCONFIG_AGENT_PROMPT = os.environ.get(
    "INDEXERCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr IndexerConfig Agent.\n"
        "Your goal is to manage indexer config resources.\n"
        "You have access to tools specifically tagged with 'IndexerConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERFLAG_AGENT_PROMPT = os.environ.get(
    "INDEXERFLAG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr IndexerFlag Agent.\n"
        "Your goal is to manage indexer flag resources.\n"
        "You have access to tools specifically tagged with 'IndexerFlag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LANGUAGE_AGENT_PROMPT = os.environ.get(
    "LANGUAGE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Language Agent.\n"
        "Your goal is to manage language resources.\n"
        "You have access to tools specifically tagged with 'Language'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOCALIZATION_AGENT_PROMPT = os.environ.get(
    "LOCALIZATION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Localization Agent.\n"
        "Your goal is to manage localization resources.\n"
        "You have access to tools specifically tagged with 'Localization'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOG_AGENT_PROMPT = os.environ.get(
    "LOG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Log Agent.\n"
        "Your goal is to manage log resources.\n"
        "You have access to tools specifically tagged with 'Log'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOGFILE_AGENT_PROMPT = os.environ.get(
    "LOGFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr LogFile Agent.\n"
        "Your goal is to manage log file resources.\n"
        "You have access to tools specifically tagged with 'LogFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MANUALIMPORT_AGENT_PROMPT = os.environ.get(
    "MANUALIMPORT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ManualImport Agent.\n"
        "Your goal is to manage manual import resources.\n"
        "You have access to tools specifically tagged with 'ManualImport'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIACOVER_AGENT_PROMPT = os.environ.get(
    "MEDIACOVER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MediaCover Agent.\n"
        "Your goal is to manage media cover resources.\n"
        "You have access to tools specifically tagged with 'MediaCover'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIAMANAGEMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "MEDIAMANAGEMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MediaManagementConfig Agent.\n"
        "Your goal is to manage media management config resources.\n"
        "You have access to tools specifically tagged with 'MediaManagementConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATA_AGENT_PROMPT = os.environ.get(
    "METADATA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Metadata Agent.\n"
        "Your goal is to manage metadata resources.\n"
        "You have access to tools specifically tagged with 'Metadata'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROFILE_AGENT_PROMPT = os.environ.get(
    "METADATAPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProfile Agent.\n"
        "Your goal is to manage metadata profile resources.\n"
        "You have access to tools specifically tagged with 'MetadataProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "METADATAPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProfileSchema Agent.\n"
        "Your goal is to manage metadata profile schema resources.\n"
        "You have access to tools specifically tagged with 'MetadataProfileSchema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROVIDERCONFIG_AGENT_PROMPT = os.environ.get(
    "METADATAPROVIDERCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProviderConfig Agent.\n"
        "Your goal is to manage metadata provider config resources.\n"
        "You have access to tools specifically tagged with 'MetadataProviderConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MISSING_AGENT_PROMPT = os.environ.get(
    "MISSING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Missing Agent.\n"
        "Your goal is to manage missing resources.\n"
        "You have access to tools specifically tagged with 'Missing'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NAMINGCONFIG_AGENT_PROMPT = os.environ.get(
    "NAMINGCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr NamingConfig Agent.\n"
        "Your goal is to manage naming config resources.\n"
        "You have access to tools specifically tagged with 'NamingConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NOTIFICATION_AGENT_PROMPT = os.environ.get(
    "NOTIFICATION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Notification Agent.\n"
        "Your goal is to manage notification resources.\n"
        "You have access to tools specifically tagged with 'Notification'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PARSE_AGENT_PROMPT = os.environ.get(
    "PARSE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Parse Agent.\n"
        "Your goal is to manage parse resources.\n"
        "You have access to tools specifically tagged with 'Parse'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PING_AGENT_PROMPT = os.environ.get(
    "PING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Ping Agent.\n"
        "Your goal is to manage ping resources.\n"
        "You have access to tools specifically tagged with 'Ping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYDEFINITION_AGENT_PROMPT = os.environ.get(
    "QUALITYDEFINITION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityDefinition Agent.\n"
        "Your goal is to manage quality definition resources.\n"
        "You have access to tools specifically tagged with 'QualityDefinition'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILE_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityProfile Agent.\n"
        "Your goal is to manage quality profile resources.\n"
        "You have access to tools specifically tagged with 'QualityProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityProfileSchema Agent.\n"
        "Your goal is to manage quality profile schema resources.\n"
        "You have access to tools specifically tagged with 'QualityProfileSchema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUE_AGENT_PROMPT = os.environ.get(
    "QUEUE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Queue Agent.\n"
        "Your goal is to manage queue resources.\n"
        "You have access to tools specifically tagged with 'Queue'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEACTION_AGENT_PROMPT = os.environ.get(
    "QUEUEACTION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueAction Agent.\n"
        "Your goal is to manage queue action resources.\n"
        "You have access to tools specifically tagged with 'QueueAction'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEDETAILS_AGENT_PROMPT = os.environ.get(
    "QUEUEDETAILS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueDetails Agent.\n"
        "Your goal is to manage queue details resources.\n"
        "You have access to tools specifically tagged with 'QueueDetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUESTATUS_AGENT_PROMPT = os.environ.get(
    "QUEUESTATUS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueStatus Agent.\n"
        "Your goal is to manage queue status resources.\n"
        "You have access to tools specifically tagged with 'QueueStatus'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASE_AGENT_PROMPT = os.environ.get(
    "RELEASE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Release Agent.\n"
        "Your goal is to manage release resources.\n"
        "You have access to tools specifically tagged with 'Release'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPROFILE_AGENT_PROMPT = os.environ.get(
    "RELEASEPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ReleaseProfile Agent.\n"
        "Your goal is to manage release profile resources.\n"
        "You have access to tools specifically tagged with 'ReleaseProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPUSH_AGENT_PROMPT = os.environ.get(
    "RELEASEPUSH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ReleasePush Agent.\n"
        "Your goal is to manage release push resources.\n"
        "You have access to tools specifically tagged with 'ReleasePush'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

REMOTEPATHMAPPING_AGENT_PROMPT = os.environ.get(
    "REMOTEPATHMAPPING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RemotePathMapping Agent.\n"
        "Your goal is to manage remote path mapping resources.\n"
        "You have access to tools specifically tagged with 'RemotePathMapping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RENAMEBOOK_AGENT_PROMPT = os.environ.get(
    "RENAMEBOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RenameBook Agent.\n"
        "Your goal is to manage rename book resources.\n"
        "You have access to tools specifically tagged with 'RenameBook'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RETAGBOOK_AGENT_PROMPT = os.environ.get(
    "RETAGBOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RetagBook Agent.\n"
        "Your goal is to manage retag book resources.\n"
        "You have access to tools specifically tagged with 'RetagBook'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

ROOTFOLDER_AGENT_PROMPT = os.environ.get(
    "ROOTFOLDER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RootFolder Agent.\n"
        "Your goal is to manage root folder resources.\n"
        "You have access to tools specifically tagged with 'RootFolder'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SEARCH_AGENT_PROMPT = os.environ.get(
    "SEARCH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Search Agent.\n"
        "Your goal is to manage search resources.\n"
        "You have access to tools specifically tagged with 'Search'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIES_AGENT_PROMPT = os.environ.get(
    "SERIES_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Series Agent.\n"
        "Your goal is to manage series resources.\n"
        "You have access to tools specifically tagged with 'Series'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

STATICRESOURCE_AGENT_PROMPT = os.environ.get(
    "STATICRESOURCE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr StaticResource Agent.\n"
        "Your goal is to manage static resource resources.\n"
        "You have access to tools specifically tagged with 'StaticResource'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SYSTEM_AGENT_PROMPT = os.environ.get(
    "SYSTEM_AGENT_PROMPT",
    default=(
        "You are the Chaptarr System Agent.\n"
        "Your goal is to manage system resources.\n"
        "You have access to tools specifically tagged with 'System'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAG_AGENT_PROMPT = os.environ.get(
    "TAG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Tag Agent.\n"
        "Your goal is to manage tag resources.\n"
        "You have access to tools specifically tagged with 'Tag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAGDETAILS_AGENT_PROMPT = os.environ.get(
    "TAGDETAILS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr TagDetails Agent.\n"
        "Your goal is to manage tag details resources.\n"
        "You have access to tools specifically tagged with 'TagDetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TASK_AGENT_PROMPT = os.environ.get(
    "TASK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Task Agent.\n"
        "Your goal is to manage task resources.\n"
        "You have access to tools specifically tagged with 'Task'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UICONFIG_AGENT_PROMPT = os.environ.get(
    "UICONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr UiConfig Agent.\n"
        "Your goal is to manage ui config resources.\n"
        "You have access to tools specifically tagged with 'UiConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATE_AGENT_PROMPT = os.environ.get(
    "UPDATE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Update Agent.\n"
        "Your goal is to manage update resources.\n"
        "You have access to tools specifically tagged with 'Update'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATELOGFILE_AGENT_PROMPT = os.environ.get(
    "UPDATELOGFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr UpdateLogFile Agent.\n"
        "Your goal is to manage update log file resources.\n"
        "You have access to tools specifically tagged with 'UpdateLogFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

# -------------------------------------------------------------------------
# 2. Agent Creation Logic
# -------------------------------------------------------------------------


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for Chaptarr...")

    model = create_model(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        ssl_verify=ssl_verify,
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

    # Load master toolsets
    agent_toolsets = []
    if mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(mcp_url)
        else:
            server = MCPServerStreamableHTTP(mcp_url)
        agent_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")
    elif mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        agent_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")

    if skills_directory and os.path.exists(skills_directory):
        agent_toolsets.append(SkillsToolset(directories=[str(skills_directory)]))

    # Define Tag -> Prompt map
    agent_defs = {
        "AuthorLookup": (AUTHORLOOKUP_AGENT_PROMPT, "Chaptarr_AuthorLookup_Agent"),
        "Backup": (BACKUP_AGENT_PROMPT, "Chaptarr_Backup_Agent"),
        "Blocklist": (BLOCKLIST_AGENT_PROMPT, "Chaptarr_Blocklist_Agent"),
        "Book": (BOOK_AGENT_PROMPT, "Chaptarr_Book_Agent"),
        "BookEditor": (BOOKEDITOR_AGENT_PROMPT, "Chaptarr_BookEditor_Agent"),
        "BookFile": (BOOKFILE_AGENT_PROMPT, "Chaptarr_BookFile_Agent"),
        "BookLookup": (BOOKLOOKUP_AGENT_PROMPT, "Chaptarr_BookLookup_Agent"),
        "Bookshelf": (BOOKSHELF_AGENT_PROMPT, "Chaptarr_Bookshelf_Agent"),
        "Calendar": (CALENDAR_AGENT_PROMPT, "Chaptarr_Calendar_Agent"),
        "CalendarFeed": (CALENDARFEED_AGENT_PROMPT, "Chaptarr_CalendarFeed_Agent"),
        "Command": (COMMAND_AGENT_PROMPT, "Chaptarr_Command_Agent"),
        "CustomFilter": (CUSTOMFILTER_AGENT_PROMPT, "Chaptarr_CustomFilter_Agent"),
        "CustomFormat": (CUSTOMFORMAT_AGENT_PROMPT, "Chaptarr_CustomFormat_Agent"),
        "Cutoff": (CUTOFF_AGENT_PROMPT, "Chaptarr_Cutoff_Agent"),
        "DelayProfile": (DELAYPROFILE_AGENT_PROMPT, "Chaptarr_DelayProfile_Agent"),
        "DevelopmentConfig": (
            DEVELOPMENTCONFIG_AGENT_PROMPT,
            "Chaptarr_DevelopmentConfig_Agent",
        ),
        "DiskSpace": (DISKSPACE_AGENT_PROMPT, "Chaptarr_DiskSpace_Agent"),
        "DownloadClient": (
            DOWNLOADCLIENT_AGENT_PROMPT,
            "Chaptarr_DownloadClient_Agent",
        ),
        "DownloadClientConfig": (
            DOWNLOADCLIENTCONFIG_AGENT_PROMPT,
            "Chaptarr_DownloadClientConfig_Agent",
        ),
        "Edition": (EDITION_AGENT_PROMPT, "Chaptarr_Edition_Agent"),
        "FileSystem": (FILESYSTEM_AGENT_PROMPT, "Chaptarr_FileSystem_Agent"),
        "Health": (HEALTH_AGENT_PROMPT, "Chaptarr_Health_Agent"),
        "History": (HISTORY_AGENT_PROMPT, "Chaptarr_History_Agent"),
        "HostConfig": (HOSTCONFIG_AGENT_PROMPT, "Chaptarr_HostConfig_Agent"),
        "ImportList": (IMPORTLIST_AGENT_PROMPT, "Chaptarr_ImportList_Agent"),
        "ImportListExclusion": (
            IMPORTLISTEXCLUSION_AGENT_PROMPT,
            "Chaptarr_ImportListExclusion_Agent",
        ),
        "Indexer": (INDEXER_AGENT_PROMPT, "Chaptarr_Indexer_Agent"),
        "IndexerConfig": (INDEXERCONFIG_AGENT_PROMPT, "Chaptarr_IndexerConfig_Agent"),
        "IndexerFlag": (INDEXERFLAG_AGENT_PROMPT, "Chaptarr_IndexerFlag_Agent"),
        "Language": (LANGUAGE_AGENT_PROMPT, "Chaptarr_Language_Agent"),
        "Localization": (LOCALIZATION_AGENT_PROMPT, "Chaptarr_Localization_Agent"),
        "Log": (LOG_AGENT_PROMPT, "Chaptarr_Log_Agent"),
        "LogFile": (LOGFILE_AGENT_PROMPT, "Chaptarr_LogFile_Agent"),
        "ManualImport": (MANUALIMPORT_AGENT_PROMPT, "Chaptarr_ManualImport_Agent"),
        "MediaCover": (MEDIACOVER_AGENT_PROMPT, "Chaptarr_MediaCover_Agent"),
        "MediaManagementConfig": (
            MEDIAMANAGEMENTCONFIG_AGENT_PROMPT,
            "Chaptarr_MediaManagementConfig_Agent",
        ),
        "Metadata": (METADATA_AGENT_PROMPT, "Chaptarr_Metadata_Agent"),
        "MetadataProfile": (
            METADATAPROFILE_AGENT_PROMPT,
            "Chaptarr_MetadataProfile_Agent",
        ),
        "MetadataProfileSchema": (
            METADATAPROFILESCHEMA_AGENT_PROMPT,
            "Chaptarr_MetadataProfileSchema_Agent",
        ),
        "MetadataProviderConfig": (
            METADATAPROVIDERCONFIG_AGENT_PROMPT,
            "Chaptarr_MetadataProviderConfig_Agent",
        ),
        "Missing": (MISSING_AGENT_PROMPT, "Chaptarr_Missing_Agent"),
        "NamingConfig": (NAMINGCONFIG_AGENT_PROMPT, "Chaptarr_NamingConfig_Agent"),
        "Notification": (NOTIFICATION_AGENT_PROMPT, "Chaptarr_Notification_Agent"),
        "Parse": (PARSE_AGENT_PROMPT, "Chaptarr_Parse_Agent"),
        "Ping": (PING_AGENT_PROMPT, "Chaptarr_Ping_Agent"),
        "QualityDefinition": (
            QUALITYDEFINITION_AGENT_PROMPT,
            "Chaptarr_QualityDefinition_Agent",
        ),
        "QualityProfile": (
            QUALITYPROFILE_AGENT_PROMPT,
            "Chaptarr_QualityProfile_Agent",
        ),
        "QualityProfileSchema": (
            QUALITYPROFILESCHEMA_AGENT_PROMPT,
            "Chaptarr_QualityProfileSchema_Agent",
        ),
        "Queue": (QUEUE_AGENT_PROMPT, "Chaptarr_Queue_Agent"),
        "QueueAction": (QUEUEACTION_AGENT_PROMPT, "Chaptarr_QueueAction_Agent"),
        "QueueDetails": (QUEUEDETAILS_AGENT_PROMPT, "Chaptarr_QueueDetails_Agent"),
        "QueueStatus": (QUEUESTATUS_AGENT_PROMPT, "Chaptarr_QueueStatus_Agent"),
        "Release": (RELEASE_AGENT_PROMPT, "Chaptarr_Release_Agent"),
        "ReleaseProfile": (
            RELEASEPROFILE_AGENT_PROMPT,
            "Chaptarr_ReleaseProfile_Agent",
        ),
        "ReleasePush": (RELEASEPUSH_AGENT_PROMPT, "Chaptarr_ReleasePush_Agent"),
        "RemotePathMapping": (
            REMOTEPATHMAPPING_AGENT_PROMPT,
            "Chaptarr_RemotePathMapping_Agent",
        ),
        "RenameBook": (RENAMEBOOK_AGENT_PROMPT, "Chaptarr_RenameBook_Agent"),
        "RetagBook": (RETAGBOOK_AGENT_PROMPT, "Chaptarr_RetagBook_Agent"),
        "RootFolder": (ROOTFOLDER_AGENT_PROMPT, "Chaptarr_RootFolder_Agent"),
        "Search": (SEARCH_AGENT_PROMPT, "Chaptarr_Search_Agent"),
        "Series": (SERIES_AGENT_PROMPT, "Chaptarr_Series_Agent"),
        "StaticResource": (
            STATICRESOURCE_AGENT_PROMPT,
            "Chaptarr_StaticResource_Agent",
        ),
        "System": (SYSTEM_AGENT_PROMPT, "Chaptarr_System_Agent"),
        "Tag": (TAG_AGENT_PROMPT, "Chaptarr_Tag_Agent"),
        "TagDetails": (TAGDETAILS_AGENT_PROMPT, "Chaptarr_TagDetails_Agent"),
        "Task": (TASK_AGENT_PROMPT, "Chaptarr_Task_Agent"),
        "UiConfig": (UICONFIG_AGENT_PROMPT, "Chaptarr_UiConfig_Agent"),
        "Update": (UPDATE_AGENT_PROMPT, "Chaptarr_Update_Agent"),
        "UpdateLogFile": (UPDATELOGFILE_AGENT_PROMPT, "Chaptarr_UpdateLogFile_Agent"),
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

    # Create Supervisor
    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        deps_type=Any,
    )

    # Define delegation tools

    @supervisor.tool
    async def assign_task_to_authorlookup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to AuthorLookup to the AuthorLookup Agent."""
        return (
            await child_agents["AuthorLookup"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    async def assign_task_to_book_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Book to the Book Agent."""
        return (
            await child_agents["Book"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_bookeditor_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to BookEditor to the BookEditor Agent."""
        return (
            await child_agents["BookEditor"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_bookfile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to BookFile to the BookFile Agent."""
        return (
            await child_agents["BookFile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_booklookup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to BookLookup to the BookLookup Agent."""
        return (
            await child_agents["BookLookup"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_bookshelf_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Bookshelf to the Bookshelf Agent."""
        return (
            await child_agents["Bookshelf"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    async def assign_task_to_developmentconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to DevelopmentConfig to the DevelopmentConfig Agent."""
        return (
            await child_agents["DevelopmentConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
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
    async def assign_task_to_edition_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Edition to the Edition Agent."""
        return (
            await child_agents["Edition"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    async def assign_task_to_metadataprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to MetadataProfile to the MetadataProfile Agent."""
        return (
            await child_agents["MetadataProfile"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_metadataprofileschema_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to MetadataProfileSchema to the MetadataProfileSchema Agent."""
        return (
            await child_agents["MetadataProfileSchema"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_metadataproviderconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to MetadataProviderConfig to the MetadataProviderConfig Agent."""
        return (
            await child_agents["MetadataProviderConfig"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
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
    async def assign_task_to_renamebook_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to RenameBook to the RenameBook Agent."""
        return (
            await child_agents["RenameBook"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_retagbook_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to RetagBook to the RetagBook Agent."""
        return (
            await child_agents["RetagBook"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_rootfolder_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to RootFolder to the RootFolder Agent."""
        return (
            await child_agents["RootFolder"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_search_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Search to the Search Agent."""
        return (
            await child_agents["Search"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_series_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Series to the Series Agent."""
        return (
            await child_agents["Series"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
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
        f"Starting {AGENT_NAME} with provider={provider}, model={model_id}, mcp={mcp_url} | {mcp_config}"
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
    )

    if skills_directory and os.path.exists(skills_directory):
        skills = load_skills_from_directory(skills_directory)
        logger.info(f"Loaded {len(skills)} skills from {skills_directory}")
    else:
        skills = [
            Skill(
                id="chaptarr_agent",
                name="Chaptarr Agent",
                description="General access to Chaptarr tools",
                tags=["chaptarr"],
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

        # Prune large messages from history
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
    print(f"chaptarr_agent v{__version__}")
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
        f"Arr Mcp ({__version__}): Chaptarr Agent\n\n"
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
        "  [Simple]  chaptarr-agent \n"
        '  [Complex] chaptarr-agent --host "value" --port "value" --debug "value" --reload --provider "value" --model-id "value" --base-url "value" --api-key "value" --mcp-url "value" --mcp-config "value" --skills-directory "value" --web\n'
    )


if __name__ == "__main__":
    agent_server()
