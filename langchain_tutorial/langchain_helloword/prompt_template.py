from langchain_core.prompts import ChatPromptTemplate

from langchain_tutorial.langchain_helloword.hello import llm

"""
使用提示次模版
"""
prompt = ChatPromptTemplate.from_messages([
    ("system","你是世界级的技术文档"),
    ("user","{input}")
])

chain = prompt | llm
message = chain.invoke({"input":"大模型中的langchain是什么"})

print(message)