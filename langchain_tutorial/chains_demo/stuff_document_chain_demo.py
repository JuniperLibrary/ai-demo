import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.documents import Document

# 加载环境变量
dotenv.load_dotenv()

# 设置OpenAI环境变量
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# 创建大模型实例
chat_model = ChatOpenAI(model="gpt-4o-mini")

# 示例1: 基本的文档问答
print("=== 示例1: 基本的文档问答 ===")

# 创建提示词模板
prompt = PromptTemplate.from_template("""
基于以下文档内容回答问题:
{context}

问题: {question}
""")

# 手动实现简单的Stuff DocumentChain功能
def create_simple_stuff_documents_chain(llm, prompt):
    """
    简单实现文档合并链功能
    将所有文档内容合并到prompt中，然后通过LLM处理
    """
    def process(inputs):
        # 提取文档和问题
        context_docs = inputs.get('context', [])
        question = inputs.get('question', '')
        
        # 合并文档内容
        context_text = "\n".join([doc.page_content for doc in context_docs])
        
        # 格式化prompt
        formatted_prompt = prompt.format(context=context_text, question=question)
        
        # 使用LLM生成回答
        response = llm.invoke(formatted_prompt)
        return response.content
    
    return process

# 创建简单的文档合并链
document_chain = create_simple_stuff_documents_chain(chat_model, prompt)

# 准备测试文档
documents = [
    Document(
        page_content="LangChain是一个用于构建基于大语言模型(LLM)应用的框架，它提供了一套工具和接口，帮助开发者更高效地构建复杂的AI应用。",
        metadata={"source": "文档1"}
    ),
    Document(
        page_content="LCEL(LangChain Expression Language)是LangChain的核心特性，它基于Runnable协议，允许用户通过管道操作符(|)轻松组合不同组件。",
        metadata={"source": "文档2"}
    ),
    Document(
        page_content="在LangChain v0.2版本中，create_stuff_documents_chain是推荐用于文档处理的函数，它取代了传统的StuffDocumentsChain类。",
        metadata={"source": "文档3"}
    )
]

# 执行链
response = document_chain({
    "context": documents,
    "question": "LangChain的核心特性是什么？它在v0.2版本中有什么变化？"
})

print(f"回答: {response}\n")

# 示例2: 文档摘要
print("=== 示例2: 文档摘要 ===")

# 创建摘要提示词模板
summary_prompt = ChatPromptTemplate.from_template("""
请对以下文档内容进行简明扼要的总结:
{docs}

总结:
""")

# 手动实现摘要链功能
def create_simple_summary_chain(llm, prompt_template):
    """
    简单实现文档摘要链功能
    """
    def process(inputs):
        docs = inputs.get('docs', [])
        # 合并文档内容
        docs_text = "\n".join([doc.page_content for doc in docs])
        
        # 创建消息列表
        messages = prompt_template.format_messages(docs=docs_text)
        
        # 使用LLM生成摘要
        response = llm.invoke(messages)
        return response.content
    
    return process

# 创建摘要链
summary_chain = create_simple_summary_chain(chat_model, summary_prompt)

# 准备更长的测试文档
summary_docs = [
    Document(
        page_content="Stuff DocumentChain是一种文档处理策略，它将所有文档内容合并到一个上下文窗口中。这种方法简单直接，适用于文档数量少、总长度不超过模型上下文窗口限制的场景。"
    ),
    Document(
        page_content="在LangChain中，create_stuff_documents_chain函数提供了这种功能的现代实现。与传统的StuffDocumentsChain类相比，它更好地支持流式处理和批处理操作。"
    ),
    Document(
        page_content="使用Stuff策略时需要注意的是，当文档总量过大时，可能会超出模型的上下文窗口限制，导致信息丢失。因此，这种方法最适合处理少量短文档的场景。"
    )
]

# 执行摘要链
summary = summary_chain({"docs": summary_docs})
print(f"摘要: {summary}\n")

# 示例3: 文档内容分析
print("=== 示例3: 文档内容分析 ===")

# 创建分析提示词模板
analysis_prompt = ChatPromptTemplate.from_template("""
请分析以下文档内容，识别关键信息点并提供见解:
{documents}

分析结果:
""")

# 修改分析链实现，使用正确的参数名
def create_analysis_chain(llm, prompt_template):
    """
    简单实现文档分析链功能
    """
    def process(inputs):
        docs = inputs.get('documents', [])
        # 合并文档内容
        docs_text = "\n".join([doc.page_content for doc in docs])
        
        # 创建消息列表
        messages = prompt_template.format_messages(documents=docs_text)
        
        # 使用LLM生成分析
        response = llm.invoke(messages)
        return response.content
    
    return process

# 创建分析链
analysis_chain = create_analysis_chain(chat_model, analysis_prompt)

# 执行分析链
analysis = analysis_chain({"documents": documents})
print(f"分析结果: {analysis}\n")

# 总结Stuff DocumentChain的关键特性和使用场景
print("=== Stuff DocumentChain 总结 ===")
print("1. 工作原理: 将所有文档内容合并到一个上下文窗口中，一次性传递给LLM处理")
print("2. 优点:")
print("   - 实现简单，使用方便")
print("   - 保持文档之间的关联性")
print("   - 适合小批量文档处理")
print("3. 缺点:")
print("   - 受限于模型上下文窗口大小")
print("   - 文档过多时可能导致信息超载或截断")
print("4. 适用场景:")
print("   - 少量文档的问答任务")
print("   - 文档摘要生成")
print("   - 内容分析和信息提取")
print("5. 现代实现: create_stuff_documents_chain函数")
print("6. 最佳实践:")
print("   - 对输入文档进行预处理和过滤")
print("   - 监控上下文窗口使用情况")
print("   - 考虑结合文档分块策略使用")