"""
为了实现OpenAI 风格 (Tool Calling) + LangChain Hub 远程模板 + 会话记忆 (Memory) 的 Agent，
我们将使用现代 LangChain 的标准架构：LCEL (LangChain Expression Language) 配合 RunnableWithMessageHistory。

pip install langchain langchain-openai langchain-community langchainhub python-dotenv  langchain-tavily
"""
import logging
import os
import dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- 1. 引入自定义日志模块 ---
from core.shared.config import get_logger

# 初始化日志 (这一步通常放在最前面)
# 你可以在这里自定义日志文件名，例如 'daily_agent.log'
logger = get_logger("agent.openai_hub", log_file="logs/agents/openai_hub.log", format_style="standard")

# 1. 加载环境变量 (.env 文件)
dotenv.load_dotenv()
logger.info("环境变量已加载")

# 确保 API KEY 存在
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("请在 .env 文件中设置 TAVILY_API_KEY")
logger.info("API Keys 已检查")

# 2. 准备工具 (Tools)
# 使用 Tavily 搜索作为示例工具
tools = [TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"),max_results=3)]
logger.info("工具初始化完成")

# 3. 准备大模型 (LLM)
# 使用支持 Tool Calling 的 OpenAI 模型
llm = ChatOpenAI(
    model="gpt-4o-mini", # 或者 gpt-3.5-turbo
    temperature=0
)
logger.info("LLM 初始化完成")

# 4. 获取远程提示词模板 (Prompt Template)
# 我们使用 "hwchase17/openai-tools-agent"
# 这是 LangChain 官方专门为 OpenAI Tool Calling 模式设计的模板
# 它包含 system message, chat_history, input 和 agent_scratchpad
logger.info(f"正在从 LangChain Hub 下载提示词模板...")
prompt = hub.pull("hwchase17/openai-tools-agent")
logging.info(f"模板下载成功，输入变量包含: {prompt.input_variables}")
logger.info(f"提示词模板已下载 输入变量: {prompt.input_variables}")

# 5. 创建 Agent (OpenAI 风格)
agent = create_tool_calling_agent(llm, tools, prompt)

# 6. 创建 Agent 执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True # 开启详细日志
)
logger.info("AgentExecutor 初始化完成")

# 7. 添加记忆功能 (Memory)
# 使用 RunnableWithMessageHistory 包装 agent_executor
# 这是 LangChain 目前推荐的添加记忆的方式

# 模拟一个数据库来存储不同 session 的历史
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",        # 用户输入的变量名
    history_messages_key="chat_history", # 提示词模板中用于存放历史记录的变量名
)

# 8. 测试运行
print("\n--- 开始对话 ---")

# 第一轮对话：查询信息
session_id = "user_123" # 模拟用户ID
print(f"\n[用户]: 北京今天天气怎么样？ (Session ID: {session_id})")
logger.info("开始第一轮对话", extra={"conversation_id": session_id, "agent_type": "openai_hub"})

response1 = agent_with_memory.invoke(
    {"input": "查询今天北京的天气情况"},
    config={"configurable": {"session_id": session_id}}
)
logger.info("第一轮完成", extra={"conversation_id": session_id})
print(f"[AI]: {response1['output']}")

# 第二轮对话：测试记忆能力
# 注意：我没有在问题里提“北京”，AI 需要从记忆中知道我在问哪里
print(f"\n[用户]: 那非常适合去哪里玩？ (测试记忆功能)")
logger.info("开始第二轮对话", extra={"conversation_id": session_id})

response2 = agent_with_memory.invoke(
    {"input": "根据上面的天气，推荐几个适合今天去游玩的具体景点"},
    config={"configurable": {"session_id": session_id}}
)
logger.info("第二轮完成", extra={"conversation_id": session_id})
print(f"[AI]: {response2['output']}")
