import json
from tavily import TavilyClient
import os
import dotenv
from core.shared.logging.config import get_logger

dotenv.load_dotenv()


logger = get_logger("agent.openai_agent", log_file="../logs/openai_agent.log", format_style="standard")

# 初始化 Tavily 客户端
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_internet(query: str):
    """
    执行互联网搜索的函数
    """
    logger.info(f"    [Tool Exec] 正在使用 Tavily 搜索: '{query}' ...")
    try:
        response = tavily.search(query=query, max_results=3)
        return json.dumps(response)
    except Exception as e:
        return f"搜索时发生错误: {e}"

# 工具映射表，方便 Agent 调用
available_tools = {
    "search_internet": search_internet
}

# 发送给 OpenAI 的工具 Schema
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "用于获取实时信息、新闻、天气或其他大模型不知道的数据。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["query"],
            },
        },
    }
]