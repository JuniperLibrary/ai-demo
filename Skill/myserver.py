# myserver.py
from mcp.server.fastmcp import FastMCP

# 初始化一个名为 "DemoServer" 的 MCP 服务器
mcp = FastMCP("DemoServer")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the weather of a specific city."""
    if "Beijing" in city:
        return "Sunny, 25°C"
    elif "Shanghai" in city:
        return "Rainy, 20°C"
    else:
        return "Unknown weather"

if __name__ == "__main__":
    # 使用 stdio 模式运行，这是 MCP 的标准通信方式
    mcp.run(transport='stdio')