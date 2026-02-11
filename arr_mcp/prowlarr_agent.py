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

AGENT_NAME = "ProwlarrAgent"
AGENT_DESCRIPTION = (
    "A multi-agent system for managing Prowlarr resources via delegated specialists."
)

# -------------------------------------------------------------------------
# 1. System Prompts
# -------------------------------------------------------------------------

SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the Prowlarr Supervisor Agent.\n"
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
        "You are the Prowlarr ApiInfo Agent.\n"
        "Your goal is to manage api info resources.\n"
        "You have access to tools specifically tagged with 'ApiInfo'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

APPPROFILE_AGENT_PROMPT = os.environ.get(
    "APPPROFILE_AGENT_PROMPT",
    default=(
        "You are the Prowlarr AppProfile Agent.\n"
        "Your goal is to manage app profile resources.\n"
        "You have access to tools specifically tagged with 'AppProfile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

APPLICATION_AGENT_PROMPT = os.environ.get(
    "APPLICATION_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Application Agent.\n"
        "Your goal is to manage application resources.\n"
        "You have access to tools specifically tagged with 'Application'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

AUTHENTICATION_AGENT_PROMPT = os.environ.get(
    "AUTHENTICATION_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Authentication Agent.\n"
        "Your goal is to manage authentication resources.\n"
        "You have access to tools specifically tagged with 'Authentication'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

BACKUP_AGENT_PROMPT = os.environ.get(
    "BACKUP_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Backup Agent.\n"
        "Your goal is to manage backup resources.\n"
        "You have access to tools specifically tagged with 'Backup'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

COMMAND_AGENT_PROMPT = os.environ.get(
    "COMMAND_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Command Agent.\n"
        "Your goal is to manage command resources.\n"
        "You have access to tools specifically tagged with 'Command'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

CUSTOMFILTER_AGENT_PROMPT = os.environ.get(
    "CUSTOMFILTER_AGENT_PROMPT",
    default=(
        "You are the Prowlarr CustomFilter Agent.\n"
        "Your goal is to manage custom filter resources.\n"
        "You have access to tools specifically tagged with 'CustomFilter'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DEVELOPMENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DEVELOPMENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr DevelopmentConfig Agent.\n"
        "Your goal is to manage development config resources.\n"
        "You have access to tools specifically tagged with 'DevelopmentConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENT_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENT_AGENT_PROMPT",
    default=(
        "You are the Prowlarr DownloadClient Agent.\n"
        "Your goal is to manage download client resources.\n"
        "You have access to tools specifically tagged with 'DownloadClient'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

DOWNLOADCLIENTCONFIG_AGENT_PROMPT = os.environ.get(
    "DOWNLOADCLIENTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr DownloadClientConfig Agent.\n"
        "Your goal is to manage download client config resources.\n"
        "You have access to tools specifically tagged with 'DownloadClientConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

FILESYSTEM_AGENT_PROMPT = os.environ.get(
    "FILESYSTEM_AGENT_PROMPT",
    default=(
        "You are the Prowlarr FileSystem Agent.\n"
        "Your goal is to manage file system resources.\n"
        "You have access to tools specifically tagged with 'FileSystem'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HEALTH_AGENT_PROMPT = os.environ.get(
    "HEALTH_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Health Agent.\n"
        "Your goal is to manage health resources.\n"
        "You have access to tools specifically tagged with 'Health'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HISTORY_AGENT_PROMPT = os.environ.get(
    "HISTORY_AGENT_PROMPT",
    default=(
        "You are the Prowlarr History Agent.\n"
        "Your goal is to manage history resources.\n"
        "You have access to tools specifically tagged with 'History'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

HOSTCONFIG_AGENT_PROMPT = os.environ.get(
    "HOSTCONFIG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr HostConfig Agent.\n"
        "Your goal is to manage host config resources.\n"
        "You have access to tools specifically tagged with 'HostConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXER_AGENT_PROMPT = os.environ.get(
    "INDEXER_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Indexer Agent.\n"
        "Your goal is to manage indexer resources.\n"
        "You have access to tools specifically tagged with 'Indexer'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERDEFAULTCATEGORIES_AGENT_PROMPT = os.environ.get(
    "INDEXERDEFAULTCATEGORIES_AGENT_PROMPT",
    default=(
        "You are the Prowlarr IndexerDefaultCategories Agent.\n"
        "Your goal is to manage indexer default categories resources.\n"
        "You have access to tools specifically tagged with 'IndexerDefaultCategories'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERPROXY_AGENT_PROMPT = os.environ.get(
    "INDEXERPROXY_AGENT_PROMPT",
    default=(
        "You are the Prowlarr IndexerProxy Agent.\n"
        "Your goal is to manage indexer proxy resources.\n"
        "You have access to tools specifically tagged with 'IndexerProxy'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERSTATS_AGENT_PROMPT = os.environ.get(
    "INDEXERSTATS_AGENT_PROMPT",
    default=(
        "You are the Prowlarr IndexerStats Agent.\n"
        "Your goal is to manage indexer stats resources.\n"
        "You have access to tools specifically tagged with 'IndexerStats'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

INDEXERSTATUS_AGENT_PROMPT = os.environ.get(
    "INDEXERSTATUS_AGENT_PROMPT",
    default=(
        "You are the Prowlarr IndexerStatus Agent.\n"
        "Your goal is to manage indexer status resources.\n"
        "You have access to tools specifically tagged with 'IndexerStatus'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOCALIZATION_AGENT_PROMPT = os.environ.get(
    "LOCALIZATION_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Localization Agent.\n"
        "Your goal is to manage localization resources.\n"
        "You have access to tools specifically tagged with 'Localization'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOG_AGENT_PROMPT = os.environ.get(
    "LOG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Log Agent.\n"
        "Your goal is to manage log resources.\n"
        "You have access to tools specifically tagged with 'Log'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

LOGFILE_AGENT_PROMPT = os.environ.get(
    "LOGFILE_AGENT_PROMPT",
    default=(
        "You are the Prowlarr LogFile Agent.\n"
        "Your goal is to manage log file resources.\n"
        "You have access to tools specifically tagged with 'LogFile'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NEWZNAB_AGENT_PROMPT = os.environ.get(
    "NEWZNAB_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Newznab Agent.\n"
        "Your goal is to manage newznab resources.\n"
        "You have access to tools specifically tagged with 'Newznab'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

NOTIFICATION_AGENT_PROMPT = os.environ.get(
    "NOTIFICATION_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Notification Agent.\n"
        "Your goal is to manage notification resources.\n"
        "You have access to tools specifically tagged with 'Notification'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

PING_AGENT_PROMPT = os.environ.get(
    "PING_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Ping Agent.\n"
        "Your goal is to manage ping resources.\n"
        "You have access to tools specifically tagged with 'Ping'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SEARCH_AGENT_PROMPT = os.environ.get(
    "SEARCH_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Search Agent.\n"
        "Your goal is to manage search resources.\n"
        "You have access to tools specifically tagged with 'Search'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

STATICRESOURCE_AGENT_PROMPT = os.environ.get(
    "STATICRESOURCE_AGENT_PROMPT",
    default=(
        "You are the Prowlarr StaticResource Agent.\n"
        "Your goal is to manage static resource resources.\n"
        "You have access to tools specifically tagged with 'StaticResource'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

SYSTEM_AGENT_PROMPT = os.environ.get(
    "SYSTEM_AGENT_PROMPT",
    default=(
        "You are the Prowlarr System Agent.\n"
        "Your goal is to manage system resources.\n"
        "You have access to tools specifically tagged with 'System'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAG_AGENT_PROMPT = os.environ.get(
    "TAG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Tag Agent.\n"
        "Your goal is to manage tag resources.\n"
        "You have access to tools specifically tagged with 'Tag'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TAGDETAILS_AGENT_PROMPT = os.environ.get(
    "TAGDETAILS_AGENT_PROMPT",
    default=(
        "You are the Prowlarr TagDetails Agent.\n"
        "Your goal is to manage tag details resources.\n"
        "You have access to tools specifically tagged with 'TagDetails'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

TASK_AGENT_PROMPT = os.environ.get(
    "TASK_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Task Agent.\n"
        "Your goal is to manage task resources.\n"
        "You have access to tools specifically tagged with 'Task'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UICONFIG_AGENT_PROMPT = os.environ.get(
    "UICONFIG_AGENT_PROMPT",
    default=(
        "You are the Prowlarr UiConfig Agent.\n"
        "Your goal is to manage ui config resources.\n"
        "You have access to tools specifically tagged with 'UiConfig'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATE_AGENT_PROMPT = os.environ.get(
    "UPDATE_AGENT_PROMPT",
    default=(
        "You are the Prowlarr Update Agent.\n"
        "Your goal is to manage update resources.\n"
        "You have access to tools specifically tagged with 'Update'.\n"
        "Use these tools to fulfill the user's request."
    ),
)

UPDATELOGFILE_AGENT_PROMPT = os.environ.get(
    "UPDATELOGFILE_AGENT_PROMPT",
    default=(
        "You are the Prowlarr UpdateLogFile Agent.\n"
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
    logger.info("Initializing Multi-Agent System for Prowlarr...")

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
        "ApiInfo": (APIINFO_AGENT_PROMPT, "Prowlarr_ApiInfo_Agent"),
        "AppProfile": (APPPROFILE_AGENT_PROMPT, "Prowlarr_AppProfile_Agent"),
        "Application": (APPLICATION_AGENT_PROMPT, "Prowlarr_Application_Agent"),
        "Authentication": (
            AUTHENTICATION_AGENT_PROMPT,
            "Prowlarr_Authentication_Agent",
        ),
        "Backup": (BACKUP_AGENT_PROMPT, "Prowlarr_Backup_Agent"),
        "Command": (COMMAND_AGENT_PROMPT, "Prowlarr_Command_Agent"),
        "CustomFilter": (CUSTOMFILTER_AGENT_PROMPT, "Prowlarr_CustomFilter_Agent"),
        "DevelopmentConfig": (
            DEVELOPMENTCONFIG_AGENT_PROMPT,
            "Prowlarr_DevelopmentConfig_Agent",
        ),
        "DownloadClient": (
            DOWNLOADCLIENT_AGENT_PROMPT,
            "Prowlarr_DownloadClient_Agent",
        ),
        "DownloadClientConfig": (
            DOWNLOADCLIENTCONFIG_AGENT_PROMPT,
            "Prowlarr_DownloadClientConfig_Agent",
        ),
        "FileSystem": (FILESYSTEM_AGENT_PROMPT, "Prowlarr_FileSystem_Agent"),
        "Health": (HEALTH_AGENT_PROMPT, "Prowlarr_Health_Agent"),
        "History": (HISTORY_AGENT_PROMPT, "Prowlarr_History_Agent"),
        "HostConfig": (HOSTCONFIG_AGENT_PROMPT, "Prowlarr_HostConfig_Agent"),
        "Indexer": (INDEXER_AGENT_PROMPT, "Prowlarr_Indexer_Agent"),
        "IndexerDefaultCategories": (
            INDEXERDEFAULTCATEGORIES_AGENT_PROMPT,
            "Prowlarr_IndexerDefaultCategories_Agent",
        ),
        "IndexerProxy": (INDEXERPROXY_AGENT_PROMPT, "Prowlarr_IndexerProxy_Agent"),
        "IndexerStats": (INDEXERSTATS_AGENT_PROMPT, "Prowlarr_IndexerStats_Agent"),
        "IndexerStatus": (INDEXERSTATUS_AGENT_PROMPT, "Prowlarr_IndexerStatus_Agent"),
        "Localization": (LOCALIZATION_AGENT_PROMPT, "Prowlarr_Localization_Agent"),
        "Log": (LOG_AGENT_PROMPT, "Prowlarr_Log_Agent"),
        "LogFile": (LOGFILE_AGENT_PROMPT, "Prowlarr_LogFile_Agent"),
        "Newznab": (NEWZNAB_AGENT_PROMPT, "Prowlarr_Newznab_Agent"),
        "Notification": (NOTIFICATION_AGENT_PROMPT, "Prowlarr_Notification_Agent"),
        "Ping": (PING_AGENT_PROMPT, "Prowlarr_Ping_Agent"),
        "Search": (SEARCH_AGENT_PROMPT, "Prowlarr_Search_Agent"),
        "StaticResource": (
            STATICRESOURCE_AGENT_PROMPT,
            "Prowlarr_StaticResource_Agent",
        ),
        "System": (SYSTEM_AGENT_PROMPT, "Prowlarr_System_Agent"),
        "Tag": (TAG_AGENT_PROMPT, "Prowlarr_Tag_Agent"),
        "TagDetails": (TAGDETAILS_AGENT_PROMPT, "Prowlarr_TagDetails_Agent"),
        "Task": (TASK_AGENT_PROMPT, "Prowlarr_Task_Agent"),
        "UiConfig": (UICONFIG_AGENT_PROMPT, "Prowlarr_UiConfig_Agent"),
        "Update": (UPDATE_AGENT_PROMPT, "Prowlarr_Update_Agent"),
        "UpdateLogFile": (UPDATELOGFILE_AGENT_PROMPT, "Prowlarr_UpdateLogFile_Agent"),
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
    async def assign_task_to_apiinfo_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to ApiInfo to the ApiInfo Agent."""
        return (
            await child_agents["ApiInfo"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_appprofile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to AppProfile to the AppProfile Agent."""
        return (
            await child_agents["AppProfile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_application_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Application to the Application Agent."""
        return (
            await child_agents["Application"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    async def assign_task_to_backup_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Backup to the Backup Agent."""
        return (
            await child_agents["Backup"].run(task, usage=ctx.usage, deps=ctx.deps)
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
    async def assign_task_to_indexer_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Indexer to the Indexer Agent."""
        return (
            await child_agents["Indexer"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_indexerdefaultcategories_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to IndexerDefaultCategories to the IndexerDefaultCategories Agent."""
        return (
            await child_agents["IndexerDefaultCategories"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_indexerproxy_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to IndexerProxy to the IndexerProxy Agent."""
        return (
            await child_agents["IndexerProxy"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_indexerstats_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to IndexerStats to the IndexerStats Agent."""
        return (
            await child_agents["IndexerStats"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_indexerstatus_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to IndexerStatus to the IndexerStatus Agent."""
        return (
            await child_agents["IndexerStatus"].run(
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
    async def assign_task_to_newznab_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Newznab to the Newznab Agent."""
        return (
            await child_agents["Newznab"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_notification_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Notification to the Notification Agent."""
        return (
            await child_agents["Notification"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_ping_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Ping to the Ping Agent."""
        return (
            await child_agents["Ping"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_search_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to Search to the Search Agent."""
        return (
            await child_agents["Search"].run(task, usage=ctx.usage, deps=ctx.deps)
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
                id="prowlarr_agent",
                name="Prowlarr Agent",
                description="General access to Prowlarr tools",
                tags=["prowlarr"],
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
    print(f"prowlarr_agent v{__version__}")
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
        f"Arr Mcp ({__version__}): Prowlarr Agent\n\n"
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
        "  [Simple]  prowlarr-agent \n"
        '  [Complex] prowlarr-agent --host "value" --port "value" --debug "value" --reload --provider "value" --model-id "value" --base-url "value" --api-key "value" --mcp-url "value" --mcp-config "value" --skills-directory "value" --web\n'
    )


if __name__ == "__main__":
    agent_server()
