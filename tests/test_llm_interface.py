import asyncio
import json
import os
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from core.shared.agents.llm_interface import LLMInterface


# 下面这一组 Fake 类用于模拟 OpenAI 兼容客户端的行为，
# 这样测试用例不需要真实访问网络，也不会依赖真实的 DashScope/OpenAI 服务。
class FakeChatCompletions:
    def __init__(self, stream_chunks=None, non_stream_response=None):
        # stream 模式下要按顺序返回的 chunk 列表
        self._stream_chunks = stream_chunks or []
        # 非流式调用时返回的完整响应对象
        self._non_stream_response = non_stream_response

    async def create(self, **kwargs):
        # 根据参数中是否包含 stream=True 来决定走哪种逻辑
        if kwargs.get("stream"):
            # 使用 async 生成器模拟服务端的流式返回
            async def gen():
                for chunk in self._stream_chunks:
                    yield chunk

            return gen()
        # 非流式调用直接返回预设的响应
        return self._non_stream_response


class FakeChat:
    def __init__(self, stream_chunks=None, non_stream_response=None):
        # 模拟 openai.AsyncOpenAI().chat.completions 这一层级结构
        self.completions = FakeChatCompletions(
            stream_chunks=stream_chunks,
            non_stream_response=non_stream_response,
        )


class FakeClient:
    def __init__(self, stream_chunks=None, non_stream_response=None):
        # 模拟 AsyncOpenAI 客户端对象，只关注 chat 字段即可
        self.chat = FakeChat(
            stream_chunks=stream_chunks,
            non_stream_response=non_stream_response,
        )


class LLMInterfaceBaseTest(unittest.TestCase):
    # 基础功能测试：环境变量与初始化逻辑
    def setUp(self):
        # 先备份原有环境变量，测试结束后要恢复
        self.original_env = os.environ.copy()

    def tearDown(self):
        # 恢复环境变量，避免对其他测试或运行环境造成影响
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_get_model_info_contains_expected_keys(self):
        # 设置模型名和 base_url 相关环境变量
        os.environ["DASHSCOPE_MODEL_NAME"] = "test-model"
        os.environ["OPENAI_BASE_URL"] = "http://example.com"
        interface = LLMInterface()
        info = interface.get_model_info()
        # 确保返回的模型信息中包含我们期望的字段和值
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["base_url"], "http://example.com")
        self.assertIn("available", info)

    def test_init_uses_default_env_when_missing(self):
        # 删除和 DashScope 相关的环境变量，模拟未配置的情况
        for key in ["DASHSCOPE_MODEL_NAME", "DASHSCOPE_BASE_URL", "DASHSCOPE_API_KEY"]:
            os.environ.pop(key, None)
        # 如果没有抛出异常，说明内部会使用默认值完成初始化
        interface = LLMInterface()
        self.assertIsNotNone(interface._get_client())


