# Week-2-ecommerce-agent-core/mcp_client.py
from typing import Any, Dict
import asyncio
from fastmcp import Client
from typing import Optional
import json

class ShopMCPClient:
    def __init__(self, base_url: str = "http://localhost:8000/mcp"):
        self.base_url = base_url
        self.client = None

    async def __aenter__(self):
        self.client = Client(self.base_url)
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        async with self.client as client:
            try:
                result = await client.read_resource(f"orders://{order_id}")
                
                # 处理 FastMCP 返回的复杂结构
                if isinstance(result, list) and result:
                    item = result[0]
                    if hasattr(item, 'text'):
                        data = json.loads(item.text)      # 把 text 里的 JSON 字符串解析成 dict
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
        async with self.client as client:
            try:
                result = await client.read_resource(f"customers://{customer_id}")
                
                # 处理 FastMCP 返回的 TextResourceContents
                if isinstance(result, list) and result:
                    item = result[0]
                    if hasattr(item, 'text'):
                        data = json.loads(item.text)      # 关键：解析 text 字段
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

