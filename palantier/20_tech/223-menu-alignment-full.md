# 全量菜单区对照表：视觉稿 vs 系统

> 文档版本：v1.0（2026-07-26）
> 范围：全站侧栏 9 个分区 + 顶部独立"概览"项
> 基准：以视觉稿侧栏（`docs/palantier/foundry/html/workshop.html` 第 46-133 行）为对齐基准
> 用户原则：**视觉稿有的 → 必须对齐；系统多出的 → 保留不动**

---

## 0. 一图速览

| 分区 | 视觉稿 | 系统 | 差距类型 |
|---|---|---|---|
| 概览 | 1 | 1 | ✅ 一致 |
| 工作台 | 5 | 8 | 🟡 系统多 3 |
| 应用程序构建工具 | 7 | 4 | 🔴 系统少 3（视觉稿缺） |
| AIP 决策引擎 | 13 | 14 | 🟡 系统多 3 + 名字差异 |
| 模型管理 | 4 | 4 | 🟡 名字差异 + 2 项路由未注册 |
| 本体·数字孪生 | 8 | 9 | 🟡 系统多 1 + 名字差异 |
| 管道与数据治理 | 8 | 8 | ✅ 一致 |
| 数据源与同步 | 6 | 6 | ✅ 一致 |
| 运维交付 | 8 | 11 | 🟡 系统多 3 |
| **合计** | **60** | **65** | — |

**全局结论**：
- ✅ **3 个分区完全对齐**（概览、管道与数据治理、数据源与同步）
- 🔴 **1 个分区有缺项**（应用程序构建工具缺 3 项 → 必须补）
- 🟡 **5 个分区系统有冗余**（按用户原则保留不动）
- ⚠️ **名字差异 8 处** + **5 项路由未注册**（标 live 但点击跳首页）

---

## 1. 概览（独立顶部）

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 概览 `index.html` | 概览 `/` | ✅ 对齐 |

---

## 2. 工作台

| # | 视觉稿 | 系统 | 状态 | 备注 |
|---|---|---|---|---|
| 1 | 应用列表 `workshop.html` | 应用列表 `/workshop` | ✅ 名字一致 | 内容差距见 ui-alignment-plan.md |
| 2 | — | 创建应用 `/workshop/create` | 🟡 系统多出 | 视觉稿作为弹窗，不进侧栏；保留不动 |
| 3 | — | 模块管理 `/workshop/module` | 🟡 系统多出 | 注意：易与"风险告警管理"混淆，建议改名 |
| 4 | 订单管理 `workshop-app-order.html` | 订单管理 `/workshop/orders` | ✅ 名字一致 | 视觉稿=暗色画布编辑器，系统=浅色运行态（定位错配，待产品决策） |
| 5 | 风险告警管理 `workshop-module.html` | 风险告警管理 `/workshop/inbox` | ✅ 名字一致 | 视觉稿文件名 `workshop-module.html` 易误解 |
| 6 | 态势大屏 `workshop-cop.html` | 态势大屏 `/workshop/cop` | ✅ 名字一致 | 内容差距：KPI 业务化、工厂/事件接入真实事件 |
| 7 | Buddy · 智能助手 `workshop-aip-chat.html` | Buddy 智能助手 `/workshop/buddy` | ✅ 名字基本一致 | 内容差距小：表用 WorkOrder 非 Order，缺风控分列 |
| 8 | — | 分析建模 `/analytics` | 🟡 系统多出 | 保留不动 |

**结论**：5 项视觉稿全部存在；系统多 3 项保留。

---

## 3. 应用程序构建工具 🔴 重点改造区

| # | 视觉稿 | 系统 | 状态 | 备注 |
|---|---|---|---|---|
| 1 | 画布编辑 `workshop-canvas.html` | 画布编辑 `/workshop/canvas` | ✅ 名字一致 | 视觉稿 145KB（最复杂）；现状基础版 |
| 2 | **组件注册表** `workshop-widget-registry.html` | — | 🔴 **缺失** | 需补：路由 + 占位页 + nav 项 |
| 3 | **变量管理器** `workshop-variables.html` | — | 🔴 **缺失** | 需补：路由 + 占位页 + nav 项 |
| 4 | **主题与样式** `workshop-styles.html` | — | 🔴 **缺失** | 需补：路由 + 占位页 + nav 项 |
| 5 | 模块接口 `workshop-module-interface.html` | 模块接口 `/workshop/module-interface` | ✅ 名字一致 | |
| 6 | 事件配置 `workshop-events.html` | 事件配置 `/workshop/events` | ✅ 名字一致 | |
| 7 | 发布入口 `workshop-publish.html` | 发布入口 `/workshop/publish` | ✅ 名字一致 | |

**结论**：视觉稿 7 项，系统仅 4 项，**缺 3 项必须补齐**（组件注册表、变量管理器、主题与样式）。

---

## 4. AIP 决策引擎

### 4.1 应用层
| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | AIP 助手 `aip-assist.html` | AIP Assist `/aip/assist` | ⚠️ 名字差异 + **路由未注册**（点击跳首页） |
| 2 | 对话机器人 `agents.html` | Chatbot Studio `/aip/studio` | ⚠️ 名字差异 |
| 3 | AIP 分析师 `aip-analyst.html` | AIP Analyst `/aip/analyst` | ⚠️ 名字差异 + **路由未注册** |

### 4.2 逻辑编排层
| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | AIP 逻辑画布 `aip-logic.html` | AIP 逻辑画布 `/aip/logic` | ✅ 名字一致 |
| 2 | Agent 工具面板 `aip-tools.html` | Agent 工具面板 `/aip/tools` | ✅ 名字一致 |
| 3 | 成熟度楼梯 `aip-maturity.html` | 成熟度楼梯 `/aip/maturity` | ✅ 名字一致 |

### 4.3 智能体
| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 智能体目录 `agent-registry.html` | 智能体注册表 `/aip/agent-registry` | ⚠️ 名字差异（目录 vs 注册表） |
| 2 | 智能体插件 `aip-capabilities.html` | 智能体插件 `/aip/capabilities` | ✅ 名字一致 |
| 3 | — | 智能体列表 `/aip/agents` | 🟡 系统多出 |
| 4 | — | 智能体导入 `/aip/agent-import` | 🟡 系统多出 |
| 5 | — | 能力导入 `/aip/capability-import` | 🟡 系统多出 |

### 4.4 评测与治理
| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | Evals 门控 `aip-evals.html` | Evals 门控 `/aip/evals` | ✅ 名字一致 |
| 2 | Draft 审批台 `aip-draft-inbox.html` | Draft 审批台 `/aip/drafts` | ✅ 名字一致 |

### 4.5 决策谱系
| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 决策谱系 `aip-decision-lineage.html` | 决策谱系 `/aip/lineage` | ✅ 名字一致 |
| 2 | 可观测性 `aip-observability.html` | 可观测性 `/aip/observability` | ✅ 名字一致 |

**结论**：5 子组结构对齐；智能体 subgroup 系统多 3 项保留；3 处名字差异；2 项路由未注册。

---

## 5. 模型管理

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 模型目录 `aip-model-catalog.html` | 模型目录 `/aip/model-catalog` | ⚠️ **路由未注册**（点击跳首页） |
| 2 | 模型供应商 `aip-model-providers.html` | 模型供应商 `/aip/model-providers` | ✅ 一致 |
| 3 | 模型路由 `aip-model-router.html` | 模型路由 `/aip/model-router` | ✅ 一致 |
| 4 | 容量管理 `aip-capacity-management.html` | 容量管理 `/aip/capacity` | ⚠️ **路由未注册** |

**结论**：4 项名字全对齐；2 项路由未注册需补组件。

---

## 6. 本体·数字孪生

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 本体管理 `ontology.html` | 本体管理 `/ontology` | ✅ 一致 |
| 2 | 对象探索 `workshop-object-view.html` | 对象探索 `/workshop/graph` | ✅ 一致 |
| 3 | 本体提案 `ontology-funnel.html` | 漏斗管道 `/ontology/funnel` | ⚠️ 名字差异（本体提案 vs 漏斗管道）—— **可能是同一页** |
| 4 | 图谱健康度 `ontology-graph-health.html` | 图谱健康度 `/ontology/graph-health` | ✅ 一致 |
| 5 | 活知识 Wiki `ontology-wiki-index.html` | 活知识 Wiki `/ontology/wiki` | ⚠️ 视觉稿"活知识 Wiki"= 索引页；系统拆成"活知识 Wiki + Wiki 索引"2 项 |
| 6 | — | Wiki 索引 `/ontology/wiki-index` | 🟡 系统多出（视觉稿合并到上一项） |
| 7 | OKF funnel `funnel.html` | OKF 行业漏斗 `/ontology/okf-funnel` | ⚠️ 名字差异（OKF funnel vs OKF 行业漏斗） |
| 8 | OKF 概览 `okf-funnel.html` | OKF 概览 `/ontology/okf-overview` | ✅ 一致 |
| 9 | 分支管理 `ontology-branches.html` | 分支管理 `/ontology/branches` | ✅ 一致 |

