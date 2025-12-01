# scripts/02_chunk_and_embed.py
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import json, os, uuid, tqdm
from utils import split_into_chunks

MILVUS_HOST = "127.0.0.1"
MILVUS_PORT = 19530
COLLECTION_NAME = "docs_rag_v1"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # 示例

def create_collection(client, dim=384):
    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=8192),
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=512),
    ]
    schema = CollectionSchema(fields, description="docs for RAG")
    if Collection.exists(COLLECTION_NAME):
        col = Collection(COLLECTION_NAME)
    else:
        col = Collection(name=COLLECTION_NAME, schema=schema)
    return col

def ingest(parsed_folder):
    # 连接 Milvus
    connections.connect(host=MILVUS_HOST, port=str(MILVUS_PORT))
    # load model
    embedder = SentenceTransformer(EMBED_MODEL)
    dim = embedder.get_sentence_embedding_dimension()
    col = create_collection(None, dim=dim)

    # 逐文件读取 MinerU 输出（假设 JSON files）
    files = [os.path.join(parsed_folder, f) for f in os.listdir(parsed_folder) if f.endswith(".json")]
    for fp in tqdm.tqdm(files):
        data = json.load(open(fp, "r", encoding="utf8"))
        # 假设 data 包含 'content' 字段 —— 需要根据 MinerU 输出结构调整
        text = data.get("content", "")
        chunks = split_into_chunks(text, max_tokens=800, overlap=100)
        ids = []
        embeds = []
        texts = []
        sources = []
        for c in chunks:
            ids.append(str(uuid.uuid4()))
            v = embedder.encode(c).tolist()
            embeds.append(v)
            texts.append(c)
            sources.append(fp)
        # insert
        entities = [ids, embeds, texts, sources]
        col.insert(entities)
    col.create_index(field_name="embedding", index_params={"index_type":"IVF_FLAT","metric_type":"COSINE","params":{"nlist":128}})
    col.flush()
    print("ingest done")
