# 76 · 蓝图 vs 已启动页比对 + Failed-to-fetch 运维自检

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 方案 · **本波落地：API 可达性 / 前端错误日志 / 供应商卡片 / 数据源·同步列表**  
> **对齐**：`foundry/html` DEMO_PAGES · [75](75-蓝图深交互分波计划.md) · [72](72-系统启停与健康检查手册.md)  
> **工程**：`aos-platform/apps/web` · `scripts/demo/ensure-api.sh`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 开发须有日志 | API JSON 日志 + 浏览器 `console` 结构化日志 |
| 最小更改 | 不推倒 S2；先修根因再加深交互 |
| 对齐蓝图 | 侧栏映射已全；深交互按深度分档补 |

---

## 1. 根因：大量 `Failed to fetch`

| 现象 | 浏览器 TypeError `Failed to fetch` |
| --- | --- |
| **根因** | Vite `:5173` 在线，**aos-api `:8080` 进程掉线** → 连接拒绝（非业务 4xx） |
| **日志真源** | `deploy/dev/aos-api.out.log` / `aos-api.err.log`（ensure / start-local-native） |
| **自检** | `bash scripts/demo/health-check.sh` · 缺 API 则 `FAIL aos-api` |
| **修复** | `bash scripts/demo/ensure-api.sh`（本波新增；**独立 session**，防 Agent shell 收尾杀进程）或 `start-local-native.sh` |

**本波前端增强（强制）：**

1. `api/client.ts`：网络失败改写为中文可行动提示 + `console.warn`/`error`（method/path/status/traceId）  
2. AppShell：顶栏 **API 状态条**（轮询 `/v1/health`，宕机红色提示日志路径）

---

## 2. 侧栏映射 vs 交互深度

约定深度：

| 档 | 含义 |
| --- | --- |
| **D3** | 可点、可存、可回看（75 W1～W4 / 74） |
| **D2** | 有操作按钮 + 列表卡片（非纯 JSON） |
| **D1** | S2 JSON / ItemsPage |
| **D0** | Stub（当前侧栏已无 D0） |

| 蓝图 id | React 路径 | 深度 | 缺口 / 本波动作 |
| --- | --- | --- | --- |
| index | `/` | D2 | OK |
| workshop* | `/workshop…` | D2～D3 | 画布 D3；运营台 D3；余 D2 |
| aip-model-providers | `/aip/model-providers` | D1→**D2** | **本波**：卡片列表 + 就绪态 |
| aip-model-router | `/aip/model-router` | D2 | 试聊已有 |
| aip-logic | `/aip/logic` | D3 | 75 W2 |
| aip-tools / studio / … | `/aip/*` | D1～D2 | 后续波加深 Adapter 表单 |
| ontology | `/ontology` | D3 | 75 W3 |
| ontology-* | `/ontology/*` | **D2** | **77 已对齐** graph-health/funnel/wiki/branches/okf |
| data-connection | `/data` | D2→**D2+** | **本波**：Sources/Syncs 列表 + Router |
| data-* | `/data/*` | **D2** | **77 已对齐** · schedules PATCH |
| apollo-hub | `/apollo` | D3 | 75 W4 |
| apollo-* | `/apollo/*` | D1～D2 | Ferry Full 仍延期 |

**蓝图 HTML 有、侧栏未挂（子页）：**  
`ontology-action/object/link/property/function` · `source-*` · `sync*.html` · `pipeline.html` — 由父页链接进入，**不强制进侧栏**；后续按需升 D2。

---

## 3. 本波交付清单

- [x] 方案本文  
- [x] `ensure-api.sh` + 拉起 API  
- [x] `api/client` 网络错误中文化 + console 日志  
- [x] AppShell API 状态条  
- [x] Providers 卡片化  
- [x] Data 页 Sources/Syncs  
- [x] 00 索引挂载 · 自测

---

## 4. 验收

1. API 停掉 → 顶栏红条 + 页内错误含「aos-api :8080」与日志路径（不再裸 `Failed to fetch`）  
2. `ensure-api.sh` 后 `/data`、`/aip/model-providers` 有数据/卡片  
3. `npm test` 绿 · `health-check.sh` API OK  

---

## 变更日志

| 版本 | 说明 |
| --- | --- |
| v1.0 | 根因自检 + 比对台账 + 本波落地项 |

*76 · 先救命（API）再对齐蓝图深度*
