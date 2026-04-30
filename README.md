# AI Agent Harness 2026 - ShopGuard E-commerce Agent

**From LangGraph Foundations to Production-Ready AI Agent in 6 Weeks**

Built by Wilson Teo | CS Bachelor | Focused on Reliable, Observable, and Deployable AI Agents.

---

## Project Goal

To build **ShopGuard** — a production-grade AI Agent Harness specialized for E-commerce customer service and operations, using modern 2026 best practices.

Instead of simple prompt-based agents, I focused on **Harness Engineering**: making agents reliable, persistent, observable, and secure enough for real business use.

---

## Final Capabilities

- **MCP Integration**: Secure, standardized data access to orders and customer profiles
- **Self-Correction**: Automatic evaluation and regeneration of low-quality responses
- **Long-term Memory**: Remembers user preferences across conversations
- **Temporal Workflows**: Handles long-running tasks (e.g., multi-day order follow-ups)
- **Production Observability**: Full tracing with LangSmith
- **Natural Conversation**: Warm, empathetic, and professional tone

---

## 6-Week Learning Journey

| Week | Focus                              | Key Technologies                     | Status |
|------|------------------------------------|--------------------------------------|--------|
| 1    | LangGraph Foundations              | State, Nodes, Edges, Router, Memory  | Completed |
| 2    | Production Core + Self-Correction  | LangSmith, Evaluation, MCP Client    | Completed |
| 3    | Standardized Data Layer            | FastMCP Server (Resources & Tools)   | Completed |
| 4    | Long-running Reliable Workflows    | Temporal Python SDK                  | Completed |
| 5    | Full Multi-Agent Harness           | Long-term Store + Guardrails         | Completed |
| 6    | Deployment & Portfolio             | FastAPI + Vercel                     | Completed |

---

## Tech Stack

- **Core Framework**: LangGraph
- **Observability**: LangSmith
- **Data Protocol**: FastMCP (Model Context Protocol)
- **Long-running Tasks**: Temporal
- **Memory**: Checkpointer (short-term) + Store (long-term)
- **LLM**: OpenRouter / Groq (free tier)
- **Deployment**: FastAPI

---

## Demo Highlights

- **Real-time customer and order data fetching via MCP** (Resources)
- **Automatic self-correction when response quality is low** (Self-Correction)
- **Triggering of long-running Temporal workflows from normal chat** (Workflows)
- **Natural conversation with user name and preference awareness** (Memory & LLM)

## Demo Guide

0. **Install dependencies and Setup .env file**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Then edit .env with your actual values (OpenRouter API key, etc)
   ```

1. **Start Temporal Server**  
   Download the Temporal CLI from: [https://temporal.io/setup/install-temporal-cli](https://temporal.io/setup/install-temporal-cli)  
   Then start the Temporal server with:
   ```bash
   temporal server start-dev
    ```

2. **Start the Worker**  
   Open a new terminal, go to the Week-6-shopguard-api directory, and run:
   ```bash
   python worker.py
   ```

3. **Start the MCP Server**  
   Open a new terminal, go to the Week-6-shopguard-api directory, and run:
   ```bash
   python server.py
   ```
   
4. **Start the API**  
   Open a new terminal, go to the Week-6-shopguard-api directory, and run:
   ```bash
   python main.py
   ```
   
5. **Send Query**  
   Open a new terminal, go to the Week-6-shopguard-api directory, and run:
   ```bash
    curl -X POST http://localhost:8001/api/chat \
    -H "Content-Type: application/json" \
    -d '{
        "message": "Hi, my order #ORD-78492 has not arrived yet. Can you check the status?",
        "thread_id": "test-001"
    }'

    curl -X POST http://localhost:8001/api/chat \
    -H "Content-Type: application/json" \
    -d '{
        "message": "The item I received is damaged. I want to request a refund.",
        "thread_id": "test-001"
    }'
    ```
6. **View the workflow graph**
    Open a new terminal, go to the Week-6-shopguard-api directory, and run:
    ```bash
    python graph.py
    ```
**Demo Video**: [https://www.loom.com/share/1e2dc830a24b44ec9304e495dc57160f]

---

## Repository Structure

- `Week-1-langgraph-foundations/` – LangGraph Academy completion
- `Week-2-ecommerce-agent-core/` – Core Agent with LangSmith + MCP
- `Week-3-mcp-server/` – Standardized data access server
- `Week-4-temporal-workflows/` – Long-running order follow-up workflows
- `Week-5-shopguard-harness/` – Full multi-agent system
- `Week-6-shopguard-api/` – Production deployment

---

## Key Learnings

- How to build reliable **Agent Harnesses** rather than simple agents
- Production observability and self-improvement mechanisms
- Standardized tool/data access using MCP
- Long-running reliable workflows with Temporal
- Vertical specialization (E-commerce) for real business value

## Future Roadmap

- Deploy as SaaS for Shopify merchants
- Add more tools (inventory check, return label generation, etc.)
- Open to freelance and collaboration opportunities

---

**Status**: Actively building production-grade AI Agent systems with focus on E-commerce.

Open to freelance projects, especially Shopify / E-commerce automation using LangGraph + MCP + Temporal.

Feel free to reach out for discussions or live demos.

---

**Teo Shi Yang**  
CS Bachelor | AI Agent Engineer  
Email: [wilsonteoshiyang@gmail.com]  
LinkedIn: [https://www.linkedin.com/in/shi-yang-teo-997671222/] | GitHub: [[this-repo](https://github.com/Wilson1113/shopguard-ai-guard)]

Last updated: April 2026