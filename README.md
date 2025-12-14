# AI Demo Project

这是一个包含多个 AI 示例项目的集合，涵盖了 LangChain, RAG, 智能客服, LeetCode 可视化等多个领域。

## 目录结构

*   `customer_service/`: 智能电商客服与销售支持系统
*   `fastapi/`: FastAPI 使用指南和示例
*   `langchain_tutorial/`: LangChain 教程和示例
*   `milvus/`: Milvus 向量数据库相关示例
*   `rag/`: RAG (检索增强生成) 示例
*   `ai-leetcode/`: LeetCode 算法可视化
*   `agent_ui/`: Agent 前端界面
*   `gupiao/`: 股票分析 API
*   `second_house/`: 二手房数据分析
*   `market_extract/`: 市场数据提取

## 环境管理

本项目统一使用 `uv` 进行 Python 依赖管理。请确保你已经安装了 `uv`。

### 1. 安装 uv

如果你还没有安装 `uv`，请根据你的操作系统参考 [uv 官方文档](https://github.com/astral-sh/uv) 进行安装。

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 同步依赖

获取代码后，在项目根目录下执行以下命令，即可一键创建虚拟环境并安装所有依赖：

```bash
uv sync
```

该命令会根据 `uv.lock` 文件安装精确版本的依赖，确保环境一致性。

### 3. 添加新依赖

如果需要为项目添加新的依赖包，请使用 `uv add` 命令：

```bash
uv add <package_name>
```

例如：
```bash
uv add pandas
```

### 4. 运行代码

你可以使用 `uv run` 来在虚拟环境中运行脚本，或者激活虚拟环境后直接运行。

**使用 uv run:**
```bash
uv run path/to/script.py
```

**激活虚拟环境:**

*   **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```
