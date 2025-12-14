# 数据库AI助手

一个强大的数据库AI助手，能够帮助用户连接MySQL或PostgreSQL数据库，通过自然语言生成SQL查询，并执行查询获取结果。

## 功能特性

- **数据库连接管理**：支持MySQL和PostgreSQL数据库连接
- **自然语言到SQL转换**：通过OpenAI API（或基础规则）将用户的自然语言问题转换为SQL查询
- **安全的SQL执行**：内置SQL安全检查，只允许执行SELECT查询
- **数据可视化**：将查询结果以表格形式展示，并支持基本的数据可视化
- **数据库表结构查看**：可查看连接数据库中的所有表及表结构
- **响应式设计**：适配各种屏幕尺寸的现代化UI界面

## 技术栈

### 前端
- HTML5 + CSS3 + JavaScript
- Tailwind CSS v3：用于快速构建现代化UI界面
- Chart.js：用于数据可视化
- Font Awesome：提供图标支持

### 后端
- Python 3.11
- Flask：轻量级Web框架
- Flask-CORS：处理跨域请求
- mysql-connector-python：MySQL数据库连接
- psycopg2-binary：PostgreSQL数据库连接
- LangChain：用于AI模型集成
- OpenAI API：用于SQL生成（可选）
- python-dotenv：环境变量管理

## 项目结构

```
ai-demo/
├── agent_ui/              # 前端界面目录
│   ├── database_agent.html  # 主要前端页面
│   ├── index.html           # 备用前端页面
│   └── app.py               # 前端Python服务（如果需要）
├── backend/               # 后端服务目录
│   ├── app.py              # 主要后端API服务
│   ├── requirements.txt    # Python依赖包
│   └── .env.example        # 环境变量示例
└── README.md              # 项目说明文档
```

## 安装与运行

### 1. 克隆项目

```bash
git clone <repository-url>
cd ai-demo
```

### 2. 配置后端服务

#### 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 配置环境变量

复制环境变量示例文件并根据需要修改：

```bash
cp .env.example .env
# 编辑.env文件，添加OpenAI API密钥（可选）
```

#### 启动后端服务

```bash
python3 app.py
```

后端服务默认运行在 http://127.0.0.1:5001

### 3. 运行前端界面

前端界面使用简单的HTTP服务器运行：

```bash
cd ..
python3 -m http.server --directory agent_ui 8000
```

然后在浏览器中访问 http://localhost:8000/database_agent.html

## 使用方法

### 1. 连接数据库

1. 点击右上角的"连接数据库"按钮
2. 选择数据库类型（MySQL或PostgreSQL）
3. 填写连接信息：
   - 主机地址
   - 端口（MySQL默认3306，PostgreSQL默认5432）
   - 数据库名称
   - 用户名
   - 密码
4. 点击"连接"按钮进行连接

### 2. 查看数据库表结构

连接成功后，可以：
- 在左侧面板查看已连接的数据库信息
- 点击"查看表结构"按钮查看所有表及字段信息

### 3. 生成和执行SQL查询

1. 在聊天输入框中输入您的查询需求（如："查询所有用户信息"）
2. 系统会生成对应的SQL查询语句
3. 检查生成的SQL，确认无误后点击"执行查询"
4. 查询结果将在聊天区域以表格形式展示
5. 对于适合可视化的数据，系统会自动生成图表

### 4. 断开数据库连接

完成工作后，点击"断开连接"按钮关闭数据库连接。

## 安全说明

- 系统内置了SQL安全检查，只允许执行SELECT查询
- 支持的数据库操作仅限于数据查询，不允许修改、删除等操作
- 建议在生产环境中进一步加强安全措施，如添加身份验证、限制数据库权限等

## 注意事项

- OpenAI API密钥为可选配置：
  - 配置API密钥后可获得更智能的SQL生成能力
  - 不配置API密钥时，系统使用基础规则生成SQL（功能有限）
- 对于大型结果集，系统会自动限制返回行数（默认最多1000行）
- 确保数据库服务器允许外部连接（如果前端和数据库不在同一网络）

## 常见问题

### Q: 连接数据库失败怎么办？
A: 请检查连接信息是否正确，确保数据库服务器正在运行且允许远程连接。

### Q: 生成的SQL不正确怎么办？
A: 尝试用更清晰的语言描述您的查询需求，或在未配置OpenAI API时考虑配置API密钥以获得更好的SQL生成质量。

### Q: 查询结果无法正常显示？
A: 可能是数据格式问题，请检查数据库中的特殊数据类型是否能正确序列化。

## 扩展与定制

- **添加更多数据库类型**：可以扩展后端支持SQLite、Oracle等其他数据库
- **增强SQL生成能力**：可以集成其他LLM模型或优化SQL生成提示模板
- **添加数据导出功能**：支持将查询结果导出为CSV、Excel等格式
- **增强数据可视化**：添加更多图表类型和自定义可视化选项

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请联系项目维护者。