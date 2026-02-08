#!/usr/bin/python
# coding: utf-8
import sys
import json
import os
import argparse
import logging
import uvicorn
from typing import Optional, Any, List
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import load_mcp_servers, MCPServerStreamableHTTP, MCPServerSSE
from arr_mcp.utils import (
    to_integer,
    to_boolean,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    create_model,
    prune_large_messages,
)

from fastapi import FastAPI, Request
from starlette.responses import Response
from pydantic import ValidationError

__version__ = "0.1.0"

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
DEFAULT_PORT = to_integer(value=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-4b-2507")
DEFAULT_OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "http://host.docker.internal:1234/v1"
)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/sse")
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())

# Model Settings
DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "8192"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))

AGENT_NAME = "BazarrAgent"
AGENT_DESCRIPTION = "Agent for managing subtitles on Bazarr."

SYSTEM_PROMPT = """
You are the Bazarr Agent.
Your goal is to assist the user manage their subtitles on Bazarr.
You can list series and movies, check for missing subtitles, and trigger downloads.
Always be warm, professional, and helpful.
If you need to find subtitles, use the search_series_subtitles or search_movie_subtitles tools.
"""


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_OPENAI_BASE_URL,
    api_key: Optional[str] = DEFAULT_OPENAI_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = None,
) -> Agent:
    logger.info(f"Creating {AGENT_NAME}")
    agent = Agent(
        model=create_model(
            provider=provider,
            model_id=model_id,
            base_url=base_url,
            api_key=api_key,
        ),
        system_prompt=SYSTEM_PROMPT,
        model_settings=ModelSettings(
            max_tokens=DEFAULT_MAX_TOKENS,
            temperature=DEFAULT_TEMPERATURE,
            top_p=DEFAULT_TOP_P,
            timeout=DEFAULT_TIMEOUT,
        ),
    )
    return agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {AGENT_NAME} v{__version__}")

    # Create the agent
    agent = create_agent(
        provider=DEFAULT_PROVIDER,
        model_id=DEFAULT_MODEL_ID,
        base_url=DEFAULT_OPENAI_BASE_URL,
        api_key=DEFAULT_OPENAI_API_KEY,
        mcp_url=DEFAULT_MCP_URL,
    )

    # Connect to MCP server
    logger.info(f"Connecting to MCP server at {DEFAULT_MCP_URL}")
    try:
        # Check if URL ends with /sse for SSE transport, otherwise assume HTTP
        if DEFAULT_MCP_URL.endswith("/sse"):
            transport = MCPServerSSE(url=DEFAULT_MCP_URL)
        else:
            transport = MCPServerStreamableHTTP(url=DEFAULT_MCP_URL, name="bazarr-mcp")

        async with transport as mcp_client:
            logger.info("Connected to MCP server")
            await agent.register_mcp_tools(mcp_client)
            logger.info(f"Registered {len(agent._function_tools)} tools")

            app.state.agent = agent
            yield
    except Exception as e:
        logger.error(f"Failed to connect to MCP server: {e}")
        # Allow starting without MCP for debug/testing
        app.state.agent = agent
        yield

    logger.info(f"Stopping {AGENT_NAME}")


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "ok", "agent": AGENT_NAME, "version": __version__}


@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        if not prompt:
            return Response(content="Missing prompt", status_code=400)

        agent: Agent = app.state.agent

        # Simple non-streaming run
        result = await agent.run(prompt)
        return {"response": result.data}
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return Response(content=str(e), status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)
