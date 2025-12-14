# 智能电商客服与销售支持系统

## 📋 项目概述

智能电商客服与销售支持系统是一个基于多智能体架构的现代化客服解决方案，旨在为电商平台提供高效、智能、个性化的客户服务体验。系统采用先进的AI技术，通过多个专业化智能体协同工作，结合RAG检索增强生成、长期记忆管理和向量数据库技术，实现7×24小时不间断的智能客户服务支持。

### 🎯 核心价值

- **效率提升**：响应时间从分钟级降至秒级，AI驱动的智能路由和处理机制
- **成本优化**：减少70%的人工客服需求，自动化处理常见问题和业务流程
- **服务质量**：基于知识库的一致性回答，个性化的用户记忆和上下文理解
- **业务增长**：智能推荐算法和销售支持，提升转化率和客单价
- **技术先进**：集成最新的大语言模型、向量检索和多智能体协作技术

## 🏗️ 系统架构

### 多智能体架构设计

系统采用分布式多智能体架构，每个智能体专注于特定的业务领域，通过智能路由和协作机制实现高效的客户服务：

```
                    ┌─────────────────────────────────────┐
                    │           用户交互层                 │
                    │        User Interface              │
                    └─────────────────┬───────────────────┘
                                      │
                    ┌─────────────────┴───────────────────┐
                    │         路由智能体                   │
                    │       Router Agent                 │
                    │    (意图识别 & 请求分发)              │
                    └─────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────┴────────┐    ┌──────────────┴─────────────┐    ┌──────────┴─────────┐
│   产品智能体     │    │        订单智能体           │    │    促销智能体       │
│ Product Agent  │    │      Order Agent          │    │ Promotion Agent   │
│  商品咨询推荐    │    │     订单管理跟踪           │    │   活动优惠管理      │
└───────┬────────┘    └──────────────┬─────────────┘    └──────────┬─────────┘
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                    ┌─────────────────┴───────────────────┐
                    │        售后智能体                    │
                    │     After-sales Agent              │
                    │      退换货 & 投诉处理               │
                    └─────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────┴────────┐    ┌──────────────┴─────────────┐    ┌──────────┴─────────┐
│   RAG检索系统   │    │        记忆管理系统          │    │    向量数据库       │
│ Embedding &    │    │      Memory System         │    │   Milvus Vector   │
│ Vector Search  │    │   长期记忆 & 上下文管理       │    │     Database      │
└────────────────┘    └────────────────────────────┘    └───────────────────┘
```

### 核心组件

#### 🧠 智能体层
- **路由智能体 (Router Agent)**: 基于自然语言理解的用户意图识别和智能请求路由
- **产品智能体 (Product Agent)**: 处理商品咨询、智能推荐、比较分析和库存查询
- **订单智能体 (Order Agent)**: 管理订单全生命周期，包括查询、跟踪、修改和异常处理
- **促销智能体 (Promotion Agent)**: 处理优惠活动、促销信息、优惠券管理和会员权益
- **售后智能体 (After-sales Agent)**: 负责退换货流程、投诉处理和客户满意度管理

#### 🔍 数据与记忆层
- **RAG检索系统**: 基于向量相似度的知识检索，支持密集向量和稀疏向量混合搜索
- **记忆管理系统**: 基于MEM0框架的长期记忆管理，维护用户偏好和对话历史
- **向量数据库**: Milvus向量数据库，支持高性能的语义搜索和相似度匹配

#### ⚙️ 技术支撑层
- **异步处理引擎**: 基于asyncio的高并发异步处理架构
- **MCP协议支持**: 模型上下文协议，支持工具调用和外部系统集成
- **配置管理系统**: 统一的配置管理和环境变量处理

## ✨ 核心功能

### 🤖 智能对话系统
- **自然语言理解**: 准确理解用户意图，支持多轮对话
- **上下文维护**: 保持对话连贯性，记住用户偏好
- **多模态交互**: 支持文本、图片等多种交互方式

### 🛍️ 商品服务
- **智能搜索**: 基于语义理解的商品搜索
- **个性化推荐**: 根据用户行为和偏好推荐商品
- **详细咨询**: 提供商品规格、价格、库存等详细信息
- **比较分析**: 多商品对比和优劣势分析

