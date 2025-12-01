# scripts/03_query_rerank_llm.py
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
import os
import openai

MILVUS_HOST="127.0.0.1"
MILVUS_PORT=19530
COLLECTION_NAME="docs_rag_v1"
EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"

openai.api_key = os.getenv("OPENAI_API_KEY")

def search(query, topk=5):
    connections.connect(host=MILVUS_HOST, port=str(MILVUS_PORT))
    col = Collection(COLLECTION_NAME)
    embedder = SentenceTransformer(EMBED_MODEL)
    qvec = embedder.encode(query).tolist()
    res = col.search([qvec], "embedding", param={"metric_type":"COSINE"}, limit=topk, output_fields=["text","source"])
    hits = res[0]
    docs = []
    for h in hits:
        docs.append({"text": h.entity.get("text"), "score": h.distance, "source": h.entity.get("source")})
    return docs

def generate_answer(question, docs):
    # 把检索到的 docs 拼接成 context
    context = "\n\n".join([f"## 来源: {d['source']}\n{d['text']}" for d in docs])
    prompt = f"""下面是相关文档片段（来自你的文档库），请基于这些内容回答问题。如果文中没有明确答案，请说“根据文档未找到明确答案”，不要编造。
问题：{question}
相关文档：
{context}
请用中文回答，尽量引用来源文件路径。
"""
    r = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # 替换为你有权限的模型
        messages=[{"role":"user","content":prompt}],
        max_tokens=512,
        temperature=0.0
    )
    return r["choices"][0]["message"]["content"]

if __name__ == "__main__":
    q = "请解释第3页中的关键结论是什么？"
    docs = search(q, topk=5)
    ans = generate_answer(q, docs)
    print(ans)
