#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最推荐的PromptTemplate用法和完整的大模型调用流程

此脚本演示了在LangChain框架中最常用且最推荐的PromptTemplate使用方法，
以及完整的大模型调用工作流，包括环境配置、模板创建、提示词生成、
模型调用和响应处理等关键步骤。

主要功能:
- 使用推荐的from_template()方法创建提示词模板
- 使用invoke()方法进行变量赋值（返回PromptValue对象）
- 使用partial()方法处理部分变量以提高模板复用性
- 展示完整的大模型调用流程（包含错误处理机制）
- 演示ChatPromptTemplate的高级用法

作者: LangChain教程
"""

# 导入必要的库
from langchain_core.prompts import PromptTemplate  # 基础提示词模板类
from langchain_openai import ChatOpenAI  # OpenAI聊天模型接口
import os  # 用于环境变量操作
from dotenv import load_dotenv  # 用于加载.env文件中的环境变量

# 加载环境变量（从.env文件中读取OpenAI API密钥等配置）
load_dotenv()

# 打印标题，标识脚本开始执行
print("===== 最推荐的PromptTemplate用法演示 =====")

# ===============================
# 1. 最推荐的方式：使用from_template()创建模板
# ===============================
print("\n1. 最推荐的方式：使用from_template()创建PromptTemplate")

# 【推荐写法】使用from_template()方法创建模板
# 优势：
# - 更简洁的语法，只需提供模板字符串
# - 自动从模板中推断出需要填充的变量（通过{变量名}语法识别）
# - 相比构造函数方式，减少了输入错误的可能性
prompt_template = PromptTemplate.from_template(
    "请分析{product}的{feature}特性，并提供改进建议。"
)

# 打印创建的模板对象，查看其结构和变量信息
print(f"创建的模板: {prompt_template}")
print(f"模板变量列表: {prompt_template.input_variables}")  # 查看自动推断的变量

# ===============================
# 2. 最推荐的方式：使用invoke()给变量赋值
# ===============================
print("\n2. 最推荐的方式：使用invoke()给变量赋值")

# 【推荐写法】使用invoke()方法进行变量赋值
# 优势：
# - 返回PromptValue类型对象，而非简单字符串
# - PromptValue对象可以更好地与LangChain中的其他组件（如模型）集成
# - 支持更复杂的变量类型和处理逻辑
# - 符合LangChain的LCEL（LangChain Expression Language）设计理念
prompt_value = prompt_template.invoke(
    input={"product": "智能手机", "feature": "电池续航"}  # 传入变量值字典
)

# 查看invoke()方法的返回类型和实际生成的提示词内容
print(f"invoke()返回类型: {type(prompt_value)}")  # 应该是PromptValue类型
print(f"提示词内容: {prompt_value.text}")  # 通过.text属性获取最终的提示词字符串

# ===============================
# 3. 最推荐的方式：使用partial()方法处理部分变量
# ===============================
print("\n3. 最推荐的方式：使用partial()方法处理部分变量")

# 【推荐写法】使用partial()方法创建部分填充的模板
# 优势：
# - 可以预先填充部分变量，创建更专用的模板
# - 提高模板的复用性，避免重复设置相同的变量
# - 简化后续调用时的参数传递
partial_template = prompt_template.partial(product="智能手机")
print(f"部分填充后的模板: {partial_template}")
print(f"剩余需要填充的变量: {partial_template.input_variables}")  # 只剩下feature变量

# 使用部分填充的模板 - 只需要提供剩余的变量值
partial_prompt = partial_template.invoke(input={"feature": "拍照质量"})
print(f"部分填充模板生成的提示词: {partial_prompt.text}")

# 链式调用方式（更简洁的写法）
# 优势：代码更简洁，逻辑更连贯，可以在一行中完成多个操作
chain_partial_template = (
    PromptTemplate
    .from_template("请分析{product}的{feature}特性，并提供改进建议。")  # 第一步：创建模板
    .partial(product="笔记本电脑")  # 第二步：部分填充变量
)
chain_prompt = chain_partial_template.invoke(input={"feature": "散热系统"})  # 第三步：填充剩余变量
print(f"链式调用生成的提示词: {chain_prompt.text}")

# ===============================
# 4. 完整的大模型调用流程
# ===============================
print("\n===== 完整的大模型调用流程 =====")

# 步骤1: 配置环境变量（已在顶部完成）
print("\n步骤1: 配置环境变量（OpenAI API密钥和基础URL）")
# 确保环境变量已正确设置
# 这里重新设置是为了演示完整性，并提供默认值以增强代码健壮性
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 提供默认值

# 步骤2: 创建提示词模板（最推荐的from_template方式）
print("步骤2: 创建提示词模板（使用from_template）")
# 创建一个更复杂的多变量模板，用于产品分析报告
workflow_template = PromptTemplate.from_template(
    """作为一名{role}，请分析以下产品的优缺点并提供改进建议：
