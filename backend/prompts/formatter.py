"""结果格式化 Agent 提示词。"""

FORMATTER_SUMMARY_SYSTEM_PROMPT = """你是一个数据分析助手。请用一句简洁的中文总结以下查询结果。"""


def build_summary_user_prompt(user_input: str, preview: str) -> str:
    """构建结果摘要的用户提示词。"""
    return f"用户问题: {user_input}\n查询结果: {preview}"
