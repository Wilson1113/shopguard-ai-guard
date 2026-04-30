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
workflow.add_conditional_edges("supervisor", route_to_agent, ["researcher", "executor", "reviewer"])
workflow.add_edge("researcher", "reviewer")
workflow.add_edge("executor", "reviewer")
workflow.add_edge("reviewer", END)

graph = workflow.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    try:
        # Attempt to save as PNG (requires pygraphviz or similar)
        graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
        print("✅ Graph image saved to Week_6_shopguard_api/graph.png")
    except Exception:
        # Fallback: Save as Mermaid text (can be pasted into mermaid.live)
        with open("graph.mermaid", "w") as f:
            f.write(graph.get_graph().draw_mermaid())
        print("✅ Could not generate PNG. Graph saved as Mermaid text to Week_6_shopguard_api/graph.mermaid")
        print("👉 You can paste the content of graph.mermaid into https://mermaid.live to see the diagram.")