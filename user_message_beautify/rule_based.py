import re
"""
1️⃣ Rule-based 实现

特点：

优点：速度快，成本低，无需依赖外部模型

缺点：只能做表面优化（大小写、空格、标点、简单同义词替换），语义优化有限

适合：结构化问题、固定领域问答、对延迟敏感场景
"""
# 简单同义词字典
synonyms = {
    "咋办": "怎么办",
    "怎么做": "如何操作",
    "json": "JSON",
}


def rule_based_beautify(question: str) -> str:
    # 1. 去多余空格
    question = re.sub(r'\s+', ' ', question).strip()

    # 2. 同义词替换
    for k, v in synonyms.items():
        question = question.replace(k, v)

    # 3. 首字母大写
    if len(question) > 0:
        question = question[0].upper() + question[1:]

    # 4. 自动补疑问号
    if not question.endswith("?"):
        question += "?"

    return question


# 测试
q = "  python json咋办  "
print(rule_based_beautify(q))
