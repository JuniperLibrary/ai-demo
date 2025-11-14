import os
from dotenv import load_dotenv
from google import genai
from pymilvus import MilvusClient,DataType, FieldSchema, CollectionSchema, MilvusException
from google.genai.errors import APIError
from typing import List, Dict

# ----------------------------------------------------
# 步骤 1: 环境配置与客户端初始化
# ----------------------------------------------------

# 加载 .env 文件中的环境变量
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Milvus 标准版连接信息
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
# MILVUS_USER = os.getenv("MILVUS_USER")
# MILVUS_PASSWORD = os.getenv("MILVUS_PASSWORD")

if not GEMINI_API_KEY:
    raise ValueError("❌ 错误：GEMINI_API_KEY 环境变量未设置。请在 .env 文件中设置您的密钥。")

try:
    # 1. 初始化 Gemini LLM 客户端
    google_client = genai.Client(api_key=GEMINI_API_KEY)

    # 2. 初始化 Milvus 标准版客户端 (修正连接格式和认证)
    MILVUS_URI = f"tcp://{MILVUS_HOST}:{MILVUS_PORT}"
    MILVUS_COLLECTION_NAME = "gemini_rag_crud_docs"

    milvus_client = MilvusClient(
        uri=MILVUS_URI
        # user=MILVUS_USER,
        # password=MILVUS_PASSWORD
    )

    EMBEDDING_DIM = 768
    embedding_model = "models/text-embedding-004"

    print(f"✅ 客户端初始化成功。连接 Milvus URI: {MILVUS_URI}")

except Exception as e:
    print(f"❌ 客户端初始化失败: {e}")
    # 如果连接失败，打印 Milvus 连接提示
    print(f"请检查 Milvus 服务是否运行在 {MILVUS_HOST}:{MILVUS_PORT}，并且 URI 格式是否正确。")
    exit()


# ----------------------------------------------------
# 步骤 2: Milvus 集合创建与 C.R.U.D. 辅助函数
# ----------------------------------------------------

def setup_milvus_collection():
    """定义、删除（如果存在）并创建 Milvus 集合，并显式创建索引。"""

    # 集合字段定义
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
    ]
    schema = CollectionSchema(fields, description="Gemini RAG CRUD Demo Collection")

    # 如果集合已存在，则先删除
    if milvus_client.has_collection(collection_name=MILVUS_COLLECTION_NAME):
        milvus_client.drop_collection(collection_name=MILVUS_COLLECTION_NAME)
        print(f"🔄 已删除旧集合: {MILVUS_COLLECTION_NAME}")

    # 创建新集合
    milvus_client.create_collection(
        collection_name=MILVUS_COLLECTION_NAME,
        schema=schema,
        description="Gemini RAG CRUD Demo Collection"
    )
    print(f"✨ 集合 {MILVUS_COLLECTION_NAME} 创建成功。")

    # === 关键修正：使用 prepare_index_params() 创建索引 ===
    try:
        index_params = milvus_client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            index_name="vector_index",
            index_type="FLAT",      # 也可以改为 IVF_FLAT / HNSW
            metric_type="L2",
            params={"dim": EMBEDDING_DIM}
        )

        milvus_client.create_index(
            collection_name=MILVUS_COLLECTION_NAME,
            index_params=index_params
        )
        print(f"🛠️ 向量字段 'vector' 索引创建成功。")

    except MilvusException as e:
        if "already exist" in str(e):
            print("⚠️ 索引已存在，跳过创建。")
        else:
            print(f"❌ 创建索引失败: {e}")
            raise

