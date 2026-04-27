from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import MessagesState
from agents import researcher_agent, executor_agent, reviewer_agent
from supervisor import supervisor_agent

def route_to_agent(state):
    """From supervisor, return state.get('next')  """
    return state.get("next", "reviewer")


workflow = StateGraph(MessagesState)

workflow.add_node("researcher", researcher_agent)
workflow.add_node("executor", executor_agent)
workflow.add_node("reviewer", reviewer_agent)
workflow.add_node("supervisor", supervisor_agent)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges("supervisor", route_to_agent)
workflow.add_edge("researcher", "reviewer")
workflow.add_edge("executor", "reviewer")
workflow.add_edge("reviewer", END)

graph = workflow.compile(checkpointer=MemorySaver())