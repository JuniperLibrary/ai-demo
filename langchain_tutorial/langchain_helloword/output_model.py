import os

import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

"""
使用json解析器
"""
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

# 初始化模型
llm = ChatOpenAI(model="gpt-4o-mini")

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术文档编写者。"),
    ("user", "{input}")
])

# 使用输出解析器
# output_parser = StrOutputParser()
output_parser = JsonOutputParser()

# 将其添加到上一个链中
# chain = prompt | llm
chain = prompt | llm | output_parser

# 调用它并提出同样的问题。答案是一个字符串，而不是ChatMessage
# message = chain.invoke({"input": "LangChain是什么?"})
# print(message)
response = chain.invoke({"input": "LangChain是什么? 用JSON格式回复，问题用question，回答用answer"})
# print(response)