"""
2️⃣ LLM-based 实现

特点：

优点：语义理解能力强，可优化成自然语言、问句更清晰

缺点：有调用成本，延迟可能较高，需要网络 / API

适合：智能问答、知识检索（RAG）、对用户体验要求高

"""

import os
import dotenv
import openai

# 加载 .env
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_BASE_URL")  # 如果是自定义 API Base，否则可删除


def llm_beautify(question: str) -> str:
    """
    使用 OpenAI 官方接口优化用户问题表达
    """
    messages = [
        {"role": "system", "content": "你是一个提问优化助手，只优化语言表达，保持原意。"},
        {"role": "user", "content": f"我的问题是：{question}"}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )

    # 返回模型输出
    return response.choices[0].message.content


q = "python json咋办"
print(llm_beautify(q))

