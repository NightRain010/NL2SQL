"""结果摘要 Chain：将查询结果转化为自然语言描述。"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from backend.config import settings

_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个数据分析助手。请用简洁的中文，用 1-2 句话总结查询结果的关键信息。"
            "不要输出 SQL 或技术术语，要让非技术人员也能理解。",
        ),
        (
            "human",
            "用户问题: {question}\n\n查询结果:\n{result_preview}\n\n请总结:",
        ),
    ]
)


def build_summary_chain():
    """
    构建结果摘要 LangChain 链。

    Returns:
        一个可调用的 Runnable，输入 dict(question, result_preview)，输出摘要字符串。
    """
    llm = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        temperature=0.3,
        max_tokens=256,
    )
    return _SUMMARY_PROMPT | llm | StrOutputParser()
