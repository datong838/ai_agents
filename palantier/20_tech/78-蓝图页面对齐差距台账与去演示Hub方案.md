# 78 · 蓝图页面对齐差距台账与去演示 Hub 方案

> **版本**：v1.1 · 2026-07-18（**W25 P1/P2 收口 · 可演示冻结** · 挂 [102](102-W25-蓝图审计P1收口与可演示冻结方案.md)）  
> **状态**：✅ UI 抛光 W15～W24 完成 · **编码默认冻结**（Apollo Full / 1.3 / doc-intel 除外点名）  
> **真源**：`docs/palantier/foundry/html/` · [26 §12](26-AOS目标态开发计划.md) · [77](77-Data与Ontology子页蓝图对齐方案.md)  
> **工程**：`aos-platform/apps/web` · `services/aos-api/aos_api/demo_story.py`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI 文案 |
| 先方案后编码 | 本文 → 再改 `apps/web` / `demo_story.py` |
| 最小更改 | 只删演示 Hub；TB API 保留；入口迁到真实页 |
| 蓝图双对齐 | 26 §12 不仅看 API，也看 foundry/html **区块/布局** |
| 演示 = 真实页 | 禁止独立「客户演示导航」；概览只链 `steps[].uiPath` |

---

## 1. 决策摘要

| 项 | 旧态 | 新态 |
| --- | --- | --- |
| 侧栏「客户演示」 | `/demo` DemoPage | **删除** |
| TB.* 按钮集中 | DemoPage 五键 | **分散**：Data / Drafts / Lineage / Capability / 概览主链 |
| 彩排话术 | 打开 `/demo` | [CUSTOMER-DEMO.md](../../aos-platform/scripts/demo/CUSTOMER-DEMO.md) 改走真实路由 |
| 后端 API | `/v1/demo/*` | **保留**（种子/写回/治理/一镜）；仅 UI 入口变更 |
| 差距口径 | 69 能力成熟度 | **本文 §3** 补「页面展示细节」列 |

---

## 2. TB.* 能力回迁映射

| TB | 能力 | API | 真实 UI 入口 |
| --- | --- | --- | --- |
| TB.0 | 本地启动 | `GET /v1/health` | `/` 概览状态条 + [72](72-系统启停与健康检查手册.md) |
| TB.1 | 行业种子 | `POST /v1/demo/ensure-seed` | `/data` · **初始化业务数据** |
| TB.2 | 数据进故事 | datasets/builds/dlq | `/data` · 子页 `/data/datasets` 等 |
| TB.3 | 本体运营 | funnel/objects | `/ontology` · `/ontology/funnel` |
| TB.4 | 写回闭环 | `POST /v1/demo/run-story` | `/aip/drafts` · **一键写回闭环** |
| TB.5 | Workshop | object-sets/query | `/workshop/canvas` |
| TB.6 | Buddy | `POST /v1/buddy/ask` | `/workshop/buddy` |
| TB.7 | 治理可见 | `GET /v1/demo/governance` | `/aip/lineage` · **治理探针** |
| TB.8 | 演示彩排包 | `run-rehearsal-smoke` · [CUSTOMER-DEMO.md](../../aos-platform/scripts/demo/CUSTOMER-DEMO.md) | `/` 四域 live 指标 · 无业务主链（[92](92-W15-概览控制面bp-ui与死代码清理方案.md)） |
| TB.9 | Capability 一镜 | `POST /v1/demo/run-capability` | `/aip/capabilities` · **业务一镜** |

---

## 3. 页面 × 蓝图 × 差异台账（全侧栏）

图例：**UI** = 展示/layout · **API** = 后端 · **深** = 可演示交互 · **薄** = 有路由但 JSON/占位 · **缺** = 未实现

### 3.1 概览 · 工作台

