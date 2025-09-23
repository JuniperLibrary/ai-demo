"""
检索增强生成（RAG）示例

本代码演示了如何使用LangChain实现RAG（Retrieval-Augmented Generation）模式：
1. 从向量数据库中检索与用户问题相关的文档
2. 将检索到的文档作为上下文提供给大语言模型
3. 让模型基于检索到的信息生成回答

这种方法可以让模型回答基于特定知识库的问题，提高回答的准确性和可靠性。
"""

# 导入提示词模板类，用于创建结构化的提示词
from langchain_core.prompts import PromptTemplate

# 导入之前创建的向量数据库和语言模型
from langchain_tutorial.langchain_helloword.embeddings import vector  # 导入已创建的FAISS向量数据库
from langchain_tutorial.langchain_helloword.output_model import llm   # 导入已配置的语言模型(ChatOpenAI)

# 第一步：创建检索器
# 将向量数据库转换为检索器，用于从数据库中检索相关文档
retriever = vector.as_retriever()
# 设置检索参数，k=3表示每次检索返回3个最相关的文档
retriever.search_kwargs = {"k": 3}
# 执行检索操作，查询"建设用地使用权是什么？"
docs = retriever.invoke("建设用地使用权是什么？")

# 可以取消注释以下代码来查看检索到的文档内容
# for i,doc in enumerate(docs):
#     print(f"⭐第{i+1}条规定：")
#     print(doc)

# 第二步：定义提示词模板
# 创建一个结构化的提示词模板，指导模型如何回答问题
prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
{info}

用户问：
{question}

请用中文回答用户问题。
"""
# 创建提示词模板对象
template = PromptTemplate.from_template(prompt_template)

# 第三步：格式化提示词
# 将检索到的文档和用户问题插入到提示词模板中
prompt = template.format(info=docs, question='建设用地使用权是什么？')

# 第四步：调用大语言模型
# 使用格式化后的提示词调用语言模型生成回答
response = llm.invoke(prompt)
# 打印模型的回答
# print(response.content)