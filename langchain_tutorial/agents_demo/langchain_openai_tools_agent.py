import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

# 1. 加载配置
dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# ==========================================
# 第一步：定义复杂工具 (Custom Tools)
# ==========================================

# 工具 1: 市场调研 (搜索)
search_tool = DuckDuckGoSearchRun(
    name="Market_Research",
    description="用于搜索市场上已有的竞品、功能列表或行业报告。在分析需求前必须先进行调研。"
)


# 工具 2: 文件保存 (带有参数校验的结构化工具)
# 定义参数结构 (使用 Pydantic)
class SaveFileArgs(BaseModel):
    filename: str = Field(description="要保存的文件名，必须以 .md 结尾")
    content: str = Field(description="文件的具体内容，Markdown 格式")


def save_report_to_file(filename: str, content: str) -> str:
    """将生成的需求文档保存到本地磁盘。"""
    try:
        # 简单防护，防止覆盖关键文件
        if not filename.endswith(".md"):
            filename += ".md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ 文件已成功保存至: {os.path.abspath(filename)}"
    except Exception as e:
        return f"❌ 文件保存失败: {e}"


save_tool = StructuredTool.from_function(
    func=save_report_to_file,
    name="Save_PRD_Document",
    description="当需求分析完成并生成完整报告后，使用此工具将报告保存到本地。",
    args_schema=SaveFileArgs  # 强类型约束
)

# 工具集
tools = [search_tool, save_tool]

# ==========================================
# 第二步：构建深度 System Prompt
# ==========================================
# 这是一个高级 Prompt，包含了角色、任务流和输出标准
system_prompt = """
你是一位拥有10年经验的资深产品经理(Product Manager)和需求分析师。
你的任务是帮助用户将模糊的想法转化为专业的《产品需求文档 (PRD)》。

### 你的工作流程：
1. **理解需求**：分析用户的原始想法。
2. **市场调研**：必须调用 'Market_Research' 工具去搜索类似的竞品（Competitors）和核心功能。
3. **深度分析**：
    - 确定目标用户 (User Personas)。
    - 列出核心功能点 (Core Features)。
    - 建议技术栈 (Tech Stack)。
    - 识别潜在风险 (Risks)。
4. **撰写报告**：生成一份结构清晰的 Markdown 格式报告。
5. **保存文件**：最后必须调用 'Save_PRD_Document' 工具将报告保存到本地文件，文件名为 '需求分析_{项目名}.md'。

### 思考原则：
- 不要凭空捏造，尽量依据搜索结果来规划功能。
- 如果用户需求太简单，请自动补充行业标准功能。
- 保持专业、客观。

现在，请根据用户的输入开始工作。
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # 用于存放中间步骤的思考和工具调用结果
])

# ==========================================
# 第三步：初始化 Agent
# ==========================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 使用 OpenAI Tools Agent (目前最稳健的单体 Agent 模式)
agent = create_openai_tools_agent(llm, tools, prompt_template)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 设为 True 可以看到它“调研 -> 思考 -> 撰写 -> 保存”的全过程
    handle_parsing_errors=True
)

# ==========================================
# 第四步：运行模拟
# ==========================================
if __name__ == "__main__":
    user_idea = "我想做一个类似大众点评的APP，但是专门针对宠物店、猫咖和宠物医院的。"

    print(f"🚀 开始分析需求: {user_idea}\n")

    try:
        result = agent_executor.invoke({"input": user_idea})
        print("\n==================================")
        print("🤖 Agent 执行完成")
        print("==================================")
        print(result['output'])
    except Exception as e:
        print(f"执行出错: {e}")