from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import dotenv
import os


# 1. 这里我们把 Server 的逻辑直接定义为 LangChain 的 Tool
# (这是 MCP 的"手动版"实现，原理一样：给模型提供工具)
@tool
def get_order_status(order_id: str) -> str:
    """根据订单号查询物流状态和商品详情。"""
    # 模拟数据库
    db = {
        "ORD-1001": {"status": "已发货", "location": "上海", "items": ["键盘"]},
    }
    order = db.get(order_id)
    if order:
        return f"状态：{order['status']}，位置：{order['location']}"
    return "未找到订单"


# 2. 初始化模型 (这里以 DeepSeek 为例，国内直连)
# api_key 去 deepseek 官网申请，非常便宜
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
llm = ChatOpenAI(model="gpt-4o-mini")


# 3. 把工具"绑定"给模型
tools = [get_order_status]
llm_with_tools = llm.bind_tools(tools)

# 4. 模拟对话
query = "帮我查一下订单 ORD-1001"
print(f"用户: {query}")

# 第一轮：模型思考并决定调用工具
ai_msg = llm_with_tools.invoke([HumanMessage(content=query)])
print(f"AI 决定调用: {ai_msg.tool_calls}")

# 第二轮：执行工具 (这一步在 Claude Desktop 中是自动的，这里我们要手动写)
for tool_call in ai_msg.tool_calls:
    if tool_call["name"] == "get_order_status":
        # 执行函数
        result = get_order_status.invoke(tool_call["args"])
        print(f"工具返回结果: {result}")

        # (可选) 第三轮：把结果喂回给 AI 生成最终那句人话
        # 在这里省略，原理你懂的