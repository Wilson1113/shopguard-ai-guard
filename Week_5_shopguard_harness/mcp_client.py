# mcp_client.py
from fastmcp import Client
from typing import Dict, Any
import json

class ShopMCPClient:
    """MCP Client"""

    def __init__(self, base_url: str = "http://localhost:8000/mcp"):
        self.base_url = base_url

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """get_order"""
        async with Client(self.base_url ) as client:
            try:
                result = await client.read_resource(f"orders://{order_id}")
                
                # 处理 FastMCP 返回的复杂结构 (list + TextResourceContents)
                if isinstance(result, list) and result:
                    item = result[0]
                    if hasattr(item, "text") and item.text:
                        data = json.loads(item.text)
                    else:
                        data = item
                else:
                    data = result

                print(f"✅ MCP get_order success: {order_id}")
                print(f"   Data: {data}")
                return data
            except Exception as e:
                print(f"❌ MCP get_order failed: {e}")
                return {}

    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """get_customer"""
        async with Client(self.base_url) as client:
            try:
                result = await client.read_resource(f"customers://{customer_id}")
                
                if isinstance(result, list) and result:
                    item = result[0]
                    if hasattr(item, "text") and item.text:
                        data = json.loads(item.text)
                    else:
                        data = item
                else:
                    data = result

                print(f"✅ MCP get_customer success: {customer_id}")
                print(f"   Data: {data}")
                return data
            except Exception as e:
                print(f"❌ MCP get_customer failed: {e}")
                return {}

    async def update_order_status(self, order_id: str, new_status: str) -> Dict[str, Any]:
        """update_order_status"""
        async with Client(self.base_url) as client:
            try:
                result = await client.call_tool(
                    name="update_order_status",
                    arguments={"order_id": order_id, "new_status": new_status}
                )
                print(f"✅ MCP update_order_status success: {order_id} -> {new_status}")
                return result
            except Exception as e:
                print(f"❌ MCP update_order_status failed: {e}")
                return {}