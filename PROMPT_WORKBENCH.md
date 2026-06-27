# Prompt Workbench

这是你的提示词库工作台。以后优先打开可视化管理站，不用再翻聊天记录。

可视化入口：

```text
桌面快捷方式：提示词库管理站
或运行：start-prompt-dashboard.ps1
```

本地地址：

```text
http://127.0.0.1:8765
```

核心用途：

- 查找：在首页直接看提示词预览，不用点进文件猜用途。
- 复制：卡片上直接点 `复制提示词`。
- 新增：网页右上或侧边栏点 `新增提示词`。
- 修改：卡片上点 `编辑`，保存后自动写回文件。
- 删除：卡片上点 `删除`，默认进入回收站，不会直接永久消失。
- 恢复：进入 `回收站` 后点 `恢复`。
- 永久删除：只有在回收站里点 `永久删除` 才会真正删除。

## 推荐使用顺序

```text
选题不够深 -> THINK-001 DeepSeek 商业逻辑深挖
标题不够吸引 -> TITLE-001 标题工厂
需要写成口播 -> WRITE-001 Gemini 标题和口播润色
只想一个平台完成 -> WRITE-002 通用人味口播生成
你自己写了初稿 -> REWRITE-001 已有初稿改写
文案像 AI -> REVIEW-001 去 AI 味审稿
最终稿发回 Codex -> cheat-score / cheat-predict / 发布 / 复盘
```

## 提示词目录

| ID | 平台 | 用途 | 适合场景 | 文件 |
|---|---|---|---|---|
| THINK-001 | DeepSeek | 商业逻辑深挖 | 有选题但讲不深 | [THINK-001](prompts/active/THINK-001-deepseek-logic-dissection.md) |
| TITLE-001 | Gemini / DeepSeek / 通用 | 标题工厂 | 标题不够吸引人 | [TITLE-001](prompts/active/TITLE-001-title-factory.md) |
| WRITE-001 | Gemini | 标题和口播润色 | 有观点，需要更抓人 | [WRITE-001](prompts/active/WRITE-001-gemini-title-script-polisher.md) |
| WRITE-002 | 通用 | 一次性生成标题和口播 | 只想用一个平台出初稿 | [WRITE-002](prompts/active/WRITE-002-universal-human-script.md) |
| REWRITE-001 | 通用 | 改写已有初稿 | 你已经写完文章或口播稿 | [REWRITE-001](prompts/active/REWRITE-001-rewrite-existing-draft.md) |
| REVIEW-001 | 通用 | 去 AI 味审稿 | 文案正确但不像人话 | [REVIEW-001](prompts/active/REVIEW-001-ai-taste-removal-review.md) |

完整目录文件：[catalog.md](prompts/catalog.md)

## 你可以直接这样对我说

```text
打开提示词库
```

```text
我要写瑞幸这条，用哪个提示词？
```

```text
把刚才这个提示词存入库，平台是 Gemini，用途是标题优化
```

```text
修改 WRITE-001，让它更适合电影解说风格
```

```text
删除 REWRITE-001
```

```text
永久删除 REWRITE-001
```

```text
列出所有适合 Gemini 的提示词
```

## 新增规则

新增提示词时，不再手动编 `P007` 这种流水号。网页会按用途自动生成语义编号：

```text
THINK-002
TITLE-002
WRITE-003
REWRITE-002
REVIEW-002
```

新增文件放在：

```text
prompts/active/
```

文件名格式：

```text
WRITE-003-short-name.md
```

新增后必须更新：

```text
prompts/catalog.json
对应的 prompts/active/*.md
```

## 删除规则

默认删除不是永久删除，而是归档：

```text
prompts/active/WRITE-002-xxx.md -> prompts/trash/WRITE-002-xxx.md
```

只有你在回收站里点 `永久删除`，或明确让我 `永久删除 WRITE-002`，才会真正删除文件。

归档后必须更新：

```text
prompts/catalog.json
对应的 prompts/active/*.md 或 prompts/trash/*.md
```

## 修改规则

你可以自己直接编辑 `.md` 文件，也可以让我改。

如果你让我改，请尽量这样说：

```text
修改 WRITE-001，把语气改得更像商业电影解说，不要太像教程
```

```text
修改 TITLE-001，标题不要太长，控制在 12-20 个字
```

## 使用提醒

不要让 AI 替你凭空决定观点。你的工作方式应该是：

```text
我先写真实想法 -> AI 帮我拆深 -> AI 帮我改顺 -> 我再加个人判断 -> Codex 帮我审稿和预测
```

最重要的是保留你的判断感。漂亮但没判断的文案，对你的账号没有长期价值。
