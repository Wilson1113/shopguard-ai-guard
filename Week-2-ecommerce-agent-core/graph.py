from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from nodes import agent_node
from langgraph.graph import MessagesState

workflow = StateGraph(MessagesState)

workflow.add_node("agent", agent_node)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Short-term Memory
checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)