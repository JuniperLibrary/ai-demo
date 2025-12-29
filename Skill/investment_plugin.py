import asyncio
import os
import dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
# 【修复 1】引入 KernelFunctionFromPrompt 类
from semantic_kernel.functions import KernelFunctionFromPrompt

dotenv.load_dotenv()

# 全局变量引用 Kernel
global_kernel_ref = None


class InvestmentPlugin:
    """
    一个包含 硬数据获取(Native) 和 软逻辑分析(Semantic) 的混合插件
    """

    @kernel_function(description="获取股票的当前价格", name="get_stock_price")
    def get_stock_price(self, ticker: str) -> str:
        print(f"    [系统日志] 正在调用 API 查询 {ticker} 价格...")
        data = {
            "AAPL": "175.50 USD",
            "TSLA": "210.20 USD",
            "NVDA": "800.00 USD"
        }
        return data.get(ticker.upper(), "未知价格")

    @kernel_function(description="获取股票的最近重大新闻", name="get_market_news")
    def get_market_news(self, ticker: str) -> str:
        print(f"    [系统日志] 正在搜索 {ticker} 的新闻...")
        news = {
            "AAPL": "苹果发布了新的 Vision Pro，市场反应平平。",
            "TSLA": "特斯拉 Cybertruck 产能爬坡顺利，但自动驾驶面临监管调查。",
            "NVDA": "英伟达发布最新 AI 芯片，算力提升 300%。"
        }
        return news.get(ticker.upper(), "无重大新闻")

    @kernel_function(description="根据新闻内容分析市场情绪 (Positive/Negative/Neutral)", name="analyze_sentiment")
    async def analyze_sentiment(self, news_text: str) -> str:
        print(f"    [系统日志] 正在调用 LLM 分析新闻情绪...")

        analyze_prompt = """
        请分析以下新闻的市场情绪：
        {{$input}}

        只输出以下单词之一：Positive, Negative, Neutral
        """

        if global_kernel_ref:
            # 【修复 2】使用 v1.x 的新写法
            # 不再使用 kernel.create_function_from_prompt
            # 而是直接实例化 KernelFunctionFromPrompt
            func = KernelFunctionFromPrompt(
                function_name="AnalyzeSentiment",
                plugin_name="TempPlugin",
                prompt=analyze_prompt
            )

            # 调用 Invoke
            result = await global_kernel_ref.invoke(func, input=news_text)
            return str(result)
        else:
            return "Error: Kernel not initialized"


async def main():
    global global_kernel_ref
    kernel = Kernel()
    global_kernel_ref = kernel

    service_id = "default"
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    # 注册插件
    kernel.add_plugin(InvestmentPlugin(), plugin_name="InvestTools")

    # 配置自动工具调用
    settings = OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    chat_service = kernel.get_service(service_id)
    history = ChatHistory()

    user_query = "帮我分析一下 Tesla (TSLA) 的情况，我需要知道现在的价格，以及基于最近的新闻，我现在应该买入还是卖出？"

    print(f"[用户指令]: {user_query}")
    history.add_user_message(user_query)

    try:
        # 增加超时时间，防止复杂的思维链超时
        result = await chat_service.get_chat_message_contents(
            chat_history=history,
            settings=settings,
            kernel=kernel
        )
        print("\n" + "=" * 50)
        print(f"[最终分析报告]:\n{result[0]}")
        print("=" * 50)

    except Exception as e:
        print(f"\n[报错详情]: {e}")


if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()

    asyncio.run(main())