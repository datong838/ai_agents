# M7-2e · Agnes-2.0-Flash 结构化规划（试验）

> **状态**：已编码 · **待 API Key 验证** · 2026-07-06  
> **定位**：与 **元宝 Prompt + Agnes 出图（默认）+ 豆包备选** **并行**，不替代  
> **引擎**：`agnes-2.0-flash`（OpenAI 兼容 API · 免费文本兜底）

---

## 一、双轨策略（拍板）

| 轨道 | 引擎 | 职责 | 状态 |
|------|------|------|------|
| **A · 美术 Prompt + 出图** | 元宝 UIA + **Agnes Image API**（豆包备选） | 各素材 `prompt_en`；参考图 API 落盘 | **保留 · 主链路 · S3 v1.3** |
| **B · 结构化规划** | **Agnes-2.0-Flash API** | 评估后拆解、分镜描述、角色/场景/道具、Pavo 简报 | **本方案 · 试验验证** |

```text
script_approved
    ├─ 轨道 A：art_brief → 元宝 → Prompt → Agnes 出图（豆包备选）→ art_assets/
    └─ 轨道 B：POST .../agnes/plan → JSON + pavo_brief.md
              → 可喂 Pavo / 未来 art_extractor / 分镜 S4
```

**为何 Agnes 做 B 不做 A 的 Prompt**：Agent 多步规划、JSON 格式化、长上下文更稳；**免费**；元宝仍负责 **与人一致的 Prompt 文案** 和已有 UIA 闭环。

---

## 二、产出契约

落盘路径（`save=true` 时）：

```text
video_projects/{project_id}/artifacts/
├── agnes_production_plan_latest.json
├── agnes_production_plan_{ts}.json
└── agnes_pavo_brief_{ts}.md          # plan.pavo_creative_brief_md
```

`agnes_production_plan_latest.json` 顶层字段：

| 字段 | 说明 |
|------|------|
| `characters` / `scenes` / `props` | 对齐 S3 三类库 ID |
| `beats` | 结构化 Beat |
| `storyboard_shots` | 分镜镜号列表（对接 Pavo / S4） |
| `pavo_creative_brief_md` | 粘贴 Pavo「剧情短片」 |

`project.json.artifacts.agnes_production_plan_latest` 指向最新 JSON。

---

## 三、代码路径

| 模块 | 路径 |
|------|------|
| HTTP 客户端 | `salesagent/.../knowledge/agnes_client.py` |
| 规划器 | `salesagent/.../knowledge/agnes_video_planner.py` |
| API | `knowledge.py`：`GET/POST .../agnes/plan`，`GET .../video/agnes/ping` |
| 验证脚本 | `salesagent/scripts/verify_agnes.py` |

---

## 四、环境配置

`salesagent/.env`：

```env
AGNES_API_KEY=sk-...
# AGNES_BASE_URL=https://apihub.agnes-ai.com/v1
# AGNES_TEXT_MODEL=agnes-2.0-flash
```

注册：https://platform.agnes-ai.com/

---

## 五、验证步骤

### 5.1 连通性

```powershell
cd c:\work\projects\wchat\salesagent
# .env 已写 AGNES_API_KEY
python scripts/verify_agnes.py ping
```

期望：`{"ok": true, "model": "agnes-2.0-flash", ...}`

### 5.2 无项目 · 样例剧本

```powershell
python scripts/verify_agnes.py plan
```

期望：stdout 含 `characters`、`storyboard_shots`、`pavo_creative_brief_md`

### 5.3 绑定短视频项目

```powershell
python scripts/verify_agnes.py plan --project-id vp_你的项目ID --category beauty
```

期望：写入 `artifacts/agnes_production_plan_latest.json`

### 5.4 HTTP API（SalesAgent 8765 已启动）

```http
GET  /knowledge/video/agnes/ping
POST /knowledge/video/project/{project_id}/agnes/plan
     {"category":"beauty","project_id":"...","user_notes":"","save":true}
GET  /knowledge/video/project/{project_id}/agnes/plan
```

---

## 六、验收标准

| # | 项 | 通过 |
|---|-----|------|
| V1 | `ping` 成功 | latency_ms 有值 |
| V2 | `plan` 样例 | JSON 含 ≥1 storyboard_shots |
| V3 | 真实项目 | 与剧本 Beat 数大致匹配 |
| V4 | Pavo 简报 | `agnes_pavo_brief_*.md` 可粘贴 Pavo 试跑 |
| V5 | 轨道 A 不变 | 元宝/豆包流程未改 |

---

## 七、修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1 | 2026-07-06 | 双轨拍板；agnes_client + planner + API + verify 脚本 |
