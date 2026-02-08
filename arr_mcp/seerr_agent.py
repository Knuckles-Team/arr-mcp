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
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "0.1.0"

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
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-4b-2507")
DEFAULT_OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "http://host.docker.internal:1234/v1"
)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", "http://localhost:8000/sse")
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))

# Model Settings
DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "8192"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_Extra_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))

AGENT_NAME = "SeerrAgent"
AGENT_DESCRIPTION = "Agent for managing media requests and discovery on Seerr."

SYSTEM_PROMPT = """
You are the Seerr Agent.
Your goal is to assist the user manage their media requests and discoveries on Seerr (Overseerr/Jellyseerr).
You can search for movies and TV shows, request them, manage existing requests, and manage users.
Always be warm, professional, and helpful.
If you need to search for something, use the search tool first.
When presenting media, show the title, year, and ID.
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
             transport = MCPServerStreamableHTTP(url=DEFAULT_MCP_URL, name="seerr-mcp")

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

@app.get("/ui")
async def ui_get():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Seerr Agent</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            #chat-container { border: 1px solid #ccc; padding: 20px; height: 400px; overflow-y: scroll; margin-bottom: 20px; }
            .message { margin-bottom: 10px; padding: 10px; border-radius: 5px; }
            .user { background-color: #e3f2fd; text-align: right; }
            .agent { background-color: #f5f5f5; }
            #input-container { display: flex; }
            #prompt { flex-grow: 1; padding: 10px; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Seerr Agent</h1>
        <div id="chat-container"></div>
        <div id="input-container">
            <input type="text" id="prompt" placeholder="Ask something..." />
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            async function sendMessage() {
                const promptInput = document.getElementById('prompt');
                const prompt = promptInput.value;
                if (!prompt) return;

                addMessage(prompt, 'user');
                promptInput.value = '';

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: prompt })
                    });
                    const data = await response.json();
                    addMessage(data.response, 'agent');
                } catch (error) {
                    addMessage('Error: ' + error.message, 'agent');
                }
            }

            function addMessage(text, sender) {
                const container = document.getElementById('chat-container');
                const div = document.createElement('div');
                div.className = `message ${sender}`;
                div.textContent = text;
                container.appendChild(div);
                container.scrollTop = container.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")

if __name__ == "__main__":
    uvicorn.run(app, host=DEFAULT_HOST, port=DEFAULT_PORT)
