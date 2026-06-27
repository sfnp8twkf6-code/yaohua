# Prompt Catalog

这个文件是给人看的索引。真实数据源是 `prompts/catalog.json`，网页管理站会读写那个 JSON 和对应 Markdown 文件。

| ID | 旧编号 | 状态 | 阶段 | 平台 | 标题 | 用途 | 文件 |
|---|---|---|---|---|---|---|---|
| THINK-001 | P001 | active | 想深 | DeepSeek | 商业逻辑深挖 | 找反常识、底层结构、争议点、生活启发 | `prompts/active/THINK-001-deepseek-logic-dissection.md` |
| TITLE-001 | P006 | active | 标题 | Gemini / DeepSeek / 通用 | 标题工厂 | 批量生成和筛选短视频标题 | `prompts/active/TITLE-001-title-factory.md` |
| WRITE-001 | P002 | active | 写稿 | Gemini | 标题和口播润色 | 标题发散、口播润色、分镜和金句 | `prompts/active/WRITE-001-gemini-title-script-polisher.md` |
| WRITE-002 | P003 | active | 写稿 | 通用 | 一次性生成标题和人味口播 | 一个平台完成标题、框架、口播稿、审稿 | `prompts/active/WRITE-002-universal-human-script.md` |
| REWRITE-001 | P004 | active | 改稿 | 通用 | 改写你的已有初稿 | 保留你的观点，优化标题、节奏、人味和获得感 | `prompts/active/REWRITE-001-rewrite-existing-draft.md` |
| REVIEW-001 | P005 | active | 审稿 | 通用 | 去 AI 味审稿 | 删除报告腔、套话、空话，补强个人判断 | `prompts/active/REVIEW-001-ai-taste-removal-review.md` |

## 维护规则

新增提示词：

```text
1. 优先用本地管理站新增。
2. 管理站会自动生成语义编号，例如 `TITLE-002`。
3. 管理站会自动写入 `prompts/catalog.json` 和 Markdown 文件。
```

归档提示词：

```text
1. 优先用本地管理站删除。
2. 删除会把文件从 `prompts/active/` 移到 `prompts/trash/`。
3. 状态会从 `active` 改为 `trash`。
```

永久删除提示词：

```text
1. 只有在回收站里点击永久删除才执行。
2. 删除文件。
3. 从 `prompts/catalog.json` 中删除对应记录。
```
