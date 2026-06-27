# Content Workbench

这是你的内容工作流工作台。它负责把选题、提示词、脚本、发布、复盘和 `cheat-on-content` 的所有技能串起来。

当前账号方向：

```text
用普通人能听懂的方式，拆解商业案例、品牌出海、财经现象和商业结构。
核心不是讲资料，而是讲一个生意为什么成立，以及这件事对普通人的选择、赚钱、认知有什么启发。
```

## 最推荐的日常流程

```text
1. 找选题
2. 用提示词库拆逻辑和标题
3. 写 90-120 秒口播稿
4. 用 cheat-score 草稿打分
5. 发布前用 cheat-predict 写预测
6. 拍完登记 cheat-shoot
7. 发布登记 cheat-publish
8. T+3 用 cheat-retro 复盘
9. 累计 5 条后用 cheat-bump 校准规则
```

## 今天怎么用

如果你不知道下一条拍什么：

```text
推荐下一条选题
```

如果你已经有一个想法：

```text
我想做一条关于【选题】的内容，帮我 seed
```

如果标题不满意：

```text
用 TITLE-001 帮我给这条内容做标题工厂
```

如果你写好了初稿：

```text
这是初稿，帮我用 REWRITE-001 改成最终发布版
```

如果文案像 AI：

```text
用 REVIEW-001 给这篇去 AI 味
```

如果准备发布：

```text
启动预测 scripts/xxx.md
```

如果发布 3 天后：

```text
复盘这条
```

## SKILL 操作菜单

| Skill | 你怎么说 | 用途 | 产物 |
|---|---|---|---|
| `cheat-seed` | `我想做一条 X` / `帮我找选题` | 深挖单个选题，生成角度和草稿 | `scripts/*.md` |
| `cheat-recommend` | `推荐下一条选题` | 从 `candidates.md` 里选最适合下一条 | 推荐列表 |
| `cheat-trends` | `抓热点` / `今天有什么可做的` | 补充候选选题池 | `candidates.md` |
| `cheat-learn-from` | `拆这个对标账号` / `学这个账号` | 从对标账号学习结构、标题、节奏 | `benchmark.md` / `script_patterns.md` |
| `transcribe` | `转录这个视频/音频` | 把对标视频、访谈、播客转文字 | `transcript.md` |
| `cheat-score` | `打分这篇 scripts/xxx.md` | 草稿评分，不写预测 | 控制台评分 |
| `cheat-predict` | `启动预测 scripts/xxx.md` | 发布前写不可变预测 | `predictions/*.md` |
| `cheat-shoot` | `拍完了 scripts/xxx.md` | 登记已拍摄，进入待发布 | `videos/<id>/` |
| `cheat-publish` | `已发布，链接是 xxx` | 记录发布链接和时间 | 更新预测文件和 state |
| `cheat-retro` | `复盘这条` / `T+3 数据来了` | 抓数据、看评论、复盘预测偏差 | `videos/<id>/report.md` |
| `cheat-persona` | `更新受众画像` | 从评论和复盘里提炼真实受众 | `audience.md` |
| `cheat-bump` | `升级 rubric` / `重校桶` | 有足够样本后校准评分规则 | `rubric_notes.md` / `rubric-memo.md` |
| `cheat-status` | `状态` / `看板` | 查看当前进度、待复盘、校准状态 | 状态报告 |
| `douyin-session` | `抓抖音数据` | 通过登录态抓作品数据和评论 | `douyin-data/` |

## 提示词库怎么接入

入口文件：[PROMPT_WORKBENCH.md](PROMPT_WORKBENCH.md)

推荐组合：

```text
DeepSeek = 想深
Gemini = 写顺
Codex = 工作流、文件、复盘、校准
```

常用路径：

```text
THINK-001 -> 先拆商业逻辑
TITLE-001 -> 批量生成标题
WRITE-001 -> 改成短视频口播
REVIEW-001 -> 去 AI 味
Codex -> 评分和预测
```

## 栏目结构

主栏目：

```text
商业模式出海拆解
```

可扩展栏目：

```text
一个生意为什么成立
消费品牌背后的结构
普通人能学到的商业判断
中国供应链和海外市场
财经现象的人性与结构
```

## 单条内容标准结构

```text
开头 3 秒：反常识或悬念
第一段：大众以为是什么
第二段：真正值得看的是什么
第三段：商业结构拆解
第四段：高潮判断
第五段：普通人启发
结尾：一句能留下来的话
```

## 不露脸视频形式

```text
真人声音或高质量 TTS
素材拼贴
动态字幕
结构图动画
关键截图标注
金句卡片
```

画面比例建议：

```text
40% 案例素材
40% 结构动画
20% 金句卡片
```

## 文件地图

| 文件/目录 | 作用 |
|---|---|
| `PROMPT_WORKBENCH.md` | 提示词库入口 |
| `prompts/catalog.md` | 提示词目录 |
| `prompts/active/` | 当前可用提示词 |
| `prompts/trash/` | 提示词回收站 |
| `candidates.md` | 选题池 |
| `scripts/` | 拍摄前脚本 |
| `predictions/` | 发布前预测 |
| `videos/` | 已拍/已发/复盘资料 |
| `rubric_notes.md` | 当前评分规则 |
| `rubric-memo.md` | 评分规则升级证据 |
| `script_patterns.md` | 你的写作结构模板 |
| `visual_patterns.md` | 画风、剪辑、字幕和视觉表达参考 |
| `audience.md` | 受众画像 |
| `.cheat-state.json` | cheat-on-content 状态 |

## 当前第一条测试内容

```text
scripts/2026-06-26_luckin-overseas-efficiency.md
```

下一步建议：

```text
用 TITLE-001 重做标题
用 REWRITE-001 改成最终发布版
启动预测
```