| 蓝图 HTML | 路由 | 蓝图展示要点 | 现有 API/能力 | 页面现状 | 差异 / 下一刀 |
| --- | --- | --- | --- | --- | --- |
| index | `/` | 四域色带卡片 + 控制面 live 指标 | health/story/models | OverviewPage | **深** ✅ 92/97 |
| workshop | `/workshop` | Module 卡片 grid | `GET /v1/modules` | WorkshopListPage | **深** ✅ 85/105 · hover 对齐 workshop.html |
| workshop-canvas | `/workshop/canvas` | 左组件库+中画布+右预览 | PATCH widgets · query | CanvasPage | **深** ✅ 90/107 · widget 示意密度 |
| workshop-module | `/workshop/inbox` | Filter+Table+ObjectView+变量条 | inbox · action | InboxPage | **深** ✅ 80 |
| workshop-object-view | `/workshop/graph` | Graph+Object View | objects/neighbors | GraphExplorerPage | **深** ✅ 83/93 @Buddy 带 order |
| workshop-aip-chat | `/workshop/buddy` | 表格+Assist+Buddy 侧栏 | buddy/ask | BuddyPage | **深** ✅ 84/95 真实 WorkOrder |
| workshop-cop | `/workshop/cop` | 大屏 KPI | metrics | CopPage | **深** ✅ 82 |
| workshop-publish | `/workshop/publish` | 发布通道 | publish API | PublishPage | **深** ✅ 84 |
| workshop-module-interface | `/workshop/module-interface` | 接口契约表 | modules | ModuleInterfacePage | **深** ✅ 83 |
| workshop-events | `/workshop/events` | 事件订阅表 | webhooks | EventsPage | **深** ✅ 83 |

### 3.2 AIP

| 蓝图 | 路由 | 蓝图要点 | API | 现状 | 差异 |
| --- | --- | --- | --- | --- | --- |
| aip-maturity | `/aip/maturity` | 楼梯 Threads→Agent | maturity | MaturityPage | **深** ✅ 81 |
| aip-model-providers | `/aip/model-providers` | 卡片+表单 | models | ProvidersPage | **深** ✅ 85/99 凭据+测连通 |
| aip-model-router | `/aip/model-router` | 路由表+试聊 | router | ModelRouterPage | **深** ✅ 82 |
| aip-capabilities | `/aip/capabilities` | Job+Session 卡片 | capabilities | CapabilityPage | **深** ✅ 83 |
| agents | `/aip/studio` | Prompt+Agent | studio | StudioPage | **深** ✅ 90/96 wo-1001 · Agnes 试聊 |
| aip-tools | `/aip/tools` | 六类工具 Wiki | tools/plugins | ToolsPage | **深** ✅ 81 |
| aip-logic | `/aip/logic` | 三栏 CoT Debug | logic/run | LogicPage | **深** ✅ 86/96 Use LLM 试聊 |
| aip-draft-inbox | `/aip/drafts` | HITL 列表+批准 | drafts | DraftInboxPage | **深** ✅ 79 |
| aip-decision-lineage | `/aip/lineage` | 谱系时间线 | lineage | DecisionLineagePage | **深** ✅ 79 |
| aip-evals | `/aip/evals` | Eval 门控表 | evals | EvalsPage | **深** ✅ 81 |

### 3.3 本体 · 数据（77 已 D2 的标注 ✅）

| 蓝图 | 路由 | 要点 | 现状 | 差异 |
| --- | --- | --- | --- | --- |
| ontology | `/ontology` | Discover+7 Tab | object-types | OntologyPage | **深** ✅ 80/82 |
| ontology-funnel 等 5 子页 | `/ontology/*` | 77 表 | **✅ D2 bp-ui** | — |
| data-connection | `/data` | Router+Sources+Tab | DataPage | **深** ✅ 85/100 Hub live 指标 |
| data 10 子页 | `/data/*` | 77 表 | **✅ D2** · media-sets/lineage/dataset-details **93 加深** | parsers JSON 折叠 OK |

### 3.4 Apollo

| 蓝图 | 路由 | 要点 | 现状 | 差异 |
| --- | --- | --- | --- | --- |
| apollo-hub | `/apollo` | 舰队+Channel | fleet/channels | ApolloPage | **深** ✅ 84 |
| release/spoke/ferry/assets/change/config | `/apollo/*` | 各子页布局 | apollo API | s2 bp-ui | **深** ✅ 81/84 · change 工作流 UI **后置**（Apollo 停车场） |

---

## 4. 本波代码落点

| 文件 | 变更 |
| --- | --- |
| `apps/web/src/pages/DemoPage.tsx` | **删除** |
| `apps/web/src/App.tsx` | 移除 `/demo` route |
| `apps/web/src/nav.ts` | 移除 `demo-story` |
| ~~`StoryChainPanel.tsx`~~ | **已删**（[92](92-W15-概览控制面bp-ui与死代码清理方案.md)） |
| `apps/web/src/pages/OverviewPage.tsx` | 去 TB Hub · 四域 live（[97](97-W20-概览四域Live指标与控制面加深方案.md)） |
| `apps/web/src/pages/DraftInboxPage.tsx` | TB.4 一键写回 |
| `apps/web/src/pages/s2/aip.tsx` | DecisionLineage TB.7 治理探针 |
| `apps/web/src/pages/CapabilityPage.tsx` | TB.9 业务一镜 |
| `apps/web/src/pages/DataPage.tsx` 等 | 去 `/demo` 链 · 文案「初始化业务数据」 |
| `demo_story.py` | `uiPath` 去 `/demo` · uiPaths 改真实路由 |
| `scripts/demo/CUSTOMER-DEMO.md` | 彩排改真实页 |
| [69](69-与目标态差距台账.md) v1.3 | 挂 78 · 演示入口口径 |
| [00-技术方案索引](00-技术方案索引.md) | 挂 78 |

---

## 5. 验收

1. 侧栏**无**「客户演示」；访问 `/demo` 重定向 `/`  
2. TB.1～TB.9 均可从对应真实页触发（无 DemoPage）  
3. 概览**无**业务主链区块；TB.8 走 [CUSTOMER-DEMO.md](../../aos-platform/scripts/demo/CUSTOMER-DEMO.md) + `run-rehearsal-smoke.sh`  
4. `npm test` 绿 · `run-rehearsal-smoke.sh` OK  

---

## 6. 下一波优先级（W5+）

| 优先级 | 项 | 依据 | 状态 |
| --- | --- | --- | --- |
| P0 | 概览 index 四域 grid 对齐 | 蓝图 index.html | ✅ [79](79-W5概览与AIP-Draft-Lineage蓝图对齐方案.md) |
| P0 | Draft/Lineage 去 JSON 主面板 | aip-draft-inbox / decision-lineage | ✅ 79 |
| P1 | Inbox 运营台变量条+Action 分栏 | workshop-module.html | ✅ [80](80-W6运营台Inbox与本体Discover蓝图对齐方案.md) |
| P1 | ontology.html 主站 Discover 布局 | vs OntologyPage | ✅ 80 |
| P2 | AIP tools/maturity/evals 薄页 D2 | s2/aip.tsx | ✅ [81](81-W7-AIP薄页与Apollo子页蓝图对齐方案.md) |
| P2 | Apollo 子页 JSON→bp-ui | remainder/apollo | ✅ 81 |

| P2 | workshop-cop 态势 KPI + Map | s2/extras JSON | ✅ [82](82-W8-COP-ModelRouter-ObjectType7Tab蓝图对齐方案.md) |
| P2 | aip-model-router 路由表 | s2/aip 部分 | ✅ 82 |
| P2 | ontology-object 7 Tab | OntologyPage 缺 Tab | ✅ 82 |

| P2 | workshop/graph Object View | s2/workshop JSON | ✅ [83](83-W9-Workshop薄页与Capabilities蓝图对齐方案.md) |
| P2 | module-interface / events | s2 JSON | ✅ 83 |
| P2 | aip-capabilities Session 区 | CapabilityPage JSON | ✅ 83 |

| **审计** | 全量 56 HTML 映射 + P0 缺口修复 | [84](84-蓝图与实现全面审计台账.md) | ✅ 84 |

| P2 | BpDiscoverCard 复用 | OntologyPage · CapabilityPage | ✅ [86](86-P2尾项DiscoverCard与Draft-Logic对齐方案.md) |
| P2 | Draft 队列+详情分栏 | DraftInboxPage | ✅ 86 |
| P2 | Logic kind 色带 + Debug 折叠 | LogicPage | ✅ 86 |

| W11 | BpDebugPanel 调试输出统一 | blueprintUi + 6 页 | ✅ [87](87-W11-Polish调试输出BpDebugPanel对齐方案.md) |

| W12 | macOS 冒烟 + 72 去 `/demo` | scripts/demo/*.sh · 72 v1.2 | ✅ [88](88-W12-macOS冒烟与72启停手册对齐方案.md) |

| W13 | aos-api pytest 全量 + CI | actions.py · run-pytest.sh · 27 G6 | ✅ [89](89-W13-aos-api-pytest回归与CI门禁方案.md) |

| W10 尾 | publish/buddy/canvas/studio 薄页 | 4 页 + styles.css | ✅ [90](90-W10剩余薄页Publish-Buddy-Canvas-Studio对齐方案.md) |

| W14 | Workshop 运行态链路 · Apollo 延后 | Inbox/Buddy/列表/主链 | ✅ [91](91-W14-Workshop运行态链路与Apollo延后方案.md) |

| W15 | 概览控制面 bp-ui · 去业务主链 | OverviewPage · 删 StoryChainPanel | ✅ [92](92-W15-概览控制面bp-ui与死代码清理方案.md) |

| W16 | Data 子页 bp-ui · Graph→Buddy · DoD 清单 | media-sets/lineage/dataset · graph buddy | ✅ [93](93-W16-Data子页与Graph-Buddy与可演示DoD方案.md) |

| W17 | Agnes 默认 · LLM 回归 | llm_gateway · providers/router · run-agnes-smoke | ✅ [94](94-W17-Agnes默认接入与LLM回归方案.md) |

| W18 | Buddy 运行态 API · 彩排聚合 | BuddyPage · run-rehearsal-smoke | ✅ [95](95-W18-Buddy运行态API数据与彩排脚本方案.md) |

| W19 | Studio/Logic AIP · CUSTOMER-DEMO | StudioPage · LogicPage · 彩排话术 | ✅ [96](96-W19-Studio-Logic-AIP薄页与彩排话术对齐方案.md) |

| W20 | 概览四域 Live 指标 | overviewMetrics · OverviewDomainGrid | ✅ [97](97-W20-概览四域Live指标与控制面加深方案.md) |

| W21 | demo README · 72 手册 · Agnes 稳态 | README · 72 v1.3 · run-agnes-smoke | ✅ [98](98-W21-演示脚本README与72手册对齐方案.md) |

| W22 | 模型供应商凭据 UI | ProvidersPage · chat 测连通 | ✅ [99](99-W22-模型供应商凭据区与连通探测UI方案.md) |

| W23 | Data Hub Live · L1 链路态 | DataPage · refresh 扩 API | ✅ [100](100-W23-Data连接Hub-Live指标与L1链路态方案.md) |

| W24 | 27/31/69 台账证据回写 | §3.24 · §9.7 · 可演示 85%～90% | ✅ [101](101-W24-门禁与波次台账W15-W23证据回写方案.md) |

| W25 | 78/84 P1/P2 收口 · 可演示冻结 | TB.8 口径 · 映射表同步 | ✅ [102](102-W25-蓝图审计P1收口与可演示冻结方案.md) |

| W29 | 27/31/69/72 W25～W28 回写 | 四台账证据 | ✅ [106](106-W29-门禁与波次台账W25-W28证据回写方案.md) |
| W30 | Canvas widget 密度 | WidgetPreview · grid | ✅ [107](107-W30-Canvas-widget密度蓝图对齐方案.md) |
| W31 | Schedules Cron 可视化 | 五段 · 预设 active | ✅ [108](108-W31-Schedules-Cron可视化蓝图对齐方案.md) |
| W32 | cosmetic 全收口 · 台账 W29～W31 | 78 §7 · 69 v1.6 | ✅ [109](109-W32-门禁台账W29-W31证据回写与cosmetic收口方案.md) |

---

## 7. 可演示冻结（2026-07-18 · W25 · W32 cosmetic 全收口）

**结论：** P0/P1/P2 UI 台账 **全部收口** · **cosmetic 停车场清零**（W28 hover · W30 Canvas · W31 Cron）；日常仅维护 `run-rehearsal-smoke.sh` + pytest + npm test。

| 停车场（不挡彩排） | 说明 |
| --- | --- |
| Apollo change 工作流 / Full Spoke | 用户要求 Apollo 后置 |
| pipeline-doc-intel | 84 永久后置 |
| pipeline DAG 编辑器 | 产品后置 |
| ~~WorkshopList hover~~ | ✅ [105](105-W28-WorkshopList卡片hover蓝图对齐方案.md) |
| ~~Canvas widget 密度~~ | ✅ [107](107-W30-Canvas-widget密度蓝图对齐方案.md) |
| ~~schedules cron 可视化~~ | ✅ [108](108-W31-Schedules-Cron可视化蓝图对齐方案.md) |
| 产品 1.3 Jupyter/R/SQL | [73](73-产品1.3分析建模下一阶段方案.md) 方案中 |

**下一编码刀（须人审）：** [73](73-产品1.3分析建模下一阶段方案.md) TA.* · 或 Apollo Full 运行时点名。

**日常维护：** `bash scripts/demo/run-freeze-check.sh`（见 [110](110-W33-可演示冻结维护Runbook方案.md)）

---

## 变更日志

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.1 | 2026-07-18 | W25 · TB.8/StoryChain 口径修正 · §7 冻结 · P1/P2 收口 |
| v1.0 | 2026-07-18 | 差距台账 + 去演示 Hub + 能力回迁 |

---

*v1.1*
