# 🚀 BizPilot AI

**Intelligent Business Automation Agent**

An AI-powered agent that connects to real business tools and takes actions — checks inventory, drafts emails, generates PDF invoices, looks up exchange rates, and summarizes sales. Built with LangChain Agents and Google Gemini.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain_Agents-0.3-green?logo=chainlink)
![Gemini](https://img.shields.io/badge/Gemini_AI-2.0_Flash-orange?logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-red?logo=streamlit)

---

## ✨ What It Does

BizPilot AI is not a chatbot that just answers questions — it's an **agent that takes actions**. Tell it what you need in natural language, and it:

1. **Reasons** about which tools to use
2. **Plans** multi-step actions
3. **Executes** tools in sequence
4. **Combines** results into a clear response

### 🛠️ Agent Tools

| Tool | What It Does |
|------|-------------|
| 📦 **Inventory Checker** | Search products, check stock levels, get low-stock alerts from the database |
| 📧 **Email Drafter** | Compose professional business emails with customizable tone |
| 🧾 **Invoice Generator** | Create formatted PDF invoices with VAT calculation |
| 💱 **Exchange Rate** | Fetch real-time currency conversion rates via API |
| 📊 **Sales Analyzer** | Generate revenue reports, top products, category breakdowns, and daily trends |
| 👥 **Customer Manager** | Look up customer contact information |

---

## 🏗️ Architecture

```
User Request (natural language)
        ↓
   🧠 LLM Agent (Gemini)
        ↓
   Reasoning: "What tools do I need?"
        ↓
   ┌─────────────────────────────────┐
   │  Tool Selection & Execution     │
   │                                 │
   │  📦 check_inventory()          │
   │  📧 draft_email()              │
   │  🧾 generate_invoice()         │
   │  💱 get_exchange_rate()         │
   │  📊 summarize_sales()          │
   │  👥 list_customers()           │
   └─────────────────────────────────┘
        ↓
   Combine Results + Reasoning
        ↓
   Formatted Response to User
```

**Key difference from RAG:** This agent doesn't just retrieve information — it **reasons, selects tools, executes actions, and chains multiple steps together**.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key (free from [Google AI Studio](https://aistudio.google.com/apikey))

### Installation

```bash
git clone https://github.com/danipy2/bizpilot-ai.git
cd bizpilot-ai

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Run

```bash
# Streamlit UI (recommended)
streamlit run streamlit_app.py

# FastAPI backend only
python main.py
```

---

## 💬 Example Conversations

### Multi-Step Reasoning
> **You:** "Check if we have laptops in stock and generate an invoice for Abebe Kebede for 2 units"
>
> **BizPilot:** *Uses check_inventory → finds Laptop Dell at 45,000 ETB, 25 in stock → uses generate_invoice → creates PDF*
>
> "✅ We have 25 Dell Inspiron laptops in stock at 45,000 ETB each. I've generated invoice INV-20261027 for Abebe Kebede: 2 × Laptop Dell = 90,000 ETB + 13,500 VAT = 103,500 ETB total."

### Business Intelligence
> **You:** "Give me a sales summary and highlight any products we need to reorder"
>
> **BizPilot:** *Uses summarize_sales → get_low_stock_alerts → combines insights*

### Currency + Pricing
> **You:** "How much would 5 standing desks cost in USD?"
>
> **BizPilot:** *Uses check_inventory → get_exchange_rate → calculates*

---

## 📁 Project Structure

```
bizpilot-ai/
├── main.py                      # FastAPI entry point
├── streamlit_app.py             # Streamlit frontend
├── config.py                    # Configuration
├── requirements.txt
├── .env.example
│
├── core/
│   └── agent.py                 # LangChain Agent brain
│
├── tools/                       # Custom agent tools
│   ├── inventory_tool.py        # 📦 Stock & product search
│   ├── email_tool.py            # 📧 Email composition
│   ├── invoice_tool.py          # 🧾 PDF invoice generation
│   ├── exchange_rate_tool.py    # 💱 Currency conversion
│   └── sales_tool.py            # 📊 Sales analytics
│
├── api/
│   └── routes/
│       └── chat.py              # Agent chat endpoint
│
├── database/
│   └── db.py                    # SQLite + seed data
│
└── output/                      # Generated invoices
```

---

## 🔌 API

### POST `/api/chat`

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me the sales summary for this week", "session_id": "user-1"}'
```

**Response:**
```json
{
  "response": "📊 SALES SUMMARY — Last 7 Days\n...",
  "tools_used": [
    {"tool": "summarize_sales", "input": "{\"days\": 7}"}
  ],
  "session_id": "user-1"
}
```

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Framework** | LangChain Agents | Tool selection, multi-step reasoning |
| **LLM** | Google Gemini 2.0 Flash | Natural language understanding & generation |
| **Function Calling** | Gemini + LangChain Tools | Structured tool invocation |
| **Backend** | FastAPI | REST API |
| **Frontend** | Streamlit | Interactive chat UI |
| **Database** | SQLite | Business data (inventory, sales, customers) |
| **PDF Generation** | fpdf2 | Invoice creation |
| **HTTP Client** | httpx | External API calls (exchange rates) |

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

## 📄 License

MIT License