class LLMInterfaceNonStreamingTest(unittest.IsolatedAsyncioTestCase):
    # 针对 non_streaming_call 和 simple_call 的行为做验证
    async def test_non_streaming_call_returns_content_and_tool_calls(self):
        # 构造 message.tool_calls 的模拟结构，格式对齐 openai 返回值
        tool_call = SimpleNamespace(
            id="call_1",
            type="function",
            function=SimpleNamespace(
                name="test_tool",
                arguments='{"arg": 1}',
            ),
        )
        message = SimpleNamespace(
            content="result",
            tool_calls=[tool_call],
        )
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=message)],
        )
        # non_stream 模式下 FakeClient 直接返回上述 response
        client = FakeClient(non_stream_response=response)
        interface = LLMInterface()
        # 覆盖 _get_client，使其返回我们的假客户端
        interface._get_client = lambda: client
        # 触发 non_streaming_call，同时传入 tools / temperature / max_tokens
        result = await interface.non_streaming_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=[{"name": "test_tool"}],
            temperature=0.2,
            max_tokens=64,
        )
        # 校验 content 字段和解析后的 tool_calls 结构
        self.assertEqual(result["content"], "result")
        self.assertEqual(len(result["tool_calls"]), 1)
        self.assertEqual(result["tool_calls"][0]["id"], "call_1")
        self.assertEqual(result["tool_calls"][0]["type"], "function")
        self.assertEqual(
            result["tool_calls"][0]["function"]["name"],
            "test_tool",
        )
        self.assertEqual(
            result["tool_calls"][0]["function"]["arguments"],
            '{"arg": 1}',
        )

    async def test_simple_call_uses_non_streaming_call(self):
        # 这里不关心底层 client，只关心 simple_call 是否正确调用 non_streaming_call
        interface = LLMInterface()

        async def fake_non_streaming_call(messages, tools=None, temperature=0.1, max_tokens=None):
            # 返回带空格的字符串，方便后面验证 strip 行为
            return {"content": " answer "}

        # 用一个假的 non_streaming_call 覆盖原方法
        interface.non_streaming_call = fake_non_streaming_call
        result = await interface.simple_call(
            system_prompt="sys",
            user_input="user",
            temperature=0.3,
            max_tokens=32,
        )
        # simple_call 内部会对字符串做 strip
        self.assertEqual(result, "answer")


class LLMInterfaceStreamingTest(unittest.IsolatedAsyncioTestCase):
    # 针对通用 streaming_call 的行为测试，包含纯文本流和工具调用两种场景
    async def test_streaming_call_yields_content_and_completion(self):
        # 构造两个 content 增量的 delta，用 SimpleNamespace 模拟 openai 的返回结构
        delta1 = SimpleNamespace(
            content="Hello",
            tool_calls=None,
        )
        delta2 = SimpleNamespace(
            content=" world",
            tool_calls=None,
        )
        chunk1 = SimpleNamespace(choices=[SimpleNamespace(delta=delta1)])
        chunk2 = SimpleNamespace(choices=[SimpleNamespace(delta=delta2)])
        stream_chunks = [chunk1, chunk2]
        client = FakeClient(stream_chunks=stream_chunks)
        interface = LLMInterface()
        interface._get_client = lambda: client
        events = []
        # 收集 streaming_call 过程中产生的所有事件
        async for event in interface.streaming_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=None,
            temperature=0.5,
        ):
            events.append(event)
        # 拆分出内容增量事件与最终完成事件
        content_chunks = [e for e in events if e["type"] == "content_chunk"]
        completion_events = [e for e in events if e["type"] == "stream_complete"]
        # content_chunk 的 content 累加后应该等于最终结果
        self.assertEqual("".join(c["content"] for c in content_chunks), "Hello world")
        self.assertEqual(len(completion_events), 1)
        self.assertEqual(completion_events[0]["content"], "Hello world")
        self.assertEqual(completion_events[0]["tool_calls"], [])

    async def test_streaming_call_with_tool_calls(self):
        # 第一块只带工具名称，不带参数
        tool_delta_name = SimpleNamespace(
            name="test_tool",
            arguments="",
        )
        # 第二块只带参数，不带名称，模拟真实流式工具参数分片
        tool_delta_args = SimpleNamespace(
            name=None,
            arguments='{"x": 1}',
        )
        tool_call_chunk1 = SimpleNamespace(
            index=0,
            id="tool_1",
            function=tool_delta_name,
        )
        tool_call_chunk2 = SimpleNamespace(
            index=0,
            id=None,
            function=tool_delta_args,
        )
        delta1 = SimpleNamespace(
            content=None,
            tool_calls=[tool_call_chunk1],
        )
        delta2 = SimpleNamespace(
            content=None,
            tool_calls=[tool_call_chunk2],
        )
        chunk1 = SimpleNamespace(choices=[SimpleNamespace(delta=delta1)])
        chunk2 = SimpleNamespace(choices=[SimpleNamespace(delta=delta2)])
        client = FakeClient(stream_chunks=[chunk1, chunk2])
        interface = LLMInterface()
        interface._get_client = lambda: client
        events = []
        async for event in interface.streaming_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=[{"name": "test_tool"}],
            temperature=0.5,
        ):
            events.append(event)
        # 工具名称第一次出现时会立刻发送 tool_call_start 事件
        tool_start_events = [e for e in events if e["type"] == "tool_call_start"]
        # 流结束时会发送 stream_complete 汇总事件
        completion_events = [e for e in events if e["type"] == "stream_complete"]
        self.assertEqual(len(tool_start_events), 1)
        self.assertEqual(tool_start_events[0]["tool_call"]["id"], "tool_1")
        self.assertEqual(
            tool_start_events[0]["tool_call"]["function"]["name"],
            "test_tool",
        )
        self.assertEqual(len(completion_events), 1)
        self.assertEqual(len(completion_events[0]["tool_calls"]), 1)
        tool_call = completion_events[0]["tool_calls"][0]
        # 最终汇总的工具调用信息需要包含完整的 id / name / arguments
        self.assertEqual(tool_call["id"], "tool_1")
        self.assertEqual(tool_call["function"]["name"], "test_tool")
        self.assertEqual(tool_call["function"]["arguments"], '{"x": 1}')


class LLMInterfaceCodeAgentTest(unittest.IsolatedAsyncioTestCase):
    # 针对 code_agent_call 的行为测试，包括内容流、工具调用及 JSON 修复逻辑
    async def test_code_agent_call_emits_content_and_completion(self):
        # 只关注纯文本增量逻辑，不携带任何工具调用
        delta1 = SimpleNamespace(
            content="code ",
            tool_calls=None,
        )
        delta2 = SimpleNamespace(
            content="result",
            tool_calls=None,
        )
        chunk1 = SimpleNamespace(choices=[SimpleNamespace(delta=delta1)])
        chunk2 = SimpleNamespace(choices=[SimpleNamespace(delta=delta2)])
        client = FakeClient(stream_chunks=[chunk1, chunk2])
        interface = LLMInterface()
        interface._get_client = lambda: client
        events = []
        async for event in interface.code_agent_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=None,
            temperature=0.1,
        ):
            events.append(event)
        content_events = [e for e in events if e["type"] == "content"]
        final_events = [
            e for e in events if e["type"] == "assistant_message_complete"
        ]
        # 所有 content 事件拼接后的结果应该和最终 complete 中的 content 保持一致
        self.assertEqual(
            "".join(e["content"] for e in content_events),
            "code result",
        )
        self.assertEqual(len(final_events), 1)
        self.assertEqual(final_events[0]["content"], "code result")
        self.assertEqual(final_events[0]["tool_calls"], [])

    async def test_code_agent_call_valid_tool_call_json(self):
        # 构造一段已经是合法 JSON 的工具调用参数
        tool_delta = SimpleNamespace(
            name="run_tool",
            arguments='{"a": 1}',
        )
        tool_call_delta = SimpleNamespace(
            index=0,
            id="call_1",
            function=tool_delta,
        )
        delta = SimpleNamespace(
            content=None,
            tool_calls=[tool_call_delta],
        )
        chunk = SimpleNamespace(choices=[SimpleNamespace(delta=delta)])
        client = FakeClient(stream_chunks=[chunk])
        interface = LLMInterface()
        interface._get_client = lambda: client
        events = []
        async for event in interface.code_agent_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=[{"name": "run_tool"}],
            temperature=0.1,
        ):
            events.append(event)
        # 工具调用完成后会产生 tool_call_complete 事件
        tool_complete_events = [
            e for e in events if e["type"] == "tool_call_complete"
        ]
        # 流结束后会产生一条 assistant_message_complete 事件
        final_events = [
            e for e in events if e["type"] == "assistant_message_complete"
        ]
        self.assertEqual(len(tool_complete_events), 1)
        tool_call = tool_complete_events[0]["tool_call"]
        self.assertEqual(tool_call["id"], "call_1")
        self.assertEqual(tool_call["function"]["name"], "run_tool")
        # arguments 必须是合法 JSON 字符串，可以被 json.loads 正常解析
        json.loads(tool_call["function"]["arguments"])
        self.assertEqual(len(final_events), 1)
        self.assertEqual(final_events[0]["tool_calls"], [tool_call])

    async def test_code_agent_call_repairs_invalid_json_arguments(self):
        # 这里模拟的是 LLM 返回 Python 风格的 dict 字符串，需要通过内部修复逻辑转成 JSON
        tool_delta = SimpleNamespace(
            name="run_tool",
            arguments="{'a': 1}",
        )
        tool_call_delta = SimpleNamespace(
            index=0,
            id="call_1",
            function=tool_delta,
        )
        delta = SimpleNamespace(
            content=None,
            tool_calls=[tool_call_delta],
        )
        chunk = SimpleNamespace(choices=[SimpleNamespace(delta=delta)])
        client = FakeClient(stream_chunks=[chunk])
        interface = LLMInterface()
        interface._get_client = lambda: client
        events = []
        async for event in interface.code_agent_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=[{"name": "run_tool"}],
            temperature=0.1,
        ):
            events.append(event)
        tool_complete_events = [
            e for e in events if e["type"] == "tool_call_complete"
        ]
        self.assertEqual(len(tool_complete_events), 1)
        tool_call = tool_complete_events[0]["tool_call"]
        repaired = tool_call["function"]["arguments"]
        # 修复后的字符串应该是合法的 JSON，并且键值与原始含义一致
        parsed = json.loads(repaired)
        self.assertEqual(parsed["a"], 1)


class LLMInterfaceErrorHandlingTest(unittest.IsolatedAsyncioTestCase):
    # 异常处理相关测试，确保 streaming_call 和 code_agent_call 在出错时不会抛出未捕获异常
    async def test_streaming_call_catches_exceptions_and_yields_error(self):
        # 构造一个会在 create 被调用时立刻抛异常的客户端
        class FailingClient:
            def __init__(self, error):
                self.chat = SimpleNamespace(
                    completions=SimpleNamespace(
                        create=self.create,
                    ),
                )
                self._error = error

            async def create(self, **kwargs):
                raise self._error

        interface = LLMInterface()
        interface._get_client = lambda: FailingClient(RuntimeError("fail"))
        events = []
        async for event in interface.streaming_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=None,
            temperature=0.1,
        ):
            events.append(event)
        # 最后一条事件应该是 type=error，并且包含异常信息
        self.assertEqual(events[-1]["type"], "error")
        self.assertIn("fail", events[-1]["error"])

    async def test_code_agent_call_catches_exceptions_and_yields_error(self):
        # 与上面类似，只是针对 code_agent_call 接口
        class FailingClient:
            def __init__(self, error):
                self.chat = SimpleNamespace(
                    completions=SimpleNamespace(
                        create=self.create,
                    ),
                )
                self._error = error

            async def create(self, **kwargs):
                raise self._error

        interface = LLMInterface()
        interface._get_client = lambda: FailingClient(RuntimeError("fail"))
        events = []
        async for event in interface.code_agent_call(
            messages=[{"role": "user", "content": "hi"}],
            tools=None,
            temperature=0.1,
        ):
            events.append(event)
        self.assertEqual(events[-1]["type"], "error")
        self.assertIn("fail", events[-1]["error"])