产品: {product}
分析重点: {focus_points}
请给出详细的分析报告，包括具体的改进建议。"""
)  # 三引号支持多行模板字符串，更易读

# 步骤3: 使用invoke()方法生成提示词（最推荐的方式）
print("步骤3: 使用invoke()方法生成提示词")
# 填充所有变量，生成最终的提示词
workflow_prompt = workflow_template.invoke({
    "role": "产品分析师",  # 角色设定
    "product": "智能手表",  # 分析对象
    "focus_points": "续航能力、健康监测准确性、用户界面友好度"  # 分析重点
})
print(f"生成的完整提示词:\n{workflow_prompt.text}")

# 步骤4: 初始化大模型（配置参数）
print("步骤4: 初始化大模型（配置参数）")

# 【推荐写法】明确指定模型参数，提高代码可读性和可维护性
# 参数说明:
# - model: 指定使用的模型，如gpt-4o-mini, gpt-4o, gpt-3.5-turbo等
# - max_tokens: 限制生成的最大token数，控制响应长度
# - temperature: 控制生成内容的随机性（0-2，值越低越确定，值越高越有创意）
# - base_url: 模型API的基础URL，便于切换不同的服务提供商或代理
chat_model = ChatOpenAI(
    model="gpt-4o-mini",  # 选择合适的模型
    max_tokens=1000,       # 控制响应长度
    temperature=0.7,       # 控制创造性（0-2，较低值更确定）
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 明确指定基础URL
)

# 步骤5: 调用大模型处理提示词
print("步骤5: 调用大模型处理提示词（请稍候...）")

# 【推荐写法】直接将PromptValue对象传递给模型
# 优势：
# - PromptValue对象包含更丰富的信息，有利于模型进行最佳处理
# - 代码更简洁，符合LangChain的设计理念
# - 支持错误处理和备选逻辑

try:
    # 直接传递PromptValue对象给模型的invoke方法
    response = chat_model.invoke(workflow_prompt)
    
    # 步骤6: 处理大模型响应
    print("步骤6: 处理并展示大模型响应")
    # 输出响应内容
    print(f"\n大模型响应内容:\n{response.content}")
    # 查看响应的类型
    print(f"\n响应类型: {type(response)}")  # 通常是BaseMessage类型
    # 查看响应中的元数据（如token使用情况、完成原因等）
    print(f"响应元数据: {response.response_metadata}")
    
except Exception as e:
    # 错误处理机制：当调用大模型失败时（如API密钥无效、网络问题等）
    print(f"\n调用大模型时出错: {e}")
    
    # 提供备选逻辑，确保程序不会中断
    print("\n备选方案: 使用模拟响应")
    print("\n智能手表分析报告:\n")
    print("1. 续航能力：当前续航约1-2天，建议优化电池容量或降低功耗。")
    print("2. 健康监测准确性：心率和血氧监测在运动时略有偏差，建议改进传感器算法。")
    print("3. 用户界面友好度：部分功能层级较深，建议优化常用功能的快捷入口。")

# ===============================
# 5. 高级用法：使用ChatPromptTemplate创建聊天模板
# ===============================
print("\n===== 高级用法：创建聊天模板并调用 =====")

# 导入聊天模板类
from langchain_core.prompts import ChatPromptTemplate

# 【推荐写法】使用ChatPromptTemplate创建更复杂的对话模板
# 优势：
# - 支持多轮对话结构，区分系统消息、用户消息、助手消息等不同角色
# - 更贴近实际聊天场景，有利于构建复杂的对话流程
# - 可以更好地控制对话上下文和角色定位
chat_template = ChatPromptTemplate.from_messages([
    # 系统消息：设定助手的角色和背景
    ("system", "你是一位专业的{field}专家。"),
    # 用户消息：提供具体的问题或任务
    ("human", "请详细解释{topic}，并给出实用建议。")
])

# 生成聊天提示词
chat_prompt = chat_template.invoke({
    "field": "人工智能",
    "topic": "大型语言模型在企业中的应用场景"
})

# 查看生成的聊天提示词结构
print(f"生成的聊天提示词:\n{chat_prompt}")

# 调用大模型（如果环境允许）
# 这里添加了条件检查，确保API密钥存在且之前的模型调用没有出错
if os.getenv("OPENAI_API_KEY") and not isinstance(response, Exception):
    try:
        # 调用模型处理聊天提示词
        chat_response = chat_model.invoke(chat_prompt)
        # 显示部分响应内容（限制在前300个字符）
        print(f"\n大模型聊天响应:\n{chat_response.content[:300]}...")
    except Exception:
        # 如果出错，静默处理（pass）以避免影响主程序流程
        pass

print("\n===== 推荐用法总结 =====")
# 总结最推荐的PromptTemplate用法和最佳实践
print("1. 使用from_template()创建PromptTemplate实例（更简洁，自动推断变量）")
print("2. 使用invoke()方法给变量赋值（返回PromptValue，更好地与LangChain集成）")
print("3. 使用partial()方法处理部分变量（提高模板复用性，简化后续调用）")
print("4. 完整的大模型调用流程：环境配置→创建模板→生成提示词→初始化模型→调用模型→处理响应")
print("5. 对于复杂对话场景，使用ChatPromptTemplate替代基本的PromptTemplate（支持多角色对话）")

# 强调代码健壮性的重要性
print("\n提示：在实际应用中，请始终添加错误处理机制，确保程序在各种情况下都能正常运行！")

# 脚本结束标记
print("\n===== 演示完成 =====")