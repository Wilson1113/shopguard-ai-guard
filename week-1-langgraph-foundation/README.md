# Week 1: LangGraph Foundations

**Course**: LangChain Academy - Introduction to LangGraph (Modules 1-6)

**Completed**: April 2026

## Overview

Completed the official LangChain Academy Introduction to LangGraph course (Modules 1-6). This week focused on building a solid understanding of LangGraph's core concepts and learning how to construct reliable, stateful AI Agent graphs.

## Key Learning Outcomes

### 1. State Management
- Defined structured States using **Pydantic `BaseModel`**
- Used **TypedDict + Annotated** with `operator.add` to implement message accumulation (reduce pattern)
- Worked with different State schemas for various use cases

### 2. Memory Systems
- **Short-term Memory**: Implemented using `Checkpointer` (`MemorySaver`) and `thread_id` for conversation persistence within the same session. Supports interruption and resumption.
- **Long-term Memory**: Used LangGraph `Store` (`InMemoryStore`) for cross-thread persistent storage.
  - Organized data with `namespace` and `key`
  - Implemented storing and retrieving user facts and preferences

### 3. Graph Construction
- Built graphs using `StateGraph`
- Created **Nodes** as executable functions
- Added **Edges** for linear flows
- Implemented **Conditional Edges** with Router functions for dynamic decision making
- Mastered the full graph assembly process: `add_node`, `add_edge`, `add_conditional_edges`, and `compile()`

### 4. Structured Output & Prompting
- Used `model.with_structured_output()` for reliable structured responses
- Properly handled dynamic content in prompts using `MessagesPlaceholder`
- Learned to avoid common prompt parsing issues with curly braces

### 5. Deployment Basics
- Understood how to compile and run LangGraph applications
- Explored different execution methods (`invoke`, `stream`, `astream_events`)

## Projects in This Folder

### 1. Research Assistant
- A functional research agent with Router and Tool Calling capabilities
- Supports dynamic routing (search vs summarize)
- Uses Checkpointer for conversation memory

### 2. Long-term Memory Demo
- Demonstrates the combination of Short-term Memory (Checkpointer) and Long-term Memory (Store)
- Agent can remember user preferences across different `thread_id`s
- Automatically extracts and saves new facts from conversations

## Tech Stack
- LangGraph
- LangChain
- Pydantic
- OpenRouter / Groq (free tier models)
- LangSmith (for tracing)

## Key Takeaways

- Developed a strong mental model of LangGraph as a state machine for building reliable AI Agents.
- Learned how to design persistent, recoverable, and observable Agent workflows.
- Built a solid foundation for developing production-grade AI Agent Harnesses in future weeks.

## Next Steps

- **Week 2**: Integrate LangSmith + Self-Correction mechanisms to build `ecommerce-agent-core`
- **Week 3**: Develop MCP Server for standardized data access
- **Final Goal**: Build an industrial-grade E-commerce AI Agent Harness (ShopGuard) within 6 weeks

---

### How to Run

```bash
cd Week-1-langgraph-foundations

pip install -r requirements.txt
```

Create .env file based on .env.example

```bash
# Run Research Assistant
python research_assistant.py

# Run Long-term Memory Demo
python long_term_memory_graph.py
```