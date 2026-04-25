# Week 5: Full Multi-Agent Harness + Long-term Memory

**Part of**: AI Agent Harness Learning Journey (6-Week Program)

**Completed**: April 2026

## Overview

In Week 5, I upgraded ShopGuard from a single agent to a **full collaborative multi-agent system** with Long-term Memory integration.

This is the core of production-grade AI Agent Harness — multiple specialized agents working together under supervision, with persistent memory across conversations.

## Key Features

- **Multi-Agent Architecture**: Researcher + Executor + Reviewer + Supervisor
- **Hierarchical Routing**: Supervisor intelligently routes requests to the right agent
- **Long-term Memory**: LangGraph Store remembers user facts and preferences across sessions
- **MCP Integration**: All agents securely access real-time order and customer data
- **Temporal Triggering**: Executor can automatically start long-running workflows
- **Self-Correction**: Reviewer ensures final output quality and natural tone

## Agent Roles

- **Researcher Agent**: Gathers information from MCP and Long-term Store
- **Executor Agent**: Performs actions and triggers Temporal workflows
- **Reviewer Agent**: Polishes the final response for empathy, clarity, and style
- **Supervisor Agent**: Decides routing and coordinates the team

## Project Structure
```
Week-5-shopguard-harness/
├── main.py                 # Demo runner
├── graph.py                # Main LangGraph with conditional routing
├── agents.py               # Individual agent nodes
├── supervisor.py           # Routing logic
├── mcp_client.py           # MCP data access
├── temporal_client.py      # Temporal workflow triggering
├── store.py                # Long-term Memory (LangGraph Store)
├── prompts.py              # Shared prompts
├── requirements.txt
└── README.md

```


## Key Technical Achievements

- Successful collaboration between specialized agents
- Persistent Long-term Memory using LangGraph Store
- Seamless integration of MCP + Temporal
- Quality control through Reviewer Agent
- Dynamic routing based on user intent

## Demo Highlights

- Automatic routing (order status → Researcher, refund → Executor)
- Long-term Memory preserves user preferences
- Temporal Workflow triggered automatically for delayed orders
- Final responses are reviewed and polished

## How to Run

```bash
cd Week-5-shopguard-harness

# Ensure MCP Server and Temporal Server are running
python main.py