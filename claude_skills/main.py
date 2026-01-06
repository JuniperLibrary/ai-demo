import asyncio
import os
import dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior  # 关键导入
from semantic_kernel.contents import ChatHistory  # 关键导入
from semantic_kernel.functions import kernel_function
import math

# 加载环境变量
dotenv.load_dotenv()


class MathPlugin:
    """
    这是一个数学技能包，包含原生计算和语义理解
    """

    @kernel_function(description="计算数字的平方根", name="Sqrt")
    def sqrt(self, number: float) -> float:
        return math.sqrt(number)

    @kernel_function(description="计算两个数字的和", name="Add")
    def add(self, number1: float, number2: float) -> float:
        return number1 + number2


async def main():
    # 1. 初始化 Kernel
    kernel = Kernel()

    # 2. 配置 AI 服务 (给 service_id 起个名字，方便后面调用)
    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    # 3. 导入 Plugin
    kernel.add_plugin(MathPlugin(), plugin_name="MathTools")

    # ---------------------------------------------------------
    # 4. (修复部分) 构建对话历史
    # ---------------------------------------------------------
    history = ChatHistory()
    history.add_system_message("你是一个数学助手，遇到计算问题请使用 MathTools。")
    history.add_user_message("帮我计算 25 的平方根，然后加上 10。")

    # ---------------------------------------------------------
    # 5. (修复部分) 配置自动工具调用 (FunctionChoiceBehavior)
    # ---------------------------------------------------------
    # Auto: 让 AI 自动决定是否调用工具
    settings = OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\n[AI 思考中]...")

    # ---------------------------------------------------------
    # 6. (修复部分) 获取 Chat 服务并直接调用
    # ---------------------------------------------------------
    # 从 kernel 中获取刚才注册的 chat 服务
    chat_service = kernel.get_service(service_id)

    # 执行对话
    # 注意：必须把 kernel 传进去，否则服务不知道去哪里找工具
    result = await chat_service.get_chat_message_contents(
        chat_history=history,
        settings=settings,
        kernel=kernel
    )

    # result 是一个列表，通常取第一个结果
    print(f"[AI 回答]: {result[0]}")


if __name__ == "__main__":
    asyncio.run(main())