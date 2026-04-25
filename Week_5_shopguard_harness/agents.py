from langchain_core.messages import AIMessage
from mcp_client import ShopMCPClient
from temporal_client import TemporalClient
from config import llm
from store import get_facts, save_fact

async def researcher_agent(state):
    """Researcher Agent: Focus on collecting information."""
    user_id = "customer_001"
    
    # 获取 Long-term Memory
    long_term = get_facts(user_id)
    long_term_str = "\n".join([f"- {k}: {v}" for k, v in long_term.items()]) or "No previous facts."

    mcp = ShopMCPClient()
    try:
        customer = await mcp.get_customer(user_id)
        order = await mcp.get_order("ORD-78492")
        
        save_fact(user_id, "last_interaction", "order_status_inquiry")
        save_fact(user_id, "name", customer.get("name"))
        
        return {
            "messages": [AIMessage(content=f"""
Researcher Report:
Customer: {customer.get('name')}
Order Status: {order.get('status')}
Long-term Facts: {long_term_str}
Preferences: {customer.get('preferences')}
""")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Research failed: {e}")]}


async def executor_agent(state):
    """Executor Agent: Execute actual operations"""
    temporal = TemporalClient()
    try:
        await temporal.trigger_order_followup("ORD-78492", "customer_001")
        return {"messages": [AIMessage(content="✅ I have triggered the long-term follow-up workflow for your order.")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Execution failed: {e}")]}


async def reviewer_agent(state):
    """Reviewer Agent: Check the final reply quality."""
    last_message = state["messages"][-1].content

    user_id = "customer_001"

    save_fact(user_id, "last_topic", "customer_inquiry")

    review_prompt = f"""You are ShopGuard, a warm, empathetic, and decisive customer service agent.

Turn the following internal information into a natural, confident, and helpful reply to the customer.

Internal Information:
{last_message}

Rules:
- Be warm and empathetic without overdoing "sorry"
- Be proactive and decisive (give clear next steps)
- Use the customer's name (Wilson) naturally
- Use bullet points only when it truly helps clarity
- Keep the response concise and action-oriented
- Never ask too many questions — give options but lead the conversation
- Sound like a real helpful person, not a script

Final Reply to Customer:"""

    final_response = llm.invoke(review_prompt).content.strip()

    return {"messages": [AIMessage(content=final_response)]}