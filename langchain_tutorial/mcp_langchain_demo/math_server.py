import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("math-server")

# 定义一个简单工具：加法
@server.tool()
async def add(a: int, b: int) -> int:
    """返回两个整数的和"""
    return a + b

async def main():
    async with stdio_server(server):
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
