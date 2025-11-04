"""
3️⃣ Hybrid 实现（推荐生产环境）

特点：

先做 rule-based 预处理 → 去掉明显问题（空格、大小写、同义词）

再用 LLM 做语义优化 → 提问更自然、可读性更强

优点：降低调用成本 + 提升优化效果
"""
from rule_based import rule_based_beautify
from llm_beautify import llm_beautify

def hybrid_beautify(question: str) -> str:
    # 1. rule-based预处理
    rule_processed = rule_based_beautify(question)

    # 2. LLM再优化
    return llm_beautify(rule_processed)


q = "  我想用python那个json怎么弄才好还有能不能快点，因为我昨天试过那个但是不行，也可能有错  "
print(hybrid_beautify(q))
