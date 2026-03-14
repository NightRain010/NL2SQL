"""Jieba 分词封装，加载自定义词典。"""

from pathlib import Path

import jieba

_DICT_DIR = Path(__file__).parent
_USER_DICT = _DICT_DIR / "user_dict.txt"
_dict_loaded = False


def _ensure_dict_loaded() -> None:
    """延迟加载自定义词典，仅在首次调用时执行。"""
    global _dict_loaded
    if _dict_loaded:
        return
    if _USER_DICT.exists():
        jieba.load_userdict(str(_USER_DICT))
    _dict_loaded = True


def tokenize(text: str) -> list[str]:
    """
    对输入文本进行精确模式分词。

    Args:
        text: 用户输入的自然语言文本。

    Returns:
        分词后的 token 列表。
    """
    _ensure_dict_loaded()
    return list(jieba.cut(text, cut_all=False))


def tokenize_for_search(text: str) -> list[str]:
    """
    搜索引擎模式分词，尽可能多地切分。

    Args:
        text: 用户输入的自然语言文本。

    Returns:
        搜索模式分词后的 token 列表。
    """
    _ensure_dict_loaded()
    return list(jieba.cut_for_search(text))
