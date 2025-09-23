"""
LangChain Agent 示例

本代码演示了如何使用LangChain创建一个智能代理(Agent)，该代理能够：
1. 使用检索工具获取相关信息
2. 根据用户问题决定何时使用工具
3. 综合工具返回的信息生成最终回答

Agent比简单的RAG更强大，因为它可以自主决定何时使用工具，以及如何处理工具返回的结果。
"""

# 导入创建检索工具的函数
from langchain.tools.retriever import create_retriever_tool

# 导入之前配置的语言模型和检索器
from langchain_tutorial.langchain_helloword.output_model import llm  # 导入语言模型
from langchain_tutorial.langchain_helloword.rag import retriever     # 导入向量检索器

# 第一步：创建检索工具
# 将检索器包装成Agent可以使用的工具
retriever_tool = create_retriever_tool(
    retriever,                      # 使用之前定义的检索器
    "CivilCodeRetriever",           # 工具名称
    "搜索有关中华人民共和国民法典的信息。关于中华人民共和国民法典的任何问题，您必须使用此工具!",  # 工具描述，指导Agent何时使用此工具
)

# 将创建的工具放入工具列表中，Agent将使用这些工具
tools = [retriever_tool]

# 导入Agent相关的模块
from langchain import hub                                # 用于获取预定义的提示词模板
from langchain.agents import create_openai_functions_agent  # 创建基于OpenAI函数调用的Agent
from langchain.agents import AgentExecutor               # Agent执行器，协调Agent与工具的交互

# 第二步：获取Agent提示词模板
# 从LangChain Hub获取预定义的Agent提示词模板
# https://smith.langchain.com/hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# 第三步：创建Agent
# 使用语言模型、工具列表和提示词模板创建Agent
agent = create_openai_functions_agent(llm, tools, prompt)

# 第四步：创建Agent执行器
# 执行器负责协调Agent的思考过程和工具的调用
# verbose=True表示打印执行过程，便于调试和观察
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 第五步：运行Agent
# 向Agent提问，Agent会根据需要调用工具并生成回答
result = agent_executor.invoke({"input": "建设用地使用权是什么"})
print("\n最终回答:")
print(result["output"])