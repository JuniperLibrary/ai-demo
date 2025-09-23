"""
文档向量化与存储示例

本代码演示了如何使用LangChain库实现以下功能：
1. 从网页加载文档内容
2. 将文档分割成小块
3. 使用OpenAI的嵌入模型将文本转换为向量
4. 使用FAISS向量数据库存储这些向量，以便后续进行相似性搜索
"""

# 导入dotenv用于加载环境变量
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 验证API密钥是否已加载
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY环境变量未设置，请检查.env文件")

# 导入WebBaseLoader用于从网页加载文档
from langchain_community.document_loaders import WebBaseLoader
# 导入BeautifulSoup库用于HTML解析
import bs4

# 第一步：从网页加载文档
# 创建WebBaseLoader实例，指定要加载的网页URL
# bs_kwargs参数使用SoupStrainer限制只解析特定ID的内容区域，提高效率
loader = WebBaseLoader(
    web_path="https://www.gov.cn/xinwen/2020-06/01/content_5516649.htm",
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="UCAP-CONTENT"))  # 只提取ID为UCAP-CONTENT的内容
)
# 执行加载操作，获取文档对象
docs = loader.load()
# print("加载的文档内容:")
# print(docs)  # 打印加载的文档内容

# 第二步：设置嵌入模型
# 导入OpenAI的嵌入模型
from langchain_openai import OpenAIEmbeddings

# 创建嵌入模型实例，使用OpenAI的text-embedding-ada-002模型
# 该模型将文本转换为高维向量表示，便于后续相似性计算
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# 导入向量存储和文本分割器
from langchain_community.vectorstores import FAISS  # FAISS是Facebook AI开发的高效向量相似性搜索库
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 第三步：文档分割
# 创建文本分割器，将长文档分割成较小的文本块
# chunk_size=500：每个文本块最多包含500个字符
# chunk_overlap=50：相邻文本块之间有50个字符的重叠，确保上下文连贯性
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# 使用分割器处理文档
documents = text_splitter.split_documents(docs)
# 打印分割后的文档数量
# print(f"文档被分割成 {len(documents)} 个文本块")

# 第四步：向量存储
# 使用FAISS创建向量数据库
# embeddings模型会将documents中的每个文本块转换为向量
# 这些向量随后被存储在FAISS向量数据库中，便于后续进行高效的相似性搜索
vector = FAISS.from_documents(documents, embeddings)

# 注：此时vector对象可用于执行相似性搜索，例如：
docs = vector.similarity_search("民法", k=1)  # 查找最相似的4个文档
# print("\n搜索结果：与'民法'最相关的文档片段：")
# for i, doc in enumerate(docs):
#     print(f"\n--- 文档 {i+1} ---")
#     print(f"内容: {doc.page_content}")
#     print(f"元数据: {doc.metadata}")
#     print("-------------------")