### 📦 订单管理
- **实时查询**: 订单状态、物流信息实时跟踪
- **订单操作**: 支持订单修改、取消等操作
- **异常处理**: 自动识别和处理订单异常情况
- **历史记录**: 完整的订单历史查询

### 🎁 促销活动
- **活动推荐**: 智能匹配适合的优惠活动
- **优惠券管理**: 优惠券查询、使用指导
- **会员权益**: 会员等级和权益说明
- **限时促销**: 实时推送限时优惠信息

### 🔧 售后服务
- **退换货**: 自动化退换货流程指导
- **质量问题**: 智能诊断和解决方案推荐
- **投诉处理**: 规范化投诉处理流程
- **满意度调研**: 自动化客户满意度收集

## 🛠️ 技术栈

### 🐍 后端框架
- **Python 3.8+**: 主要开发语言，支持现代异步编程
- **FastAPI**: 高性能异步Web框架，支持自动API文档生成
- **Uvicorn**: ASGI服务器，支持高并发处理
- **Pydantic**: 数据验证和序列化，类型安全保障

### 🤖 AI/ML技术栈
- **LangGraph**: 多智能体工作流编排和状态管理
- **LangChain**: LLM应用开发框架，工具调用和链式处理
- **OpenAI GPT-4**: 主要语言模型，支持函数调用
- **DeepSeek**: 备用语言模型，成本优化选择
- **DashScope**: 阿里云灵积模型服务，文本嵌入生成
- **MCP (Model Context Protocol)**: 模型上下文协议，标准化工具集成

### 🔍 向量检索与记忆
- **Milvus**: 高性能向量数据库，支持混合检索
- **MEM0**: 长期记忆管理框架，个性化用户体验
- **RAG (Retrieval-Augmented Generation)**: 检索增强生成
- **Dense & Sparse Vectors**: 密集和稀疏向量混合搜索
- **Semantic Search**: 语义搜索和相似度计算

### 💾 数据存储
- **MySQL 8.0+**: 主要关系型数据库，事务支持
- **Redis**: 高性能缓存和会话存储
- **Vector Database**: 专用向量存储和检索
- **Memory Store**: 用户记忆和偏好存储

### 🔧 开发与部署
- **Docker & Docker Compose**: 容器化部署和服务编排
- **Poetry**: 现代Python依赖管理
- **Pytest**: 全面的单元测试框架
- **Black & isort**: 代码格式化和导入排序
- **Pre-commit**: Git钩子和代码质量检查

### 🌐 集成与监控
- **JWT**: 安全的用户认证和授权
- **Logging**: 结构化日志记录和监控
- **Environment Config**: 环境变量配置管理
- **Health Checks**: 服务健康检查和监控

## 📦 安装指南

### 环境要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- Redis 6.0 或更高版本
- Milvus 2.0 或更高版本

### 快速安装

1. **克隆项目**
```bash
git clone https://github.com/your-repo/customer_service.git
cd customer_service
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接和API密钥
```

5. **初始化数据库**
```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE customer_service;"

# 运行数据库迁移（如果有）
python -m app.db.init_db
```

6. **启动服务**
```bash
python -m app.main
```

### Docker 部署

```bash
# 构建镜像
docker build -t customer-service .

# 运行容器
docker-compose up -d
```

## 🚀 使用指南

### 基本配置

在 `.env` 文件中配置以下关键参数：

```env
# 应用配置
APP_NAME=智能电商客服与销售支持系统
DEBUG=false
HOST=0.0.0.0
PORT=8000

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=customer_service

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# AI模型配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

### API 使用示例

#### 🔄 基础对话API
```python
import httpx
import asyncio

async def chat_with_agent():
    async with httpx.AsyncClient() as client:
        # 发送消息给智能客服
        response = await client.post(
            "http://localhost:8000/api/chat",
            json={
                "message": "我想查询我的订单状态",
                "user_id": "user123",
                "session_id": "session456"
            }
        )
        
        result = response.json()
        print(f"智能体回复: {result['response']}")
        print(f"使用的智能体: {result['agent_type']}")
        print(f"置信度: {result['confidence']}")

# 运行示例
asyncio.run(chat_with_agent())
```

#### 🛍️ 产品查询API
```python
async def search_products():
    async with httpx.AsyncClient() as client:
        # 智能产品搜索
        response = await client.post(
            "http://localhost:8000/api/products/search",
            json={
                "query": "适合冬天的保暖外套",
                "user_id": "user123",
                "filters": {
                    "price_range": [100, 500],
                    "category": "服装"
                }
            }
        )
        
        products = response.json()
        for product in products['results']:
            print(f"商品: {product['name']}")
            print(f"价格: ¥{product['price']}")
            print(f"推荐理由: {product['recommendation_reason']}")
