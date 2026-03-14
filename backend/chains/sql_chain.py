"""SQL 生成 Chain：Prompt + LLM + OutputParser 组合。"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from backend.config import settings

_SQL_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个 MySQL 专家。根据给定的表结构和用户问题，生成精确的 SELECT 查询。\n"
            "只输出 SQL 语句，不要任何解释。\n"
            "规则：仅使用 SELECT，禁止 INSERT/UPDATE/DELETE/DROP 等修改操作。",
        ),
        (
            "human",
            "表结构:\n{schema_context}\n\n用户问题: {question}\n\n请生成 SQL:",
        ),
    ]
)


def build_sql_chain():
    """
    构建 SQL 生成 LangChain 链。

    Returns:
        一个可调用的 Runnable，输入 dict(schema_context, question)，输出 SQL 字符串。
    """
    llm = ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        temperature=0.1,
        max_tokens=1024,
    )
    return _SQL_PROMPT | llm | StrOutputParser()
