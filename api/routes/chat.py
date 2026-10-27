"""
BizPilot AI — Chat API Route
Endpoint for interacting with the business automation agent.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from core.agent import run_agent
from database.db import save_message, get_conversation_history

router = APIRouter(tags=["Agent"])


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message to the agent")
    session_id: str = Field(default="default", description="Session ID for conversation history")


class ToolUsage(BaseModel):
    tool: str
    input: str


class AgentResponse(BaseModel):
    response: str
    tools_used: List[ToolUsage]
    session_id: str


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Send a message to the BizPilot AI agent.
    The agent will reason about the request, select appropriate tools,
    execute them, and return a comprehensive response.
    """
    try:
        # Get conversation history
        history = get_conversation_history(request.session_id)
        chat_history = [
            {"role": h["role"], "content": h["content"]}
            for h in history
        ]

        # Save user message
        save_message(request.session_id, "user", request.message)

        # Run agent
        result = await run_agent(
            user_input=request.message,
            chat_history=chat_history,
        )

        # Save agent response
        save_message(
            request.session_id,
            "assistant",
            result["output"],
            tool_calls=str(result["tools_used"]) if result["tools_used"] else None,
        )

        return AgentResponse(
            response=result["output"],
            tools_used=[ToolUsage(**t) for t in result["tools_used"]],
            session_id=request.session_id,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
