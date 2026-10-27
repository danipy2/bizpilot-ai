# 🧠 BizPilot AI — AI-Powered Business Operations Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.x-1C3C3C?logo=langchain)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-8E75B2?logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)

---

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-0ea5e9)](https://bizpilot-ai.onrender.com)

---

## 📌 Description

**BizPilot AI** is an AI-powered business operations assistant built with LangChain and Google Gemini. It provides a smart agent equipped with **6 specialized tools** designed to help small and medium enterprises (SMEs) in Ethiopia streamline daily operations — from managing stock to generating invoices — all through a conversational interface.

---

## 🧰 Tools & Capabilities

- 📦 **Inventory Management** — Track stock levels, add/update products, and get low-stock alerts
- ✉️ **Email Drafting** — Generate professional business emails from a short prompt
- 🧾 **Invoice Generation** — Create and export PDF invoices for clients instantly
- 💱 **Exchange Rate Lookup** — Fetch live currency exchange rates for financial planning
- 📈 **Sales Analytics** — Visualize and summarize sales trends, top products, and revenue insights
- 🤖 **Conversational Business Assistant** — Ask any business question and get AI-powered guidance

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11** | Core language |
| **LangChain** | Agent framework & tool orchestration |
| **Google Gemini** | Large language model (LLM) backend |
| **FastAPI** | Backend API layer |
| **Streamlit** | Web application frontend |
| **SQLite** | Lightweight local database |
| **fpdf2** | PDF invoice generation |
| **Render** | Cloud deployment platform |

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> Get your key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/danipy2/bizpilot-ai.git
cd bizpilot-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your environment variable
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 4. Launch the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
bizpilot-ai/
├── streamlit_app.py       # Main application entry point
├── pages/                 # Multi-page Streamlit views
│   ├── inventory.py       # Inventory management UI
│   ├── invoice.py         # Invoice generation UI
│   └── analytics.py       # Sales analytics dashboard
├── core/                  # Agent & tools logic
│   ├── agent.py           # LangChain agent setup
│   └── tools/             # Individual tool implementations
├── data/                  # SQLite database files
├── config.py              # App-wide configuration constants
└── requirements.txt       # Python dependencies
```

---

## 👤 Author

**Daniel Molla**  
GitHub: [@danipy2](https://github.com/danipy2)
