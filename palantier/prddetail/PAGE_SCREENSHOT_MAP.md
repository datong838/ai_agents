# AOS HTML 页面 ↔ Palantir 截图映射表

> 用于驱动后续按截图重做页面的工作。每行：页面 → 主参考截图（本地路径） → 当前差距

截图根目录：`/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/images/foundry/`

---

## ✅ 已完成（按截图 1:1 复刻）

| HTML 页面 | 主参考截图 | 状态 |
|-----------|-----------|------|
| `aip-draft-inbox.html` | `ontologies/reviews.png` | ✅ 三栏审批台（左任务列表 / 中详情 / 右活动历史） |
| `ontology.html` | `ontology-manager/oma-discover-view.png` + `oma-fallback-sections.png` | ✅ OMA Discover 视图（收藏/最近/重要表格/群组） |
| `ontology-object.html` | `ontology-manager/oma-user-interface-object-type-view.png` + `oma-user-interface-overview-annotated.png` | ✅ Object Type View（左侧页面栏 + 右侧 6 section：元数据/属性/操作/链接图/数据/使用） |
| `ontology-property.html` | `ontology-manager/oma-user-interface-property-editor-v2.png` | ✅ 属性编辑器（左映射条 + 中属性表 + 右 General/Display/Interaction 详情 + 底 Backing 数据预览） |
| `ontology-link.html` | `ontology-manager/oma-user-interface-link-type.png` | ✅ Link Type 详情（左 Overview/Security/Datasources/Usage 导航 + 顶 Ontology/Status 卡 + Configuration 三选 Join Method + 可视化连线 + Object type A/B 下拉 + Properties 0 底部） |
| `ontology-action.html` | `ontology-manager/oma-user-interface-action-type.png` | ✅ Action Type 详情（左 9 项导航 + 顶 Description 表 + 右 Status/RID + Action type overview Input/Rules 双栏 + Dependents 2 计数列表 + 依赖卡） |
| `ontology-function.html` | `ontology-manager/oma-user-interface-function-type.png` | ✅ Function Type 详情（顶部只读提示条 + 左 1.1.2 Latent 版本 + Name + Documentation + Class Name 关联 + RID + 暗色 Code Preview + Inputs 1 + Output type） |
| `pipeline.html` | `pipeline-builder/top-toolbar@2x.png` + `samplegraph@2x.png` + `outputs-sidebar@2x.png` | ✅ Pipeline Builder（顶部工具栏+画布+底部预览+右侧输出侧栏） |
| `data-connection.html` | `data-connection/data-connection-app-portal.png` | ✅ Data Connection 应用门户（左侧分类导航+统计条+应用卡片网格） |
| `lineage.html` | `data-lineage/data-lineage-ui-reference.png` | ✅ Data Lineage（左侧搜索/属性面板+中央沿袭图+节点详情条+图例+工具条） |
| `ontology-funnel.html` | `ontologies/proposal-overview.png` | ✅ Proposal Overview（深色顶栏+左侧导航+中央变更列表+右侧步骤面板） |
| `ontology-branches.html` | `pipeline-builder/branches-new@2x.png` + `pb-branch-selector.png` + `branches-multiple-protected.png` | ✅ 分支管理（分支选择器下拉+Global/Pipeline Builder tabs+Active/Fallback/Protection tabs+保护规则面板+分支列表表格） |
| `ontology-graph-health.html` | `object-explorer/home_object_type_graph_link.png` | ✅ 对象关系图（顶部 ontology 名称+List/Graph 切换+左侧 Layout/Remove 工具+右侧图例+中央 SVG 节点连线+基数标签+悬停弹窗） |
| `pipeline-proposals.html` | `pipeline-builder/proposals-tab@2x.png` | ✅ 管道提案列表（Edit/Proposals/History tabs+Viewing all [open] proposals 筛选+提案卡片列表） |
| `builds.html` | `pipeline-builder/health-build-status@2x.png` | ✅ Build Status Check 对话框（标题+副标题+info banner+Rule section+Group section+Notes textarea+Issues checkbox+Cancel/Save actions） |
| `ontology-wiki.html` | `ontology/object-apps-slate-editor-view.png` | ✅ Slate 编辑器视图（topbar + toolbar tabs + 左 widget 树 + 中央画布 + 右属性面板 + 深色 Object Set 弹窗覆盖层） |
| `workshop-canvas.html` | `ontology/object-apps-slate-editor-view.png` | ✅ Slate 编辑器视图（简化版，无 Object Set 弹窗，侧栏激活态为画布编辑） |
| `workshop-object-view.html` | `object-explorer/admin_airline_exploration.png` | ✅ 对象探索结果表格（tab 栏 + 搜索条 + 视图工具栏 + 5 行航司数据带 avatar） |
| `pipeline-list.html` | `pipeline-builder/file-tree-side-bar.png` | ✅ Pipeline Builder 界面（顶部工具栏 + 左 Legend 图例 + 中央 SVG 节点图 + 右文件树 13 节点） |
| `pipeline-doc-intel.html` | `pipeline-builder/llm-doc-classification.png` + `llm-doc-entity-extract-prompt.png` | ✅ LLM 文档智能分类配置（左迷你画布 + 右配置面板：模板选择网格 + Multiplicity/Context/Categories/Column 字段 + 可选配置 Output type/Include errors/Skip recomputing + 高级模型配置 Model/Temperature/MaxTokens + 实体提取参考 + 输出预览表） |
| `schedules.html` | `data-lineage/manage-schedules.png` + `manage-schedule-details.png` | ✅ 管理计划（左数据沿袭图 + 右计划详情面板：最新运行+运行历史条+最后更新+目标数据集列表+搭建时机 Cron/触发器+搭建范围+操作按钮） |
| `source-new.html` | `data-connection/data-connection-new-source-page.png` | ✅ 新建数据源向导（4 步指示器 + 类型选择已完成提示 + 连接方式 Through agent/Direct + 代理选择列表 + 命名&项目表单 + 连接配置 Host/Port/DB/User/Pwd/JDBC + 测试连接） |
| `source-detail.html` | `data-connection/db-explorer.png` | ✅ 数据库浏览器三栏（左 schema 树+搜索+表列详情+FK标记 / 中央 SVG 关系图+表节点+FK连线+数据预览表 / 右已选表列表+创建同步按钮） |
| `data-connection-agents.html` | `data-connection/agent-metrics.png` + `agent-requirements.png` | ✅ 边缘代理详情（左代理列表 + 右 5 tab：指标仪表板 12 卡片+sparkline / 状态硬件要求表+网络架构图 / 数据源表 / 健康监控规则 / YAML 配置） |
| `sync.html` | `data-connection/data-connection-batch-sync-s3.png` + `incremental-jdbc-sync.png` | ✅ 批量同步配置（4 tab：配置 SQL+增量同步+预览表+S3 参考 / 计划 Cron / 运行历史 / 高级选项） |
| `sync-routing.html` | `data-connection/data-connection-source-capabilities.png` | ✅ 源能力页面（6 功能卡片：批量同步/流式同步/虚拟表/媒体集/导出/Webhooks + 已创建同步表） |
| `workshop.html` | `ontology/object-apps-workshop-module.png` | ✅ Workshop 模块编辑器（暗色主题 #1A1A2E，三栏：左 240px 变量面板 / 中央画布 4 统计卡+表格+趋势图+详情 / 右 280px 属性面板） |
| `workshop-module.html` | `ontology/object-apps-workshop-editor-view.png` | ✅ 风险告警管理运行时（三栏：左筛选列表 / 中风控告警表格 3 行 / 右订单详情+活动日志） |
| `health.html` | `data-lineage/data-lineage-icon-issues-reported.png` + `view-histogram.png` | ✅ 数据健康（4 tab：全部检查 15 行检查表+直方图+问题面板 / 检查组 4 卡片+状态条 / 监测中 / 问题列表） |

---

## 🔥 高优先级（有明确截图，功能核心）

### Pipeline Builder / 管道构建
（pipeline.html / pipeline-list.html / pipeline-doc-intel.html / builds.html / pipeline-proposals.html 已完成）

### Data Connection / 数据连接
（data-connection.html / source-new.html / source-detail.html / data-connection-agents.html / sync.html / sync-routing.html 已完成）

### Workshop / 工作台
（workshop.html / workshop-module.html / workshop-canvas.html / workshop-object-view.html 已完成）

### Data Lineage / 数据沿袭
（lineage.html / schedules.html / health.html 已完成）

**🔥 高优先级全部完成！**

---

## 🟡 中优先级（有截图，可复刻）

| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `dataset.html` | `data-lineage/dataset-preview.png` | ✅ 数据集预览（5 tab：预览 8 行数据表+列类型+右侧信息面板 / 历史 5 行构建表 / 详情 模式+文件+同步 / 健康 4 卡片 / 比较） |
| `code-repositories.html` | `code-repositories/code-view.png` + `branch-view.png` | ✅ 代码库 IDE（三栏：仓库列表 5 项 / 文件树 6 文件+代码编辑器 PySpark / 元数据面板 仓库信息+关联资源+提交） |
| `media-sets.html` | `media-sets-advanced-formats/`(目录) | ✅ 媒体集（4 tab：浏览 PDF 文件列表+预览+OCR / 同步 SharePoint 配置+历史 / 变换 4 卡片 / 设置 保留策略+存储策略） |
| `agents.html` | `functions/`(目录) | ✅ Chatbot Studio（4 tab：Prompt 系统提示 / Tools 已绑定工具 / Try 对话预览 / Publish L4 门控） |
| `aip-logic.html` | `logic/logic-app-overview.png` | ✅ AIP 逻辑画布（3 tab：编辑 三栏 块链+LLM 配置+运行预览 / 自动化 Uses / 运行历史） |
| `aip-tools.html` | `functions/`(目录) | ✅ Agent 工具面板（三栏：工具目录 8 类 / 已启用 5 工具 / 工具详情 6 种 detail 视图） |
| `aip-evals.html` | `pipeline-builder/unit-test-pass-fail.png` | ✅ Evals 门控（统计卡 通过率 87% + 分项结果表 + L4 门控横幅） |
| `aip-decision-lineage.html` | `data-lineage/data-lineage-ui-reference.png` | ✅ 决策谱系（单 Trace 卡片 6 节点时间线 含熔断降级场景） |
| `aip-maturity.html` | —（自定义） | ✅ 成熟度楼梯（L1-L4 四列卡片 + 升级按钮 + L4 熔断护栏） |
| `aip-model-providers.html` | `pipeline-builder/llm-doc-model-configs.png` | ✅ 模型供应商（已接入 3 卡 + 可接入 5 类型 + 类型化配置面板 5 表单切换） |
| `aip-model-router.html` | —（自定义） | ✅ 模型路由（6 行路由规则表 + 模型预热状态面板） |
| `aip-capabilities.html` | —（自定义） | ✅ 重能力接入（已接入 4 卡 + 可接入 4 类型 + 类型化配置面板 4 表单切换） |

