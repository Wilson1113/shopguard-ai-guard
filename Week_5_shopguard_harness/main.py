import asyncio
from graph import graph
from langchain_core.messages import HumanMessage
import uuid

async def run_demo():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    queries = [
        "Hi, my order #ORD-78492 hasn't arrived yet. Can you check the status?",
        "The item I received is damaged. I want to request a refund.",
        "What is my customer information?"
    ]

    for query in queries:
        print(f"\n👤 Customer: {query}")
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config
        )
        print(f"🤖 ShopGuard: {result['messages'][-1].content}")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(run_demo())