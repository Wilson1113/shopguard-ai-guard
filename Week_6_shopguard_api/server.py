from fastmcp import FastMCP
from datetime import datetime
from schemas import Order, Customer

# Simulating Database
fake_db = {
    "orders": {
        "ORD-78492": Order(
            order_id="ORD-78492",
            customer_id="customer_001",
            status="shipped",
            total_amount=129.99,
            created_at=datetime.now(),
            items=[{"name": "Wireless Headphones", "quantity": 1}]
        )
    },
    "customers": {
        "customer_001": Customer(
            customer_id="customer_001",
            name="Wilson Teo",
            email="studioyoung_@example.com",
            country="AU",
            preferences={"summary_style": "bullet_points"}
        )
    }
}

# Creating MCP Server
mcp = FastMCP("shop-mcp-server")

# ====================== Resources ======================
@mcp.resource("orders://{order_id}")
async def get_order(order_id: str) -> Order:
    """Get order details by ID"""
    print(f"🔍 Getting order {order_id}")
    if order_id in fake_db["orders"]:
        data = fake_db["orders"][order_id].model_dump()
        data["created_at"] = data["created_at"].isoformat()
        return data
    raise ValueError(f"Order {order_id} not found")

@mcp.resource("customers://{customer_id}")
async def get_customer(customer_id: str) -> Customer:
    """Get customer profile"""
    print(f"🔍 Getting customer {customer_id}")
    if customer_id in fake_db["customers"]:
        data = fake_db["customers"][customer_id].model_dump()
        return data
    raise ValueError(f"Customer {customer_id} not found")

# ====================== Tools ======================
@mcp.tool()
async def update_order_status(order_id: str, new_status: str) -> str:
    """Update order status"""
    print(f"🔍 Updating order {order_id} to {new_status}")
    if order_id in fake_db["orders"]:
        fake_db["orders"][order_id].status = new_status
        return f"✅ Order {order_id} status updated to '{new_status}'"
    return f"❌ Order {order_id} not found"

@mcp.tool()
async def notify_customer(customer_id: str, message: str) -> str:
    """Send notification to customer"""
    print(f"📧 Notification to {customer_id}: {message}")
    return f"✅ Notification sent to {customer_id}"

if __name__ == "__main__":
    print("🚀 Starting Shop MCP Server...")
    print("📡 Running on http://localhost:8000")
    print("This MCP server provides orders, customers, and tools for AI Agents.")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )

