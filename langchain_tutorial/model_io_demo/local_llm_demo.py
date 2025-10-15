#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LangChain调用本地大模型的多种方法演示

此脚本展示了使用LangChain框架调用本地大模型（通过Ollama）的多种方法，
包括基本调用、使用提示词模板、流式响应、参数配置、异步调用等高级特性。
"""

import asyncio
import time
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


def print_separator(title):
    """打印分隔线，使输出更清晰"""
    print(f"\n{'='*30} {title} {'='*30}\n")


def basic_usage_demo():
    """1. 基本调用方法演示"""
    print_separator("基本调用方法")
    
    # 初始化本地大模型
    # 注意：需要先安装Ollama并下载相应的模型
    llm = ChatOllama(
        model="deepseek-r1:1.5b"  # 可以替换为其他本地模型，如 "llama2:latest"
    )
    
    # 方法1：直接传入字符串
    print("\n方法1: 直接传入字符串")
    response = llm.invoke("你好，请简单介绍一下你自己！")
    print(f"响应内容: {response.content}")
    
    # 方法2：使用HumanMessage对象
    print("\n方法2: 使用HumanMessage对象")
    messages = [HumanMessage(content="你好，请简单介绍一下你自己！")]
    response = llm.invoke(messages)
    print(f"响应内容: {response.content}")
    
    return llm


def chat_prompt_template_demo(llm):
    """2. 使用ChatPromptTemplate创建结构化提示"""
    print_separator("使用ChatPromptTemplate")
    
    # 创建聊天提示词模板
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一位专业的{role}，请用简洁专业的语言回答问题。"),
        ("human", "请解释{topic}，并给出具体的例子。")
    ])
    
    # 使用模板生成提示词
    prompt = template.invoke({"role": "技术顾问", "topic": "机器学习中的监督学习"})
    print(f"生成的提示词结构: {prompt}")
    
    # 使用生成的提示词调用模型
    response = llm.invoke(prompt)
    print(f"\n模型响应: {response.content}")


def streaming_response_demo(llm):
    """3. 流式响应演示"""
    print_separator("流式响应")
    
    print("\n流式输出响应内容:")
    start_time = time.time()
    
    # 使用stream=True启用流式响应
    for chunk in llm.stream("请详细解释什么是人工智能，以及它与机器学习的区别。"):
        print(chunk.content, end="", flush=True)
    
    print(f"\n\n流式响应耗时: {time.time() - start_time:.2f}秒")


def parameters_configuration_demo():
    """4. 模型参数配置演示"""
    print_separator("模型参数配置")
    
    # 配置不同参数的模型实例
    
    # 参数说明:
    # - model: 使用的模型名称
    # - temperature: 控制响应的随机性 (0.0-2.0，越低越确定，越高越有创意)
    # - max_tokens: 限制生成的最大token数
    # - top_p: 控制token采样的累积概率，较低值会使输出更集中
    # - num_ctx: 上下文窗口大小
    
    # 创建确定性较高的模型
    deterministic_llm = ChatOllama(
        model="deepseek-r1:1.5b",
        temperature=0.1,  # 低温度，输出更确定
        max_tokens=300,   # 限制响应长度
        top_p=0.9         # 适当的top_p值
    )
    
    # 创建更具创造性的模型
    creative_llm = ChatOllama(
        model="deepseek-r1:1.5b",
        temperature=1.0,  # 高温度，输出更有创意
        max_tokens=300,
        top_p=0.95
    )
    
    question = "请描述一下未来5年人工智能可能的发展方向。"
    
    print("\n【确定性较高的回答】:")
    deterministic_response = deterministic_llm.invoke(question)
    print(deterministic_response.content)
    
    print("\n【创造性较高的回答】:")
    creative_response = creative_llm.invoke(question)
    print(creative_response.content)
    
    return deterministic_llm  # 返回一个配置好的模型供后续使用


def multi_turn_conversation_demo(llm):
    """5. 多轮对话演示"""
    print_separator("多轮对话")
    
    # 多轮对话需要维护消息历史
    messages = [
        SystemMessage(content="你是一位友好的助手，善于解答技术问题。"),
        HumanMessage(content="什么是Python？")
    ]
    
    # 第一轮响应
    response = llm.invoke(messages)
    print(f"助手: {response.content}")
    
    # 将助手的响应添加到消息历史中
    messages.append(AIMessage(content=response.content))
    
    # 添加第二轮问题
    messages.append(HumanMessage(content="Python的主要优势是什么？"))
    
    # 第二轮响应
    response = llm.invoke(messages)
    print(f"助手: {response.content}")


async def async_invoke_demo(llm):
    """6. 异步调用演示"""
    print_separator("异步调用")
    
    # 异步调用单个请求
    start_time = time.time()
    response = await llm.ainvoke("请简单介绍一下LangChain框架。")
    print(f"异步调用结果: {response.content}")
    print(f"异步调用耗时: {time.time() - start_time:.2f}秒")
    
    # 并发异步调用多个请求
    print("\n并发异步调用多个请求:")
    start_time = time.time()
    
    tasks = [
        llm.ainvoke("什么是机器学习？"),
        llm.ainvoke("什么是深度学习？"),
        llm.ainvoke("什么是自然语言处理？")
    ]
    
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"\n问题 {i+1} 的响应: {result.content}")
    
    print(f"\n并发异步调用总耗时: {time.time() - start_time:.2f}秒")


def batch_processing_demo(llm):
    """7. 批量处理演示"""
    print_separator("批量处理")
    
    # 准备多条消息
    batch_messages = [
        [HumanMessage(content="Python的主要特点是什么？")],
        [HumanMessage(content="如何安装Python？")],
        [HumanMessage(content="Python中有哪些常用的数据类型？")]
    ]
    
    print("批量处理多条消息:")
    start_time = time.time()
    
    # 使用batch方法批量处理
    results = llm.batch(batch_messages)
    
    for i, result in enumerate(results):
        print(f"\n问题 {i+1} 的响应: {result.content}")
    
    print(f"\n批量处理耗时: {time.time() - start_time:.2f}秒")


def custom_output_format_demo(llm):
    """8. 自定义输出格式演示"""
    print_separator("自定义输出格式")
    
    # 使用提示词指导模型生成特定格式的输出
    prompt_with_format = """
