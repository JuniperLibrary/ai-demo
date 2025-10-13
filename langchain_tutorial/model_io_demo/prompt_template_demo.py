# PromptTemplate使用演示程序
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("===== 1. PromptTemplate获取实例的两种方式 =====")

# 方式1：使用构造方法
print("\n方式1: 使用构造方法")
prompt_template1 = PromptTemplate(
    template="你是一个{role},你的名字叫{name}",
    input_variables=["role", "name"],
)
print(f"构造方法创建的模板: {prompt_template1}")
print(f"格式化结果: {prompt_template1.format(role='人工智能专家', name='小智')}")

# 方式2：使用from_template()（推荐）
print("\n方式2: 使用from_template()")
prompt_template2 = PromptTemplate.from_template(template="你是一个{role},你的名字叫{name}")
print(f"from_template创建的模板: {prompt_template2}")
print(f"格式化结果: {prompt_template2.format(role='编程老师', name='小码')}")

print("\n===== 2. 多变量模板的使用 =====")
multi_var_template = PromptTemplate.from_template(
    template="请评价{product}的优缺点，包括{aspect1}和{aspect2}。"
)
print(f"多变量模板: {multi_var_template}")
# 使用不同参数生成提示词
prompt1 = multi_var_template.format(product="智能手机", aspect1="电池续航", aspect2="拍照质量")
prompt2 = multi_var_template.format(product="笔记本电脑", aspect1="处理速度", aspect2="便携性")
print(f"提示词1: {prompt1}")
print(f"提示词2: {prompt2}")

print("\n===== 3. 无变量模板的使用 =====")
no_var_template = PromptTemplate.from_template("Tell me a joke")
print(f"无变量模板: {no_var_template}")
print(f"格式化结果: {no_var_template.format()}")

print("\n===== 4. 部分提示词模板的使用 =====")

# 方式1：在构造方法中使用partial_variables
print("\n方式1: 在构造方法中使用partial_variables")
partial_template1 = PromptTemplate.from_template(
    template="请评价{product}的优缺点，包括{aspect1}和{aspect2}。",
    partial_variables={"aspect1": "电池续航"}
)
print(f"部分变量模板1: {partial_template1}")
print(f"格式化结果: {partial_template1.format(product='智能手机', aspect2='拍照质量')}")

# 方式2：调用partial()方法
print("\n方式2: 调用partial()方法")
template = PromptTemplate.from_template(
    template="请评价{product}的优缺点，包括{aspect1}和{aspect2}。"
)
partial_template2 = template.partial(aspect1="电池续航", aspect2="拍照质量")
print(f"原模板: {template}")
print(f"部分变量模板2: {partial_template2}")
print(f"格式化结果: {partial_template2.format(product='智能手机')}")

# 链式调用方式
print("\n链式调用方式:")
partial_template3 = (PromptTemplate
                    .from_template("请评价{product}的优缺点，包括{aspect1}和{aspect2}。")
                    .partial(aspect1="电池续航", aspect2="拍照质量"))
print(f"链式调用创建的部分变量模板: {partial_template3}")
print(f"格式化结果: {partial_template3.format(product='智能手机')}")

print("\n===== 5. 组合提示词的使用 =====")
combined_template = (
    PromptTemplate.from_template("Tell me a joke about {topic}")
    + ", make it funny"
    + "\n\nand in {language}"
)
print(f"组合提示词模板: {combined_template}")
print(f"格式化结果: {combined_template.format(topic='sports', language='chinese')}")

print("\n===== 6. 给变量赋值的两种方式 =====")

template = PromptTemplate.from_template(
    template="请评价{product}的优缺点，包括{aspect1}和{aspect2}。")

# 方式1：使用format() - 返回str类型
print("\n方式1: 使用format()")
format_result = template.format(product="智能手机", aspect1="电池续航", aspect2="拍照质量")
print(f"format()结果: {format_result}")
print(f"format()返回类型: {type(format_result)}")

# 方式2：使用invoke() - 返回PromptValue类型（推荐）
print("\n方式2: 使用invoke()")
invoke_result = template.invoke(input={"product": "智能手机", "aspect1": "电池续航", "aspect2": "拍照质量"})
print(f"invoke()结果: {invoke_result}")
print(f"invoke()返回类型: {type(invoke_result)}")

print("\n===== 7. 结合大模型的使用 =====")

# 配置OpenAI环境
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 检查API密钥是否设置
if not os.getenv("OPENAI_API_KEY"):
    print("警告: 未设置OPENAI_API_KEY环境变量，将使用模拟响应")
    # 模拟大模型响应
    print("\n模拟大模型响应:")
    print("智能手机的优点包括便携性好、功能丰富、拍照质量高；缺点包括电池续航有限、长时间使用影响视力等。")
else:
    try:
        # 获取对话模型
        chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            max_tokens=500
        )
        
        # 生成提示词
        prompt = template.invoke(input={"product": "智能手机", "aspect1": "电池续航", "aspect2": "拍照质量"})
        
        # 调用大模型
        print("\n正在调用大模型，请稍候...")
        response = chat_model.invoke(prompt)
        print(f"大模型响应: {response.content}")
    except Exception as e:
        print(f"调用大模型时出错: {e}")