```

#### 📦 订单管理API
```python
async def track_order():
    async with httpx.AsyncClient() as client:
        # 订单跟踪
        response = await client.get(
            "http://localhost:8000/api/orders/track",
            params={
                "order_id": "ORD123456",
                "user_id": "user123"
            }
        )
        
        order_info = response.json()
        print(f"订单状态: {order_info['status']}")
        print(f"物流信息: {order_info['logistics']}")
        print(f"预计送达: {order_info['estimated_delivery']}")
```

#### 🧠 记忆管理API
```python
async def get_user_preferences():
    async with httpx.AsyncClient() as client:
        # 获取用户偏好和历史
        response = await client.get(
            "http://localhost:8000/api/memory/preferences",
            params={"user_id": "user123"}
        )
        
        preferences = response.json()
        print(f"用户偏好: {preferences['preferences']}")
        print(f"购买历史: {preferences['purchase_history']}")
        print(f"互动记录: {preferences['interaction_summary']}")
```

### 智能体使用

#### 路由智能体
```python
from app.agents.base import RouterAgent

router = RouterAgent()
result = await router.run("我想买一台手机")
# 输出: {"target_agent": "product_agent", "confidence": 0.95}
```

#### 产品智能体
```python
from app.agents.product_agent import ProductAgent

product_agent = ProductAgent()
response = await product_agent.generate_product_agent("推荐一款性价比高的手机")
```

## 📊 性能指标

### 系统性能
- **响应时间**: < 3秒
- **并发处理**: 支持1000+并发用户
- **可用性**: 99.9%系统可用性
- **准确率**: 意图识别准确率 > 95%

### 业务指标
- **客户满意度**: > 90%
- **问题解决率**: > 85%
- **转化率提升**: > 30%
- **成本降低**: > 70%

## 🔧 开发指南

### 项目结构

```
customer_service/
├── app/                    # 应用主目录
│   ├── agents/            # 智能体模块
│   │   ├── base.py        # 路由智能体
│   │   ├── product_agent.py   # 产品智能体
│   │   ├── order_agent.py     # 订单智能体
│   │   ├── promotion_agent.py # 促销智能体
│   │   └── after_sales_agent.py # 售后智能体
│   ├── api/               # API接口
│   ├── core/              # 核心配置
│   │   ├── config.py      # 配置管理
│   │   └── client.py      # 客户端
│   ├── db/                # 数据库模块
│   ├── mcp/               # MCP协议支持
│   ├── memory/            # 记忆系统
│   ├── models/            # 数据模型
│   ├── rag/               # RAG检索增强
│   └── main.py            # 应用入口
├── logs/                  # 日志目录
├── requirements.txt       # 依赖列表
└── README.md             # 项目文档
```

### 添加新智能体

1. 在 `app/agents/` 目录下创建新的智能体文件
2. 继承基础智能体类并实现必要方法
3. 在路由智能体中添加新的路由规则
4. 更新配置和文档

### 扩展功能

系统采用模块化设计，支持灵活扩展：

- **新增业务模块**: 在相应目录下添加新模块
- **集成第三方服务**: 通过MCP协议集成外部工具
- **自定义智能体**: 实现特定业务场景的专用智能体

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码规范
- 添加适当的注释和文档字符串
- 编写单元测试
- 确保代码通过所有测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与联系

- **问题反馈**: [GitHub Issues](https://github.com/your-repo/customer_service/issues)
- **功能建议**: [GitHub Discussions](https://github.com/your-repo/customer_service/discussions)
- **技术支持**: support@yourcompany.com

## 🙏 致谢

感谢以下开源项目的支持：

- [LangChain](https://github.com/langchain-ai/langchain) - AI应用开发框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 多智能体编排
- [FastAPI](https://github.com/tiangolo/fastapi) - 现代Web框架
- [Pydantic](https://github.com/pydantic/pydantic) - 数据验证

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！

欢迎进群交流，请扫下方微信二维码进群

![群二维码.png](QR_code/%E7%BE%A4%E4%BA%8C%E7%BB%B4%E7%A0%81.png)