class LLMInterfaceScenarioTest(unittest.IsolatedAsyncioTestCase):
    # 模拟真实用户场景的测试类
    # 演示如何在测试中构造特定问题并验证大模型的预期行为（使用 Mock）

    async def test_scenario_coding_question(self):
        # 场景1：用户让模型写一个Python加法函数
        # 模拟用户的具体提问
        user_question = "请写一个Python函数计算两个数的和"
        
        # 模拟大模型的分段响应
        delta1 = SimpleNamespace(content="好的，", tool_calls=None)
        delta2 = SimpleNamespace(content="这是一个简单的加法函数：\n", tool_calls=None)
        delta3 = SimpleNamespace(content="```python\ndef add(a, b):\n    return a + b\n```", tool_calls=None)
        
        # 构造流式返回块
        chunks = [
            SimpleNamespace(choices=[SimpleNamespace(delta=delta1)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=delta2)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=delta3)]),
        ]
        
        # 设置 Mock 客户端
        client = FakeClient(stream_chunks=chunks)
        interface = LLMInterface()
        interface._get_client = lambda: client
        
        # 调用接口
        full_content = ""
        async for event in interface.streaming_call(
            messages=[{"role": "user", "content": user_question}],
            tools=None
        ):
            if event["type"] == "content_chunk":
                full_content += event["content"]
        
        # 验证模型返回了完整的代码内容
        expected_content = "好的，这是一个简单的加法函数：\n```python\ndef add(a, b):\n    return a + b\n```"
        self.assertEqual(full_content, expected_content)

    async def test_scenario_weather_tool_usage(self):
        # 场景2：用户询问天气，模型决定调用天气工具
        user_question = "北京今天天气怎么样？"
        
        # 模拟模型先回复一句客套话，然后发起工具调用
        delta1 = SimpleNamespace(content="正在为您查询北京的天气...", tool_calls=None)
        
        # 模拟工具调用参数的分片返回（更接近真实情况）
        tool_delta_name = SimpleNamespace(name="get_current_weather", arguments="")
        tool_delta_arg1 = SimpleNamespace(name=None, arguments='{"location": "')
        tool_delta_arg2 = SimpleNamespace(name=None, arguments='Beijing"}')
        
        tool_chunk1 = SimpleNamespace(index=0, id="call_weather_1", function=tool_delta_name)
        tool_chunk2 = SimpleNamespace(index=0, id=None, function=tool_delta_arg1)
        tool_chunk3 = SimpleNamespace(index=0, id=None, function=tool_delta_arg2)
        
        delta2 = SimpleNamespace(content=None, tool_calls=[tool_chunk1])
        delta3 = SimpleNamespace(content=None, tool_calls=[tool_chunk2])
        delta4 = SimpleNamespace(content=None, tool_calls=[tool_chunk3])
        
        chunks = [
            SimpleNamespace(choices=[SimpleNamespace(delta=delta1)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=delta2)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=delta3)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=delta4)]),
        ]
        
        client = FakeClient(stream_chunks=chunks)
        interface = LLMInterface()
        interface._get_client = lambda: client
        
        # 调用接口，传入定义好的工具列表
        tools = [{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                    },
                    "required": ["location"],
                },
            }
        }]
        
        events = []
        async for event in interface.streaming_call(
            messages=[{"role": "user", "content": user_question}],
            tools=tools
        ):
            events.append(event)
            
        # 验证流程：先有内容输出，后有工具调用
        content_chunks = [e for e in events if e["type"] == "content_chunk"]
        self.assertTrue(len(content_chunks) > 0)
        self.assertEqual(content_chunks[0]["content"], "正在为您查询北京的天气...")
        
        # 验证最终的 stream_complete 事件中包含完整的工具调用信息
        completion_event = [e for e in events if e["type"] == "stream_complete"][0]
        self.assertEqual(len(completion_event["tool_calls"]), 1)
        tool_call = completion_event["tool_calls"][0]
        
        self.assertEqual(tool_call["function"]["name"], "get_current_weather")
        self.assertEqual(tool_call["function"]["arguments"], '{"location": "Beijing"}')


