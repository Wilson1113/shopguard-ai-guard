from schemas import CustomerInput
from temporalio import activity
from mcp_client import ShopMCPClient

@activity.defn
async def check_order_status_activity(order_id: str) -> str:
    """Check OrderStatus (simulate calling MCP)"""
    print(f"📦 Activity: Checking status for order {order_id}")
    mcp = ShopMCPClient()
    try:
        order = await mcp.get_order(order_id)
        return f"Order {order_id} status: {order.get('status', 'unknown')}"
    except Exception as e:
        return f"Failed to check order {order_id}: {str(e)}"


@activity.defn
async def notify_customer_activity(customer: CustomerInput) -> str:
    """Send Customer Notification"""
    print(f"📧 Activity: Notifying customer {customer.customer_id}")
    mcp = ShopMCPClient()
    try:
        result = await mcp.update_order_status("ORD-78492", "follow_up_sent")  # 示例
        return f"Notification sent to {customer.customer_id}: {customer.message}"
    except Exception as e:
        return f"Failed to notify customer: {str(e)}"