**结论**：8 项视觉稿全有；名字差异 2 处；视觉稿"本体提案"和系统"漏斗管道"路径相同，疑为同一页（待确认）。

---

## 7. 管道与数据治理 ✅ 完全对齐

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 管道构建 `pipeline-list.html` | 管道构建 `/data/pipelines` | ✅ |
| 2 | 管道提案 `pipeline-proposals.html` | 管道提案 `/data/pipeline-proposals` | ✅ |
| 3 | 计划编辑器 `schedules.html` | 计划编辑器 `/data/schedules` | ✅ |
| 4 | 搭建 `builds.html` | 搭建 `/data/builds` | ✅ |
| 5 | 数据集预览 `dataset.html` | 数据集预览 `/data/datasets` | ✅ |
| 6 | 代码库 `code-repositories.html` | 代码库 `/data/code-repos` | ✅ |
| 7 | 数据沿袭 `lineage.html` | 数据沿袭 `/data/lineage` | ✅ |
| 8 | 数据健康 `health.html` | 数据健康 `/data/health` | ✅ |

---

## 8. 数据源与同步 ✅ 完全对齐

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | 数据链接器 `data-connection.html` | 数据链接器 `/data` | ✅ |
| 2 | 边缘代理 `data-connection-agents.html` | 边缘代理 `/data/agents` | ✅ |
| 3 | 同步配置 `sync.html` | 同步配置 `/data/sync-config` | ✅ |
| 4 | 同步路由 `sync-routing.html` | 同步路由 `/data/sync-routes` | ✅ |
| 5 | 媒体集 `media-sets.html` | 媒体集 `/data/media-sets` | ✅ |
| 6 | 文档智能 `document-intelligence.html` | 文档智能 `/aip/doc-intelligence` | ⚠️ **路由未注册** |

**结论**：6 项全有；文档智能路由未注册需补组件。

---

## 9. 运维交付

| # | 视觉稿 | 系统 | 状态 |
|---|---|---|---|
| 1 | — | 本机探活 `/settings/local-platform` | 🟡 系统多出（开发辅助） |
| 2 | — | 启停说明 `/settings/ops-start-guide` | 🟡 系统多出（开发辅助） |
| 3 | Hub 舰队 `apollo-hub.html` | Hub 舰队 `/apollo` | ✅ |
| 4 | Release 通道 `apollo-release.html` | Release 通道 `/apollo/release` | ✅ |
| 5 | Spoke 详情 `apollo-spoke.html` | Spoke 详情 `/apollo/spoke` | ✅ |
| 6 | Ferry 摆渡 `apollo-ferry.html` | Ferry 摆渡 `/apollo/ferry` | ✅ |
| 7 | FDE 资产包 `apollo-assets.html` | FDE 资产包 `/apollo/assets` | ✅ |
| 8 | 变更审批 `apollo-change-mgmt.html` | 变更审批 `/apollo/change` | ✅ |
| 9 | 配置与密钥 `apollo-config.html` | 配置与密钥 `/apollo/config` | ✅ |
| 10 | 接入案例 `integration-cases.html` | 接入案例 `/apollo/cases` | ✅ |
| 11 | — | SaaS 开通 `/apollo/provisioning` | 🟡 系统多出 |

**结论**：视觉稿 8 项全有；系统多 3 项保留。

---

## 10. 全局问题汇总

### 10.1 路由未注册（标 live 但点击跳首页） — 共 5 项

| 菜单 | 路径 | 所属分区 | 处理建议 |
|---|---|---|---|
| AIP Assist | `/aip/assist` | AIP 决策引擎·应用层 | 补真实页面 或 改 status="s2" 走占位 |
| AIP Analyst | `/aip/analyst` | AIP 决策引擎·应用层 | 同上 |
| 模型目录 | `/aip/model-catalog` | 模型管理 | 同上 |
| 容量管理 | `/aip/capacity` | 模型管理 | 同上 |
| 文档智能 | `/aip/doc-intelligence` | 数据源与同步 | 同上 |

### 10.2 名字差异（建议统一以视觉稿为准） — 共 8 处

