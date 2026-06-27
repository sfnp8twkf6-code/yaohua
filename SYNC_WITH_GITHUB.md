# GitHub Sync

推荐使用 GitHub 私有仓库同步这套内容资产。

## Windows 推送

如果你已经在 GitHub 网页创建了私有仓库，复制仓库 URL 后运行：

```powershell
git remote add origin <你的 GitHub 仓库 URL>
git branch -M main
git push -u origin main
```

以后每次同步：

```powershell
git pull
git add .
git commit -m "Update content workspace"
git push
```

## Mac 拉取

```bash
git clone <你的 GitHub 仓库 URL> ~/ContentStrategyRoom
cd ~/ContentStrategyRoom
bash tools/install-content-strategy-room.sh
```

以后每次同步：

```bash
git pull
git add .
git commit -m "Update content workspace"
git push
```

## 冲突规则

- 如果两台电脑改了同一个提示词或脚本，先不要强行覆盖。
- 以最新的真实想法和最终稿为准，保留更好的版本。
- 登录态、缓存、虚拟环境和原始平台数据不进入仓库。
