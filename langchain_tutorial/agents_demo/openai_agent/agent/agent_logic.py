"""
最核心的 Agent 运行逻辑
"""

import json
from openai import OpenAI
from sqlalchemy.orm import Session
import dotenv

from core.shared.logging.config import get_logger
from langchain_tutorial.agents_demo.openai_agent.database import crud

logger = get_logger("agent.openai_agent", log_file="../logs/openai_agent.log", format_style="standard")

dotenv.load_dotenv()
# 初始化 OpenAI 客户端
client = OpenAI()


def run_agent_engine(
        db: Session,
        session_id: str,
        user_input: str,
        system_prompt: str,
        tools_map: dict,  # 传入：函数名 -> 函数对象的映射
        tools_schema: list  # 传入：发给 OpenAI 的 JSON Schema
):
    """
    通用的 Agent 运行引擎。
    它可以运行任何类型的 Agent，只要传入不同的 tools_map 和 tools_schema。
    """
    # 1. 保存用户消息
    user_msg = {"role": "user", "content": user_input}
    crud.save_message(db, session_id, user_msg)

    while True:
        # 2. 从数据库获取完整上下文
        history = crud.get_history(db, session_id)

        # 可以在 history 最前面临时加一个 System Prompt (不存库，只用于本次推理)
        # 或者在数据库里存一个 system 类型的消息。这里为了简单，我们动态插入。
        messages_payload = [{"role": "system", "content": system_prompt}] + history

        # 3. 调用 OpenAI API
        logger.info(f"  >> [Engine] 调用 GPT-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_payload,
            tools=tools_schema,
            tool_choice="auto",
            temperature=0
        )
        response_message = response.choices[0].message
        ai_msg_dict = response_message.model_dump(exclude_none=True)

        # 4. 保存 AI 的回复
        crud.save_message(db, session_id, ai_msg_dict)

        # 5. 检查并执行工具调用
        if not response_message.tool_calls:
            logger.info("  >> [Engine] 最终回答生成完毕。")
            return response_message.content

        logger.info(f"  >> [Engine] 模型决定调用 {len(response_message.tool_calls)} 个工具。")
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # --- 关键修改：从传入的 tools_map 中查找工具 ---
            function_to_call = tools_map.get(function_name)

            if function_to_call:
                try:
                    # 执行工具
                    function_response = function_to_call(**function_args)
                except Exception as e:
                    function_response = f"Error executing {function_name}: {str(e)}"
            else:
                function_response = f"Error: Tool '{function_name}' not found in registry."

            # 6. 保存工具的执行结果
            tool_msg = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response),  # 确保转为字符串
            }
            crud.save_message(db, session_id, tool_msg)

        # 继续下一次循环...
