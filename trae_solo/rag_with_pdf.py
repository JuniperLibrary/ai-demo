# RAG 流程与 PDF 处理集成示例
from typing import List
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb
import os
from dotenv import load_dotenv
from google import genai
from pdf_processor import PDFProcessor
from trae_solo.openai_agent import get_openai_agent

# 加载环境变量
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# 初始化模型和客户端
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
chromadb_client = chromadb.EphemeralClient()
chromadb_collection = chromadb_client.get_or_create_collection(name="pdf_rag")

# 初始化 Google 客户端
google_client = genai.Client(api_key=gemini_api_key)

# 模型类型枚举
class ModelType:
    GOOGLE = "google"
    OPENAI = "openai"

# 文本转向量

def embed_chunk(chunk: str) -> List[float]:
    embedding = embedding_model.encode(chunk, normalize_embeddings=True)
    return embedding.tolist()

# 保存向量到数据库
def save_embeddings(chunks: List[str]) -> None:
    for i, chunk in enumerate(chunks):
        embedding = embed_chunk(chunk)
        chromadb_collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(i)]
        )

# 召回
def retrieve(query: str, top_k: int) -> List[str]:
    query_embedding = embed_chunk(query)
    results = chromadb_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0]

# 重排
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks][:top_k]

# 生成回答
def generate(query: str, chunks: List[str], model_type: str = ModelType.GOOGLE, openai_model: str = "gpt-4o") -> str:
    """生成回答
    
    Args:
        query: 用户查询
        chunks: 检索到的文档片段列表
        model_type: 模型类型，可选值为 google 或 openai
        openai_model: OpenAI 模型名称，默认为 gpt-4o
        
    Returns:
        生成的回答文本
    """
    joined_chunks = "\n\n".join(chunks)

    prompt = f"""
    你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。
    用户问题: {query}
    相关片段: {joined_chunks}
    请基于上述内容作答，不要编造信息。
    """

    print(f"{prompt}\n\n---\n")

    if model_type == ModelType.GOOGLE:
        # 使用 Google Gemini 生成
        response = google_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    elif model_type == ModelType.OPENAI:
        # 使用 OpenAI 生成
        agent = get_openai_agent(model=openai_model)
        return agent.generate(query, chunks)
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")

# 完整的 RAG 流程（从 PDF 到回答）
def rag_from_pdf(pdf_path: str, query: str, top_k: int = 5, rerank_k: int = 3, 
                 model_type: str = ModelType.GOOGLE, openai_model: str = "gpt-4o") -> str:
    """从 PDF 文件开始的完整 RAG 流程
    
    Args:
        pdf_path: PDF 文件路径
        query: 用户查询
        top_k: 召回的文档数量
        rerank_k: 重排后保留的文档数量
        model_type: 模型类型，可选值为 google 或 openai
        openai_model: OpenAI 模型名称，默认为 gpt-4o
        
    Returns:
        生成的回答
    """
    # 1. 处理 PDF 并分块
    print("正在处理 PDF 文件...")
    pdf_chunks = PDFProcessor.split_pdf_into_chunks(pdf_path)
    print(f"PDF 处理完成，共生成 {len(pdf_chunks)} 个块")
    
    # 2. 将块转换为向量并保存到数据库
    print("正在将文本块转换为向量...")
    save_embeddings(pdf_chunks)
    print("向量保存完成")
    
    # 3. 召回相关文档
    print(f"正在召回与查询 '{query}' 相关的文档...")
    retrieved_chunks = retrieve(query, top_k)
    print(f"召回完成，共找到 {len(retrieved_chunks)} 个相关文档")
    
    # 4. 重排文档
    print("正在重排文档...")
    reranked_chunks = rerank(query, retrieved_chunks, rerank_k)
    print(f"重排完成，保留 {len(reranked_chunks)} 个最相关文档")
    
    # 5. 生成回答
    print(f"正在使用 {model_type} 模型生成回答...")
    answer = generate(query, reranked_chunks, model_type, openai_model)
    
    return answer

# 示例用法
if __name__ == "__main__":
    # 替换为实际的 PDF 文件路径和查询
    pdf_path = "example.pdf"
    query = "请总结这份文档的主要内容"
    
    print("=== 使用 Google Gemini 模型 ===")
    try:
        answer = rag_from_pdf(pdf_path, query, model_type=ModelType.GOOGLE)
        print("\n--- 最终回答 ---")
        print(answer)
    except FileNotFoundError:
        print(f"错误：未找到文件 {pdf_path}")
        print("请将示例代码中的 pdf_path 替换为实际的 PDF 文件路径")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")
    
    print("\n\n=== 使用 OpenAI 模型 ===")
    try:
        answer = rag_from_pdf(pdf_path, query, model_type=ModelType.OPENAI, openai_model="gpt-4o")
        print("\n--- 最终回答 ---")
        print(answer)
    except FileNotFoundError:
        print(f"错误：未找到文件 {pdf_path}")
        print("请将示例代码中的 pdf_path 替换为实际的 PDF 文件路径")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")
