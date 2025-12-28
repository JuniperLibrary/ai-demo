from core.shared.config import get_logger
from langchain_tutorial.agents_demo.openai_agent.agent.agent_logic import run_agent_engine
from langchain_tutorial.agents_demo.openai_agent.database.connection import init_db, SessionLocal
from langchain_tutorial.agents_demo.openai_agent.tools.search_tavily import tools_schema as search_schema, available_tools as search_map
from langchain_tutorial.agents_demo.openai_agent.tools.tools_finance import finance_tools_map, finance_tools_schema
from langchain_tutorial.agents_demo.openai_agent.tools.tools_requirements import req_tools_schema, req_tools_map

logger = get_logger("agent.openai_agent", log_file="logs/openai_agent.log", format_style="standard")


# --- 1. 导入所有工具 ---
# 搜索工具
from langchain_tutorial.agents_demo.openai_agent.tools.search_tavily import (
    available_tools as search_map,
    tools_schema as search_schema
)
# 金融工具
from langchain_tutorial.agents_demo.openai_agent.tools.tools_finance import (
    finance_tools_map,
    finance_tools_schema
)
# 需求文档工具
from langchain_tutorial.agents_demo.openai_agent.tools.tools_requirements import (
    req_tools_map,
    req_tools_schema
)


def main():
    init_db()
    db_session = SessionLocal()

    try:
        # --- 2. 混合工具箱 (Merge Tools) ---
        # Python 字典合并语法 {**dict1, **dict2, ...}
        # 注意：如果不同文件中有同名函数，后面的会覆盖前面的，所以命名要规范
        mixed_tools_map = {
            **search_map,
            **finance_tools_map,
            **req_tools_map
        }

        # Python 列表合并语法 list1 + list2 + ...
        mixed_tools_schema = search_schema + finance_tools_schema + req_tools_schema

        # --- 3. 定义全能 Agent 场景 ---
        session_id = "user_super_001"
        print(f"\n=== 启动 全能商业助手 (Session: {session_id}) ===")
        print(f"载入工具数量: {len(mixed_tools_map)} 个 (搜索, 金融, 文件操作)")

        # 定义一个复杂的 System Prompt，告诉它如何综合运用这些能力
        super_system_prompt = """
        你是一个全能的商业分析助手。你同时拥有以下能力：
        1. **联网搜索**：获取最新的市场新闻、竞品信息。
        2. **金融计算**：获取实时股价，计算投资回报率。
        3. **文件管理**：将分析结果整理成 Markdown 报告并保存到本地。

        **工作原则**：
        - 遇到不知道的实时信息，先搜索。
        - 遇到数据计算，严禁自己瞎编，必须调用计算工具。
        - 任务结束后，主动询问用户是否需要将结果保存为报告。
        """

        # --- 4. 模拟一个跨领域的复杂任务 ---

        # 任务背景：用户想调研特斯拉，看现在买入合不合适，并写报告。
        # 这个任务需要：搜索(查新闻) -> 金融(查股价) -> 金融(算收益) -> 文件(存报告)

        q1 = """
        我想做一份关于特斯拉(TSLA)的简易投资分析。
        请帮我查一下它最近有什么大新闻，现在的股价是多少？
        如果我买入100股，假设未来3年每年增长15%，到时候能值多少钱？
        最后把这些信息整理成一份 'tsla_analysis.md' 报告保存下来。
        """

        print(f"\n[用户]: {q1}")

        # 运行引擎
        run_agent_engine(
            db=db_session,
            session_id=session_id,
            user_input=q1,
            system_prompt=super_system_prompt,
            tools_map=mixed_tools_map,  # <--- 传入混合后的工具映射
            tools_schema=mixed_tools_schema  # <--- 传入混合后的工具定义
        )

    finally:
        db_session.close()


