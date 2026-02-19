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

__version__ = "0.2.14"

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
DEFAULT_CUSTOM_SKILLS_DIRECTORY = os.getenv("CUSTOM_SKILLS_DIRECTORY", None)
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

AGENT_NAME = "ChaptarrAgent"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing Chaptarr resources via delegated specialists."
)


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
        "You have access to tools specifically tagged with 'authorlookup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BACKUP_AGENT_PROMPT = os.environ.get(
    "BACKUP_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Backup Agent.\n"
        "Your goal is to manage backup resources.\n"
        "You have access to tools specifically tagged with 'backup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BLOCKLIST_AGENT_PROMPT = os.environ.get(
    "BLOCKLIST_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Blocklist Agent.\n"
        "Your goal is to manage blocklist resources.\n"
        "You have access to tools specifically tagged with 'blocklist'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOK_AGENT_PROMPT = os.environ.get(
    "BOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Book Agent.\n"
        "Your goal is to manage book resources.\n"
        "You have access to tools specifically tagged with 'book'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKEDITOR_AGENT_PROMPT = os.environ.get(
    "BOOKEDITOR_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookEditor Agent.\n"
        "Your goal is to manage book editor resources.\n"
        "You have access to tools specifically tagged with 'bookeditor'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKFILE_AGENT_PROMPT = os.environ.get(
    "BOOKFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookFile Agent.\n"
        "Your goal is to manage book file resources.\n"
        "You have access to tools specifically tagged with 'bookfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKLOOKUP_AGENT_PROMPT = os.environ.get(
    "BOOKLOOKUP_AGENT_PROMPT",
    default=(
        "You are the Chaptarr BookLookup Agent.\n"
        "Your goal is to manage book lookup resources.\n"
        "You have access to tools specifically tagged with 'booklookup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BOOKSHELF_AGENT_PROMPT = os.environ.get(
    "BOOKSHELF_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Bookshelf Agent.\n"
        "Your goal is to manage bookshelf resources.\n"
        "You have access to tools specifically tagged with 'bookshelf'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDAR_AGENT_PROMPT = os.environ.get(
    "CALENDAR_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Calendar Agent.\n"
        "Your goal is to manage calendar resources.\n"
        "You have access to tools specifically tagged with 'calendar'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CALENDARFEED_AGENT_PROMPT = os.environ.get(
    "CALENDARFEED_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CalendarFeed Agent.\n"
        "Your goal is to manage calendar feed resources.\n"
        "You have access to tools specifically tagged with 'calendarfeed'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

COMMAND_AGENT_PROMPT = os.environ.get(
    "COMMAND_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Command Agent.\n"
        "Your goal is to manage command resources.\n"
        "You have access to tools specifically tagged with 'command'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFILTER_AGENT_PROMPT = os.environ.get(
    "CUSTOMFILTER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CustomFilter Agent.\n"
        "Your goal is to manage custom filter resources.\n"
        "You have access to tools specifically tagged with 'customfilter'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFORMAT_AGENT_PROMPT = os.environ.get(
    "CUSTOMFORMAT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr CustomFormat Agent.\n"
        "Your goal is to manage custom format resources.\n"
        "You have access to tools specifically tagged with 'customformat'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUTOFF_AGENT_PROMPT = os.environ.get(
    "CUTOFF_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Cutoff Agent.\n"
        "Your goal is to manage cutoff resources.\n"
        "You have access to tools specifically tagged with 'cutoff'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DELAYPROFILE_AGENT_PROMPT = os.environ.get(
    "DELAYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DelayProfile Agent.\n"
        "Your goal is to manage delay profile resources.\n"
        "You have access to tools specifically tagged with 'delayprofile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DEVELOPMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DEVELOPMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DevelopmentConfig Agent.\n"
        "Your goal is to manage development config resources.\n"
        "You have access to tools specifically tagged with 'developmentconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DISKSPACE_AGENT_PROMPT = os.environ.get(
    "DISKSPACE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DiskSpace Agent.\n"
        "Your goal is to manage disk space resources.\n"
        "You have access to tools specifically tagged with 'diskspace'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENT_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DownloadClient Agent.\n"
        "Your goal is to manage download client resources.\n"
        "You have access to tools specifically tagged with 'downloadclient'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr DownloadClientConfig Agent.\n"
        "Your goal is to manage download client config resources.\n"
        "You have access to tools specifically tagged with 'downloadclientconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

EDITION_AGENT_PROMPT = os.environ.get(
    "EDITION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Edition Agent.\n"
        "Your goal is to manage edition resources.\n"
        "You have access to tools specifically tagged with 'edition'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

FILESYSTEM_AGENT_PROMPT = os.environ.get(
    "FILESYSTEM_AGENT_PROMPT",
    default=(
        "You are the Chaptarr FileSystem Agent.\n"
        "Your goal is to manage file system resources.\n"
        "You have access to tools specifically tagged with 'filesystem'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HEALTH_AGENT_PROMPT = os.environ.get(
    "HEALTH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Health Agent.\n"
        "Your goal is to manage health resources.\n"
        "You have access to tools specifically tagged with 'health'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HISTORY_AGENT_PROMPT = os.environ.get(
    "HISTORY_AGENT_PROMPT",
    default=(
        "You are the Chaptarr History Agent.\n"
        "Your goal is to manage history resources.\n"
        "You have access to tools specifically tagged with 'history'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HOSTCONFIG_AGENT_PROMPT = os.environ.get(
    "HOSTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr HostConfig Agent.\n"
        "Your goal is to manage host config resources.\n"
        "You have access to tools specifically tagged with 'hostconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLIST_AGENT_PROMPT = os.environ.get(
    "IMPORTLIST_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ImportList Agent.\n"
        "Your goal is to manage import list resources.\n"
        "You have access to tools specifically tagged with 'importlist'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

IMPORTLISTEXCLUSION_AGENT_PROMPT = os.environ.get(
    "IMPORTLISTEXCLUSION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ImportListExclusion Agent.\n"
        "Your goal is to manage import list exclusion resources.\n"
        "You have access to tools specifically tagged with 'importlistexclusion'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXER_AGENT_PROMPT = os.environ.get(
    "INDEXER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Indexer Agent.\n"
        "Your goal is to manage indexer resources.\n"
        "You have access to tools specifically tagged with 'indexer'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERCONFIG_AGENT_PROMPT = os.environ.get(
    "INDEXERCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr IndexerConfig Agent.\n"
        "Your goal is to manage indexer config resources.\n"
        "You have access to tools specifically tagged with 'indexerconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERFLAG_AGENT_PROMPT = os.environ.get(
    "INDEXERFLAG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr IndexerFlag Agent.\n"
        "Your goal is to manage indexer flag resources.\n"
        "You have access to tools specifically tagged with 'indexerflag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LANGUAGE_AGENT_PROMPT = os.environ.get(
    "LANGUAGE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Language Agent.\n"
        "Your goal is to manage language resources.\n"
        "You have access to tools specifically tagged with 'language'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOCALIZATION_AGENT_PROMPT = os.environ.get(
    "LOCALIZATION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Localization Agent.\n"
        "Your goal is to manage localization resources.\n"
        "You have access to tools specifically tagged with 'localization'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOG_AGENT_PROMPT = os.environ.get(
    "LOG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Log Agent.\n"
        "Your goal is to manage log resources.\n"
        "You have access to tools specifically tagged with 'log'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOGFILE_AGENT_PROMPT = os.environ.get(
    "LOGFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr LogFile Agent.\n"
        "Your goal is to manage log file resources.\n"
        "You have access to tools specifically tagged with 'logfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MANUALIMPORT_AGENT_PROMPT = os.environ.get(
    "MANUALIMPORT_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ManualImport Agent.\n"
        "Your goal is to manage manual import resources.\n"
        "You have access to tools specifically tagged with 'manualimport'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIACOVER_AGENT_PROMPT = os.environ.get(
    "MEDIACOVER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MediaCover Agent.\n"
        "Your goal is to manage media cover resources.\n"
        "You have access to tools specifically tagged with 'mediacover'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MEDIAMANAGEMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "MEDIAMANAGEMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MediaManagementConfig Agent.\n"
        "Your goal is to manage media management config resources.\n"
        "You have access to tools specifically tagged with 'mediamanagementconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATA_AGENT_PROMPT = os.environ.get(
    "METADATA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Metadata Agent.\n"
        "Your goal is to manage metadata resources.\n"
        "You have access to tools specifically tagged with 'metadata'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROFILE_AGENT_PROMPT = os.environ.get(
    "METADATAPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProfile Agent.\n"
        "Your goal is to manage metadata profile resources.\n"
        "You have access to tools specifically tagged with 'metadataprofile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "METADATAPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProfileSchema Agent.\n"
        "Your goal is to manage metadata profile schema resources.\n"
        "You have access to tools specifically tagged with 'metadataprofileschema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

METADATAPROVIDERCONFIG_AGENT_PROMPT = os.environ.get(
    "METADATAPROVIDERCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr MetadataProviderConfig Agent.\n"
        "Your goal is to manage metadata provider config resources.\n"
        "You have access to tools specifically tagged with 'metadataproviderconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

MISSING_AGENT_PROMPT = os.environ.get(
    "MISSING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Missing Agent.\n"
        "Your goal is to manage missing resources.\n"
        "You have access to tools specifically tagged with 'missing'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NAMINGCONFIG_AGENT_PROMPT = os.environ.get(
    "NAMINGCONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr NamingConfig Agent.\n"
        "Your goal is to manage naming config resources.\n"
        "You have access to tools specifically tagged with 'namingconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NOTIFICATION_AGENT_PROMPT = os.environ.get(
    "NOTIFICATION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Notification Agent.\n"
        "Your goal is to manage notification resources.\n"
        "You have access to tools specifically tagged with 'notification'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PARSE_AGENT_PROMPT = os.environ.get(
    "PARSE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Parse Agent.\n"
        "Your goal is to manage parse resources.\n"
        "You have access to tools specifically tagged with 'parse'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PING_AGENT_PROMPT = os.environ.get(
    "PING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Ping Agent.\n"
        "Your goal is to manage ping resources.\n"
        "You have access to tools specifically tagged with 'ping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYDEFINITION_AGENT_PROMPT = os.environ.get(
    "QUALITYDEFINITION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityDefinition Agent.\n"
        "Your goal is to manage quality definition resources.\n"
        "You have access to tools specifically tagged with 'qualitydefinition'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILE_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityProfile Agent.\n"
        "Your goal is to manage quality profile resources.\n"
        "You have access to tools specifically tagged with 'qualityprofile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUALITYPROFILESCHEMA_AGENT_PROMPT = os.environ.get(
    "QUALITYPROFILESCHEMA_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QualityProfileSchema Agent.\n"
        "Your goal is to manage quality profile schema resources.\n"
        "You have access to tools specifically tagged with 'qualityprofileschema'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUE_AGENT_PROMPT = os.environ.get(
    "QUEUE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Queue Agent.\n"
        "Your goal is to manage queue resources.\n"
        "You have access to tools specifically tagged with 'queue'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEACTION_AGENT_PROMPT = os.environ.get(
    "QUEUEACTION_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueAction Agent.\n"
        "Your goal is to manage queue action resources.\n"
        "You have access to tools specifically tagged with 'queueaction'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUEDETAILS_AGENT_PROMPT = os.environ.get(
    "QUEUEDETAILS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueDetails Agent.\n"
        "Your goal is to manage queue details resources.\n"
        "You have access to tools specifically tagged with 'queuedetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

QUEUESTATUS_AGENT_PROMPT = os.environ.get(
    "QUEUESTATUS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr QueueStatus Agent.\n"
        "Your goal is to manage queue status resources.\n"
        "You have access to tools specifically tagged with 'queuestatus'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASE_AGENT_PROMPT = os.environ.get(
    "RELEASE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Release Agent.\n"
        "Your goal is to manage release resources.\n"
        "You have access to tools specifically tagged with 'release'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPROFILE_AGENT_PROMPT = os.environ.get(
    "RELEASEPROFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ReleaseProfile Agent.\n"
        "Your goal is to manage release profile resources.\n"
        "You have access to tools specifically tagged with 'releaseprofile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RELEASEPUSH_AGENT_PROMPT = os.environ.get(
    "RELEASEPUSH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr ReleasePush Agent.\n"
        "Your goal is to manage release push resources.\n"
        "You have access to tools specifically tagged with 'releasepush'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

REMOTEPATHMAPPING_AGENT_PROMPT = os.environ.get(
    "REMOTEPATHMAPPING_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RemotePathMapping Agent.\n"
        "Your goal is to manage remote path mapping resources.\n"
        "You have access to tools specifically tagged with 'remotepathmapping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RENAMEBOOK_AGENT_PROMPT = os.environ.get(
    "RENAMEBOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RenameBook Agent.\n"
        "Your goal is to manage rename book resources.\n"
        "You have access to tools specifically tagged with 'renamebook'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

RETAGBOOK_AGENT_PROMPT = os.environ.get(
    "RETAGBOOK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RetagBook Agent.\n"
        "Your goal is to manage retag book resources.\n"
        "You have access to tools specifically tagged with 'retagbook'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

ROOTFOLDER_AGENT_PROMPT = os.environ.get(
    "ROOTFOLDER_AGENT_PROMPT",
    default=(
        "You are the Chaptarr RootFolder Agent.\n"
        "Your goal is to manage root folder resources.\n"
        "You have access to tools specifically tagged with 'rootfolder'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SEARCH_AGENT_PROMPT = os.environ.get(
    "SEARCH_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Search Agent.\n"
        "Your goal is to manage search resources.\n"
        "You have access to tools specifically tagged with 'search'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SERIES_AGENT_PROMPT = os.environ.get(
    "SERIES_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Series Agent.\n"
        "Your goal is to manage series resources.\n"
        "You have access to tools specifically tagged with 'series'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

STATICRESOURCE_AGENT_PROMPT = os.environ.get(
    "STATICRESOURCE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr StaticResource Agent.\n"
        "Your goal is to manage static resource resources.\n"
        "You have access to tools specifically tagged with 'staticresource'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SYSTEM_AGENT_PROMPT = os.environ.get(
    "SYSTEM_AGENT_PROMPT",
    default=(
        "You are the Chaptarr System Agent.\n"
        "Your goal is to manage system resources.\n"
        "You have access to tools specifically tagged with 'system'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAG_AGENT_PROMPT = os.environ.get(
    "TAG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Tag Agent.\n"
        "Your goal is to manage tag resources.\n"
        "You have access to tools specifically tagged with 'tag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAGDETAILS_AGENT_PROMPT = os.environ.get(
    "TAGDETAILS_AGENT_PROMPT",
    default=(
        "You are the Chaptarr TagDetails Agent.\n"
        "Your goal is to manage tag details resources.\n"
        "You have access to tools specifically tagged with 'tagdetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TASK_AGENT_PROMPT = os.environ.get(
    "TASK_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Task Agent.\n"
        "Your goal is to manage task resources.\n"
        "You have access to tools specifically tagged with 'task'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UICONFIG_AGENT_PROMPT = os.environ.get(
    "UICONFIG_AGENT_PROMPT",
    default=(
        "You are the Chaptarr UiConfig Agent.\n"
        "Your goal is to manage ui config resources.\n"
        "You have access to tools specifically tagged with 'uiconfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATE_AGENT_PROMPT = os.environ.get(
    "UPDATE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr Update Agent.\n"
        "Your goal is to manage update resources.\n"
        "You have access to tools specifically tagged with 'update'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATELOGFILE_AGENT_PROMPT = os.environ.get(
    "UPDATELOGFILE_AGENT_PROMPT",
    default=(
        "You are the Chaptarr UpdateLogFile Agent.\n"
        "Your goal is to manage update log file resources.\n"
        "You have access to tools specifically tagged with 'updatelogfile'.\n"
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
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
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

    # Always load default skills

    skill_dirs = [get_skills_path()]

    if custom_skills_directory and os.path.exists(custom_skills_directory):

        skill_dirs.append(str(custom_skills_directory))

    agent_toolsets.append(SkillsToolset(directories=skill_dirs))

    agent_defs = {
        "authorlookup": (AUTHORLOOKUP_AGENT_PROMPT, "Chaptarr_AuthorLookup_Agent"),
        "backup": (BACKUP_AGENT_PROMPT, "Chaptarr_Backup_Agent"),
        "blocklist": (BLOCKLIST_AGENT_PROMPT, "Chaptarr_Blocklist_Agent"),
        "book": (BOOK_AGENT_PROMPT, "Chaptarr_Book_Agent"),
        "bookeditor": (BOOKEDITOR_AGENT_PROMPT, "Chaptarr_BookEditor_Agent"),
        "bookfile": (BOOKFILE_AGENT_PROMPT, "Chaptarr_BookFile_Agent"),
        "booklookup": (BOOKLOOKUP_AGENT_PROMPT, "Chaptarr_BookLookup_Agent"),
        "bookshelf": (BOOKSHELF_AGENT_PROMPT, "Chaptarr_Bookshelf_Agent"),
        "calendar": (CALENDAR_AGENT_PROMPT, "Chaptarr_Calendar_Agent"),
        "calendarfeed": (CALENDARFEED_AGENT_PROMPT, "Chaptarr_CalendarFeed_Agent"),
        "command": (COMMAND_AGENT_PROMPT, "Chaptarr_Command_Agent"),
        "customfilter": (CUSTOMFILTER_AGENT_PROMPT, "Chaptarr_CustomFilter_Agent"),
        "customformat": (CUSTOMFORMAT_AGENT_PROMPT, "Chaptarr_CustomFormat_Agent"),
        "cutoff": (CUTOFF_AGENT_PROMPT, "Chaptarr_Cutoff_Agent"),
        "delayprofile": (DELAYPROFILE_AGENT_PROMPT, "Chaptarr_DelayProfile_Agent"),
        "developmentconfig": (
            DEVELOPMENTCONFIG_AGENT_PROMPT,
            "Chaptarr_DevelopmentConfig_Agent",
        ),
        "diskspace": (DISKSPACE_AGENT_PROMPT, "Chaptarr_DiskSpace_Agent"),
        "downloadclient": (
            DOWNLOADCLIENT_AGENT_PROMPT,
            "Chaptarr_DownloadClient_Agent",
        ),
        "downloadclientconfig": (
            DOWNLOADCLIENTCONFIG_AGENT_PROMPT,
            "Chaptarr_DownloadClientConfig_Agent",
        ),
        "edition": (EDITION_AGENT_PROMPT, "Chaptarr_Edition_Agent"),
        "filesystem": (FILESYSTEM_AGENT_PROMPT, "Chaptarr_FileSystem_Agent"),
        "health": (HEALTH_AGENT_PROMPT, "Chaptarr_Health_Agent"),
        "history": (HISTORY_AGENT_PROMPT, "Chaptarr_History_Agent"),
        "hostconfig": (HOSTCONFIG_AGENT_PROMPT, "Chaptarr_HostConfig_Agent"),
        "importlist": (IMPORTLIST_AGENT_PROMPT, "Chaptarr_ImportList_Agent"),
        "importlistexclusion": (
            IMPORTLISTEXCLUSION_AGENT_PROMPT,
            "Chaptarr_ImportListExclusion_Agent",
        ),
        "indexer": (INDEXER_AGENT_PROMPT, "Chaptarr_Indexer_Agent"),
        "indexerconfig": (INDEXERCONFIG_AGENT_PROMPT, "Chaptarr_IndexerConfig_Agent"),
        "indexerflag": (INDEXERFLAG_AGENT_PROMPT, "Chaptarr_IndexerFlag_Agent"),
        "language": (LANGUAGE_AGENT_PROMPT, "Chaptarr_Language_Agent"),
        "localization": (LOCALIZATION_AGENT_PROMPT, "Chaptarr_Localization_Agent"),
        "log": (LOG_AGENT_PROMPT, "Chaptarr_Log_Agent"),
        "logfile": (LOGFILE_AGENT_PROMPT, "Chaptarr_LogFile_Agent"),
        "manualimport": (MANUALIMPORT_AGENT_PROMPT, "Chaptarr_ManualImport_Agent"),
        "mediacover": (MEDIACOVER_AGENT_PROMPT, "Chaptarr_MediaCover_Agent"),
        "mediamanagementconfig": (
            MEDIAMANAGEMENTCONFIG_AGENT_PROMPT,
            "Chaptarr_MediaManagementConfig_Agent",
        ),
        "metadata": (METADATA_AGENT_PROMPT, "Chaptarr_Metadata_Agent"),
        "metadataprofile": (
            METADATAPROFILE_AGENT_PROMPT,
            "Chaptarr_MetadataProfile_Agent",
        ),
        "metadataprofileschema": (
            METADATAPROFILESCHEMA_AGENT_PROMPT,
            "Chaptarr_MetadataProfileSchema_Agent",
        ),
        "metadataproviderconfig": (
            METADATAPROVIDERCONFIG_AGENT_PROMPT,
            "Chaptarr_MetadataProviderConfig_Agent",
        ),
        "missing": (MISSING_AGENT_PROMPT, "Chaptarr_Missing_Agent"),
        "namingconfig": (NAMINGCONFIG_AGENT_PROMPT, "Chaptarr_NamingConfig_Agent"),
        "notification": (NOTIFICATION_AGENT_PROMPT, "Chaptarr_Notification_Agent"),
        "parse": (PARSE_AGENT_PROMPT, "Chaptarr_Parse_Agent"),
        "ping": (PING_AGENT_PROMPT, "Chaptarr_Ping_Agent"),
        "qualitydefinition": (
            QUALITYDEFINITION_AGENT_PROMPT,
            "Chaptarr_QualityDefinition_Agent",
        ),
        "qualityprofile": (
            QUALITYPROFILE_AGENT_PROMPT,
            "Chaptarr_QualityProfile_Agent",
        ),
        "qualityprofileschema": (
            QUALITYPROFILESCHEMA_AGENT_PROMPT,
            "Chaptarr_QualityProfileSchema_Agent",
        ),
        "queue": (QUEUE_AGENT_PROMPT, "Chaptarr_Queue_Agent"),
        "queueaction": (QUEUEACTION_AGENT_PROMPT, "Chaptarr_QueueAction_Agent"),
        "queuedetails": (QUEUEDETAILS_AGENT_PROMPT, "Chaptarr_QueueDetails_Agent"),
        "queuestatus": (QUEUESTATUS_AGENT_PROMPT, "Chaptarr_QueueStatus_Agent"),
        "release": (RELEASE_AGENT_PROMPT, "Chaptarr_Release_Agent"),
        "releaseprofile": (
            RELEASEPROFILE_AGENT_PROMPT,
            "Chaptarr_ReleaseProfile_Agent",
        ),
        "releasepush": (RELEASEPUSH_AGENT_PROMPT, "Chaptarr_ReleasePush_Agent"),
        "remotepathmapping": (
            REMOTEPATHMAPPING_AGENT_PROMPT,
            "Chaptarr_RemotePathMapping_Agent",
        ),
        "renamebook": (RENAMEBOOK_AGENT_PROMPT, "Chaptarr_RenameBook_Agent"),
        "retagbook": (RETAGBOOK_AGENT_PROMPT, "Chaptarr_RetagBook_Agent"),
        "rootfolder": (ROOTFOLDER_AGENT_PROMPT, "Chaptarr_RootFolder_Agent"),
        "search": (SEARCH_AGENT_PROMPT, "Chaptarr_Search_Agent"),
        "series": (SERIES_AGENT_PROMPT, "Chaptarr_Series_Agent"),
        "staticresource": (
            STATICRESOURCE_AGENT_PROMPT,
            "Chaptarr_StaticResource_Agent",
        ),
        "system": (SYSTEM_AGENT_PROMPT, "Chaptarr_System_Agent"),
        "tag": (TAG_AGENT_PROMPT, "Chaptarr_Tag_Agent"),
        "tagdetails": (TAGDETAILS_AGENT_PROMPT, "Chaptarr_TagDetails_Agent"),
        "task": (TASK_AGENT_PROMPT, "Chaptarr_Task_Agent"),
        "uiconfig": (UICONFIG_AGENT_PROMPT, "Chaptarr_UiConfig_Agent"),
        "update": (UPDATE_AGENT_PROMPT, "Chaptarr_Update_Agent"),
        "updatelogfile": (UPDATELOGFILE_AGENT_PROMPT, "Chaptarr_UpdateLogFile_Agent"),
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

        # Collect tool names for logging
        all_tool_names = []
        for ts in tag_toolsets:
            try:
                # Unwrap FilteredToolset
                current_ts = ts
                while hasattr(current_ts, "wrapped"):
                    current_ts = current_ts.wrapped

                # Check for .tools (e.g. SkillsToolset)
                if hasattr(current_ts, "tools") and isinstance(current_ts.tools, dict):
                    all_tool_names.extend(current_ts.tools.keys())
                # Check for ._tools (some implementations might use private attr)
                elif hasattr(current_ts, "_tools") and isinstance(
                    current_ts._tools, dict
                ):
                    all_tool_names.extend(current_ts._tools.keys())
                else:
                    # Fallback for MCP or others where tools are not available sync
                    all_tool_names.append(f"<{type(current_ts).__name__}>")
            except Exception as e:
                logger.info(f"Unable to retrieve toolset: {e}")
                pass

        tool_list_str = ", ".join(all_tool_names)
        logger.info(f"Available tools for {agent_name} ({tag}): {tool_list_str}")
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            name=agent_name,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
            model_settings=settings,
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
    async def assign_task_to_authorlookup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to authorlookup to the AuthorLookup Agent."""
        try:

            return (
                await child_agents["authorlookup"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in authorlookup agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_backup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to backup to the Backup Agent."""
        try:

            return (
                await child_agents["backup"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in backup agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_blocklist_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to blocklist to the Blocklist Agent."""
        try:

            return (
                await child_agents["blocklist"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in blocklist agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_book_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to book to the Book Agent."""
        try:

            return (
                await child_agents["book"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in book agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_bookeditor_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to bookeditor to the BookEditor Agent."""
        try:

            return (
                await child_agents["bookeditor"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in bookeditor agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_bookfile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to bookfile to the BookFile Agent."""
        try:

            return (
                await child_agents["bookfile"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in bookfile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_booklookup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to booklookup to the BookLookup Agent."""
        try:

            return (
                await child_agents["booklookup"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in booklookup agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_bookshelf_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to bookshelf to the Bookshelf Agent."""
        try:

            return (
                await child_agents["bookshelf"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in bookshelf agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_calendar_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to calendar to the Calendar Agent."""
        try:

            return (
                await child_agents["calendar"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in calendar agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_calendarfeed_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to calendarfeed to the CalendarFeed Agent."""
        try:

            return (
                await child_agents["calendarfeed"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in calendarfeed agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_command_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to command to the Command Agent."""
        try:

            return (
                await child_agents["command"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in command agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_customfilter_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to customfilter to the CustomFilter Agent."""
        try:

            return (
                await child_agents["customfilter"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in customfilter agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_customformat_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to customformat to the CustomFormat Agent."""
        try:

            return (
                await child_agents["customformat"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in customformat agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_cutoff_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to cutoff to the Cutoff Agent."""
        try:

            return (
                await child_agents["cutoff"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in cutoff agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_delayprofile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to delayprofile to the DelayProfile Agent."""
        try:

            return (
                await child_agents["delayprofile"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in delayprofile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_developmentconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to developmentconfig to the DevelopmentConfig Agent."""
        try:

            return (
                await child_agents["developmentconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in developmentconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_diskspace_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to diskspace to the DiskSpace Agent."""
        try:

            return (
                await child_agents["diskspace"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in diskspace agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_downloadclient_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to downloadclient to the DownloadClient Agent."""
        try:

            return (
                await child_agents["downloadclient"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in downloadclient agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_downloadclientconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to downloadclientconfig to the DownloadClientConfig Agent."""
        try:

            return (
                await child_agents["downloadclientconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in downloadclientconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_edition_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to edition to the Edition Agent."""
        try:

            return (
                await child_agents["edition"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in edition agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_filesystem_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to filesystem to the FileSystem Agent."""
        try:

            return (
                await child_agents["filesystem"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in filesystem agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_health_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to health to the Health Agent."""
        try:

            return (
                await child_agents["health"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in health agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_history_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to history to the History Agent."""
        try:

            return (
                await child_agents["history"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in history agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_hostconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to hostconfig to the HostConfig Agent."""
        try:

            return (
                await child_agents["hostconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in hostconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_importlist_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to importlist to the ImportList Agent."""
        try:

            return (
                await child_agents["importlist"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in importlist agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_importlistexclusion_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to importlistexclusion to the ImportListExclusion Agent."""
        try:

            return (
                await child_agents["importlistexclusion"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in importlistexclusion agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_indexer_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to indexer to the Indexer Agent."""
        try:

            return (
                await child_agents["indexer"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in indexer agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_indexerconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to indexerconfig to the IndexerConfig Agent."""
        try:

            return (
                await child_agents["indexerconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in indexerconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_indexerflag_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to indexerflag to the IndexerFlag Agent."""
        try:

            return (
                await child_agents["indexerflag"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in indexerflag agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_language_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to language to the Language Agent."""
        try:

            return (
                await child_agents["language"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in language agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_localization_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to localization to the Localization Agent."""
        try:

            return (
                await child_agents["localization"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in localization agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_log_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to log to the Log Agent."""
        try:

            return (
                await child_agents["log"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in log agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_logfile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to logfile to the LogFile Agent."""
        try:

            return (
                await child_agents["logfile"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in logfile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_manualimport_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to manualimport to the ManualImport Agent."""
        try:

            return (
                await child_agents["manualimport"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in manualimport agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_mediacover_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to mediacover to the MediaCover Agent."""
        try:

            return (
                await child_agents["mediacover"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in mediacover agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_mediamanagementconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to mediamanagementconfig to the MediaManagementConfig Agent."""
        try:

            return (
                await child_agents["mediamanagementconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in mediamanagementconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_metadata_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to metadata to the Metadata Agent."""
        try:

            return (
                await child_agents["metadata"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in metadata agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_metadataprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to metadataprofile to the MetadataProfile Agent."""
        try:

            return (
                await child_agents["metadataprofile"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in metadataprofile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_metadataprofileschema_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to metadataprofileschema to the MetadataProfileSchema Agent."""
        try:

            return (
                await child_agents["metadataprofileschema"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in metadataprofileschema agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_metadataproviderconfig_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to metadataproviderconfig to the MetadataProviderConfig Agent."""
        try:

            return (
                await child_agents["metadataproviderconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in metadataproviderconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_missing_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to missing to the Missing Agent."""
        try:

            return (
                await child_agents["missing"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in missing agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_namingconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to namingconfig to the NamingConfig Agent."""
        try:

            return (
                await child_agents["namingconfig"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in namingconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_notification_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to notification to the Notification Agent."""
        try:

            return (
                await child_agents["notification"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in notification agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_parse_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to parse to the Parse Agent."""
        try:

            return (
                await child_agents["parse"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in parse agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_ping_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ping to the Ping Agent."""
        try:

            return (
                await child_agents["ping"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in ping agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_qualitydefinition_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to qualitydefinition to the QualityDefinition Agent."""
        try:

            return (
                await child_agents["qualitydefinition"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in qualitydefinition agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_qualityprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to qualityprofile to the QualityProfile Agent."""
        try:

            return (
                await child_agents["qualityprofile"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in qualityprofile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_qualityprofileschema_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to qualityprofileschema to the QualityProfileSchema Agent."""
        try:

            return (
                await child_agents["qualityprofileschema"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in qualityprofileschema agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_queue_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to queue to the Queue Agent."""
        try:

            return (
                await child_agents["queue"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in queue agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_queueaction_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to queueaction to the QueueAction Agent."""
        try:

            return (
                await child_agents["queueaction"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in queueaction agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_queuedetails_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to queuedetails to the QueueDetails Agent."""
        try:

            return (
                await child_agents["queuedetails"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in queuedetails agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_queuestatus_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to queuestatus to the QueueStatus Agent."""
        try:

            return (
                await child_agents["queuestatus"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in queuestatus agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_release_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to release to the Release Agent."""
        try:

            return (
                await child_agents["release"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in release agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_releaseprofile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to releaseprofile to the ReleaseProfile Agent."""
        try:

            return (
                await child_agents["releaseprofile"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in releaseprofile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_releasepush_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to releasepush to the ReleasePush Agent."""
        try:

            return (
                await child_agents["releasepush"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in releasepush agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_remotepathmapping_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to remotepathmapping to the RemotePathMapping Agent."""
        try:

            return (
                await child_agents["remotepathmapping"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in remotepathmapping agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_renamebook_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to renamebook to the RenameBook Agent."""
        try:

            return (
                await child_agents["renamebook"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in renamebook agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_retagbook_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to retagbook to the RetagBook Agent."""
        try:

            return (
                await child_agents["retagbook"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in retagbook agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_rootfolder_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to rootfolder to the RootFolder Agent."""
        try:

            return (
                await child_agents["rootfolder"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in rootfolder agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_search_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to search to the Search Agent."""
        try:

            return (
                await child_agents["search"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in search agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_series_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to series to the Series Agent."""
        try:

            return (
                await child_agents["series"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in series agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_staticresource_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to staticresource to the StaticResource Agent."""
        try:

            return (
                await child_agents["staticresource"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in staticresource agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_system_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to system to the System Agent."""
        try:

            return (
                await child_agents["system"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in system agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_tag_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to tag to the Tag Agent."""
        try:

            return (
                await child_agents["tag"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in tag agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_tagdetails_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to tagdetails to the TagDetails Agent."""
        try:

            return (
                await child_agents["tagdetails"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in tagdetails agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_task_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to task to the Task Agent."""
        try:

            return (
                await child_agents["task"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in task agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_uiconfig_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to uiconfig to the UiConfig Agent."""
        try:

            return (
                await child_agents["uiconfig"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in uiconfig agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_update_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to update to the Update Agent."""
        try:

            return (
                await child_agents["update"].run(task, usage=ctx.usage, deps=ctx.deps)
            ).output

        except Exception as e:

            logger.error(f"Error in update agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

    @supervisor.tool
    async def assign_task_to_updatelogfile_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to updatelogfile to the UpdateLogFile Agent."""
        try:

            return (
                await child_agents["updatelogfile"].run(
                    task, usage=ctx.usage, deps=ctx.deps
                )
            ).output

        except Exception as e:

            logger.error(f"Error in updatelogfile agent: {e}", exc_info=True)

            return f"Error executing task: {e}"

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
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
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
        custom_skills_directory=custom_skills_directory,
        ssl_verify=ssl_verify,
    )

    # Always load default skills

    skills = load_skills_from_directory(get_skills_path())

    logger.info(f"Loaded {len(skills)} default skills from {get_skills_path()}")

    # Load custom skills if provided

    if custom_skills_directory and os.path.exists(custom_skills_directory):

        custom_skills = load_skills_from_directory(custom_skills_directory)

        skills.extend(custom_skills)

        logger.info(
            f"Loaded {len(custom_skills)} custom skills from {custom_skills_directory}"
        )

    if not skills:

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
        "--custom-skills-directory",
        default=DEFAULT_CUSTOM_SKILLS_DIRECTORY,
        help="Directory containing additional custom agent skills",
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

        parser.print_help()

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
        custom_skills_directory=args.custom_skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
        ssl_verify=not args.insecure,
    )


if __name__ == "__main__":
    agent_server()