| 视觉稿名字 | 系统名字 | 建议 |
|---|---|---|
| AIP 助手 | AIP Assist | 改为"AIP 助手" |
| 对话机器人 | Chatbot Studio | 改为"对话机器人" |
| AIP 分析师 | AIP Analyst | 改为"AIP 分析师" |
| 智能体目录 | 智能体注册表 | 改为"智能体目录" |
| 本体提案 | 漏斗管道 | 待确认是否同一页 |
| OKF funnel | OKF 行业漏斗 | 改为"OKF funnel" |
| Buddy · 智能助手 | Buddy 智能助手 | 微调（中点号） |

### 10.3 视觉稿有、系统缺 — 共 3 项（必须补）

| 菜单 | 视觉稿文件 | 所属分区 | 处理建议 |
|---|---|---|---|
| 组件注册表 | `workshop-widget-registry.html` | 应用程序构建工具 | 新增 nav 项 + 路由 + 占位页 |
| 变量管理器 | `workshop-variables.html` | 应用程序构建工具 | 同上 |
| 主题与样式 | `workshop-styles.html` | 应用程序构建工具 | 同上 |

### 10.4 系统多出、保留不动 — 共 12 项

| 菜单 | 所属分区 | 备注 |
|---|---|---|
| 创建应用 | 工作台 | 视觉稿作弹窗，不进侧栏 |
| 模块管理 | 工作台 | 易与"风险告警管理"混淆 |
| 分析建模 | 工作台 | 系统增强 |
| 智能体列表 | AIP 决策引擎·智能体 | 系统增强 |
| 智能体导入 | AIP 决策引擎·智能体 | 系统增强 |
| 能力导入 | AIP 决策引擎·智能体 | 系统增强 |
| Wiki 索引 | 本体·数字孪生 | 视觉稿合并到"活知识 Wiki" |
| 本机探活 | 运维交付 | 开发辅助 |
| 启停说明 | 运维交付 | 开发辅助 |
| SaaS 开通 | 运维交付 | 系统增强 |

---

## 11. 改造优先级建议（已根据用户决策更新）

| 优先级 | 任务 | 工作量 | 影响 | 用户决策 |
|---|---|---|---|---|
| **P0** | 修复 5 项路由未注册（做真实页面） | 中 | 用户体验立即改善 | ✅ 直接做真实页面 |
| **P0** | 补齐 3 项缺失菜单（组件注册表/变量管理器/主题与样式） | 中 | 侧栏与视觉稿一致 | ✅ 直接做真实页面 |
| **P1** | 名字统一（8 处） | 极低 | 视觉一致 | ✅ 全部按视觉稿改 |
| **P1** | 工作台·应用列表内容对齐（见 223-ui-alignment-plan.md Phase A） | 中 | 高频入口 | ✅ 进行中 |
| **P2** | 各分区内容深度对齐（按 223-ui-alignment-plan.md Phase B/C） | 大 | 全站视觉统一 | ✅ 后续专门写计划 |

---

## 12. 用户已确认事项（决策记录）

| 问题 | 用户决策 |
|---|---|
| "本体提案" vs "漏斗管道" | **同义页**，按视觉稿改名"本体提案" |
| "活知识 Wiki" 拆分 | **按视觉稿合并为 1 项**（指向 `ontology-wiki-index.html`） |
| 5 项路由未注册的菜单 | **直接做真实页面**，严格按照视觉稿（不用占位页） |
| 名字统一（8 处） | **全部按视觉稿改** |
| 改造节奏 | **后续专门写计划**（Phase A→B→C→D→E→F 顺序） |
| OKF funnel | 按视觉稿改名"OKF funnel"（去掉"行业"） |
| Module 核心原则 | Module 是在线定制出来的，不是写代码写出来的；新建 Module 能力必须很强 |

---

## 13. 附录：相关文件位置

### 13.1 视觉稿（基准）
- 侧栏结构：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/workshop.html` 第 46-133 行
- 全局样式：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html/assets/demo.css`

### 13.2 系统侧栏（待改）
- 导航定义：`/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/nav.ts`
- 主路由：`/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/App.tsx`
- S2 路由：`/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/pages/s2/routes.tsx`
- 全局外壳：`/Users/ddt/work/projects/ai_agent/aos-platform/apps/web/src/shell/AppShell.tsx`

### 13.3 配套文档
- 工作台深度差距：`/Users/ddt/work/projects/ai_agent/docs/palantier/20_tech/223-ui-alignment-plan.md`
- 全量页面差距盘点：`/Users/ddt/work/projects/ai_agent/docs/palantier/20_tech/223-full-ui-gap-analysis.md`
