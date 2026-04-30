from fastapi import APIRouter
from schemas import ChatRequest, ChatResponse
from graph import graph
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id or "default"}}

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=request.message)]},
        config
    )

    return ChatResponse(
        response=result["messages"][-1].content
    )