# ... (其他代码不变)
def setup_milvus_collection():
    """定义、删除（如果存在）并创建 Milvus 集合，并显式创建索引。"""
    from pymilvus import DataType, FieldSchema, CollectionSchema, MilvusException

    # 集合字段定义
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
    ]
    schema = CollectionSchema(fields, description="Gemini RAG CRUD Demo Collection")

    # 如果集合已存在，则先删除
    if milvus_client.has_collection(collection_name=MILVUS_COLLECTION_NAME):
        milvus_client.drop_collection(collection_name=MILVUS_COLLECTION_NAME)
        print(f"🔄 已删除旧集合: {MILVUS_COLLECTION_NAME}")

    # 创建新集合
    milvus_client.create_collection(
        collection_name=MILVUS_COLLECTION_NAME,
        schema=schema,
        description="Gemini RAG CRUD Demo Collection"
    )
    print(f"✨ 集合 {MILVUS_COLLECTION_NAME} 创建成功。")

    # === 关键修正：使用 prepare_index_params() 创建索引 ===
    try:
        index_params = milvus_client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            index_name="vector_index",
            index_type="FLAT",      # 也可以改为 IVF_FLAT / HNSW
            metric_type="L2",
            params={"dim": EMBEDDING_DIM}
        )

        milvus_client.create_index(
            collection_name=MILVUS_COLLECTION_NAME,
            index_params=index_params
        )
        print(f"🛠️ 向量字段 'vector' 索引创建成功。")

    except MilvusException as e:
        if "already exist" in str(e):
            print("⚠️ 索引已存在，跳过创建。")
        else:
            print(f"❌ 创建索引失败: {e}")
            raise



# 假设您已移除了顶部的 types 导入
def embed_text(texts_to_embed: List[str], task_type: str) -> List[List[float]]:
    """调用 Gemini 嵌入模型将文本转为向量。"""
    try:
        # ⚠️ 修正：使用字典直接作为配置参数
        config = {
            "task_type": task_type
        }

        response = google_client.models.embed_content(
            model=embedding_model,
            contents=texts_to_embed,
            config=config  # 使用字典传入配置
        )
        return [
            embedding_obj.values
            for embedding_obj in response.embeddings
        ]
    except APIError as e:
        print(f"❌ Gemini 嵌入调用失败: {e}")
        return []

# --- C.R.U.D. 操作函数 ---

def create_doc(doc_id: int, text: str):
    """【增】插入一条新记录。"""
    embeddings = embed_text([text], task_type="RETRIEVAL_DOCUMENT")
    if not embeddings: return

    data_to_insert = [
        {"id": doc_id, "text": text, "vector": embeddings[0]}
    ]
    milvus_client.insert(
        collection_name=MILVUS_COLLECTION_NAME,
        data=data_to_insert
    )
    milvus_client.flush(collection_name=MILVUS_COLLECTION_NAME)
    print(f"💾 【增】记录 ID {doc_id} 插入成功。")


def retrieve_doc(doc_id: int) -> List[Dict]:
    """【查】根据 ID 检索记录。"""
    filter_expr = f"id == {doc_id}"
    print(f"🔍 【查】正在查询 ID {doc_id}...")

    result = milvus_client.query(
        collection_name=MILVUS_COLLECTION_NAME,
        filter=filter_expr,
        output_fields=["id", "text"]
    )
    return result


def update_doc(doc_id: int, new_text: str):
    """【改】更新一条记录 (使用 Upsert)。"""
    new_embeddings = embed_text([new_text], task_type="RETRIEVAL_DOCUMENT")
    if not new_embeddings: return

    # 保持数据结构为 MilvusClient 推荐的行式数据
    data_to_upsert = [
        {"id": doc_id, "text": new_text, "vector": new_embeddings[0]}
    ]

    try:
        milvus_client.upsert(
            collection_name=MILVUS_COLLECTION_NAME,
            data=data_to_upsert
        )
        milvus_client.flush(collection_name=MILVUS_COLLECTION_NAME)
        print(f"📝 【改】记录 ID {doc_id} 更新/Upsert 成功。")
    except Exception as e:
        print(f"❌ 【改】记录 ID {doc_id} 更新失败。请检查 MilvusClient 版本兼容性。错误: {e}")


def delete_doc(doc_id: int):
    """【删】根据 ID 删除记录。"""
    expr = f"id in [{doc_id}]"

    milvus_client.delete(
        collection_name=MILVUS_COLLECTION_NAME,
        filter=expr
    )
    milvus_client.flush(collection_name=MILVUS_COLLECTION_NAME)
    print(f"🗑️ 【删】记录 ID {doc_id} 删除成功。")


