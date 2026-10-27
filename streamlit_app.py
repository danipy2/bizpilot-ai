"""
BizPilot AI — Streamlit Application
Interactive chat interface for the business automation agent.
"""

import asyncio
import uuid

import streamlit as st

st.set_page_config(
    page_title="BizPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# --- Load Streamlit Cloud secrets into env vars ---
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
if "EXCHANGE_RATE_API_KEY" in st.secrets:
    os.environ["EXCHANGE_RATE_API_KEY"] = st.secrets["EXCHANGE_RATE_API_KEY"]

# --- Check API key before importing AI modules ---
if not os.environ.get("GOOGLE_API_KEY"):
    st.error("⚠️ **GOOGLE_API_KEY not configured.** Please add it in Streamlit Cloud → App Settings → Secrets.")
    st.code('[secrets]\nGOOGLE_API_KEY = "your-gemini-api-key-here"', language="toml")
    st.info("Get a free Gemini API key at https://aistudio.google.com/apikey")
    st.stop()

from core.agent import run_agent
from database.db import init_db, seed_data, save_message, get_conversation_history

init_db()
seed_data()


def run_async(coro):
    """Helper to run async functions in Streamlit."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# --- Custom CSS ---
st.markdown("""
<style>
    .tool-badge {
        display: inline-block;
        background: #e3f2fd;
        color: #1565c0;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1565C0;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.markdown("# 🚀 BizPilot AI")
    st.caption("Intelligent Business Automation Agent")
    st.divider()

    st.markdown("### 🛠️ Available Tools")
    tools_info = {
        "📦 Inventory": "Search products, check stock",
        "📧 Email": "Draft professional emails",
        "🧾 Invoice": "Generate PDF invoices",
        "💱 Exchange Rate": "Currency conversion",
        "📊 Sales": "Revenue reports & trends",
        "👥 Customers": "Customer information",
    }
    for tool_name, desc in tools_info.items():
        st.markdown(f"**{tool_name}**")
        st.caption(desc)

    st.divider()

    # Example prompts
    st.markdown("### 💡 Try Asking")
    examples = [
        "Show me today's sales summary",
        "Which products are low on stock?",
        "Generate an invoice for Abebe Kebede for 2 laptops",
        "What's the USD to ETB exchange rate?",
        "Draft an email to a supplier about restocking",
        "List all customers",
    ]
    for example in examples:
        if st.button(example, key=f"ex_{example[:20]}", use_container_width=True):
            st.session_state.pending_message = example
            st.rerun()

    st.divider()

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(f"Session: `{st.session_state.session_id[:8]}...`")
    st.caption("Built with LangChain Agents & Gemini AI")

# --- Main Chat Interface ---
st.markdown('<p class="main-title">🚀 BizPilot AI</p>', unsafe_allow_html=True)
st.caption(
    "Your intelligent business assistant — manages inventory, drafts emails, "
    "generates invoices, checks exchange rates, and analyzes sales."
)
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show tools used
        if message["role"] == "assistant" and message.get("tools_used"):
            tools = message["tools_used"]
            tool_names = [t["tool"] for t in tools]
            badges = " ".join(
                f'<span class="tool-badge">🔧 {name}</span>'
                for name in tool_names
            )
            st.markdown(f"**Tools used:** {badges}", unsafe_allow_html=True)

# Check for pending message from sidebar example buttons
pending = st.session_state.pop("pending_message", None)

# Chat input
prompt = st.chat_input("Ask BizPilot to do something for your business...")

# Use pending message if no direct input
if pending and not prompt:
    prompt = pending

if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking and executing tools..."):
            # Get history for context
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]  # Exclude current message
            ]

            # Save user message
            save_message(st.session_state.session_id, "user", prompt)

            # Run the agent
            result = run_async(run_agent(
                user_input=prompt,
                chat_history=history,
            ))

            response = result["output"]
            tools_used = result["tools_used"]

            # Save assistant response
            save_message(
                st.session_state.session_id,
                "assistant",
                response,
                tool_calls=str(tools_used) if tools_used else None,
            )

            # Display response
            st.markdown(response)

            # Show tools used
            if tools_used:
                tool_names = [t["tool"] for t in tools_used]
                badges = " ".join(
                    f'<span class="tool-badge">🔧 {name}</span>'
                    for name in tool_names
                )
                st.markdown(f"**Tools used:** {badges}", unsafe_allow_html=True)

    # Save to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "tools_used": tools_used,
    })
