#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain中各种Template类型的辨析与使用指南

此脚本详细辨析了LangChain框架中的不同类型的模板（Template），
包括它们的特点、适用场景、使用方法以及优缺点比较。

主要涵盖的模板类型：
1. PromptTemplate - 基础提示词模板
2. ChatPromptTemplate - 对话式提示词模板
3. FewShotPromptTemplate - 少样本学习提示词模板
4. FewShotChatMessagePromptTemplate - 对话式少样本学习模板
5. MessagesPlaceholder - 动态消息占位符
6. SystemMessagePromptTemplate/HumanMessagePromptTemplate - 特定角色消息模板
"""

from langchain_core.prompts import (
    PromptTemplate,                     # 基础提示词模板
    ChatPromptTemplate,                 # 对话式提示词模板
    FewShotPromptTemplate,              # 少样本学习提示词模板
    FewShotChatMessagePromptTemplate,   # 对话式少样本学习模板
    MessagesPlaceholder                 # 动态消息占位符
)
from langchain_core.prompts.chat import (
    SystemMessagePromptTemplate,        # 系统消息提示词模板
    HumanMessagePromptTemplate          # 人类消息提示词模板
)
from langchain_core.messages import HumanMessage, AIMessage

def print_separator(title):
    """打印分隔线，用于区分不同部分的输出"""
    print(f"\n{'=' * 50}")
    print(f"{title}")
    print(f"{'=' * 50}")

def demo_prompt_template():
    """1. PromptTemplate - 基础提示词模板"""
    print_separator("1. PromptTemplate - 基础提示词模板")
    
    # 创建方式1：使用构造方法
    prompt1 = PromptTemplate(
        template="你是一个{role}，请解释{topic}",
        input_variables=["role", "topic"]
    )
    
    # 创建方式2：使用from_template()方法（推荐）
    prompt2 = PromptTemplate.from_template("你是一个{role}，请解释{topic}")
    
    # 使用示例
    formatted_prompt = prompt2.format(role="技术专家", topic="机器学习")
    
    print("特点：")
    print("- 最基础、最简单的提示词模板类型")
    print("- 以单一文本字符串作为模板")
    print("- 支持使用{变量名}格式进行变量替换")
    print("- 适用于简单的文本生成场景")
    print("\n示例输出：")
    print(formatted_prompt)

def demo_chat_prompt_template():
    """2. ChatPromptTemplate - 对话式提示词模板"""
    print_separator("2. ChatPromptTemplate - 对话式提示词模板")
    
    # 创建对话提示词模板
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一位专业的{role}，请用简洁专业的语言回答问题。"),
        ("human", "请详细解释{topic}，并给出具体的例子。")
    ])
    
    # 使用示例
    prompt_value = chat_template.invoke({
        "role": "数据科学家", 
        "topic": "深度学习"
    })
    
    print("特点：")
    print("- 支持多轮对话结构，区分不同角色的消息")
    print("- 每个消息包含角色类型(system/human/ai)和内容")
    print("- 返回ChatPromptValue对象，更适合与聊天模型集成")
    print("- 适用于构建复杂的对话流程")
    print("\n消息结构：")
    print(f"消息类型: {type(prompt_value)}")
    print(f"消息数量: {len(prompt_value.messages)}")
    print(f"第一条消息: {prompt_value.messages[0]}")

def demo_few_shot_prompt_template():
    """3. FewShotPromptTemplate - 少样本学习提示词模板"""
    print_separator("3. FewShotPromptTemplate - 少样本学习提示词模板")
    
    # 准备示例数据
    examples = [
        {"input": "今天天气真好", "output": "积极"},
        {"input": "工作压力很大", "output": "消极"},
        {"input": "这个项目进展顺利", "output": "积极"},
    ]
    
    # 创建示例提示词模板
    example_prompt = PromptTemplate.from_template(
        "输入: {input}\n输出: {output}"
    )
    
    # 创建少样本提示词模板
    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="输入: {new_input}\n输出: ",
        input_variables=["new_input"]
    )
    
    # 使用示例
    formatted_prompt = few_shot_template.format(new_input="我感到很开心")
    
    print("特点：")
    print("- 支持提供少量示例来指导模型的输出")
    print("- 由示例集合、示例模板、前缀和后缀组成")
    print("- 适用于需要模型学习特定模式或格式的场景")
    print("- 可以提高模型在特定任务上的表现")
    print("\n示例输出（包含少样本学习示例）：")
    print(formatted_prompt)

def demo_few_shot_chat_template():
    """4. FewShotChatMessagePromptTemplate - 对话式少样本学习模板"""
    print_separator("4. FewShotChatMessagePromptTemplate - 对话式少样本学习模板")
    
    # 准备对话示例
    examples = [
        {
            "user_input": "什么是人工智能？",
            "ai_response": "人工智能(AI)是计算机科学的一个分支，旨在创建能够模拟人类智能的系统。"
        },
        {
            "user_input": "什么是机器学习？",
            "ai_response": "机器学习是人工智能的一个子集，它使计算机系统能够从数据中学习并改进，而无需明确编程。"
        }
    ]
    
    # 创建示例消息模板
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{user_input}"),
        ("ai", "{ai_response}")
    ])
    
    # 创建对话式少样本学习模板
    few_shot_chat_template = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt
    )
    
    # 创建最终的聊天模板
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位AI助手，擅长解释技术概念。"),
        few_shot_chat_template,
        ("human", "什么是深度学习？")
    ])
    
    # 使用示例
    prompt_value = final_prompt.invoke({})
    
    print("特点：")
    print("- 结合了ChatPromptTemplate和FewShotPromptTemplate的特点")
    print("- 支持提供对话形式的示例")
    print("- 更适合复杂的对话场景和需要示例的聊天任务")
    print("- 可以嵌套在其他ChatPromptTemplate中使用")
    print("\n消息结构：")
    print(f"消息数量: {len(prompt_value.messages)}")
    print(f"部分消息示例: {prompt_value.messages[:2]}")

def demo_messages_placeholder():
    """5. MessagesPlaceholder - 动态消息占位符"""
    print_separator("5. MessagesPlaceholder - 动态消息占位符")
    
    # 创建包含动态消息占位符的模板
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI助手，你的名字叫{name}。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    # 准备动态消息历史
    chat_history = [
        HumanMessage(content="你好，你是谁？"),
        AIMessage(content="我是一个AI助手，可以帮助你解答问题。")
    ]
    
    # 使用示例
    prompt_value = chat_template.invoke({
        "name": "小智",
        "chat_history": chat_history,
        "question": "今天天气怎么样？"
    })
    
    print("特点：")
    print("- 允许在模板中动态插入消息列表")
    print("- 特别适合实现多轮对话历史的管理")
    print("- 使模板更加灵活，能够处理不确定数量和类型的消息")
    print("- 与Memory模块结合使用效果最佳")
    print("\n完整消息序列：")
    for i, msg in enumerate(prompt_value.messages):
        print(f"消息{i+1}: {msg}")

def demo_role_message_templates():
    """6. SystemMessagePromptTemplate/HumanMessagePromptTemplate - 特定角色消息模板"""
    print_separator("6. 特定角色消息模板")
    
    # 创建系统消息模板
    system_template = "你是一位专业的{field}专家。"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    
    # 创建人类消息模板
    human_template = "请详细解释{topic}，并给出实用建议。"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    # 组合成聊天模板
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        human_message_prompt
    ])
    
    # 使用示例
    prompt_value = chat_prompt.invoke({
        "field": "人工智能",
        "topic": "大型语言模型在企业中的应用"
    })
    
    print("特点：")
    print("- 为特定角色消息提供专门的模板类")
    print("- SystemMessagePromptTemplate：用于创建系统指令消息")
    print("- HumanMessagePromptTemplate：用于创建人类问题消息")
    print("- 提供更精细的消息控制和类型区分")
    print("\n生成的角色消息：")
    for msg in prompt_value.messages:
        print(f"{msg.type}: {msg.content}")

def compare_templates():
    """7. 各类模板的综合比较"""
    print_separator("7. 各类模板的综合比较")
    
    comparison = [
        {"模板类型": "PromptTemplate", 
         "主要特点": "基础文本模板", 
         "适用场景": "简单的单轮文本生成", 
         "返回类型": "字符串", 
         "复杂度": "低", 
         "最佳实践": "简单任务首选，使用from_template()方法创建"},
        
        {"模板类型": "ChatPromptTemplate", 
         "主要特点": "支持多角色对话", 
         "适用场景": "复杂对话、多轮交互", 
         "返回类型": "ChatPromptValue", 
         "复杂度": "中", 
         "最佳实践": "使用from_messages()方法创建，适合聊天模型"},
        
        {"模板类型": "FewShotPromptTemplate", 
         "主要特点": "提供少样本学习示例", 
         "适用场景": "需要示例指导的任务", 
         "返回类型": "字符串", 
         "复杂度": "中", 
         "最佳实践": "与PromptTemplate配合使用，提高特定任务表现"},
        
        {"模板类型": "FewShotChatMessagePromptTemplate", 
         "主要特点": "对话式少样本学习", 
         "适用场景": "复杂对话中的示例学习", 
         "返回类型": "ChatPromptValue", 
         "复杂度": "高", 
         "最佳实践": "嵌套使用，适合复杂对话场景"},
        
        {"模板类型": "MessagesPlaceholder", 
         "主要特点": "动态消息占位符", 
         "适用场景": "多轮对话历史管理", 
         "返回类型": "-（作为组件使用）", 
         "复杂度": "中", 
         "最佳实践": "与Memory模块结合，处理对话历史"},
        
        {"模板类型": "角色特定模板", 
         "主要特点": "细化的角色消息控制", 
         "适用场景": "需要精确定义消息角色的场景", 
         "返回类型": "-（作为组件使用）", 
         "复杂度": "中", 
         "最佳实践": "在需要精细控制时使用"}
    ]
    
    # 打印比较表格
    print(f"{'模板类型':<30}{'主要特点':<20}{'适用场景':<25}{'返回类型':<20}{'复杂度':<10}{'最佳实践':<30}")
    print("-" * 130)
    for item in comparison:
        print(f"{item['模板类型']:<30}{item['主要特点']:<20}{item['适用场景']:<25}{item['返回类型']:<20}{item['复杂度']:<10}{item['最佳实践']:<30}")

def usage_recommendations():
    """8. 使用场景推荐"""
    print_separator("8. 使用场景推荐")
    
    recommendations = [
        {"场景": "简单的文本生成任务", "推荐模板": "PromptTemplate", "原因": "最简单直接，性能最佳"},
        {"场景": "聊天机器人开发", "推荐模板": "ChatPromptTemplate", "原因": "支持多角色对话，与聊天模型匹配度高"},
        {"场景": "需要提供示例的任务（如分类、翻译）", "推荐模板": "FewShotPromptTemplate", "原因": "通过示例指导模型输出格式和内容"},
        {"场景": "复杂对话+示例学习", "推荐模板": "FewShotChatMessagePromptTemplate", "原因": "结合了对话能力和示例学习功能"},
        {"场景": "多轮对话应用", "推荐模板": "ChatPromptTemplate + MessagesPlaceholder", "原因": "有效管理对话历史，实现上下文理解"},
        {"场景": "需要精确控制消息类型", "推荐模板": "角色特定模板组合", "原因": "提供更精细的消息角色控制"},
        {"场景": "企业级应用开发", "推荐模板": "ChatPromptTemplate", "原因": "更灵活，功能更强大，扩展性更好"},
        {"场景": "与Memory模块集成", "推荐模板": "ChatPromptTemplate + MessagesPlaceholder", "原因": "最佳的对话历史管理组合"}
    ]
    
    print(f"{'场景':<40}{'推荐模板':<40}{'原因':<40}")
    print("-" * 120)
    for rec in recommendations:
        print(f"{rec['场景']:<40}{rec['推荐模板']:<40}{rec['原因']:<40}")

def main():
    """主函数，运行所有演示和比较"""
    print("LangChain中各种Template类型的辨析与使用指南")
    print("=" * 50)
    
    # 运行各个模板的演示
    demo_prompt_template()
    demo_chat_prompt_template()
    demo_few_shot_prompt_template()
    demo_few_shot_chat_template()
    demo_messages_placeholder()
    demo_role_message_templates()
    
    # 运行综合比较和使用场景推荐
    compare_templates()
    usage_recommendations()
    
    print("\n" + "=" * 50)
    print("总结：")
    print("- PromptTemplate适用于简单场景，ChatPromptTemplate适用于复杂对话")
    print("- 少样本模板用于需要示例指导的任务")
    print("- MessagesPlaceholder是多轮对话的关键组件")
    print("- 选择模板时应根据具体任务需求和复杂度来决定")
    print("=" * 50)

if __name__ == "__main__":
    main()