# ----------------------------------------------------
# 步骤 3: 向量搜索和 RAG 问答函数
# ----------------------------------------------------

def ask_rag(query: str, k: int = 2) -> str:
    """执行完整的 RAG 流程：嵌入 -> 搜索 -> 生成。"""

    print("\n--- RAG 流程开始 ---")

    # 1. 嵌入查询
    query_vector = embed_text([query], task_type="RETRIEVAL_QUERY")[0]

    print(f"🔍 【查】正在 Milvus 中搜索最相似的 {k} 个文档...")

    # 2. Milvus 搜索
    search_results = milvus_client.search(
        collection_name=MILVUS_COLLECTION_NAME,
        data=[query_vector],
        limit=k,
        output_fields=["id", "text"]
    )

    # 3. 提取检索到的上下文
    contexts = [hit['text'] for hit in search_results[0]]
    context_str = "\n".join(contexts)

    print(f"📚 检索到的上下文：\n---\n{context_str}\n---")

    # 4. 构建 RAG Prompt
    rag_prompt = f"""你是一位知识助手，请根据用户的问题和下列提供的上下文生成准确的回答。

用户问题: {query}

上下文: 
{context_str}

请基于上述上下文作答，不要编造信息。如果上下文没有相关信息，请说明。"""

    # 5. 调用 Gemini LLM 生成答案
    llm_response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=rag_prompt
    )

    return llm_response.text


# ----------------------------------------------------
# 步骤 4: 运行主程序并演示 CRUD
# ----------------------------------------------------

if __name__ == "__main__":
    # (A) 设置 Milvus 集合
    setup_milvus_collection()

    # (B) 演示 CRUD 操作
    print("\n\n=== 开始演示 Milvus CRUD 操作 ===")

    # 1. 增 (CREATE)
    create_doc(doc_id=101, text="Milvus 是一个专门设计用于向量搜索的开源数据库。")
    create_doc(doc_id=102, text="Gemini 2.5 Pro 是 Google 目前最强大的多模态 AI 模型。")
    create_doc(doc_id=103, text="RAG 架构可以显著提高大型语言模型回答的准确性。")

    # ⚠️ 关键修正：加载集合到内存，使其可查询！
    """
    Milvus 采用存储计算分离架构。
    insert 操作将数据写入存储层（例如 MinIO/S3）。
    load_collection 操作将数据从存储层复制并加载到专门处理查询请求的查询节点（Query Node）的内存中。
    只有数据在查询节点内存中时，才能进行 query、search 或 retrieve 操作。
    """
    print(f"\n🧠 正在加载集合 {MILVUS_COLLECTION_NAME}...")
    milvus_client.load_collection(collection_name=MILVUS_COLLECTION_NAME)
    print("✅ 集合加载完成，可执行查询。")

    # 2. 查 (RETRIEVE/QUERY)
    retrieved_data = retrieve_doc(doc_id=101)
    print(f"📖 【查】ID 101 的记录详情: {retrieved_data}")

    # 3. 改 (UPDATE/UPSERT)
    new_content = "Milvus 是一个由 Zilliz 维护的开源向量数据库，提供高效的存储和检索。"
    update_doc(doc_id=101, new_text=new_content)

    # 4. 删 (DELETE)
    delete_doc(doc_id=102)
    retrieved_data_after_delete = retrieve_doc(doc_id=102)
    print(f"📖 【查】ID 102 删除后的查询结果 (应为空): {retrieved_data_after_delete}")

    # (C) 执行 RAG 问答 (搜索)
    print("\n\n=== 执行 RAG 向量搜索 (SEARCH) ===")

    user_query = "谁维护着 Milvus 数据库？"

    print(f"❓ 用户问题: {user_query}")
    answer = ask_rag(user_query, k=1)

    print("\n🎉 RAG 最终答案:")
    print("=" * 30)
    print(answer)
    print("=" * 30)