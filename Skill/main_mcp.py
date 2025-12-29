# main_mcp.py
import asyncio
import os
import json
import dotenv
import sys

# Semantic Kernel 导入
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function

# MCP 导入
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

dotenv.load_dotenv()


# ==============================================================================
# 核心：定义 MCP 桥接插件 (Adapter)
# ==============================================================================
class McpBridgePlugin:
    """
    这个插件充当 Semantic Kernel 和 MCP Server 之间的桥梁。
    """

    def __init__(self, session: ClientSession):
        self.session = session

    @kernel_function(description="调用外部 MCP 工具执行任务", name="call_mcp_tool")
    async def call_mcp_tool(self, tool_name: str, arguments_json: str) -> str:
        """
        通用路由函数：LLM 会把工具名和参数传给这个函数，然后转发给 MCP。
        """
        print(f"    [🌉 MCP Bridge] 正在转发请求 -> 工具: {tool_name}, 参数: {arguments_json}")

        try:
            # 解析参数 (LLM 有时给的是 JSON 字符串)
            args = json.loads(arguments_json) if isinstance(arguments_json, str) else arguments_json

            # --- 真正的 MCP 调用发生在这里 ---
            result = await self.session.call_tool(tool_name, arguments=args)

            # MCP 返回的是一个对象，我们需要提取文本内容
            output_text = result.content[0].text
            print(f"    [✅ MCP 响应] {output_text}")
            return output_text

        except Exception as e:
            error_msg = f"调用 MCP 工具失败: {str(e)}"
            print(f"    [❌ Error] {error_msg}")
            return error_msg


# ==============================================================================
# 主逻辑
# ==============================================================================
async def main():
    # 1. 配置 MCP 服务器连接参数 (连接到我们刚才写的 myserver.py)
    server_params = StdioServerParameters(
        command="python",  # 使用 python 运行
        args=["myserver.py"],  # 脚本路径
        env=None
    )

    print(">>> 正在连接 MCP 服务器...")

    # 2. 建立 MCP 连接上下文
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化 MCP 会话
            await session.initialize()

            # --- 关键步骤：动态获取 MCP 工具列表 ---
            # 我们需要知道服务器上有哪些工具，以便告诉 LLM
            tools_response = await session.list_tools()
            mcp_tools = tools_response.tools

            # 构建工具描述字符串 (System Prompt)
            # 因为我们用的是“路由模式”，LLM 需要知道有哪些工具名和参数结构可用
            tools_desc = []
            for t in mcp_tools:
                tools_desc.append(f"- 工具名: {t.name}\n  描述: {t.description}\n  参数Schema: {t.inputSchema}")

            system_prompt_tools = "\n".join(tools_desc)
            print(f">>> 发现 {len(mcp_tools)} 个 MCP 工具:\n{system_prompt_tools}")

            # --------------------------------------------------------
            # 开始 Semantic Kernel 流程
            # --------------------------------------------------------
            kernel = Kernel()

            # 配置 AI 服务
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id="default",
                    ai_model_id="gpt-4o-mini",
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
            )

            # 3. 注册我们的桥接插件 (注入 session)
            kernel.add_plugin(McpBridgePlugin(session), plugin_name="McpTools")

            # 4. 构建 System Prompt
            # 我们必须明确告诉 LLM：如果想用这些工具，请调用 McpTools-call_mcp_tool
            system_prompt = f"""
            你是一个拥有 MCP 工具扩展能力的助手。
            你可以使用的外部工具如下：
            {system_prompt_tools}

            **重要指令**：
            如果你需要使用上述任何工具，请务必调用插件 `McpTools` 中的 `call_mcp_tool` 函数。
            - `tool_name` 填入上面列表中的工具名。
            - `arguments_json` 填入符合 Schema 的 JSON 字符串。
            """

            # 5. 配置自动调用
            settings = OpenAIChatPromptExecutionSettings(
                service_id="default",
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )

            chat_service = kernel.get_service("default")
            history = ChatHistory()
            history.add_system_message(system_prompt)

            # --- 测试任务 ---
            user_input = "你好，请帮我查询一下 Shanghai 的天气，顺便算一下 123 加 456 等于多少？"
            print(f"\n[用户]: {user_input}")
            history.add_user_message(user_input)

            # 执行
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