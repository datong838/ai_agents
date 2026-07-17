# 环境准备 — Vidu 视频生成（SkillHub 接入）

> **角色**：谛听 **「做视频」** 远期能力的外部执行层（文/图 → 短视频片段）  
> **阶段**：**POC 准备**（非 MVP 阻塞项；与 M6-3 文案、M6-2 `video_script` 技能对齐）  
> **Skill 来源**：[SkillHub · vidu-video-generate-2](https://skillhub.cn/skills/vidu-video-generate-2)  
> **官方 API**：[Vidu 开放平台 · Skills 文档](https://platform.vidu.cn/docs/skills)  
> **前置文档**：[skillhub.md](skillhub.md)（SkillHub CLI 安装与 `--dir` 规范）

---

## 1. 背景与在谛听中的定位

| 项 | 说明 |
|----|------|
| 产品诉求 | 从已有 **私域/多平台文案 + 商品图**，生成可用于抖音/视频号的 **短片段** |
| 远期技能 | M6-2 技能库 `video_script`（口播稿 + 分镜）；M6-3 §十二「文章 → 分镜输入」 |
| 本方案 | **不先做谛听内置 UI**，先用 **SkillHub 安装 Vidu Skill**，在 Cursor Agent 内跑通「文生视频 / 图生视频」POC |
| 与元宝关系 | 元宝负责 **长文/识图**；Vidu 负责 **视频生成**；职责分离，互不替代 |

```mermaid
flowchart LR
  A[M6-3 文案母稿] --> B[video_script 分镜/提示词]
  B --> C[Vidu Skill CLI]
  C --> D[Vidu 开放平台 API]
  D --> E[mp4 下载到 data_root]
  E --> F[知识库 media / 发布]
```

---

## 2. 三者关系

| 名称 | 类型 | 必需 | 用途 |
|------|------|------|------|
| **Vidu 开放平台** | 云端 API | **是** | 文生视频、图生视频、参考生视频、首尾帧视频 |
| **SkillHub** | 国内 Skill 商店 + CLI | **是**（推荐） | 搜索、安装、更新 Vidu 相关 Agent Skill |
| **vidu-video-generate-2** | Cursor/Agent Skill | **是**（本 POC） | 封装 `vidu_cli.py`，对话式识别意图并调 API |

> SkillHub 上另有全量能力包 **vidu-generation**（含 TTS、声音复刻、文生图等）。  
> 本阶段仅装 **视频生成专版** `vidu-video-generate-2`，范围更小、与「做视频」目标一致。  
> 官方技能索引见 [platform.vidu.cn/docs/skills](https://platform.vidu.cn/docs/skills)。

---

## 3. 前置条件

| # | 项 | 要求 | 自检 |
|---|-----|------|------|
| 1 | 操作系统 | Windows 10+（本机开发） | ✅ |
| 2 | Python | 3.11+（与 Skill 内 `vidu_cli.py` 一致） | `python --version` |
| 3 | Node.js | 20+（SkillHub 安装脚本不强制，项目已有） | 见 [08-Node.js](08-Node.js-独立安装.md) |
| 4 | 网络 | 可访问 `platform.vidu.cn`、`skillhub.cn` | 浏览器打开控制台 |
| 5 | SkillHub CLI | 已安装 | 见 [skillhub.md §一](skillhub.md) |
| 6 | Vidu 账号 | 已注册并创建 API Key | 见 §5 |

---

## 4. 安装 SkillHub CLI

按 [skillhub.md](skillhub.md) 执行，**仅搜索/安装技能时不必重复询问优先源**。

```bash
command -v skillhub && skillhub --version
```

未安装时：

```bash
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash
```

---

## 5. 安装 Vidu Skill（vidu-video-generate-2）

### 5.1 搜索与确认

```bash
skillhub search vidu
# 或精确搜索
skillhub search vidu-video-generate
```

在 [SkillHub 技能页](https://skillhub.cn/skills/vidu-video-generate-2) 确认版本与说明后再安装。

### 5.2 安装到 Cursor Skills 目录

⚠️ **必须** `--dir` 指向当前 Agent 的 skills 目录，否则默认 `./skills/` 不会被识别。

**Windows（本机 Cursor）**：

```bash
skillhub install vidu-video-generate-2 --dir "%USERPROFILE%\.cursor\skills"
```

**Linux / macOS**：

```bash
skillhub install vidu-video-generate-2 --dir ~/.cursor/skills
```

安装后典型路径：

```
~/.cursor/skills/vidu-video-generate-2/
├── SKILL.md
├── scripts/
│   └── vidu_cli.py          # 核心 CLI（以实际包为准）
└── ...
```

> 安装完成后 **重启 Cursor**，或在对话中 @ 该 Skill，Agent 才会加载。

### 5.3 与 clawhub 的关系

SkillHub 文档说明：国内优先 `skillhub`，无匹配时可回退 `clawhub`。  
Vidu 官方也在 ClawHub 发布 [vidu-video-generate](https://clawhub.ai/x-jihua/vidu-video-generate) / [vidu-generation](https://clawhub.ai/x-jihua/vidu-generation)；**本方案优先 SkillHub 国内镜像**。

---

## 6. Vidu 开放平台与 API Key

### 6.1 注册与开 Key

1. 打开 [Vidu 开放平台（国内）](https://platform.vidu.cn)（海外用户用 [platform.vidu.com](https://platform.vidu.com)）。
2. 登录 → **API 管理** → 创建 **API Key**。
3. 查看 **套餐 / 积分 / 每日额度**（视频生成按任务扣费，POC 前建议设预算提醒）。

### 6.2 环境变量

在项目或用户级环境中配置（**勿提交 git**）：

**Windows PowerShell（当前会话）**：

```powershell
$env:VIDU_API_KEY = "your_api_key_here"
# 国内默认；海外改为 https://api.vidu.com/ent/v2
$env:VIDU_BASE_URL = "https://api.vidu.cn/ent/v2"
```

**写入用户环境（持久）**：系统设置 → 环境变量 → 用户变量 → 新建 `VIDU_API_KEY`。

**推荐：谛听 monorepo 本地文件**（若后续 SalesAgent/脚本统一读取）：

```bash
# salesagent/.env 追加（勿 commit）
VIDU_API_KEY=your_api_key_here
VIDU_BASE_URL=https://api.vidu.cn/ent/v2
```

> 模板可后续补入 `salesagent/.env.example`；当前 POC 阶段先用户级配置即可。

---

## 7. Skill 能力矩阵（vidu-video-generate-2）

| 类型 | CLI 子命令（典型） | 触发场景 | 谛听 POC 用途 |
|------|-------------------|----------|---------------|
| 文生视频 | `text2video` | 纯文字描述 | 分镜文案 → 5s 预览片段 |
| 图生视频 | `img2video` | 商品图 + 描述 | **尚雅绣主图 → 动效展示** |
| 参考生视频 | `ref2video` | 多图 + 描述 | 多 SKU 同框种草 |
| 首尾帧视频 | `start-end2video` | 首帧 + 尾帧 + 描述 | 前后对比、转场 |

**异步任务**：提交后返回 `task_id`，需轮询状态并下载（生成 URL 约 **2 小时**内有效，需及时落盘）。

**典型调用**（`{baseDir}` 替换为 Skill 安装目录）：

```bash
# 文生视频
python "{baseDir}/scripts/vidu_cli.py" text2video --prompt "30岁宝妈护肤台，柔和自然光，产品特写"

# 图生视频（商品图）
python "{baseDir}/scripts/vidu_cli.py" img2video --image "C:/work/salesagent/data/beauty/raw/uploads/product.jpg" --prompt "镜头缓慢推近，肤质透亮"

# 轮询并下载
python "{baseDir}/scripts/vidu_cli.py" status <task_id> --wait --download "./uploads"
```

具体参数（`--model-version`、`--duration`、`--aspect-ratio`、`--transition` 等）以安装后的 `SKILL.md` 与 [Vidu API 文档](https://platform.vidu.cn/docs/skills) 为准。

---

## 8. POC 验收清单

按顺序执行，全部通过视为 **环境准备完成**：

| # | 步骤 | 命令 / 动作 | 期望 |
|---|------|-------------|------|
| 1 | SkillHub | `skillhub --version` | 有版本号 |
| 2 | Skill 已装 | 目录存在 `%USERPROFILE%\.cursor\skills\vidu-video-generate-2` | 含 `SKILL.md`、`scripts/` |
| 3 | API Key | `echo $env:VIDU_API_KEY`（PowerShell） | 非空 |
| 4 | 文生视频 smoke | Cursor 对话：「用 Vidu 生成 5 秒竖屏护肤台空镜，1080p」 | 返回 task_id 或可下载 mp4 |
| 5 | 图生视频 smoke | 选一张 `yanpanji.com` 商品图 + 简短 prompt | 生成成功并下载到本地目录 |
| 6 | 落盘规范 | 视频存到 `C:/work/salesagent/data/_staging/vidu/` 或 `diting/data/` | 文件名含日期与 work_id |

**失败排查**：

| 现象 | 处理 |
|------|------|
| `VIDU_API_KEY` 未设置 | §6.2 配置后重开终端 / Cursor |
| Skill 找不到 | 检查 `--dir` 是否为 `.cursor/skills`；重启 Cursor |
| 401 / 403 | Key 无效或额度用尽 → 开放平台控制台 |
| 任务一直 pending | 用 `status --wait` 轮询；高峰时段延长超时 |
| 下载链接过期 | 2h 内下载；POC 脚本应 **生成即落盘** |

---

## 9. 与谛听产品的衔接规划（编码前共识）

| 阶段 | 内容 | 依赖 |
|------|------|------|
| **P0 环境**（本文） | SkillHub + Vidu Key + Cursor 内手动 POC | 无 |
| **P1 脚本化** | `ditingclient/scripts/vidu_smoke.py` 封装 CLI；日志写入 `data/logs/` | P0 |
| **P2 技能库** | M6-2 启用 `video_script`：母稿 → 分镜 JSON → Vidu prompt | [M7-1 总体方案](../M7-1-短视频创作-导演智能体总体方案.md) |
| **P3 客户端** | 知识库 Tab **「短视频」**；异步任务 + 本地 mp4 预览 | M7-1a–d |
| **P4 入库** | `media_node` 增加视频路径；角色/场景库 | M7-2 美术 Skill |

**首期不做**：服务端代调 Vidu（Key 留本机）；不做全自动发布抖音。

---

## 10. 安全与合规

| 项 | 要求 |
|----|------|
| API Key | 仅本机 `.env` / 用户环境变量；**禁止** commit、禁止写进文案库 JSON |
| 生成内容 | 美妆类遵守广告法；不用「7 天见效」等违规表述（与 [M6-3-2 头条 SOP](../M6-3-2-私域转今日头条-SOP.md) 一致） |
| 素材版权 | 图生视频仅使用 **自有商品图 / 已授权素材** |
| 费用 | POC 前在 Vidu 控制台确认单次积分；批量生成需审批 |

---

## 11. Windows 与 Linux 差异

| 项 | Windows（开发机） | Linux（未来 CVM） |
|----|-------------------|-------------------|
| Skill 目录 | `%USERPROFILE%\.cursor\skills` | `~/.cursor/skills` |
| Python | `C:\Python314\python.exe` 或 3.11 venv | `python3.11` |
| 视频落盘 | `C:/work/salesagent/data/_staging/vidu/` | `/www/wwwroot/salesagent/data/_staging/vidu/` |
| SkillHub 安装 | 同 skillhub.md；需 curl 或 Git Bash | `curl \| bash` 直接可用 |

---

## 12. 相关链接

| 资源 | URL |
|------|-----|
| SkillHub 技能页 | https://skillhub.cn/skills/vidu-video-generate-2 |
| SkillHub 安装说明 | [skillhub.md](skillhub.md) |
| Vidu 官方 Skills 索引 | https://platform.vidu.cn/docs/skills |
| Vidu 开放平台（国内） | https://platform.vidu.cn |
| 官方 vidu-skills 仓库 | https://github.com/shengshu-ai/vidu-skills |
| 谛听 M6-3 文案脚手架 | [M6-3-智能写作技能-文案脚手架方案.md](../M6-3-智能写作技能-文案脚手架方案.md) |
| 谛听 M6-2 video_script | [M6-2-通用客服智能体与话术策略知识库方案.md](../M6-2-通用客服智能体与话术策略知识库方案.md) |

---

## 13. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-04 | 初稿：SkillHub + vidu-video-generate-2 环境准备；Vidu API Key；POC 验收与谛听衔接规划 |
