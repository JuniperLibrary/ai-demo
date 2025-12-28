import os
import json

# 定义文档存放目录
DOCS_DIR = "docs"
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)


def save_document(filename: str, content: str):
    """
    将文本内容保存为文件 (Markdown格式推荐)
    """
    # 安全起见，确保文件名只有文件名部分，没有路径跳转
    filename = os.path.basename(filename)
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = os.path.join(DOCS_DIR, filename)

    print(f"    [Req Tool] 正在保存需求文档到: {filepath} ...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"status": "success", "message": f"File saved at {filepath}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


def read_document(filename: str):
    """
    读取已有的需求文档内容
    """
    filename = os.path.basename(filename)
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = os.path.join(DOCS_DIR, filename)

    print(f"    [Req Tool] 正在读取文档: {filepath} ...")
    if not os.path.exists(filepath):
        return json.dumps({"error": "File not found"})

    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


# --- 工具映射表 ---
req_tools_map = {
    "save_document": save_document,
    "read_document": read_document
}

# --- JSON Schema ---
req_tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "save_document",
            "description": "将整理好的需求、PRD或会议纪要保存到本地文件。通常在需求分析的最后阶段调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "文件名，例如 'shopping_app_prd'"},
                    "content": {"type": "string", "description": "Markdown格式的文档完整内容"},
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_document",
            "description": "读取之前的需求文档以便进行修改或补充。",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "要读取的文件名"},
                },
                "required": ["filename"],
            },
        },
    }
]