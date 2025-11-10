import os
from openai import OpenAI

# 推荐：环境变量保存 OpenAI KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
你是一个专业技术助理，回答尽量精准短句，不废话。
"""

async def chat_agent(user_message: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    return resp.choices[0].message.content
