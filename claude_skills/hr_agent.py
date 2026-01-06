import asyncio
import os
import dotenv
from typing import List

# 引入 Semantic Kernel 核心组件
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function

# 加载环境变量 (.env)
dotenv.load_dotenv()


# ==============================================================================
# 1. 模拟向量数据库 (RAG 知识库)
# ==============================================================================
class CompanyPolicyPlugin:
    """
    负责检索公司非结构化的规章制度 (模拟 RAG)
    """

    def __init__(self):
        # 模拟存入向量库的文档切片
        self.knowledge_base = {
            "remote_work": "公司远程办公(WFH)政策：1. 员工必须入职满 6 个月。 2. 过去 30 天内没有迟到早退记录。 3. 实习生(Intern)无权申请。",
            "reimbursement": "报销政策：餐饮报销上限为 50 元/天，交通报销需要发票。",
            "security": "安全政策：所有员工必须完成入职安全培训才能访问内网。"
        }

    @kernel_function(description="查阅公司政策手册，获取关于特定主题的规定", name="search_policy")
    def search_policy(self, query: str) -> str:
        print(f"    [🔍 RAG 检索] 正在在知识库中搜索关于 '{query}' 的政策...")
        if "远程" in query or "WFH" in query or "remote" in query:
            return self.knowledge_base["remote_work"]
        elif "报销" in query or "钱" in query:
            return self.knowledge_base["reimbursement"]
        else:
            return "未在员工手册中找到相关规定。"


# ==============================================================================
# 2. 模拟 HR 数据库 (结构化数据)
# ==============================================================================
class HRDatabasePlugin:
    """
    负责查询员工的个人档案状态
    """

    def __init__(self):
        # 模拟 SQL 数据库
        self.employees = {
            "Alice": {
                "id": "E001",
                "role": "Full-Time",
                "join_date": "2023-01-01",
                "lateness_count": 0
            },
            "Bob": {
                "id": "E002",
                "role": "Intern",
                "join_date": "2024-05-01",
                "lateness_count": 2
            }
        }

    @kernel_function(description="根据姓名查询员工的详细档案信息", name="get_employee_info")
    def get_employee_info(self, name: str) -> str:
        print(f"    [🗄️ DB 查询] 正在查询员工 '{name}' 的数据库档案...")
        employee = self.employees.get(name)
        if employee:
            return str(employee)
        return "查无此人"


# ==============================================================================
# 3. 模拟 办公自动化系统 (Action)
# ==============================================================================
class OfficeActionPlugin:
    """
    负责执行具体的审批动作，如发邮件、发通知
    """

    @kernel_function(description="发送审批结果通知邮件", name="send_notification")
    def send_notification(self, employee_name: str, result: str, reason: str) -> str:
        print(f"\n    [📧 发送邮件] TO: {employee_name}@company.com")
        print(f"    [邮件主题] 关于您的远程办公申请结果")
        print(f"    [邮件内容] 结果：{result}。原因：{reason}\n")
        return "邮件发送成功"


# ==============================================================================
# 4. 主程序
# ==============================================================================
async def main():
    print(">>> 系统启动中...")

    # 初始化 Kernel
    kernel = Kernel()

    # 配置 OpenAI 服务
    service_id = "default"
    try:
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )
    except Exception as e:
        print(f"OpenAI 服务初始化失败: {e}")
        return

    # 加载插件
    kernel.add_plugin(CompanyPolicyPlugin(), plugin_name="Policy")
    kernel.add_plugin(HRDatabasePlugin(), plugin_name="HRDB")
    kernel.add_plugin(OfficeActionPlugin(), plugin_name="Office")

    # 配置自动工具调用 (SK v1.x 标准写法)
    settings = OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    chat_service = kernel.get_service(service_id)
    history = ChatHistory()

    # --- 执行任务 ---
    task = "员工 Alice 申请下周远程办公(WFH)，请根据公司政策和她的个人情况进行审批，并发送通知邮件告知她结果。"
    print(f"🔥 [接收任务]: {task}\n")
    history.add_user_message(task)

    try:
        # 获取回复
        result = await chat_service.get_chat_message_contents(
            chat_history=history,
            settings=settings,
            kernel=kernel
        )

        print("=" * 50)
        print(f"🤖 [Agent 最终反馈]:\n{result[0]}")
        print("=" * 50)

    except Exception as e:
        print(f"运行时发生错误: {e}")


# ==============================================================================
# 5. 程序入口 (标准写法)
# ==============================================================================
if __name__ == "__main__":
    # 在非 Jupyter 环境下，直接运行 asyncio.run 即可
    # 不需要 nest_asyncio
    asyncio.run(main())