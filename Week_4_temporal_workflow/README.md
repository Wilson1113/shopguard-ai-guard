# Week 4: Temporal - Long-Running Reliable Workflows

**Part of**: AI Agent Harness Learning Journey (6-Week Program)

**Completed**: April 2026

## Overview

In Week 4, I integrated **Temporal** to enable long-running, reliable, and resumable workflows for the ShopGuard E-commerce Agent.

This allows the agent to handle tasks that span multiple days (e.g., order follow-ups, return processing, delayed shipment tracking) without losing state even if the server restarts.

## Key Features Implemented

- Temporal Workflow for multi-attempt order follow-up
- Reliable Activity execution with automatic retries
- Integration with existing MCP Server for real data access
- Graceful cancellation handling
- Dynamic Workflow ID generation to prevent conflicts
- Clear observability through Temporal Web UI

## Core Components

### Workflows
- `OrderFollowUpWorkflow`: Automatically checks order status multiple times and notifies the customer if needed.

### Activities
- `check_order_status_activity`: Checks order status via MCP
- `notify_customer_activity`: Sends notifications to customers

## Project Structure
```
Week-4-temporal-workflows/
├── main.py                 # Worker startup + demo
├── workflows.py            # Temporal Workflow definitions
├── activities.py           # Reusable activities
├── schemas.py              # Data models
├── requirements.txt
└── README.md

```


## How to Run

```bash
cd Week-4-temporal-workflows

# 1. Make sure Temporal Server is running
# (docker run ... or temporal server start-dev)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Worker + demo workflow
python main.py
