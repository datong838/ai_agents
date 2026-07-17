# ai_agents

文档仓。本地工作区即本仓根目录：`c:\work\projects\wchat\docs`（**不再**套一层 `docs/`）。

## 目录

```text
./
├── palantier/     # AOS / Palantir 对标产品与技术方案（含 20_tech、foundry/html）
├── examples/      # 示例（如客户前置）
├── scripts/       # 文档相关脚本
└── …              # 其他专题文档
```

主入口（AOS 目标态）：

- [palantier/00-索引.md](palantier/00-索引.md)
- [palantier/20_tech/00-技术方案索引.md](palantier/20_tech/00-技术方案索引.md)
- [palantier/20_tech/26-AOS目标态开发计划.md](palantier/20_tech/26-AOS目标态开发计划.md)

## 用法

在 `c:\work\projects\wchat\docs` 直接：

```powershell
git add -A
git commit -m "..."
git push origin main
```

无需再拷贝到其它克隆目录。

## 本地优先（禁止被 pull 覆盖）

**本机磁盘上的 docs 是真源。** 默认禁止 `git pull` / `merge` / `rebase` / `reset --hard`，避免远程把本地改写掉。

启用保护（每个新开的 PowerShell 一次）：

```powershell
cd c:\work\projects\wchat\docs
. .\scripts\use-protected-git.ps1
```

Cursor 若打开的是本目录，已通过 `.vscode/settings.json` 指向 `bin\git.cmd`。

日常只 push，不要 pull。确需用远程覆盖本地时：

```powershell
$env:ALLOW_PULL = "1"
git pull
# 或：git fetch origin; $env:ALLOW_PULL="1"; git reset --hard origin/main
```
