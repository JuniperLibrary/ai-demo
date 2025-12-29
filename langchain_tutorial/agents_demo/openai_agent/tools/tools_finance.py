import json

from core.shared.logging.config import get_logger

# 1. 定义具体的 Python 函数 (Mock 数据)

logger = get_logger("agent.openai_agent", log_file="../logs/openai_agent.log", format_style="standard")

def get_stock_price(ticker: str):
    """模拟查询股票价格"""
    logger.info(f"[Finance Tool] 正在查询 {ticker} 的股价...")
    ticker = ticker.upper()
    # 模拟数据
    mock_db = {
        "AAPL": {"price": 175.50, "currency": "USD"},
        "TSLA": {"price": 210.20, "currency": "USD"},
        "BTC":  {"price": 65000.00, "currency": "USD"},
        "600519": {"price": 1700.00, "currency": "CNY"} # 茅台
    }
    result = mock_db.get(ticker, {"error": "Ticker not found"})
    return json.dumps(result)

def calculate_investment_return(principal: float, rate: float, years: int):
    """计算复利收益"""
    logger.info(f"[Finance Tool] 计算复利: 本金{principal}, 利率{rate}, 年限{years}")
    final_amount = principal * ((1 + rate) ** years)
    profit = final_amount - principal
    return json.dumps({
        "final_amount": round(final_amount, 2),
        "total_profit": round(profit, 2)
    })

# 2. 定义工具映射表 (Registry)
finance_tools_map = {
    "get_stock_price": get_stock_price,
    "calculate_investment_return": calculate_investment_return
}

# 3. 定义发送给 OpenAI 的 Schema
finance_tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "查询指定股票代码的当前价格。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "股票代码，如 AAPL, TSLA, 600519"},
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_investment_return",
            "description": "计算投资复利回报。",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "初始本金"},
                    "rate": {"type": "number", "description": "年利率 (例如 0.05 代表 5%)"},
                    "years": {"type": "integer", "description": "投资年限"},
                },
                "required": ["principal", "rate", "years"],
            },
        },
    }
]