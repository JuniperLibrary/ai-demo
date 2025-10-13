# 少量示例提示词模板的完整演示

# 导入相关包
import os
import dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 加载环境变量
dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

# ==================== 案例1：反义词查找器 ====================
print("\n=== 案例1：反义词查找器 ===")

# 定义示例提示词模板
example_prompt = PromptTemplate.from_template(
    template="Input: {input}\nOutput: {output}",
)

# 创建示例数据集
examples = [
    {"input": "高兴", "output": "悲伤"},
    {"input": "高", "output": "矮"},
    {"input": "长", "output": "短"},
    {"input": "精力充沛", "output": "无精打采"},
    {"input": "阳光", "output": "阴暗"},
    {"input": "粗糙", "output": "光滑"},
    {"input": "干燥", "output": "潮湿"},
    {"input": "富裕", "output": "贫穷"},
]

# 定义嵌入模型
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

# 创建语义相似性示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    FAISS,
    k=2,
)

# 定义小样本提示词模板
similar_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="给出每个词组的反义词",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"],
)

# 初始化聊天模型
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 测试几个词汇
words_to_test = ["忧郁", "寒冷", "肥胖", "快乐"]

for word in words_to_test:
    # 生成提示词
    prompt = similar_prompt.invoke({"word": word})
    print(f"\n为 '{word}' 生成的提示词：")
    print(prompt.text)
    
    # 调用大模型
    response = chat_model.invoke(prompt)
    print(f"反义词: {response.content}")

# ==================== 案例2：数学问题解答器 ====================
print("\n\n=== 案例2：数学问题解答器 ===")

# 定义数学问题的示例
math_examples = [
    {"question": "2 + 3 = ?", "answer": "5"},
    {"question": "10 - 4 = ?", "answer": "6"},
    {"question": "5 × 6 = ?", "answer": "30"},
    {"question": "12 ÷ 3 = ?", "answer": "4"}
]

# 创建数学问题的示例提示词模板
math_example_prompt = PromptTemplate.from_template(
    template="问题: {question}\n答案: {answer}",
)

# 创建数学问题的小样本提示词模板（不使用示例选择器）
math_prompt = FewShotPromptTemplate(
    examples=math_examples,
    example_prompt=math_example_prompt,
    suffix="问题: {question}\n答案:",
    input_variables=["question"],
)

# 测试数学问题
math_questions = [
    "7 + 8 = ?",
    "20 - 15 = ?",
    "8 × 7 = ?",
    "24 ÷ 6 = ?"
]

for question in math_questions:
    # 生成提示词
    prompt = math_prompt.invoke({"question": question})
    print(f"\n为 '{question}' 生成的提示词：")
    print(prompt.text)
    
    # 调用大模型
    response = chat_model.invoke(prompt)
    print(f"答案: {response.content}")

# ==================== 案例3：情感分析 ====================
print("\n\n=== 案例3：情感分析 ===")

# 定义情感分析的示例
sentiment_examples = [
    {"text": "这部电影真是太棒了，我非常喜欢！", "sentiment": "积极"},
    {"text": "今天天气很差，心情也跟着不好了。", "sentiment": "消极"},
    {"text": "这个产品功能一般，价格适中。", "sentiment": "中性"},
    {"text": "我很失望，这个餐厅的食物太难吃了。", "sentiment": "消极"}
]

# 创建情感分析的示例选择器
sentiment_selector = SemanticSimilarityExampleSelector.from_examples(
    sentiment_examples,
    embeddings,
    FAISS,
    k=2,
)

# 创建情感分析的小样本提示词模板
sentiment_prompt = FewShotPromptTemplate(
    example_selector=sentiment_selector,
    example_prompt=PromptTemplate.from_template("文本: {text}\n情感: {sentiment}"),
    prefix="分析以下文本的情感倾向，只能回答'积极'、'消极'或'中性'",
    suffix="文本: {text}\n情感:",
    input_variables=["text"],
)

# 测试情感分析
sentiment_texts = [
    "这本书的内容非常丰富，让我收获颇丰。",
    "等了两个小时还没上菜，服务态度真差。",
    "今天是周末，可以好好休息一下了。",
    "这个手机的续航能力一般，但拍照功能不错。"
]

for text in sentiment_texts:
    # 生成提示词
    prompt = sentiment_prompt.invoke({"text": text})
    print(f"\n为文本 '{text}' 生成的提示词：")
    print(prompt.text)
    
    # 调用大模型
    response = chat_model.invoke(prompt)
    print(f"情感分析结果: {response.content}")

print("\n=== 所有示例演示完成 ===")