# LangChain中各种Template类型的详细辨析

## 1. 主要模板类型及特点

### PromptTemplate（基础提示词模板）
- **核心特点**：最基础、最简单的模板类型，以单一文本字符串形式存在
- **适用场景**：简单的单轮文本生成任务
- **返回类型**：字符串
- **使用方式**：`PromptTemplate.from_template("模板文本{变量}")`
- **优势**：使用简单，性能最佳，适合快速应用

**代码示例**：
```python
from langchain_core.prompts import PromptTemplate

# 使用from_template()方法创建模板（推荐）
prompt = PromptTemplate.from_template("你是一个{role}，请解释{topic}")

# 格式化模板
formatted_prompt = prompt.format(role="技术专家", topic="机器学习")
print(formatted_prompt)
# 输出: 你是一个技术专家，请解释机器学习
```

### ChatPromptTemplate（对话式提示词模板）
- **核心特点**：支持多角色对话结构，区分系统消息、用户消息等
- **适用场景**：复杂对话、多轮交互、聊天机器人开发
- **返回类型**：ChatPromptValue对象
- **使用方式**：`ChatPromptTemplate.from_messages([("system", "系统消息"), ("human", "用户消息{变量}")])`
- **优势**：更贴近实际聊天场景，与聊天模型匹配度高

**代码示例**：
```python
from langchain_core.prompts import ChatPromptTemplate

# 创建对话提示词模板
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的{role}，请用简洁专业的语言回答问题。"),
    ("human", "请详细解释{topic}，并给出具体的例子。")
])

# 使用模板
prompt_value = chat_template.invoke({
    "role": "数据科学家", 
    "topic": "深度学习"
})
```

### FewShotPromptTemplate（少样本学习模板）
- **核心特点**：支持提供少量示例来指导模型输出
- **适用场景**：需要模型学习特定模式或格式的任务（分类、翻译等）
- **返回类型**：字符串
- **组成**：示例集合、示例模板、前缀和后缀
- **优势**：通过示例提高模型在特定任务上的表现

**代码示例**：
```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

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
```

### FewShotChatMessagePromptTemplate（对话式少样本模板）
- **核心特点**：结合了对话模板和少样本学习功能
- **适用场景**：复杂对话场景中的示例学习
- **返回类型**：ChatPromptValue对象
- **使用方式**：嵌套在其他ChatPromptTemplate中使用
- **优势**：既支持多轮对话，又能提供学习示例

**代码示例**：
```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

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
```

### MessagesPlaceholder（动态消息占位符）
- **核心特点**：允许在模板中动态插入消息列表
- **适用场景**：多轮对话历史管理
- **使用方式**：`MessagesPlaceholder(variable_name="chat_history")`
- **优势**：使模板更加灵活，能处理不确定数量的消息
- **最佳搭配**：与Memory模块结合使用效果最佳

**代码示例**：
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

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

# 使用模板
prompt_value = chat_template.invoke({
    "name": "小智",
    "chat_history": chat_history,
    "question": "今天天气怎么样？"
})
```

### 角色特定模板
- **类型**：SystemMessagePromptTemplate、HumanMessagePromptTemplate等
- **核心特点**：为特定角色消息提供专门的模板类
- **适用场景**：需要精确控制消息类型的复杂场景
- **优势**：提供更精细的消息角色控制

**代码示例**：
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate

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
```

## 2. 模板选择指南

| 应用场景 | 推荐模板 | 选择理由 |
|---------|---------|--------|
| 简单文本生成 | PromptTemplate | 最简单直接，性能最佳 |
| 聊天机器人开发 | ChatPromptTemplate | 支持多角色对话，与聊天模型匹配度高 |
| 需要示例的任务 | FewShotPromptTemplate | 通过示例指导模型输出格式和内容 |
| 复杂对话+示例学习 | FewShotChatMessagePromptTemplate | 结合对话能力和示例学习功能 |
| 多轮对话应用 | ChatPromptTemplate + MessagesPlaceholder | 有效管理对话历史，实现上下文理解 |
| 企业级应用开发 | ChatPromptTemplate | 更灵活，功能更强大，扩展性更好 |
| 与Memory模块集成 | ChatPromptTemplate + MessagesPlaceholder | 最佳的对话历史管理组合 |

## 3. 各类模板的综合比较

| 模板类型 | 主要特点 | 适用场景 | 返回类型 | 复杂度 | 最佳实践 |
|---------|---------|---------|---------|--------|--------|
| PromptTemplate | 基础文本模板 | 简单的单轮文本生成 | 字符串 | 低 | 简单任务首选，使用from_template()方法创建 |
| ChatPromptTemplate | 支持多角色对话 | 复杂对话、多轮交互 | ChatPromptValue | 中 | 使用from_messages()方法创建，适合聊天模型 |
| FewShotPromptTemplate | 提供少样本学习示例 | 需要示例指导的任务 | 字符串 | 中 | 与PromptTemplate配合使用，提高特定任务表现 |
| FewShotChatMessagePromptTemplate | 对话式少样本学习 | 复杂对话中的示例学习 | ChatPromptValue | 高 | 嵌套使用，适合复杂对话场景 |
| MessagesPlaceholder | 动态消息占位符 | 多轮对话历史管理 | -（作为组件使用） | 中 | 与Memory模块结合，处理对话历史 |
| 角色特定模板 | 细化的角色消息控制 | 需要精确定义消息角色的场景 | -（作为组件使用） | 中 | 在需要精细控制时使用 |

## 4. 最佳实践总结

1. **优先使用便捷创建方法**：使用`from_template()`创建PromptTemplate，使用`from_messages()`创建ChatPromptTemplate

2. **根据复杂度选择**：简单任务用PromptTemplate，复杂对话用ChatPromptTemplate

3. **多轮对话必备**：实现多轮对话时，务必使用MessagesPlaceholder管理对话历史

4. **性能与功能平衡**：在对性能要求极高的场景下选择基础模板，在功能要求复杂的场景下选择高级模板

5. **模板组合使用**：根据实际需求，可以组合使用多种模板类型，如将少样本模板嵌套在聊天模板中

6. **变量赋值方式**：
   - 使用`invoke()`方法（推荐）：返回PromptValue对象，更好地与LangChain集成
   - 使用`format()`方法：返回字符串，适合直接使用
   - 使用`partial()`方法：处理部分变量，提高模板复用性

7. **错误处理**：在生产环境中使用try-except捕获可能的错误，并提供备选逻辑

## 5. 实际应用场景示例

### 简单文本生成应用
```python
# 适用场景：内容生成、简单问答
template = PromptTemplate.from_template("写一段关于{topic}的介绍，大约200字。")
prompt = template.invoke({"topic": "人工智能伦理"})
```

### 聊天机器人应用
```python
# 适用场景：客服机器人、虚拟助手
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的客服助手，负责帮助用户解答关于{product}的问题。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
```

### 需要示例的分类任务
```python
# 适用场景：情感分析、意图识别
examples = [
    {"text": "产品质量很好，非常满意", "label": "正面"},
    {"text": "物流太慢了，等了一周才到", "label": "负面"}
]
example_prompt = PromptTemplate.from_template("文本: {text}\n标签: {label}")

few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="文本: {new_text}\n标签: ",
    input_variables=["new_text"]
)
```

通过合理选择和使用这些模板类型，您可以构建出更加灵活、强大和高效的提示词系统，充分发挥大语言模型的能力。