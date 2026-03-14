"""NLP 模块测试：分词与意图识别。"""

from backend.nlp.tokenizer import tokenize
from backend.nlp.intent import recognize_intent


class TestTokenizer:
    """Jieba 分词测试。"""

    def test_basic_tokenize(self):
        """测试基础分词功能。"""
        tokens = tokenize("查一下张三的数学成绩")
        assert isinstance(tokens, list)
        assert len(tokens) > 0

    def test_tokenize_returns_strings(self):
        """确保返回的都是字符串。"""
        tokens = tokenize("全班平均分是多少")
        assert all(isinstance(t, str) for t in tokens)


class TestIntentRecognizer:
    """意图识别测试。"""

    def test_query_data_intent(self):
        """测试数据查询意图。"""
        result = recognize_intent("查一下张三的数学成绩")
        assert result.intent_type in ("query_data", "aggregate")
        assert result.is_valid is True
        assert 0.0 <= result.confidence <= 1.0

    def test_aggregate_intent(self):
        """测试聚合统计意图。"""
        result = recognize_intent("全班数学平均分是多少")
        assert result.intent_type == "aggregate"
        assert result.is_valid is True

    def test_compare_intent(self):
        """测试对比分析意图。"""
        result = recognize_intent("男生和女生的平均分哪个高")
        assert result.intent_type in ("compare", "aggregate")
        assert result.is_valid is True

    def test_unknown_intent(self):
        """测试无法识别的意图。"""
        result = recognize_intent("今天天气怎么样")
        assert result.intent_type == "unknown"
        assert result.is_valid is False

    def test_entities_extracted(self):
        """测试实体提取。"""
        result = recognize_intent("查一下数学的平均分")
        entity_labels = {e.label for e in result.entities}
        assert len(result.entities) > 0
