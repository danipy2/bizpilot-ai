"""
BizPilot AI — FastAPI Application
REST API for the business automation agent.
"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat
from database.db import init_db, seed_data

# Initialize
init_db()
seed_data()

app = FastAPI(
    title="BizPilot AI",
    description=(
        "Intelligent Business Automation Agent — "
        "An AI agent that connects to business tools and takes actions: "
        "inventory management, email drafting, invoice generation, "
        "exchange rates, and sales analytics."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")


@app.get("/", tags=["Health"])
async def root():
    return {"app": "BizPilot AI", "docs": "/docs", "status": "running"}


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
