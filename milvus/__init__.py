import os
from dotenv import load_dotenv
from google import genai
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# -------------------------------
# 1. 加载环境变量
# -------------------------------
# load_dotenv()
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
# os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# -------------------------------
# 2. 初始化大模型
# -------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

google_client = genai.Client(api_key=api_key)

# -------------------------------
# 3. 连接 Milvus
# -------------------------------
connections.connect(host="localhost", port="19530")

# -------------------------------
# 4. 创建集合 schema
# -------------------------------
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1536)
]
schema = CollectionSchema(fields, "finance research RAG collection")
collection_name = "finance_docs"

# 如果集合不存在就创建
if collection_name not in Collection.list():
    collection = Collection(name=collection_name, schema=schema)
else:
    collection = Collection(name=collection_name)

# -------------------------------
# 5. 插入示例文档
# -------------------------------
sample_docs = [
    "美联储如果提前降息，将可能导致市场流动性快速回归，引发成长科技股重新成为主线。",
    "长端利率维持高位期间，债券投资者更关注 carry 和 roll down 收益而非 capital gain。",
    "黄金通常在美元持续走弱和真实利率下降的宏观环境下表现更强劲。"
]

# 调用 OpenAI embeddings
from openai import OpenAI
client = OpenAI()

def embed(text):
    return client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    ).data[0].embedding

vectors = [embed(d) for d in sample_docs]
collection.insert([sample_docs, vectors])

# -------------------------------
# 6. RAG查询
# -------------------------------
question = "如果美国进入降息周期，对科技股代表意义是什么？"
q_emb = embed(question)

collection.load()
search_results = collection.search(
    data=[q_emb],
    anns_field="vector",
    param={"metric_type": "COSINE"},
    limit=2
)

context = "\n".join([hit.entity.get("text") for hit in search_results[0]])

prompt = f"""
根据以下研究资料回答问题，禁止瞎编：
{context}

问题：{question}
"""

# 调用 LangChain ChatOpenAI

# 定义消息列表，其中包含了您构建的 prompt 字符串
messages = [
    {
        "role": "user",
        "content": prompt
        # prompt 仍然是包含 RAG 指令的大字符串
    }
]

# 使用消息列表作为 contents
response = google_client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages  # <--- 传入消息列表
)
print(response.text)
