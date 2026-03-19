# 后端：NLP 分词与意图识别

## 模块位置

`backend/nlp/`

## 组件

### tokenizer.py — Jieba 分词
- `tokenize(text)` — 精确模式分词
- `tokenize_for_search(text)` — 搜索引擎模式
- 首次调用时延迟加载 `user_dict.txt` 自定义词典

### intent.py — 意图分类器
- `recognize_intent(raw_text) → IntentResult`
- 基于关键词匹配的规则引擎，支持 5 种意图：

| intent_type | 说明 | 关键词示例 |
|-------------|------|-----------|
| query_data | 查询具体数据 | 查、查询、看看、显示 |
| aggregate | 聚合统计 | 平均、总分、最高、人数 |
| compare | 对比分析 | 比较、哪个高、排名 |
| trend | 趋势分析 | 趋势、变化、逐年 |
| unknown | 无法识别 | （无命中） |

### entities.py — 实体提取
- `extract_entities(text, tokens) → list[Entity]`
- 支持实体类型：person、course、time、metric、value
- 人名：2-4 字中文 + 上下文含"的/同学/学生"
- 时间：正则匹配 "2024年/上学期/期末" 等
- 课程：预定义词表（数学/物理/计算机/数据库等）

### user_dict.txt — 自定义词典
- 包含领域专有词："平均分""最高分""及格率""数据库""这学期"等

## 测试

- `test_nlp.py`：7 个用例（分词、各意图类型识别、实体提取）
