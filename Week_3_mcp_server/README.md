# Week 3: MCP Server - Standardized Data Access Layer

**Part of**: AI Agent Harness Learning Journey (6-Week Program)

**Completed**: April 2026

## Overview

In Week 3, I built a **production-grade MCP (Model Context Protocol) Server** for the ShopGuard E-commerce Agent.

The goal was to move away from hard-coded data access and implement a standardized, secure, and discoverable way for AI Agents to interact with external data sources (orders, customers, inventory, etc.).

This MCP Server acts as the **data access layer** for the entire Agent Harness.

## Key Features

- Full MCP protocol compliance using **FastMCP**
- Resource-based data access (`orders://{order_id}`, `customers://{customer_id}`)
- Tool-based actions (`update_order_status`, `notify_customer`)
- Simulated Shopify-like database (easily replaceable with real API / PostgreSQL)
- Proper URI template handling (`://{param}` format)
- Clean separation of resources, tools, and server configuration

## Implemented Resources & Tools

### Resources (Read-only data)
- `orders://{order_id}` → Get detailed order information
- `customers://{customer_id}` → Get customer profile and preferences
- `inventory://{product_id}` → Get product stock level

### Tools (Actionable operations)
- `update_order_status` → Change order status (shipped → delivered, etc.)
- `notify_customer` → Send notification to customer

## Project Structure

```
Week-3-mcp-server/
├── main.py              # Server startup
├── server.py            # MCP Server definition + registration
├── schemas.py           # Pydantic data models (Order, Customer, etc.)
├── requirements.txt
└── README.md
```


## How to Run

```bash
cd Week-3-mcp-server

pip install -r requirements.txt

# Start the MCP Server
python main.py

# test the MCP Server
python test_client.py
```