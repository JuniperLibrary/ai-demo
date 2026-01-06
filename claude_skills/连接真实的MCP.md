使用“真实”的 MCP 服务器（Official Reference Servers）意味着你的 Agent 将不再连接我们写的那个假 Python 脚本，而是连接由 Anthropic 或社区维护的**生产级服务器**。

最经典、最容易上手的真实案例是 **Filesystem MCP Server（文件系统服务器）**。
连接上它之后，你的 Agent 就真正拥有了**操作你电脑本地文件**的能力（读取目录、写文件、读取文件）。

### 前置准备

绝大多数官方 MCP Server 都是通过 `uv` (Python 极速包管理器) 分发的。你需要先安装它：

```bash
pip install uv
```

安装完成后，确保 `uvx` 命令可用（通常安装 `uv` 后会自动包含 `uvx`）。可以在终端输入 `uvx --version` 测试一下。

---

### 实战：连接官方 Filesystem MCP Server

我们将修改之前的代码，让 SK 连接到官方的文件系统服务，并让 Agent 在你的电脑上写一个文件。

#### 1. 确定工作目录
为了安全，我们只允许 Agent 访问你电脑上的某一个特定文件夹，例如 `test_mcp_folder`。
请在你的项目根目录下手动创建一个文件夹：`test_mcp_folder`。

#### 2. 修改代码 (`main_real_mcp.py`)

代码逻辑和之前连接本地 Mock Server **完全一样**，唯一的区别是启动参数 `StdioServerParameters` 变了。

```python
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
                print(f"    [✅ MCP 响应] {output_text[:100]}...") # 只打印前100个字符避免刷屏
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
    # 我们使用 `uvx` 命令动态下载并运行官方 server
    server_params = StdioServerParameters(
        command="uvx", 
        args=[
            "@modelcontextprotocol/server-filesystem", # 官方包名
            allowed_path                               # 参数：允许访问的路径
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
                print("\n" + "="*50)
                print(f"[AI 回答]: {result[0]}")
                print("="*50)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 运行效果预期

1.  **启动**：程序会调用 `uvx`，第一次运行会自动下载 `@modelcontextprotocol/server-filesystem` 包（需要联网）。
2.  **工具发现**：你会看到控制台打印出真实的工具列表：
    *   `read_file`: Read the complete contents of a file
    *   `write_file`: Create a new file or completely overwrite...
    *   `list_directory`: ...
    *   ...
3.  **AI 执行**：
    *   AI 会先调用 `write_file`，参数 `{ "path": "hello_mcp.py", "content": "print('Hello from Real MCP!')" }`。
    *   Bridge 收到后，转发给 `uvx` 进程。
    *   **结果**：你的 `test_mcp_folder` 文件夹里真的会出现一个 `hello_mcp.py` 文件！
    *   AI 接着调用 `read_file`，读取刚才写的内容。
4.  **最终回答**：AI 确认文件已创建并读取成功。

### 还可以连接什么真实的 Server？

你只需要修改 `server_params` 里的 `args`，就可以瞬间拥有其他能力：

**1. 连接真实 SQLite 数据库**
让 AI 直接操作你的业务数据库。
```python
server_params = StdioServerParameters(
    command="uvx",
    args=["mcp-server-sqlite", "--db-path", "./my_data.db"]
)
```

**2. 连接 Google Drive (需要配置)**
让 AI 读取你的云文档。
*(注：这通常需要本地 clone 对应的 repo 并配置 OAuth)*

**3. 连接 Git**
让 AI 读取你的代码仓库。
```python
server_params = StdioServerParameters(
    command="uvx",
    args=["mcp-server-git", "--repository", "/path/to/your/repo"]
)
```

这就是 MCP 的核心价值：**只需要改一行配置（启动命令），你的 Agent 就能切换不同的“义肢”，去操作完全不同的真实世界系统。**