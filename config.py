"""
BizPilot AI — Configuration
Centralised settings for the business automation agent.
Supports both local .env and Streamlit Cloud secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Load Streamlit Cloud secrets if available ---
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        if "GOOGLE_API_KEY" in st.secrets:
            os.environ.setdefault("GOOGLE_API_KEY", st.secrets["GOOGLE_API_KEY"])
        if "EXCHANGE_RATE_API_KEY" in st.secrets:
            os.environ.setdefault("EXCHANGE_RATE_API_KEY", st.secrets["EXCHANGE_RATE_API_KEY"])
except Exception:
    pass  # Not running inside Streamlit, that's fine

# --- Paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = DATA_DIR / "bizpilot.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- API Keys ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "")

# --- Model Configuration ---
LLM_MODEL = "gemini-2.0-flash"
LLM_TEMPERATURE = 0.2  # Lower for more deterministic tool use

# --- Agent Configuration ---
MAX_ITERATIONS = 10  # Max reasoning steps per query
VERBOSE_AGENT = True  # Show agent reasoning in logs
