import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI

async def main():
    # 启动 MCP Client，连接 math_server.py
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["math_server.py"],
            }
        }
    )

    await client.start()

    # 获取 MCP 提供的工具
    tools = await client.get_tools()

    # 用 OpenAI ChatGPT 作为大模型
    llm = ChatOpenAI(model="gpt-4o-mini")  # 或者 "gpt-4o"

    # 创建 Agent
    agent = create_openai_functions_agent(llm=llm, tools=tools)

    # 让 Agent 执行任务（自动调用 MCP 工具）
    resp = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "请帮我算一下 123 + 456"}]}
    )

    print("🤖 Agent 回复：", resp)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