请将下列问题回答为JSON格式，包含"question"和"answer"字段：
问题：什么是计算机科学？
    """
    
    response = llm.invoke(prompt_with_format)
    print(f"JSON格式输出:\n{response.content}")
    
    # 使用系统消息指导输出格式
    messages = [
        SystemMessage(content="你的回答必须以XML格式输出，包含在<response>标签内。"),
        HumanMessage(content="什么是人工智能？")
    ]
    
    response = llm.invoke(messages)
    print(f"\nXML格式输出:\n{response.content}")


def error_handling_demo():
    """9. 错误处理演示"""
    print_separator("错误处理")
    
    try:
        # 尝试使用一个可能不存在的模型
        invalid_llm = ChatOllama(model="non_existent_model")
        response = invalid_llm.invoke("你好")
        print(response.content)
    except Exception as e:
        print(f"\n捕获到错误: {type(e).__name__}: {str(e)}")
        print("\n错误处理建议：")
        print("1. 确保Ollama已正确安装")
        print("2. 检查指定的模型名称是否正确")
        print("3. 确保模型已通过Ollama下载")
        print("4. 检查Ollama服务是否正在运行")


def main():
    """主函数，运行所有演示"""
    print("LangChain调用本地大模型的多种方法演示\n")
    
    try:
        # 运行基本调用演示
        llm = basic_usage_demo()
        
        # 运行其他演示
        chat_prompt_template_demo(llm)
        streaming_response_demo(llm)
        configured_llm = parameters_configuration_demo()
        multi_turn_conversation_demo(configured_llm)
        
        # 运行异步演示
        asyncio.run(async_invoke_demo(configured_llm))
        
        # 继续运行其他演示
        batch_processing_demo(configured_llm)
        custom_output_format_demo(configured_llm)
        error_handling_demo()
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except ImportError as e:
        print(f"\n导入错误: {e}")
        print("请确保已安装所需的依赖: pip install langchain langchain-ollama")
    except Exception as e:
        print(f"\n演示过程中发生错误: {e}")
    finally:
        print("\n\n所有演示完成！")


if __name__ == "__main__":
    main()