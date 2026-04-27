async def supervisor_agent(state):
    last_message = state["messages"][-1].content.lower()

    if any(word in last_message for word in ["status", "arrived", "delay", "where", "track", "check"]):
        return {"next": "researcher"}
    elif any(word in last_message for word in ["refund", "damaged", "return", "replace"]):
        return {"next": "executor"}
    else:
        return {"next": "reviewer"}