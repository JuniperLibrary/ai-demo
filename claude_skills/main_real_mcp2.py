import asyncio
import os
import json
import dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function

# MCP 客户端依赖
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

dotenv.load_dotenv()


# ==============================================================================
# 通用适配器 (完全复用，不用改)
# ==============================================================================
class McpBridgePlugin:
    def __init__(self, session: ClientSession):
        self.session = session

    @kernel_function(description="调用外部 MCP 工具执行任务", name="call_mcp_tool")
    async def call_mcp_tool(self, tool_name: str, arguments_json: str) -> str:
        print(f"    [🌉 Bridge] 转发 -> {tool_name} args={arguments_json}")
        try:
            # 兼容处理：LLM 有时会直接传 dict，有时传 json string
            args = json.loads(arguments_json) if isinstance(arguments_json, str) else arguments_json

            result = await self.session.call_tool(tool_name, arguments=args)

            # 提取结果文本
            if result.content and len(result.content) > 0:
                output_text = result.content[0].text
                print(f"    [✅ MCP 响应] {output_text[:100]}...")  # 只打印前100个字符避免刷屏
                return output_text
            return "Success (No content returned)"

        except Exception as e:
            return f"Error calling tool: {str(e)}"


# ==============================================================================
# 主程序
# ==============================================================================
async def main():
    # 1. 设置允许 Agent 访问的本地目录 (请修改为你自己的真实路径)
    # 例如 Mac: "/Users/yourname/Documents/test_mcp"
    # 例如 Win: "C:\\Users\\yourname\\Documents\\test_mcp"
    allowed_path = os.path.abspath("./test_mcp_folder")

    # 确保目录存在
    if not os.path.exists(allowed_path):
        os.makedirs(allowed_path)

    print(f">>> 目标挂载目录: {allowed_path}")

    # 2. 配置连接参数：连接官方 Filesystem Server
    # 修改 main_real_mcp.py 中的 server_params
    server_params = StdioServerParameters(
        command="npx",  # <--- 改为 npx (Node.js 运行器)
        args=[
            "-y",  # <--- 自动安装，不询问
            "@modelcontextprotocol/server-filesystem",
            allowed_path
        ]
    )

    print(">>> 正在启动并连接官方 MCP Filesystem Server (这可能需要几秒钟下载)...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. 获取工具列表 (看看官方 Server 提供了什么)
            tools_response = await session.list_tools()
            mcp_tools = tools_response.tools

            tools_desc = []
            for t in mcp_tools:
                # 简化 Schema 描述以节省 Token
                tools_desc.append(f"- {t.name}: {t.description}")

            system_prompt_tools = "\n".join(tools_desc)
            print(f">>> 连接成功！获取到以下真实工具:\n{system_prompt_tools}")

            # --- SK 初始化流程 ---
            kernel = Kernel()
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id="default",
                    ai_model_id="gpt-4o-mini",
                    api_key=os.getenv("OPENAI_API_KEY"),
                )
            )

            # 注册桥接插件
            kernel.add_plugin(McpBridgePlugin(session), plugin_name="McpTools")

            # 构建 System Prompt
            system_prompt = f"""
            你连接到了一个本地文件系统。
            你可以使用的工具如下：
            {system_prompt_tools}

            如果要操作文件，请调用 `McpTools-call_mcp_tool`。
            务必严格遵循工具的参数结构。
            """

            settings = OpenAIChatPromptExecutionSettings(
                service_id="default",
                function_choice_behavior=FunctionChoiceBehavior.Auto()
            )

            chat_service = kernel.get_service("default")
            history = ChatHistory()
            history.add_system_message(system_prompt)

            # --- 真实任务测试 ---
            # 让 AI 创建一个 Python 脚本，然后读取它
            user_input = "请在当前目录下创建一个名为 'hello_mcp.py' 的文件，内容是打印一句 'Hello from Real MCP!'。创建完成后，请读取这个文件确认内容。"

            print(f"\n[用户]: {user_input}")
            history.add_user_message(user_input)

            try:
                result = await chat_service.get_chat_message_contents(
                    chat_history=history,
                    settings=settings,
                    kernel=kernel
                )
                print("\n" + "=" * 50)
                print(f"[AI 回答]: {result[0]}")
                print("=" * 50)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())