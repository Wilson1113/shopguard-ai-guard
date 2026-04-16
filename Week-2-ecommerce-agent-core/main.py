from graph import graph
from langchain_core.messages import HumanMessage
import uuid

def run_demo():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    test_queries = [
        "Hi, my order #ORD-78492 hasn't arrived yet. Can you check the status?",
        "The item I received is damaged. I want to request a refund.",
        "Do you remember what I asked about earlier?"
    ]

    print("🛍️  ShopGuard E-commerce Agent Demo (Week 2)\n")
    
    for query in test_queries:
        print(f"👤 Customer: {query}")
        result = graph.invoke(
            {"messages": [HumanMessage(content=query)]},
            config
        )
        print(f"🤖 ShopGuard: {result['messages'][-1].content}")
        print("-" * 80)

if __name__ == "__main__":
    run_demo()