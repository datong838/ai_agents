# 93 · W16 Data 子页 bp-ui 加深 · Graph→Buddy 上下文 · 可演示 DoD 清单

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[77](77-Data与Ontology子页蓝图对齐方案.md) · [91](91-W14-Workshop运行态链路与Apollo延后方案.md) · [87](87-W11-Polish调试输出BpDebugPanel对齐方案.md)  
> **约束**：Apollo 不深化 · 概览无业务主链 · JSON 仅 `<details>`/BpDebugPanel 折叠

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 20_tech 约束 | 先本文后改 `apps/web` |
| 最小更改 | 仅 3 页 + 索引回写 |
| 禁 JSON 主面板 | 主区 BpTable/BpPropGrid/BpLineageTimeline |
| Apollo 延后 | DoD 不含 `/apollo/*` 深水 |

---

## 1. 范围

| 项 | 文件 | 动作 |
| --- | --- | --- |
| 媒体集列表 | `s2/data.tsx` · `MediaSetsPage` | `card-list` → `BpTable` + `BpMetricGrid`；解析 → `BpDebugPanel` |
| 数据集详情 Tab | `s2/data.tsx` · `DatasetsPage` | `details` Tab：`JsonBlock` → `BpPropGrid` + `<details>` 折叠 JSON |
| 数据沿袭 | `s2/remainder.tsx` · `DataLineagePage` | 沿袭链 → `BpLineageTimeline`；History 保持 `JsonBlock`（调试折叠） |
| Graph @Buddy | `s2/workshop.tsx` · `GraphExplorerPage` | 链 `/workshop/buddy?order={objectId}&assist=1`（对齐 Inbox） |

---

## 2. Graph→Buddy 契约

与 [91](91-W14-Workshop运行态链路与Apollo延后方案.md) Inbox 一致：

```text
/workshop/buddy?order=<objectId>&assist=1
```

`BuddyPage` 已 `useSearchParams` 读 `order`/`assist`；Graph 选中实例后带参跳转。

---

## 3. 本地可演示 DoD 清单（挂 70/72）

> **用途**：TB.8 彩排前自检；**不含** Apollo Full / 现场 Ferry / 客户 IdP。

### 3.1 基建（TB.0 · [72](72-系统启停与健康检查手册.md)）

| # | 检查 | 命令/入口 |
| --- | --- | --- |
| D1 | API 健康 | `curl -s localhost:8080/v1/health` 或 `bash scripts/demo/ensure-api.sh` |
| D2 | Web 可访问 | `http://localhost:5173/` |
| D3 | 冒烟脚本 | `bash scripts/demo/run-demo-smoke.sh` |
| D4 | pytest 回归 | `bash scripts/ci/run-pytest.sh`（179+ passed） |
| D5 | 前端单测 | `cd apps/web && npm test`（18 绿） |

### 3.2 故事路径（TB.1～TB.7 · [70](70-业务平台可演示优先计划.md)）

| # | 客户可见 | 路由 |
| --- | --- | --- |
| S1 | 行业种子 | `/data` · **初始化业务数据** |
| S2 | 数据进故事 | `/data/datasets` · `/data/builds` · `/data/lineage`（本波加深） |
| S3 | 本体运营 | `/ontology` · `/ontology/funnel` |
| S4 | 写回闭环 | `/aip/drafts` · **一键写回闭环** |
| S5 | Workshop | `/workshop/inbox` → `/workshop/graph` → `/workshop/buddy?order=…` |
| S6 | AIP 辅助 | `/aip/capabilities` · **业务一镜** |
| S7 | 治理可见 | `/aip/lineage` · **治理探针** |

### 3.3 本波增量验收

1. `/data/media-sets` 主区为表格，解析结果在折叠调试面板 ✅  
2. `/data/datasets` · details Tab 为属性网格，非裸 JSON ✅  
3. `/data/lineage` 沿袭链为时间线组件 ✅  
4. `/workshop/graph` 选中对象后 @Buddy 带 `order` 参数 ✅  
5. `npm test` 绿 ✅  

---

## 4. 风险

| 风险 | 缓解 |
| --- | --- |
| Buddy 无 order 时行为 | 仍链 `/workshop/buddy` 空参（与 Inbox 一致） |
| Dataset detail 字段多 | `flattenRecordProps` 限 12 键；完整 JSON 在 `<details>` |

---

## 变更日志

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-18 | W16 方案 + DoD 清单 |

---

*v1.0*
