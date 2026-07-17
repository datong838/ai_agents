# 43 · T-UI S2 业务深页（按域·API 可接线）方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：T-UI **S2 第一刀** — 将蓝图 Stub 中**已有 aos-api 契约**的页升为 live  
> **对齐**：[38](38-T-UI-壳与蓝图视觉对齐方案.md) · [34](34-系统启动与蓝图符合性检查记录.md) · [T-UI](T-UI-前端工程与foundry-html落地规范.md) · foundry/html v1.6.5  
> **工程**：`aos-platform/apps/web`（+ 最小 API：`GET /v1/schedules`）  
> **硬规则**：UI 真源=html 叙事；只调 aos-api；诚实 — 无契约页仍 Stub；不 1:1 复刻 html 动效

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文通过后再改 nav/App |
| 最小更改 | 复用 PageChrome + api client；一文件多薄页 |
| 不影响主路径 | 已 live 页不改行为 |
| 中文 | 页标题/lede 中文 |

---

## 1. 目标 / 非目标

| 目标 | 非目标 |
| --- | --- |
| 按域把可接线 S2 → `status: live` + 真实读/写面板 | html 像素级 1:1、大屏动效 |
| 侧栏徽标去掉 S2（升格页） | Ferry / Release 通道 / OKF 漏斗（无契约或延期） |
| vitest 绿；nav 段序不变 | Playwright 视觉 CI |

---

## 2. 本刀升格清单（API → 页）

### 2.1 工作台

| path | API | 交互 |
| --- | --- | --- |
| `/workshop/graph` | object-types · objects · neighbors | 选类型/实例 → 1-hop 邻居 |
| `/workshop/events` | GET/POST `/v1/actions/webhooks` | 列表 + 注册 Demo webhook |

### 2.2 AIP

| path | API | 交互 |
| --- | --- | --- |
| `/aip/tools` | `/v1/aip/tools` | 列表 |
| `/aip/model-providers` | `/v1/aip/providers` | 列表 |
| `/aip/model-router` | providers + `/v1/aip/models/warmup` | 读 + Warmup 按钮 |
| `/aip/evals` | evals/status · evals/set | 状态 + 门控切换 |
| `/aip/lineage` | drafts 列表；可选 lineageId 查询 | 只读谱系入口 |

### 2.3 本体

| path | API | 交互 |
| --- | --- | --- |
| `/ontology/graph-health` | `/v1/ontology/graph-health` | 分数 + metrics |
| `/ontology/funnel` | `/v1/funnel/WorkOrder/status` | 阶段展示 |
| `/ontology/wiki` | `/v1/wiki/WorkOrder/wo-1001` | 活知识只读 |
| `/ontology/branches` | `/v1/ontology/branches` | 分支列表 |

### 2.4 数据

| path | API | 交互 |
| --- | --- | --- |
| `/data/media-sets` | `/v1/media-sets` | 列表 |
| `/data/pipelines` | `/v1/pipelines` | 列表 |
| `/data/builds` | `/v1/builds` | 列表 |
| `/data/datasets` | `/v1/datasets` | 列表 + 点进 history |
| `/data/schedules` | **新增** `GET /v1/schedules` | 列表 |
| `/data/health` | object-store/health · mysql/health | 双探针 |
| `/data/agents` | `/v1/edge/agents/local` | 边缘代理 |

### 2.5 Apollo

| path | API | 交互 |
| --- | --- | --- |
| `/apollo/spoke` | `/v1/apollo/spokes/local` | 详情 |
| `/apollo/config` | `/v1/apollo/config` | 配置（无密钥明文） |
| `/apollo/assets` | POST `/v1/apollo/assets` | 打包按钮 + 结果 |

### 2.6 仍 Stub（本刀不做）

| path | 原因 |
| --- | --- |
| `/workshop/cop` · `/workshop/module-interface` | 无稳定契约 / P2 |
| `/aip/maturity` | 楼梯叙事页，后置 |
| `/ontology/okf-funnel` | 行业专用 |
| `/data/pipeline-proposals` · `/data/code-repos` · `/data/lineage` | 无契约或与决策谱系混淆 |
| `/apollo/release` · `/apollo/ferry` · `/apollo/change` | Ferry 延期；通道/变更后置 |

---

## 3. 代码落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../43-*.md` | 本文 |
| `aos_api/routers/wave_ext.py` | `GET /v1/schedules` |
| `apps/web/src/nav.ts` | 升格项 `s2` → `live` |
| `apps/web/src/pages/s2/*.tsx` | 薄页 + 共用 JsonPanel |
| `apps/web/src/App.tsx` | 注册 live 路由；剩余 s2 仍 stub |
| `apps/web/src/nav.test.ts` | 断言升格数量 / 关键 path live |
| `26` / `31` / `34` / `00` | S2 进度回写 |

---

## 4. 自测

- [ ] vitest 全绿
- [ ] 升格 path `status===live`；仍 stub 的 path 存在
- [ ] （可选）浏览器点开 graph-health / datasets / evals 有数据（需 API 起）

---

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| 内存 Facade 空列表 | 页上提示「先去数据连接跑 Pipeline」 |
| 与 html 视觉差 | lede 标明「S2 MVP · 契约接线」 |

---

*v1.0 · T-UI S2 第一刀*
