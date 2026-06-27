# Content Strategy Room

这是你的自媒体内容策划工作区，用 GitHub 私有仓库在 Windows 和 Mac 之间同步。

## 同步内容

- `prompts/`：提示词库，包括可视化管理站数据。
- `candidates.md`：选题池。
- `scripts/`：脚本草稿。
- `predictions/`：发布前预测。
- `videos/`：复盘资料和元数据。
- `rubric_notes.md` / `script_patterns.md` / `audience.md`：内容系统记忆。
- `visual_patterns.md`：长期保存画风、剪辑、字幕和视觉表达参考。
- `codex-skills/content-strategy-room/`：可安装到 Codex 的策划会 SKILL。

## 不同步内容

登录态、缓存、虚拟环境、抖音抓取原始数据和大视频文件不会进入 GitHub。每台电脑需要各自登录平台账号或重新配置本地环境。

## Mac 第一次使用

```bash
git clone <你的 GitHub 私有仓库 URL> ~/ContentStrategyRoom
cd ~/ContentStrategyRoom
bash tools/install-content-strategy-room.sh
bash start-prompt-dashboard.sh
```

然后在 Codex 里打开 `~/ContentStrategyRoom`，输入：

```text
$content-strategy-room 启动内容策划会
```

## Windows 使用

```powershell
cd D:\新建文件夹
.\tools\install-content-strategy-room.ps1
.\start-prompt-dashboard.ps1
```

以后修改提示词、候选池、脚本和复盘后，用 Git 同步即可。
