from server import mcp

if __name__ == "__main__":
    print("🚀 Starting Shop MCP Server...")
    print("📡 Running on http://localhost:8000")
    print("This MCP server provides orders, customers, and tools for AI Agents.")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )

