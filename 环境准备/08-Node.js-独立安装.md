# 环境准备 — Node.js 独立安装

> **角色**：谛听客户端 **Electron + Vite + npm** 工具链（Phase 0 起）  
> **阶段**：**顺序 0 必须**（与 Python、Git 同级）  
> **要求**：Node **20+**（**定稿：与线上一致 v22.22.3 LTS + npm 10.9.8**）  
> **关联**：[00-索引 §2.0](00-索引.md)、[开发计划 Phase 0](../开发计划-总览.md)

---

## 1. 为什么建议独立安装

| 来源 | 是否推荐作项目默认 Node | 原因 |
|------|------------------------|------|
| **nodejs.org 官方安装包** | ✅ **推荐** | 完整 node + npm + npx；PATH 稳定；与 Cursor / 钉钉 Real 解耦 |
| `C:\Program Files\nodejs\` 旧版 v16 | ❌ 需升级或卸载 | 低于项目要求 20+ |
| 钉钉 Real `.real\.bin\node` | ⚠️ 可用但不推荐长期依赖 | 随 Real 客户端更新，路径与版本不可控 |
| Cursor 内置 `helpers\node.exe` | ❌ 不可用 | 仅 `node.exe`，**无 npm**，仅供 Cursor 内部 |

本仓库 **谛听客户端**后续将使用：`npm install`、`npm run dev`、Electron 构建等，请按本文完成**独立安装**。

---

## 2. 版本选型

| 项 | 建议 |
|----|------|
| 主版本 | **20.x LTS** 或 **22.x LTS** |
| **项目定稿（本地 = 线上）** | **Node v22.22.3** + **npm 10.9.8**（[发布说明](https://nodejs.org/en/blog/release/v22.22.3)） |
| 架构 | Windows **x64** |
| 包管理器 | 安装包自带 **npm**（无需单独装） |
| 本项目最低要求 | `>= 20.0.0`（见 [00-索引](00-索引.md) 顺序 0） |

下载页：[https://nodejs.org/](https://nodejs.org/) → 选择 **LTS** → Windows Installer (`.msi`)。

---

## 3. Windows 安装步骤

### 3.1 安装前（本机若已有 Node 16）

1. 打开 **PowerShell**（普通权限即可），查看当前版本：

```powershell
node -v
npm -v
Get-Command node | Select-Object Source
```

2. 若显示 **v16.x** 且路径为 `C:\Program Files\nodejs\`：
   - **推荐**：直接安装 Node 20/22 LTS 官方 MSI，安装程序通常**覆盖**同目录；
   - 或先到「设置 → 应用 → 已安装的应用」卸载 **Node.js**，再装新版。

3. **清理干扰 PATH**（若曾把钉钉 Real 的 Node 加入用户 PATH）：
   - `Win + R` → `sysdm.cpl` → **高级** → **环境变量**
   - 在「用户变量」Path 中**删除** `C:\Users\<用户名>\.real\.bin\node`（若存在）
   - 不要将 Cursor 的 `...\cursor\...\helpers` 加入 PATH

### 3.2 执行安装

1. 从 [nodejs.org](https://nodejs.org/) 下载 **LTS** 的 `.msi`（例如 `node-v20.x.x-x64.msi`）。
2. 双击安装，建议勾选：
   - ✅ **Add to PATH**（自动加入系统 PATH）
   - ✅ **Automatically install necessary tools**（可选，会装构建工具；POC 阶段可跳过）
3. 安装路径保持默认即可：`C:\Program Files\nodejs\`
4. 安装完成后 **关闭并重新打开** 所有终端（含 Cursor 内置终端）。

### 3.3 可选：命令行安装

**winget**（Windows 10/11）：

```powershell
winget install OpenJS.NodeJS.LTS
```

**Chocolatey**（若已装 choco）：

```powershell
choco install nodejs-lts -y
```

安装后同样需**新开终端**再验证。

---

## 4. 安装后检查与验证

### 4.1 基础命令（必做）

在**新开的 PowerShell** 中执行：

```powershell
node -v          # 期望：v20.x.x 或 v22.x.x
npm -v           # 期望：10.x 或与 Node 版本匹配的 npm
npx -v           # 应有版本号，无报错
where.exe node   # 期望：C:\Program Files\nodejs\node.exe（仅一条或该条在最前）
Get-Command node | Format-List Name, Source
```

**通过标准**：

| 检查项 | 通过条件 |
|--------|----------|
| 版本 | `node -v` 主版本 **≥ 20** |
| 路径 | `node.exe` 来自 `C:\Program Files\nodejs\`，**不是** `.real` 或 `cursor\helpers` |
| npm | `npm -v` 有输出，无「不是内部或外部命令」 |
| 唯一默认 | `where node` 第一条为官方安装目录（旧 v16 已覆盖或已卸载） |

### 4.2 npm  registry 连通（建议）

```powershell
npm ping
```

期望：`Ping success` 或类似成功信息。若超时，可临时使用国内镜像（仅开发机）：

```powershell
npm config set registry https://registry.npmmirror.com
npm ping
```

### 4.3 最小功能冒烟（建议）

在任意空目录执行：

```powershell
mkdir $env:TEMP\node-smoke-test -Force | Out-Null
cd $env:TEMP\node-smoke-test
npm init -y
npm install lodash@4 --no-fund --no-audit
node -e "console.log(require('lodash').VERSION)"
```

期望：打印 `4.x.x`，无报错。测完可删除该目录。

### 4.4 与本仓库相关的后续验证（Phase 0 后）

脚手架就绪后，在 `ditingclient/` 目录：

```powershell
cd C:\work\projects\wchat\ditingclient
npm install
npm run dev
```

期望：依赖安装成功，Electron/Vite 开发窗口可启动（Phase 0 任务 **S0-B**）。

---

## 5. 常见问题

### Q1：`node -v` 仍是 v16 或 v22.22.0（Cursor）

- **原因**：终端未重启，或 PATH 中旧路径 / Cursor helpers 抢先。
- **处理**：
  1. 完全退出 Cursor 后重开；
  2. 用**外部** Windows Terminal / PowerShell 再测；
  3. 检查系统与用户 Path，确保 `C:\Program Files\nodejs\` 存在且无更靠前的冲突 `node.exe`。

### Q2：同时存在多个 `node.exe`

```powershell
where.exe node
```

只应让 **官方安装目录** 排在第一位；其余（`.real`、DevEco、Cursor）不要加入 PATH，或从 PATH 移除。

### Q3：npm 全局包权限错误（可选）

开发期尽量少用全局安装；若 `npm install -g` 报权限错误，可配置前缀到用户目录：

```powershell
mkdir $env:USERPROFILE\.npm-global -Force
npm config set prefix "$env:USERPROFILE\.npm-global"
```

并将 `%USERPROFILE%\.npm-global` 加入用户 Path（npm 会提示具体路径）。

### Q4：与钉钉 Real `.real` 的关系

- 独立安装 **不会破坏** 钉钉 Real；Real 仍使用自己的 `.real\.bin\node`。
- 不要把 `.real\.bin\node` 写在系统 PATH 里与官方 Node 混用。
- **谛听 / wchat 项目**统一用官方 Node 即可。

---

## 6. Linux 上线（与本地版本对齐）

### 6.1 版本定稿（开发机 = 生产机）

| 环境 | Node | npm | 说明 |
|------|------|-----|------|
| **Windows 开发机**（DESKTOP-TH91SO5） | **v22.22.3** | **10.9.8** | 已验收（§4） |
| **Linux CVM**（SalesAgent / 运维机） | **v22.22.3** | **10.9.8** | 须与上表**完全一致** |

> **何时需要在线上装 Node？**  
> - **SalesAgent CVM（POC/MVP）**：运行时以 **Python + uvicorn** 为主，**可不装 Node**。  
> - **若 CVM 上要跑** `npm run build`、前端打包脚本、或运维工具：按本节安装，且**锁定 v22.22.3**。  
> - **谛听客户端**：仅在 **Windows 工作站** 构建安装包，不在 Linux CVM 装 Node。

升级 Node 时：**先改开发机 → 验收 → 再改 CVM → 同步更新本文与 [00-索引 §2.0](00-索引.md)**。

### 6.2 方式 A — 官方二进制包（推荐，版本最准）

适用于 **Ubuntu / Debian / CentOS** 等 x86_64 Linux；与 Windows 装 **同一次发布** 的 Linux 包。

```bash
# 变量：与本地定稿一致
NODE_VERSION=22.22.3
NODE_DIST=node-v${NODE_VERSION}-linux-x64
INSTALL_PREFIX=/usr/local

cd /tmp
curl -fsSLO "https://nodejs.org/dist/v${NODE_VERSION}/${NODE_DIST}.tar.xz"
# 可选：校验 SHA256（见 https://nodejs.org/dist/v22.22.3/SHASUMS）
# echo "2e5d13569282d016861fae7c8f935e741693c269101a5bebcf761a5376d1f99f  ${NODE_DIST}.tar.xz" | sha256sum -c -

sudo tar -xJf "${NODE_DIST}.tar.xz" -C "${INSTALL_PREFIX}" --strip-components=1
rm -f "${NODE_DIST}.tar.xz"

# 验证（必须与开发机一致）
node -v    # v22.22.3
npm -v     # 10.9.8
npx -v     # 10.9.8
which node # 期望 /usr/local/bin/node
```

**卸载 / 覆盖旧版**：删除 `${INSTALL_PREFIX}/bin/node`、`npm`、`npx` 及 `${INSTALL_PREFIX}/lib/node_modules` 后重新解压，或用新版本覆盖解压。

### 6.3 方式 B — nvm（多版本共存时）

```bash
# 安装 nvm（若未装）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc   # 或 ~/.profile

nvm install 22.22.3
nvm alias default 22.22.3
nvm use 22.22.3

node -v && npm -v
```

systemd 服务若需固定 Node：在 `Environment=PATH=/home/<user>/.nvm/versions/node/v22.22.3/bin:...` 中写死路径。

### 6.4 方式 C — NodeSource 22.x（不推荐单独用于锁补丁号）

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v && npm -v
```

