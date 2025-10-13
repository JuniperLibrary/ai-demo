# 从文档中加载Prompt的演示程序
from langchain_core.prompts import load_prompt
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

print("===== 从YAML文件加载Prompt =====")
# 从YAML文件加载prompt，使用绝对路径
yaml_prompt = load_prompt(os.path.join(current_dir, "prompt.yaml"), encoding="utf-8")
print("YAML文件中定义的Prompt模板:")
print(yaml_prompt)
print()

# 使用YAML中的prompt模板生成提示词
name = "年轻人"
what = "滑稽"
yaml_result = yaml_prompt.format(name=name, what=what)
print(f"使用YAML模板生成的提示词: {yaml_result}")
print()

print("===== 从JSON文件加载Prompt =====")
# 从JSON文件加载prompt，使用绝对路径
json_prompt = load_prompt(os.path.join(current_dir, "prompt.json"), encoding="utf-8")
print("JSON文件中定义的Prompt模板:")
print(json_prompt)
print()

# 使用JSON中的prompt模板生成提示词
name = "张三"
what = "搞笑的"
json_result = json_prompt.format(name=name, what=what)
print(f"使用JSON模板生成的提示词: {json_result}")
print()

print("===== 额外演示: 动态替换参数 =====")
# 演示动态替换不同的参数
for name, what in [("程序员", "编程"), ("小朋友", "冒险"), ("老师", "教育")]:
    yaml_output = yaml_prompt.format(name=name, what=what)
    json_output = json_prompt.format(name=name, what=what)
    print(f"YAML - {name}, {what}: {yaml_output}")
    print(f"JSON - {name}, {what}: {json_output}")
    print()