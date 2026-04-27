from fastapi import FastAPI
from routers.chat import router as chat_router

app = FastAPI(
    title="ShopGuard AI Agent API",
    description="Production E-commerce AI Agent with Multi-Agent + MCP + Temporal",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "ShopGuard AI Agent is running!",
        "endpoints": ["/api/chat"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)