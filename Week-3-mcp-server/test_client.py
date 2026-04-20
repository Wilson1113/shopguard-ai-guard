import asyncio
from fastmcp import Client
from pprint import pprint

async def test_mcp_server():
    # 连接到你的 MCP Server
    async with Client("http://localhost:8000/mcp") as client:
        
        print("✅ Connected to MCP Server")
        
        # 1. 先测试 list_tools
        print("\n📋 Listing available tools...")
        tools = await client.list_tools()
        pprint(tools)
        
        # 2. 测试调用工具（以 update_order_status 为例）
        print("\n🔧 Calling update_order_status tool...")
        result = await client.call_tool(
            name="update_order_status",
            arguments={
                "order_id": "ORD-78492",
                "new_status": "delivered"
            }
        )
        pprint(result)

        # 3. 测试读取资源 (使用 orders:// 协议)
        print("\n📦 Reading order resource...")
        order = await client.read_resource("orders://ORD-78492")
        pprint(order)

async def main():
    try:
        await test_mcp_server()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())