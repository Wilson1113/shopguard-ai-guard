import asyncio
from graph import graph
from langchain_core.messages import HumanMessage
import uuid

async def run_demo():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    test_queries = [
        "Hi, my order #ORD-78492 hasn't arrived yet. Can you check the status?",
        "The item I received is damaged. I want to request a refund.",
        "Do you remember my preferences? I like bullet points.",
        "What is my customer information?"
    ]

    print("🛍️  ShopGuard E-commerce Agent Demo (with MCP Integration)\n")
    print("=" * 80)

    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] 👤 Customer: {query}")
        
        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config
        )
        
        print(f"🤖 ShopGuard: {result['messages'][-1].content}")
        print("-" * 80)

    print("\n✅ Demo completed. Check above for MCP Success/Failed messages.")

if __name__ == "__main__":
    asyncio.run(run_demo())