**🟡 中优先级全部完成！**

---

## 🟢 低优先级（Apollo / 入口 / 自定义）

| HTML 页面 | 主参考截图 | 备注 |
|-----------|-----------|------|
| `index.html` | `data-connection/data-connection-app-portal.png` | ✅ AOS 概览入口（4 大区域面板：工作台唯一入口+模块示例 / AIP 4 卡片+6 快捷链接 / 本体 4 卡片 / 数据集成 4 卡片 / 交付 Apollo 4 卡片） |
| `funnel.html` | —（自定义业务） | ✅ OKF 行业漏斗（左侧行业选择 3 按钮+源 Schema 6 列映射状态 / 右侧映射表 6 行含置信度+映射方式 badge / 四阶段进度条 Schema→映射→清洗→发布） |
| `okf-funnel.html` | —（AOS 自有概念） | ✅ OKF 行业漏斗概览（4 统计卡片：7 行业模板/23 已映射/83% 覆盖率/12 待确认 · 6 行业模板卡片含跨境电商/环科院/湃肽/微商城/淘宝/拼多多 · 最近映射活动表 4 行 · OKF 优势说明区 · 链接进入 funnel.html 映射工作台） |
| `apollo-hub.html` | —（AOS 自有概念） | ✅ Hub 舰队总览（状态条 Hub 区域+在线 5/6+最近 Probe / 5 Spoke 卡片含健康/降级/离线状态+Probe 延迟+通道版本+Full/Lite 标记 / 注册新 Spoke） |
| `apollo-release.html` | —（AOS 自有概念） | ✅ Release 通道管道（rc→beta→stable 三段流水线+版本号+Spoke 数 / hotfix 旁路通道+CVE 修复 / Recall 回滚区） |
| `apollo-spoke.html` | —（AOS 自有概念） | ✅ Spoke 详情（出站轮询 callout / Full vs Lite 形态切换+能力对比 / 部署计划 3 项 Bundle+Config Override / Plan Diff 预览） |
| `apollo-ferry.html` | —（AOS 自有概念） | ✅ Ferry 摆渡向导（4 步指示器 / Bundle 选择 2 选项+SemVer / 气隙传输说明） |
| `apollo-assets.html` | —（AOS 自有概念） | ✅ FDE 资产包（4 行资产表：apollo-core/fde-维修派单/fde-库存预警/config-overrides + SemVer+通道 badge+状态） |
| `apollo-change-mgmt.html` | —（AOS 自有概念） | ✅ 变更审批（左侧 3 变更单列表 / 右侧 CHG-2026-0412 详情：变更类型+目标 Spoke+Bundle+窗口 / 3 步审批流 / 批准+驳回按钮） |
| `apollo-config.html` | —（AOS 自有概念） | ✅ 配置与密钥（维护窗口开始/结束 / 3 项覆盖：模型默认+连接池+API密钥 Vault引用 / 禁止明文密钥提示） |
| `workshop-aip-chat.html` | —（自定义） | ✅ Buddy 智能助手（左：订单表 3 行+Assist 弹窗 / 右：Buddy 侧栏 上下文 chip+对话区+输入框） |
| `workshop-cop.html` | —（自定义） | ✅ 态势大屏（4 KPI 卡片 / 供应链 SVG 网络 3 工厂→CDC→FD→3 仓+履约率 / 钻取面板 3 工厂卡片 / 风险工厂 3 条 / 实时事件 5 条） |
| `workshop-events.html` | —（自定义） | ✅ 事件配置（3 行已注册事件表：触发器+动作+目标变量+幂等 / 幂等护栏提示） |
| `workshop-module-interface.html` | —（自定义） | ✅ 模块接口（左：接口定义 3 字段 input/output / 右：嵌套 Loop 可视化 父→子 Module / Interface 契约说明） |
| `workshop-publish.html` | —（自定义） | ✅ 发布入口（目标通道 4 选 rc/beta/stable/hotfix / 4 快捷链接 Release+资产包+Hub+画布 / 出站轮询说明） |
| `integration-cases.html` | —（AOS 自有概念） | ✅ 接入案例（6 格统计条 9 平台/9 连接器/47 同步/38 本体/9 OKF/12 应用 · 6 节点端到端链路 · 9 平台案例卡片含 mini 流程+指标 · G1-G10 阻塞项网格） |

**🟢 低优先级全部完成！**

---

## 工作方法

1. **每次重做一个页面前**：先 Read 对应截图，把布局、组件、配色、字号、间距精确提取
2. **保持 Palantir 全局壳**：`p-app` + `p-nav-global` + `p-sidebar` + `p-header` + `p-content`
3. **页面内容按截图重做**：用 `p-card` / `p-table` / `p-badge` / `p-btn` / `p-tabs` 等已有组件类
4. **特殊布局**：如三栏审批台、画布、对象图等，追加专用 CSS 块到 `demo.css` 末尾
5. **每个页面重做完**：本地服务器预览验证，再标记完成
