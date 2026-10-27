"""
BizPilot AI — Streamlit Application
Interactive chat interface for the business automation agent.
"""

import asyncio
import uuid
import os
import sys
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="BizPilot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load secrets — works on both Streamlit Cloud and Render.com
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ.setdefault("GOOGLE_API_KEY", st.secrets["GOOGLE_API_KEY"])
    if "EXCHANGE_RATE_API_KEY" in st.secrets:
        os.environ.setdefault("EXCHANGE_RATE_API_KEY", st.secrets["EXCHANGE_RATE_API_KEY"])
except Exception:
    pass  # On Render.com, secrets come via env vars directly — that's fine

if not os.environ.get("GOOGLE_API_KEY"):
    st.error("⚠️ **GOOGLE_API_KEY not configured.** Add it as an Environment Variable on Render.com.")
    st.stop()

sys.path.insert(0, str(Path(__file__).parent))
from core.agent import run_agent
from database.db import init_db, seed_data, save_message, get_conversation_history

init_db()
seed_data()

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  #MainMenu, footer { visibility: hidden; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #1a3a5c 100%);
  }
  section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
    text-align: left !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 0.8rem !important;
    margin-bottom: 4px !important;
    transition: all 0.2s !important;
  }
  section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.15) !important;
    transform: translateX(3px) !important;
  }

  /* Hero banner */
  .hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1565C0 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }
  .hero-icon { font-size: 4rem; }
  .hero-text h1 { font-size: 2.2rem; font-weight: 800; margin: 0 0 0.3rem; }
  .hero-text p  { opacity: 0.85; margin: 0; font-size: 1rem; }

  /* Tool pills */
  .tool-pill {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    color: white;
    margin: 3px 2px;
  }

  /* Chat messages */
  .chat-user {
    background: linear-gradient(135deg, #1565C0, #1976D2);
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.2rem;
    color: white;
    margin: 0.5rem 0;
    max-width: 75%;
    margin-left: auto;
    box-shadow: 0 4px 12px rgba(21,101,192,0.25);
  }
  .chat-bot {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    max-width: 80%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    color: #1e293b;
  }

  /* Tool badge */
  .tool-badge {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px;
  }

  /* Stats */
  .stat-row {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  }
  .stat-row .n { font-size: 1.6rem; font-weight: 800; color: #1565C0; }
  .stat-row .l { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# Session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 BizPilot AI")
    st.markdown("*Business Automation Agent*")
    st.markdown("---")

    st.markdown("### 🛠 Available Tools")
    tools_info = [
        ("📦", "Inventory",      "Search products & stock levels"),
        ("✉️", "Email Drafter",  "Compose professional emails"),
        ("🧾", "PDF Invoices",   "Generate printable invoices"),
        ("💱", "Exchange Rates", "Live ETB currency conversion"),
        ("📊", "Sales Reports",  "Revenue trends & analytics"),
        ("👥", "Customers",      "Customer lookup & history"),
    ]
    for icon, name, desc in tools_info:
        st.markdown(f"**{icon} {name}**")
        st.caption(desc)

    st.markdown("---")
    st.markdown("### 💬 Quick Examples")
    examples = [
        "Show today's sales summary",
        "Which items are low on stock?",
        "Generate invoice for Abebe — 2 laptops",
        "USD to ETB exchange rate?",
        "Draft email to supplier about restock",
        "List our top customers",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex[:20]}", use_container_width=True):
            st.session_state.pending_message = ex
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    st.caption(f"Session: `{st.session_state.session_id[:8]}…`")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-icon">🤖</div>
  <div class="hero-text">
    <h1>BizPilot AI</h1>
    <p>Intelligent business automation agent. I can check inventory, draft emails,
       generate PDF invoices, look up exchange rates, and analyze your sales — all in one conversation.</p>
    <div style="margin-top:0.8rem">
      <span class="tool-pill">📦 Inventory</span>
      <span class="tool-pill">✉️ Email</span>
      <span class="tool-pill">🧾 Invoices</span>
      <span class="tool-pill">💱 FX Rates</span>
      <span class="tool-pill">📊 Sales</span>
      <span class="tool-pill">🔗 Tool Chaining</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Stats row
n_msgs = len(st.session_state.messages)
n_turns = n_msgs // 2
s1, s2, s3, s4 = st.columns(4)
for col, val, lbl in [
    (s1, "6", "Available Tools"),
    (s2, str(n_turns), "Conversation Turns"),
    (s3, "Gemini", "AI Model"),
    (s4, "100% Free", "API Cost"),
]:
    col.markdown(f"""<div class="stat-row">
      <div class="n">{val}</div><div class="l">{lbl}</div></div>""",
      unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🤖"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("tools_used"):
            badges = " ".join(
                f'<span class="tool-badge">🔧 {t["tool"]}</span>'
                for t in msg["tools_used"]
            )
            st.markdown(f"<small>Tools used: {badges}</small>", unsafe_allow_html=True)

# Pending from sidebar
pending = st.session_state.pop("pending_message", None)
prompt  = st.chat_input("Ask BizPilot anything about your business…")
if pending and not prompt:
    prompt = pending

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 Thinking and executing tools…"):
            history = [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.messages[:-1]]
            save_message(st.session_state.session_id, "user", prompt)
            result     = run_async(run_agent(user_input=prompt, chat_history=history))
            response   = result["output"]
            tools_used = result["tools_used"]
            save_message(st.session_state.session_id, "assistant", response,
                         tool_calls=str(tools_used) if tools_used else None)

        st.markdown(response)
        if tools_used:
            badges = " ".join(
                f'<span class="tool-badge">🔧 {t["tool"]}</span>'
                for t in tools_used
            )
            st.markdown(f"<small>Tools used: {badges}</small>", unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant", "content": response, "tools_used": tools_used,
    })