def main1():
    # 1. 初始化数据库
    init_db()
    db_session = SessionLocal()

    try:
        # ==========================================
        # 场景 A: 搜索 Agent (原来的功能)
        # ==========================================
        session_id_1 = "user_search_01"
        print(f"\n=== 启动 搜索助手 (Session: {session_id_1}) ===")

        q1 = "马斯克最近有什么新闻？"
        print(f"[用户]: {q1}")

        # 调用引擎，传入搜索工具箱
        ans1 = run_agent_engine(
            db=db_session,
            session_id=session_id_1,
            user_input=q1,
            system_prompt="你是一个新闻助手，擅长使用搜索工具获取最新资讯。",
            tools_map=search_map,  # <--- 注入搜索函数
            tools_schema=search_schema  # <--- 注入搜索定义
        )
        print(f"[AI]: {ans1}")

        # ==========================================
        # 场景 B: 金融 Agent (新功能)
        # ==========================================
        session_id_2 = "user_finance_01"
        print(f"\n=== 启动 金融理财顾 (Session: {session_id_2}) ===")

        # 它可以查股价，也可以算数学
        q2 = "我现在有10万块钱，想买特斯拉(TSLA)的股票，假设年化收益是8%，存10年后能赚多少钱？"
        print(f"[用户]: {q2}")

        # 调用引擎，传入金融工具箱
        ans2 = run_agent_engine(
            db=db_session,
            session_id=session_id_2,
            user_input=q2,
            system_prompt="你是一个专业的理财顾问。如果涉及计算，必须调用计算工具，严禁自己估算。",
            tools_map=finance_tools_map,  # <--- 注入金融函数
            tools_schema=finance_tools_schema  # <--- 注入金融定义
        )
        print(f"[AI]: {ans2}")

    finally:
        db_session.close()


def main2():
    init_db()
    db_session = SessionLocal()

    try:
        # ==========================================
        # 场景: 需求分析 Agent (资深产品经理)
        # ==========================================
        session_id = "user_pm_001"
        print(f"\n=== 启动 需求分析专家 Agent (Session: {session_id}) ===")

        # 定义一个强大的 System Prompt
        pm_system_prompt = """
        你是一位拥有10年经验的资深产品经理(Product Manager)和系统架构师。

        你的工作流程如下：
        1. **引导沟通**：用户提出的需求通常很模糊。不要立即生成文档，而是先提出关键问题（用户画像、核心痛点、使用场景、竞品），引导用户完善想法。
        2. **结构化分析**：在收集到足够信息后，梳理出结构化的内容，包括：
           - 项目背景与目标
           - 用户角色 (User Roles)
           - 核心功能模块 (Functional Requirements)
           - 技术约束与非功能需求
        3. **生成并保存文档**：
           - 当用户确认需求无误后，你**必须**调用 `save_document` 工具。
           - 文档内容必须是格式清晰的 Markdown。
           - 保存成功后，告知用户文件名。

        请保持专业、耐心，逻辑严密。
        """

        # 模拟多轮对话过程

        # Round 1: 用户提出模糊需求
        q1 = "我想做一个类似 滴滴打车 的小程序，专门用来叫 货车 拉货。"
        print(f"\n[用户]: {q1}")
        run_agent_engine(
            db=db_session,
            session_id=session_id,
            user_input=q1,
            system_prompt=pm_system_prompt,
            tools_map=req_tools_map,
            tools_schema=req_tools_schema
        )

        # Round 2: 用户回答细节（模拟用户补充信息）
        # 实际场景中，这里应该是你看着 AI 的提问来回答
        q2 = "用户主要是搬家的年轻人和有拉货需求的小商户。司机是自带面包车或小货车的人。核心功能要有地图定位、按里程计费、预约用车。不需要支付功能，线下结算即可。"
        print(f"\n[用户]: {q2}")
        run_agent_engine(
            db=db_session,
            session_id=session_id,
            user_input=q2,
            system_prompt=pm_system_prompt,
            tools_map=req_tools_map,
            tools_schema=req_tools_schema
        )

        # Round 3: 要求生成文档
        q3 = "我觉得差不多了，帮我生成一份详细的 PRD 文档并保存下来。"
        print(f"\n[用户]: {q3}")
        run_agent_engine(
            db=db_session,
            session_id=session_id,
            user_input=q3,
            system_prompt=pm_system_prompt,
            tools_map=req_tools_map,
            tools_schema=req_tools_schema
        )

    finally:
        db_session.close()


if __name__ == "__main__":
    main()
    # main1()
    # main2()