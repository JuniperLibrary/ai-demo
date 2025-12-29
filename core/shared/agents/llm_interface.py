#!/usr/bin/env python3
"""
大模型接口类 - 封装所有LLM调用相关逻辑
"""

import os
import json
from typing import Dict, Any, List, AsyncGenerator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

try:
    # 使用 openai 提供的 AsyncOpenAI 客户端，兼容 DashScope 的 OpenAI 模式
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    # 在未安装 openai 库的环境中，将 OPENAI_AVAILABLE 标记为 False
    # 构造函数会据此直接抛错，避免运行时才发现问题
    OPENAI_AVAILABLE = False
    print("警告: openai模块未安装，将使用模拟模式")


class LLMInterface:
    """大模型接口 - 封装所有与LLM交互的逻辑"""
    
    def __init__(self, model_name: str = None, base_url: str = None, api_key: str = None):
        # 模型名称优先使用传入参数，其次使用环境变量，最后回退到默认模型 qwen-turbo
        self.model_name = model_name or os.getenv("DASHSCOPE_MODEL_NAME", "qwen-turbo")
        # 没有 openai 库时直接失败，避免后续调用时报更隐蔽的错误
        if not OPENAI_AVAILABLE:
            raise ValueError("OpenAI模块未安装，无法使用LLM功能")
        self.client = None
        if self.client is None:
            # base_url 和 api_key 可以通过参数或环境变量传入
            base_url = base_url or os.getenv("DASHSCOPE_BASE_URL")
            api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
            # 如果都没有配置，则使用 DashScope 的 OpenAI 兼容默认值，方便本地测试
            if not base_url or not api_key:
                base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
                api_key = "test_key"
                print("使用默认环境变量进行测试")

            try:
                # 初始化异步客户端，后续所有方法通过 self.client 进行调用
                self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
            except Exception as e:
                print(f"AsyncOpenAI客户端初始化失败: {e}")
                raise
    
    def _get_client(self):
        """获取OpenAI客户端实例"""
        return self.client
    
    async def streaming_call(self, messages: List[Dict], tools: List[Dict] = None, 
                           temperature: float = 0.7) -> AsyncGenerator[Dict[str, Any], None]:
        """流式LLM调用 - 支持工具调用，统一的流式调用接口"""
        try:
            # 通过内部封装方法获取客户端，方便单元测试时进行替换
            client = self._get_client()
            # LLM 流式调用的公共参数
            api_params = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "temperature": temperature
            }
            
            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = "auto"
            
            # OpenAI 兼容接口，返回一个可以 async for 的流式响应对象
            response = await client.chat.completions.create(**api_params)
            
            # content_buffer 用于累积完整的自然语言回复
            content_buffer = ""
            # tool_calls_buffer 按工具调用的 index 聚合增量的工具调用信息
            tool_calls_buffer = []

            async for chunk in response:
                # 安全检查：确保 choices 存在且不为空
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                if not delta:
                    continue

                # 处理内容流：每次增量内容都会先推给前端，同时累积到 content_buffer
                if delta.content:
                    content_buffer += delta.content
                    yield {
                        "type": "content_chunk",
                        "content": delta.content
                    }
                
                # 处理工具调用：工具调用信息也可能以多次增量的形式返回
                if delta.tool_calls:
                    for tc_delta in delta.tool_calls:
                        # 确保 tool_calls_buffer 足够长，index 与返回的 index 对齐
                        while len(tool_calls_buffer) <= tc_delta.index:
                            tool_calls_buffer.append({
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                                "_notified": False  # 标记该工具调用是否已经通知前端
                            })
                        
                        current_tool = tool_calls_buffer[tc_delta.index]
                        
                        # 更新工具调用信息
                        if tc_delta.id:
                            current_tool["id"] = tc_delta.id
                        if tc_delta.function.name:
                            current_tool["function"]["name"] = tc_delta.function.name
                            # 第一次收到工具名称时，立即通知前端，让前端可以提前渲染工具调用占位
                            if not current_tool["_notified"]:
                                current_tool["_notified"] = True
                                yield {
                                    "type": "tool_call_start",
                                    "tool_call": {
                                        "id": current_tool["id"],
                                        "function": {"name": current_tool["function"]["name"]}
                                    },
                                    "index": tc_delta.index
                                }
                        if tc_delta.function.arguments:
                            # 工具参数通常会被拆成多个增量片段，这里直接进行字符串拼接
                            current_tool["function"]["arguments"] += tc_delta.function.arguments
            
            # 流结束，返回完整响应
            # 清理 tool_calls_buffer 中的临时字段，只保留对业务有意义的信息
            clean_tool_calls = []
            for tool_call in tool_calls_buffer:
                if tool_call["function"]["name"]:  # 只包含有效的工具调用
                    clean_call = {
                        "id": tool_call["id"],
                        "type": tool_call["type"],
                        "function": {
                            "name": tool_call["function"]["name"],
                            "arguments": tool_call["function"]["arguments"]
                        }
                    }
                    clean_tool_calls.append(clean_call)
            
            yield {
                "type": "stream_complete",
                "content": content_buffer,
                "tool_calls": clean_tool_calls
            }
                    
        except Exception as e:
            print(f"流式LLM调用失败: {e}")
            yield {
                "type": "error",
                "error": str(e)
            }
    
    async def non_streaming_call(self, messages: List[Dict], tools: List[Dict] = None,
                                temperature: float = 0.1, max_tokens: int = None) -> Dict[str, Any]:
        """非流式LLM调用 - 统一的非流式调用接口，支持工具调用"""
        try:
            client = self._get_client()

            # LLM非流式调用
            api_params = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "temperature": temperature
            }

            # 添加max_tokens参数(如果指定)
            if max_tokens:
                api_params["max_tokens"] = max_tokens

            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = "auto"

            response = await client.chat.completions.create(**api_params)
            message = response.choices[0].message
            
            # 转换 tool_calls 为标准字典格式，保持与 streaming_call 一致
            tool_calls = []
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_calls.append({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
            
            # 非流式接口统一返回 content + tool_calls 两个字段
            return {
                "content": message.content or "",
                "tool_calls": tool_calls
            }
            
        except Exception as e:
            print(f"LLM调用失败: {e}")
            raise
    
    async def simple_call(self, system_prompt: str, user_input: str,
                         temperature: float = 0.1, max_tokens: int = None) -> str:
        """简单调用 - 便捷方法，用于简单的分析任务

        Args:
            system_prompt: 系统提示词
            user_input: 用户输入
            temperature: 温度参数(0-1)
            max_tokens: 最大输出token数,默认None(使用模型默认值)

        Returns:
            模型响应内容
        """
        # simple_call 只是对 non_streaming_call 的一层封装，自动构造 messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        # 打印调试信息，方便在本地排查 prompt 结构问题
        print(f"=== 简单调用 ==={json.dumps(messages, ensure_ascii=False)}" )
        try:
            response = await self.non_streaming_call(
                messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            # 对返回文本做 strip，去除首尾多余空白字符
            return response["content"].strip()
        except Exception as e:
            print(f"简单调用失败: {e}")
            return "error"

    
    def get_model_info(self) -> Dict[str, str]:
        """获取当前模型信息"""
        return {
            "model_name": self.model_name,
            "base_url": os.getenv("OPENAI_BASE_URL", "default"),
            "available": str(OPENAI_AVAILABLE)
        }

    async def code_agent_call(
        self, 
        messages: List[Dict], 
        tools: List[Dict] = None,
        temperature: float = 0.1
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """专为代码生成Agent设计的流式调用接口"""
        try:
            client = self._get_client()
            
            api_params = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "temperature": temperature
            }
            
            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = "auto"
            
            response = await client.chat.completions.create(**api_params)
            
            assistant_message = ""
            tool_calls_by_index = {}

            # 使用 async for 循环处理流式响应
            async for chunk in response:
                # 安全检查：确保 choices 存在且不为空
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                if not delta:
                    continue

                # 处理内容流
                if delta.content:
                    assistant_message += delta.content
                    yield {
                        "type": "content",
                        "content": delta.content
                    }
                
                # 处理工具调用
                if delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        index = tool_call_delta.index
                        
                        # 初始化工具调用
                        if index not in tool_calls_by_index:
                            tool_calls_by_index[index] = {
                                "id": "",
                                "type": "function",
                                "function": {
                                    "name": "",
                                    "arguments": ""
                                }
                            }
                        
                        # 更新工具调用信息
                        if tool_call_delta.id:
                            tool_calls_by_index[index]["id"] = tool_call_delta.id
                        
                        if tool_call_delta.function:
                            if tool_call_delta.function.name:
                                tool_calls_by_index[index]["function"]["name"] = tool_call_delta.function.name
                            if tool_call_delta.function.arguments:
                                tool_calls_by_index[index]["function"]["arguments"] += tool_call_delta.function.arguments
            
            # 验证和清理工具调用
            valid_tool_calls = []
            for index in sorted(tool_calls_by_index.keys()):
                tool_call = tool_calls_by_index[index]
                
                # 验证工具调用完整性
                if tool_call["id"] and tool_call["function"]["name"]:
                    # 验证和修复JSON参数
                    args_str = tool_call["function"]["arguments"].strip()
                    
                    if args_str:
                        try:
                            # 先直接尝试解析JSON
                            test_parse = json.loads(args_str)
                            print(f"🔧 JSON验证成功: {test_parse}")
                            # JSON有效，保持原样
                            tool_call["function"]["arguments"] = args_str
                        except json.JSONDecodeError as e:
                            print(f"⚠️ 工具参数JSON无效: {args_str}, 错误: {e}")
                            # 尝试修复常见问题
                            try:
                                import re
                                # 修复单引号问题 - 更精确的正则表达式
                                fixed_args = args_str
                                # 修复字典键的单引号
                                fixed_args = re.sub(r"'(\w+)':", r'"\1":', fixed_args)
                                # 修复字符串值的单引号
                                fixed_args = re.sub(r":\s*'([^']*)'", r': "\1"', fixed_args)
                                # 修复布尔值
                                fixed_args = re.sub(r'\btrue\b', 'true', fixed_args)
                                fixed_args = re.sub(r'\bfalse\b', 'false', fixed_args)
                                
                                test_parse = json.loads(fixed_args)
                                tool_call["function"]["arguments"] = fixed_args
                                print(f"🔧 JSON修复成功: {test_parse}")
                            except Exception as fix_error:
                                print(f"🔧 正则修复失败: {fix_error}")
                                # 尝试使用ast.literal_eval作为备选
                                try:
                                    import ast
                                    test_parse = ast.literal_eval(args_str)
                                    # 转换为JSON格式
                                    tool_call["function"]["arguments"] = json.dumps(test_parse, ensure_ascii=False)
                                    print(f"🔧 使用ast.literal_eval修复成功")
                                except Exception as e2:
                                    print(f"❌ 所有修复方法都失败，保留原始参数: {args_str}")
                                    # 保留原始参数，不要设为空对象
                                    tool_call["function"]["arguments"] = args_str
                    else:
                        tool_call["function"]["arguments"] = "{}"
                    
                    valid_tool_calls.append(tool_call)
                    
                    # 发送单个工具调用完成事件
                    yield {
                        "type": "tool_call_complete",
                        "tool_call": tool_call
                    }
            
            # 返回完整响应
            yield {
                "type": "assistant_message_complete",
                "content": assistant_message,
                "tool_calls": valid_tool_calls
            }
                    
        except Exception as e:
            print(f"代码Agent LLM调用失败: {e}")
            yield {
                "type": "error",
                "error": str(e)
            }
