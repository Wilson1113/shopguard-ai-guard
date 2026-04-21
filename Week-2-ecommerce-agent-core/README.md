# Week 2 + Week 3: E-commerce Agent Core with MCP Integration

**Part of**: AI Agent Harness Learning Journey (6-Week Program)

**Completed**: April 2026

## Overview

In Week 2 and Week 3, I built the core of **ShopGuard** — a production-ready E-commerce Customer Service Agent.

The focus was on moving from basic LangGraph to a more industrial-grade system by integrating:
- Full observability and self-correction with **LangSmith**
- Standardized data access through **MCP (Model Context Protocol)**
- Clean, modular architecture for maintainability

This project demonstrates how to build a reliable AI Agent that can securely fetch real customer and order data via MCP, while maintaining high response quality through self-correction.

## Key Features

- **LangSmith Integration**: Full tracing and custom evaluation for every agent run
- **Self-Correction Mechanism**: Automatically evaluates and improves low-quality responses (score < 0.85)
- **MCP Integration**: Agent communicates with external data sources through standardized MCP protocol
  - `get_customer()` — retrieves customer profile and preferences
  - `get_order()` — retrieves real-time order information
- **Professional Prompting**: Domain-specific system prompt for e-commerce customer service
- **Short-term Memory**: LangGraph Checkpointer with `thread_id`
- **Modular Design**: Clean separation of config, prompts, nodes, graph, and MCP client

## Demo Highlights

The agent can:
- Greet customers using their real name from MCP
- Respect user preferences (e.g., bullet points)
- Show empathy when handling issues (delayed orders, damaged items)
- Provide clear next steps and ask for confirmation
- Self-correct when response quality is insufficient

## Project Structure

```
Week-2-ecommerce-agent-core/
├── config.py          # LLM and LangSmith configuration
├── prompts.py         # Professional e-commerce system prompts
├── nodes.py           # Agent node with self-correction + MCP integration
├── graph.py           # LangGraph assembly
├── mcp_client.py      # MCP Client wrapper
├── main.py            # Async demo runner
├── requirements.txt
└── .env.example
```


## Technologies Used

- **LangGraph** — Core stateful agent framework
- **LangSmith** — Production observability and evaluation
- **FastMCP** — Standardized Model Context Protocol for data access
- **Pydantic** — Structured data handling
- **OpenRouter** — LLM access (free tier)

## Key Learnings

- How to integrate external data sources securely using MCP protocol
- Building reliable self-correction loops with structured evaluation
- Designing modular agent architecture for scalability
- Using async patterns with LangGraph for MCP calls

## Next Steps

- Week 4: Implement Temporal for long-running workflows (e.g., multi-day order follow-ups)
- Week 5: Full multi-agent harness + Long-term Memory (Store)
- Week 6: FastAPI deployment + complete ShopGuard portfolio project

---

**How to Run Demo**

```bash
cd Week-2-ecommerce-agent-core

# 1. Start MCP Server (in another terminal)
cd ../Week-3-mcp-server
python main.py

# 2. Run the Agent
cd ../Week-2-ecommerce-agent-core
python main.py