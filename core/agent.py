"""
BizPilot AI — Agent Core
The AI agent brain that uses LangChain to reason, select tools, 
and execute multi-step business tasks.
"""

from typing import List, Dict, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage

import config
from tools.inventory_tool import check_inventory, get_low_stock_alerts
from tools.email_tool import draft_email
from tools.invoice_tool import generate_invoice
from tools.exchange_rate_tool import get_exchange_rate
from tools.sales_tool import summarize_sales, list_customers


# --- System Prompt ---
SYSTEM_PROMPT = """You are BizPilot AI, an intelligent business automation agent for small and medium businesses in Ethiopia.

Your role is to help business owners and managers with daily operations by using your available tools. You can:

1. 📦 **Inventory Management** — Search products, check stock levels, identify low-stock items
2. 📧 **Email Drafting** — Compose professional business emails
3. 🧾 **Invoice Generation** — Create PDF invoices for customers
4. 💱 **Exchange Rates** — Look up currency conversion rates
5. 📊 **Sales Analytics** — Generate sales summaries, view trends, and business insights
6. 👥 **Customer Management** — Look up customer information

GUIDELINES:
- Always use the appropriate tool to get real data. Never make up inventory, sales, or price information.
- When the user's request requires multiple tools, use them in sequence and combine the results.
- Be proactive: if a user asks about inventory, also mention if any items are low on stock.
- Format your responses clearly with emojis and structured layouts.
- Prices are in Ethiopian Birr (ETB) unless specified otherwise.
- Be concise but thorough. Provide actionable insights when presenting data.
- If a task cannot be done with your available tools, explain what you can do instead.

PERSONALITY:
- Professional but friendly
- Proactive with suggestions
- Data-driven in recommendations
"""


def get_tools() -> list:
    """Get all available agent tools."""
    return [
        check_inventory,
        get_low_stock_alerts,
        draft_email,
        generate_invoice,
        get_exchange_rate,
        summarize_sales,
        list_customers,
    ]


def get_agent() -> AgentExecutor:
    """Create and return the BizPilot AI agent."""

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=config.LLM_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        temperature=config.LLM_TEMPERATURE,
    )

    # Get tools
    tools = get_tools()

    # Create prompt with chat history support
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create executor with iteration limit
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=config.VERBOSE_AGENT,
        max_iterations=config.MAX_ITERATIONS,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    return executor


def format_chat_history(history: List[Dict]) -> list:
    """Convert chat history dicts to LangChain message format."""
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


async def run_agent(
    user_input: str,
    chat_history: Optional[List[Dict]] = None,
) -> Dict:
    """
    Run the BizPilot AI agent with the given input.

    Args:
        user_input: The user's message/request.
        chat_history: Previous conversation messages.

    Returns:
        Dictionary with the agent's response, tool calls used, and intermediate steps.
    """
    if chat_history is None:
        chat_history = []

    agent = get_agent()
    history_messages = format_chat_history(chat_history)

    # Run the agent
    result = await agent.ainvoke({
        "input": user_input,
        "chat_history": history_messages,
    })

    # Extract tool usage information
    tools_used = []
    for step in result.get("intermediate_steps", []):
        if len(step) >= 2:
            action = step[0]
            tools_used.append({
                "tool": action.tool,
                "input": str(action.tool_input)[:200],
            })

    return {
        "output": result["output"],
        "tools_used": tools_used,
    }
