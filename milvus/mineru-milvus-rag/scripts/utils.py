import re
def split_into_chunks(doc_text, max_tokens=500, overlap=50):
    # 简单基于句子分割 + 滑窗（示例）
    sentences = re.split(r'(?<=[。！？\.\?!])\s*', doc_text)
    chunks = []
    cur = ""
    for s in sentences:
        if len(cur) + len(s) <= max_tokens:
            cur += s
        else:
            chunks.append(cur.strip())
            # overlap: 取上一段后 overlap 字符（或句子）加入新段
            cur = s
    if cur:
        chunks.append(cur.strip())
    return chunks