NodeSource 可能装到 **22.x 最新补丁**而非恰好 **22.22.3**。装完后**必须**核对：

```bash
node -v   # 若不是 v22.22.3，改用法 A 或 B
```

### 6.5 国内镜像（可选）

CVM 拉取 nodejs.org 慢时，可用 npmmirror 分发站（仍须 **v22.22.3**）：

```bash
NODE_VERSION=22.22.3
NODE_DIST=node-v${NODE_VERSION}-linux-x64
curl -fsSLO "https://npmmirror.com/mirrors/node/v${NODE_VERSION}/${NODE_DIST}.tar.xz"
```

npm  registry（与开发机一致时可设）：

```bash
npm config set registry https://registry.npmmirror.com
npm ping
```

### 6.6 Linux 验收清单

在 CVM 上执行，**全部通过**才算与本地对齐：

```bash
node -v                    # 必须：v22.22.3
npm -v                     # 必须：10.9.8
npx -v                     # 必须：10.9.8
which node npm npx         # 路径唯一、无旧版抢先
npm ping                   # PONG（registry 可达）
```

可将以下写入部署脚本或 Ansible，发布前自动检查：

```bash
test "$(node -v)" = "v22.22.3" || { echo "Node version mismatch"; exit 1; }
test "$(npm -v)" = "10.9.8" || { echo "npm version mismatch"; exit 1; }
```

### 6.7 与本项目其他组件

| 组件 | Linux CVM 是否需要 Node |
|------|-------------------------|
| SalesAgent `uvicorn :8765` | **否**（Python 3.11+） |
| Chroma / BGE / DeepSeek | **否** |
| MVP 夜间 ingest（Qwen-VL） | **否** |
| 仅在 CVM 执行前端 build 脚本时 | **是**（v22.22.3） |

---

## 7. 验收清单

### 7.1 Windows 开发机（已完成）

在 [00-索引 §2.0](00-索引.md) 勾选：

- [x] `node -v` = **v22.22.3**，路径为 `C:\Program Files\nodejs\`
- [x] `npm -v` / `npx -v` = **10.9.8**
- [x] `npm ping` 通过（npmmirror）
- [ ] （可选）§4.3 lodash 冒烟

### 7.2 Linux CVM（上线前，若安装 Node）

- [ ] `node -v` = **v22.22.3**
- [ ] `npm -v` = **10.9.8**
- [ ] §6.6 脚本检查通过

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-17 | 初稿：Windows 独立安装、验证、与 .real/Cursor 区分 |
| v1.1 | 2026-06-17 | §6 扩写 Linux 上线；锁定 **v22.22.3 + npm 10.9.8** 与本地一致 |
