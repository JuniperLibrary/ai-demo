# main_remote_mcp.py
import asyncio
import os
import json
import dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function

# 关键修改：导入 sse_client
from mcp.client.sse import sse_client
from mcp import ClientSession

dotenv.load_dotenv()


# --- 1. 依然使用同一个 Bridge Plugin (复用代码) ---
class McpBridgePlugin:
    def __init__(self, session: ClientSession):
        self.session = session

    @kernel_function(description="调用外部 MCP 工具执行任务", name="call_mcp_tool")
    async def call_mcp_tool(self, tool_name: str, arguments_json: str) -> str:
        print(f"    [🌉 Remote Bridge] 转发 -> {tool_name} args={arguments_json}")
        try:
            args = json.loads(arguments_json) if isinstance(arguments_json, str) else arguments_json
            result = await self.session.call_tool(tool_name, arguments=args)
            output_text = result.content[0].text
            print(f"    [✅ Remote 响应] {output_text}")
            return output_text
        except Exception as e:
            return f"Error: {str(e)}"


# --- 2. 主逻辑 ---
async def main():
    # 定义远程 MCP Server 的地址 (对应 server 代码里的 /sse 路由)
    remote_server_url = "http://localhost:8000/sse"

    print(f">>> 正在连接远程服务器: {remote_server_url} ...")

    # 关键修改：使用 sse_client 连接 HTTP URL
    async with sse_client(remote_server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 动态获取远程工具列表
            tools_response = await session.list_tools()
            mcp_tools = tools_response.tools

            tools_desc = []
            for t in mcp_tools:
                tools_desc.append(f"- Tool: {t.name}\n  Desc: {t.description}\n  Schema: {t.inputSchema}")
            system_prompt_tools = "\n".join(tools_desc)

            print(f">>> 成功连接！发现 {len(mcp_tools)} 个远程工具。")

            # --- 以下 SK 逻辑与本地版完全一致 ---
            kernel = Kernel()
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id="default",
                    ai_model_id="gpt-4o-mini",
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
            )

            # 注册插件
            kernel.add_plugin(McpBridgePlugin(session), plugin_name="McpTools")

            system_prompt = f"""
            你可以使用远程服务器上的工具。
            可用工具列表：
            {system_prompt_tools}

            如果要调用，请使用 `McpTools-call_mcp_tool`，传入工具名和 JSON 参数。
            """

            settings = OpenAIChatPromptExecutionSettings(
                service_id="default",
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )

            chat_service = kernel.get_service("default")
            history = ChatHistory()
            history.add_system_message(system_prompt)

            # 测试指令
            user_input = "Remote Server 你好，帮我算一下 88 加 22，然后查一下 Shenzhen 的天气。"
            print(f"\n[用户]: {user_input}")
            history.add_user_message(user_input)

            result = await chat_service.get_chat_message_contents(
                chat_history=history,
                settings=settings,
                kernel=kernel
            )

            print("\n" + "=" * 50)
            print(f"[AI 回答]: {result[0]}")
            print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())