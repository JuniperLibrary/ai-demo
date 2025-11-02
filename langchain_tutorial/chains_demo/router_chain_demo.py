#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangChain RouterChain 示例演示

本文件展示了RouterChain的基本概念、实现和使用方法。
RouterChain用于根据输入特征将请求智能路由到不同的处理链。
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.router import RouterRunnable
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化语言模型
chat_model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


def create_router_chain():
    """
    创建一个简单的RouterChain示例
    
    在现代LangChain中，RouterChain的功能通常通过RouterRunnable实现
    这个函数演示如何根据输入问题的领域将请求路由到不同的专业链
    """
    # 定义不同领域的处理链
    
    # 1. 数学问题处理链
    math_prompt = ChatPromptTemplate.from_template(
        "你是一位数学专家，请详细解答以下数学问题：\n{query}"
    )
    math_chain = math_prompt | chat_model | StrOutputParser()
    
    # 2. 编程问题处理链
    coding_prompt = ChatPromptTemplate.from_template(
        "你是一位编程专家，请详细解答以下编程问题：\n{query}"
    )
    coding_chain = coding_prompt | chat_model | StrOutputParser()
    
    # 3. 历史问题处理链
    history_prompt = ChatPromptTemplate.from_template(
        "你是一位历史专家，请详细解答以下历史问题：\n{query}"
    )
    history_chain = history_prompt | chat_model | StrOutputParser()
    
    # 创建路由函数，根据输入内容决定使用哪个链
    def route_query(query: str):
        """
        根据查询内容确定应该使用哪个专业链
        
        在更复杂的场景中，这个函数可以使用LLM来进行意图识别
        """
        query_lower = query.lower()
        
        # 简单的关键词匹配路由逻辑
        if any(keyword in query_lower for keyword in ["计算", "数学", "方程", "几何", "代数"]):
            return math_chain
        elif any(keyword in query_lower for keyword in ["代码", "编程", "python", "java", "算法"]):
            return coding_chain
        elif any(keyword in query_lower for keyword in ["历史", "朝代", "战争", "人物", "事件"]):
            return history_chain
        else:
            # 默认返回数学链
            return math_chain
    
    # 创建路由运行时
    router_chain = RunnableLambda(route_query)
    
    return router_chain


def create_advanced_router_chain():
    """
    创建一个更高级的RouterChain示例
    使用LLM来智能决定路由
    """
    # 定义不同的专业处理链（与上面相同）
    math_prompt = ChatPromptTemplate.from_template(
        "你是一位数学专家，请详细解答以下数学问题：\n{query}"
    )
    math_chain = math_prompt | chat_model | StrOutputParser()
    
    coding_prompt = ChatPromptTemplate.from_template(
        "你是一位编程专家，请详细解答以下编程问题：\n{query}"
    )
    coding_chain = coding_prompt | chat_model | StrOutputParser()
    
    history_prompt = ChatPromptTemplate.from_template(
        "你是一位历史专家，请详细解答以下历史问题：\n{query}"
    )
    history_chain = history_prompt | chat_model | StrOutputParser()
    
    # 创建一个使用LLM进行路由决策的函数
    router_prompt = ChatPromptTemplate.from_template(
        "请分析用户的问题，确定它属于哪个类别（数学、编程或历史）：\n\n问题：{query}\n\n请只返回一个词：数学、编程或历史"
    )
    
    # 创建路由决策链
    router_decision_chain = router_prompt | chat_model | StrOutputParser()
    
    # 创建路由映射
    chain_map = {
        "数学": math_chain,
        "编程": coding_chain,
        "历史": history_chain
    }
    
    # 定义完整的路由逻辑
    def route_with_llm(input_data: dict):
        # 使用LLM确定类别
        category = router_decision_chain.invoke(input_data)
        # 根据类别选择对应的链
        selected_chain = chain_map.get(category, math_chain)  # 默认使用数学链
        # 执行选中的链
        return selected_chain.invoke(input_data)
    
    # 创建最终的路由链
    advanced_router_chain = RunnableLambda(route_with_llm)
    
    return advanced_router_chain


def main():
    """
    主函数，演示RouterChain的使用
    """
    print("=== LangChain RouterChain 示例 ===\n")
    
    # 创建简单的路由链
    simple_router = create_router_chain()
    print("1. 简单路由链示例：")
    print("问题：1 + 2 * 3 = ?")
    response1 = simple_router.invoke("1 + 2 * 3 = ?")
    print(f"回答：{response1}\n")
    
    print("问题：Python中如何实现快速排序？")
    response2 = simple_router.invoke("Python中如何实现快速排序？")
    print(f"回答：{response2}\n")
    
    # 创建高级路由链（使用LLM进行路由决策）
    advanced_router = create_advanced_router_chain()
    print("\n2. 高级路由链示例（使用LLM进行智能路由）：")
    print("问题：唐朝的开国皇帝是谁？")
    response3 = advanced_router.invoke({"query": "唐朝的开国皇帝是谁？"})
    print(f"回答：{response3}\n")
    
    print("3. 总结RouterChain的核心概念：")
    print("- RouterChain用于根据输入特征将请求智能路由到不同的处理链")
    print("- 在现代LangChain中，通常使用RouterRunnable或自定义RunnableLambda实现")
    print("- 它由两部分组成：路由逻辑和多个目标处理链")
    print("- 适用于构建多领域专家系统、复杂问答机器人等场景")
    print("- 可以使用简单规则或LLM进行智能路由决策")


if __name__ == "__main__":
    main()