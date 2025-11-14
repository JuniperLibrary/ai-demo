# 🌟 Gemini + Milvus RAG 演示项目

本项目演示了如何结合 Google Gemini API 和 Milvus 向量数据库来构建一个简单的检索增强生成（RAG）系统。

## 🚀 运行步骤

1.  **克隆项目**
    ```bash
    git clone <YOUR_REPO_URL>
    cd gemini-milvus-rag-project
    ```

2.  **设置环境**
    创建一个名为 `.env` 的文件，并填入您的 API Key：
    ```ini
    # .env 文件内容
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **运行 RAG 管道**
    ```bash
    python rag_pipeline.py
    ```
    运行后，程序将自动：
    * 初始化 Gemini 和 Milvus 客户端。
    * 创建或清空 Milvus 集合。
    * 使用 Gemini 嵌入模型将示例文本转换为向量。
    * 将向量存储到 Milvus。
    * 对预设问题执行向量搜索和 LLM 问答。

---
