# remote_server.py
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response

# 1. 创建 MCP Server 实例
server = Server("RemoteDemoServer")

# 2. 定义工具 (和之前一样)
@server.list_tools()
async def handle_list_tools():
    from mcp.types import Tool
    return [
        Tool(
            name="add_numbers",
            description="Add two numbers together.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_weather",
            description="Get weather for a city.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "add_numbers":
        return [
            {"type": "text", "text": str(arguments["a"] + arguments["b"])}
        ]
    elif name == "get_weather":
        city = arguments.get("city", "Unknown")
        return [
            {"type": "text", "text": f"The weather in {city} is Sunny, 28°C (Remote Data)"}
        ]
    raise ValueError(f"Unknown tool: {name}")

# 3. 配置 SSE 传输 (Web 接口)
sse = SseServerTransport("/messages") # 定义接收 POST 消息的端点

async def handle_sse(request):
    """处理 SSE 连接建立 (GET /sse)"""
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

async def handle_messages(request):
    """处理客户端发送的消息 (POST /messages)"""
    await sse.handle_post_message(request.scope, request.receive, request._send)

# 4. 启动 Starlette Web 应用
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),        # 建立连接通道
        Route("/messages", endpoint=handle_messages, methods=["POST"]) # 接收指令
    ]
)

if __name__ == "__main__":
    # 运行在 8000 端口
    print("🚀 Starting Remote MCP Server on http://0.0.0.0:8000 ...")
    uvicorn.run(app, host="0.0.0.0", port=8000)