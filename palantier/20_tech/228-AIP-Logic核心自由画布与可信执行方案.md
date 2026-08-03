# 228 · AIP Logic 核心自由画布与可信执行方案

> 版本：v1.4（2026-08-02，端口拖线与方向箭头收口）
> 状态：**Stage A 自由画布、端口拖线/有向箭头与 Stage B 可信 dry-run/历史均已完成阶段门；Stage C 发布/生产自动化继续禁用并须另立方案**
> 目标页面：`/aip/logic`、新增兼容入口 `/aip/logic/:flowId`
> 对照页面：`/data/pipelines/:pipelineId`
> Stage A 基线：m1 `9d2f145`；Stage B 最终：m1 `1fb0fa2`；画布交互收口：m1 `186ddd9`

## 1. 使用 Rules

1. 先复核产品方案、技术方案、真实浏览器、前后端契约与管道画布实现，再冻结编码范围。
2. AIP Logic 是核心能力，必须以“用户可完成完整任务”验收，不以卡片样式、按钮存在或纯函数数量代替。
3. 最小改动不等于保留错误架构：复用管道画布已经验证的 `@dnd-kit/core` 交互模型，但 Logic 的数据、执行和治理契约保持独立。
4. 保存必须经服务端提交、回包一致性校验和 GET 重读；刷新与 API 重启后可恢复。禁止 localStorage 冒充生产持久化。
5. 试跑必须 fail-closed，明确 `dry_run=true`、`production_written=false`、执行版本和图 hash；未实现生产写时不得显示“生产执行”可用。
6. Ontology 写操作仍走 Action / Automate / Draft 审批；Logic 调试器只展示提议 edits，不直接写对象。
7. 四 Worker 文件互斥；共享路由、OpenAPI、manifest 与最终合并由 Planner 单点维护。
8. 每阶段必须专项、累计和浏览器回归全绿，之后才能进入下一阶段。

## 2. 产品与技术依据

1. `07-AIP引擎k-LLM与AgentStudio产品方案.md` §2.2、§3、§3.5、§9.1：Logic 是无代码 LLM Function 构建、测试、发布环境；块链输出为值或 Ontology edits；试跑不落库。
2. `222plan-分阶段开发与里程碑计划.md` Phase D：Block 绑定、动态属性、调试、保存、自动化、历史和拖拽均是验收项。旧文档虽写“Phase D 完成”，但其 §6.3 checklist 仍未勾选，且当前实机不满足，不能继续引用为完成证据。
3. 管道画布已验证：节点从组件栏拖入、节点自由移动、连接、属性折叠、保存、刷新恢复及 API 重启重放，可作为交互基线；AIP Logic 与 Pipeline Builder 业务语义仍分离。

## 3. 当前实测与 P0 风险

### 3.1 浏览器实测

1. 当前中栏是纵向列表，不是自由画布；Block 只能用上下箭头排序。
2. 左侧 Block 点击或 HTML5 drop 只会追加到列表末尾；既有 Block 不能拖动到任意坐标，也没有真实连接端点或可编辑边。
3. 浏览器添加第 5 个 Block 后刷新，立即恢复硬编码的 4 个 Block，证明没有保存/加载链路。
4. 右栏属性只改 React 会话状态；“历史”只记录当前页面会话；自动化 toggle 也是本地状态。
5. `/aip/logic` 未进入现有 interaction-honesty manifest，核心页面没有同等级防回归门。

### 3.2 契约与执行真实性

1. 前端向 `POST /v1/aip/logic/execute` 发送 `dry_run`，但后端 `LogicExecuteRequest` 不声明该字段，Pydantic 会忽略它；页面的“不落库”承诺没有契约证据。
2. 前端种类为 `use_llm/get_property/apply_action/...`，后端 mock 仅特殊识别 `llm/tool/branch/handoff`；多数 Block 实际落入通用 task 分支。
3. 后端默认 `_execute_mock`，却没有把 `mode=mock`、`production_written=false` 显式返回；前端仍可切到“生产执行”，属于假能力。
4. 仓库同时存在 `/v1/aip/logic/execute`、`/v1/aip/logic/run`、`/v1/logic-flows`、`/api/aip/logic-state` 和 `/api/aip/logic-version` 多套 Logic 契约，当前页面没有 canonical 真源。
5. 当前 `aip_logic_engine`、`logic_flows`、logic-state/version 均为进程内存储，不能满足 API 重启重放。

结论：该页是 **P0 核心任务与交互真实性缺口**，必须按多阶段核心工程治理。

## 4. 目标用户任务

1. 打开一个 Logic Flow，GET 加载服务端已确认的名称、版本、节点、连接和状态。
2. 从左侧拖入 Block 到鼠标落点，也可点击添加到可见空位。
3. 自由拖动节点；选中节点后编辑类型专属配置；移动和编辑均产生 dirty 状态。
4. 从源节点进入连接模式并点击目标节点完成连接；可删除边；重复边、自环和环路前置拒绝。
5. 保存时带 `expected_version`；后端原子校验、版本递增、完整回包；前端校验回包并 GET 重读。
6. 刷新浏览器或重启 API 后，图、坐标、配置、连接和版本一致恢复。
7. 只有已保存且无环的版本可以 dry-run；结果逐节点对应，明确模式、图 hash、版本、耗时、token 和 `production_written=false`。
8. 历史读取服务端运行记录；错误和未注册能力明确 fail-closed。
9. 发布、生产 Automate、Draft 写回和 Evals 门控只有在真实契约闭环后才启用；本波不能完成的控件前置禁用并说明原因。

## 5. Canonical 图与 API 契约

### 5.1 图模型

```text
LogicGraph
  id, name, description, status(draft|published|archived)
  schema_version, revision, published_version, graph_hash
  created_at, updated_at, persisted
  nodes[]: id, kind, label, position_x, position_y, config
  edges[]: id, source_node_id, source_port,
           target_node_id, target_port, branch_path, order
  entry_node_ids[]
```

约束：org/project 只从 `Principal` 获取，不接受客户端租户字段；ID 非空且 graph 内唯一；坐标为有限非负数；edge 端点和 entry 必须存在；禁止自环、重复边和 DAG 环；Branch 最多一个 default；Handoff 校验激活上游；配置大小、JSON bytes 与节点/边数量设上限；服务端不信任客户端 hash。DTO 使用 `extra=forbid`，未知 kind 或拼错的安全字段一律 422，不再 silent fallback。

### 5.2 单一主路径

- `POST /v1/aip/logic/graphs`、`GET /v1/aip/logic/graphs`：显式创建/列出资源。
- `GET /v1/aip/logic/graphs/{graph_id}`：加载 canonical snapshot；不存在返回 404，不回落成假成功 demo。
- `PUT /v1/aip/logic/graphs/{graph_id}`：完整替换图，必传 `expected_revision`，成功返回已提交 snapshot；陈旧写 409 且不改变服务端。
- `POST /v1/aip/logic/graphs/validate`：校验未保存草稿并返回逐节点/边结构化错误。
- `POST /v1/aip/logic/graphs/{graph_id}/dry-run`：只执行指定已保存 revision；响应带 `mode=dry_run`、`evaluated_revision`、`graph_hash`、`run_id`、`production_written=false`。
- `GET /v1/aip/logic/graphs/{graph_id}/runs`：服务端运行历史。
- `POST /v1/aip/logic/graphs/{graph_id}/publish`、`GET .../revisions`：Stage C 在 Evals/Draft 门闭环后启用。

旧 `/v1/aip/logic/execute` 在调用清零前保留兼容，但标 deprecated 并统一调用 canonical executor；`/v1/aip/logic/run` 只保留 edits dry-run 门卫语义；`/v1/logic/run-graph` 后续委托 canonical executor；`/v1/logic-flows` 属 Data Connection 步骤链，不作为 AIP Logic 页面真源。logic-state/version 不再供此页面混用。

### 5.3 默认入口

现有 `/aip/logic` 解析为开发入口：若无资源，显示“未保存模板”并由用户显式创建，不把 404 伪装成已加载；新增 `/aip/logic/:flowId` 作为资源入口。页面切换 flowId 时必须立即清空旧图并用加载代次隔离，防止 A 图覆盖 B。

## 6. 前端交互设计

1. 复用管道画布的 DnD 设计：`DndContext`、pointer/keyboard sensors、palette droppable、按 zoom 修正 delta 和 drop 坐标。
2. 画布为自由绝对定位 DAG；SVG 边按节点中心/端口坐标绘制；连接同时支持“点击源→点击目标”和“输出端口拖到输入端口”，正式边与预览边均以箭头表达 source→target 方向。
3. 工具栏：保存、刷新、dry-run、缩放、1:1、统计、收起属性、清空；dirty 时保存显示 `*`。
4. 右栏保留属性/历史/自动化三个 Tab，但历史改为服务端，自动化在真实保存/发布门禁前只读或明确禁用。
5. 节点移动、连边、删边、改属性、添加/删除均标 dirty；flowId 切换或刷新前提示未保存更改。
6. 初始 4 节点仅作为服务端 seed；前端不再每次硬编码重建。

## 7. 分阶段与四 Worker 冻结分工

### Stage A：可信图基座与自由画布

| Worker | 独占范围 | 任务 |
|---|---|---|
| W1 | 新增 `logicCanvasGraph.ts`、`LogicGraphCanvas.tsx`、专属 CSS 与测试 | DnD、坐标、节点、端口、SVG 边、缩放、dirty、图归一化；不改现有页面、后端与共享路由 |
| W2 | 新增 canonical models/store/router/迁移及后端测试 | tenant-scoped CRUD、revision CAS、DAG 校验、不可变 revision、持久化与重启恢复；不改 Web |
| W3 | 第二小波独占 `LogicCanvasPage.tsx` 与页面交互测试 | 在 W1/W2 合入并对齐后，串联加载、保存回读、属性、冲突和错误；修复顶层 label；只开放可信能力 |
| Planner（W4） | 共享 route/OpenAPI/manifest、合并、阶段门与浏览器 | Stage A1 并行 W1/W2；合并回归后 Stage A2 W3；最终完成保存→刷新→API 重启恢复 |

后端新增文件建议：`aip_logic_graph_models.py`、`aip_logic_graph_store.py`、`routers/aip_logic_graphs.py`、独立 Alembic migration、`test_aip_logic_graph_store.py`、`test_aip_logic_graph_api.py`。数据库 current 表以 `(org_id, project_id, graph_id)` 为联合键，revision 表保存不可变快照与 checksum；禁止把新表塞入未登记 runtime DDL。

### Stage B：可信 dry-run 与历史

1. W2 扩展 canonical executor 和运行历史持久化，统一 10 种 Block kind；legacy 只允许显式 `task→execute / llm→use_llm / tool→use_tool`，未知 kind fail-fast。
2. W1/W3 补逐节点结果、错误定位、历史下钻和失败态组件测试。
3. Planner 禁用未闭环的生产执行、发布和自动化写入口，完成实机 dry-run。

### Stage C：治理发布（独立退出门）

1. 对接真实 Evals gate、版本发布、Draft/Ontology edits 与 Automate；Automation 绑定不可变 published revision；任何依赖未闭环则保持禁用，不以 mock 替代。
2. 发布版本不可原地修改；草稿从已发布版本派生；Evals 失败不得发布或绑定生产自动化。
3. 本 Stage 如范围过大可拆下一份 `228-` 子方案，但 Stage A/B 完成不允许宣称“生产发布已完成”。

## 8. 测试与浏览器验收

### 8.1 每阶段自动门

1. 前端纯函数：坐标缩放、drop 定位、节点/边 normalize、DAG 校验、回包一致性、flowId 竞态。
2. DOM：拖入、节点移动、连接/删边、属性编辑、dirty/save、冲突、GET 失败、PUT 已提交后重读失败。
3. 后端：空图、完整 round-trip、重复/未知端点/entry、自环/环路、Branch default/Handoff、expected_revision 冲突、跨 tenant/graph 隔离、重启恢复、并发 PUT 仅一胜一 409、读者只见完整旧/新快照。
4. dry-run：正确拓扑和分支跳过、Handoff 等待激活上游、所有 10 kind 映射、失败停止、未保存/版本错配拒绝、缺失/拼错 dryRun fail-closed、`production_written=false`。
5. 每 Worker 专项→阶段累计→Web/后端相关→typecheck/build→`git diff --check`；最终跑完整 CI。

### 8.2 浏览器主任务

1. 从左侧拖入 Branch 到指定空白坐标。
2. 拖动 Use LLM 节点跨越至少 150px。
3. Input→Get Property→Use LLM→Branch→Apply Action 建立连接，删除并重建一条边。
4. 编辑 Prompt 与 Branch 条件，保存并确认版本递增。
5. 强制刷新后位置、配置、边一致；重启 API 后再次一致。
6. dry-run 显示逐节点结果、版本/hash 且确认 `production_written=false`。
7. 制造版本冲突，页面保留本地草稿并提示刷新/合并，不覆盖服务端。
8. 生产执行、发布、自动化若未闭环必须 disabled，并显示具体原因。

## 9. 防回归与文档联动

1. 将 `/aip/logic` 与 `/aip/logic/:flowId` 的实际 route/component 加入 interaction-honesty manifest；总数从 35 调整并同步扫描器基线。
2. 扫描门新增：核心画布不得只有 HTML5 `onDrop` + 本地 append；必须存在 canonical GET/PUT、真实 DnD 节点和保存后重读测试。
3. 更新 `228-结构化风险修复计划.md`、`227-未完成项补齐计划.md`：227 历史页治理仍完成，但 AIP Logic 属独立核心补强，不回写旧百分比。

## 10. 非目标与风险

1. 不直接复制 Pipeline 的数据节点/构建/部署语义；只复用成熟交互模式。
2. 不在调试器展示模型私有 CoT；只展示服务端脱敏的步骤摘要、工具调用、token、耗时与提议 edits。
3. 不在 Stage A/B 实现真实 Ontology 生产写回；Apply Action 只产生可审计提议或 fail-closed。
4. 现有多套 Logic API 是历史债务；本波先停止页面混用和建立 deprecated adapter，删除旧 API 另立兼容清理任务。
5. 数据库迁移必须单 head、可升级、可回滚；禁止新增未登记 runtime DDL。

## 11. 四路审计结论

1. W1 前端审计确认：当前“连接”只是数组相邻装饰线，标签编辑写错层级；管道的 DnD、请求代次、保存一致性与属性折叠模式可复用，但管道专属节点/CSS 不直接复制。
2. W2 后端审计确认：至少 5 套 Logic 契约并存；Pipeline persistence 可借鉴完整快照/原子提交，但其缺租户隔离、CAS 和不可变历史，Logic 必须补齐后再使用。
3. W3 产品/门禁审计确认：当前耗时、Token、命中分支、历史和自动化存在合成或本地假状态；`/aip/logic` 必须作为第 36 个页面进入 interaction-honesty 门，不能申请 allowlist。
4. Planner 浏览器实测确认：新增第 5 Block 后刷新恢复 4 Block；因此 Stage A 的完成证据必须包含浏览器与 API 重启重放，而非只有组件测试。

## 12. Stage A 实施记录（已完成）

1. P0 止误导已完成：旧页面移除“生产执行”切换，安全试跑严格校验 `dryRun=true`、`productionWritten=false`，历史明确为当前会话，自动化保持禁用；累计 Web 回归通过后合入 m1 `02e9791`。
2. 自由画布基座已完成：10 种 canonical Block、调色板拖入/点击添加、节点自由移动、端口连接、Branch 路径端口、删边、删节点清边、缩放和 DAG 前置拒绝；专项 12 项及累计回归通过后合入 m1 `3c18795`。
3. 保存真实性适配已完成：创建/替换都要求响应快照严格一致，并再次 GET 核对 revision、hash 和完整图快照；专项 11 项相关测试通过后合入 m1 `f049787`。
4. 受控属性编辑器已完成：全部 10 kind 的关键配置、entry 设置、JSON 草稿显式应用及 Branch path 严格校验；专项 15 项及累计 1704 项 Web 回归通过后合入 m1 `00002cc`。
5. 后端 canonical store 与 Router 已完成并合入：专项 29 项、相关累计 169 项、API 全量 `8098 passed / 4 skipped / 2 subtests passed`；租户隔离、revision CAS、不可变快照、checksum、DAG/端口/Branch/Handoff 校验及数据库重启恢复均通过。
6. 页面串联、OpenAPI/路由基线、第 36 页 interaction-honesty 门和数据库迁移均已合入；Web 全量 `107 files / 1711 tests`、typecheck、Vite build 与 honesty scanner 36 页通过。
7. 浏览器实机完成 Branch 拖入、LLM 节点约 `170×120px` 自由移动、连边删除重建、Prompt 编辑、保存创建与 revision 2 更新；强刷与 API 重启后均恢复 4 节点、3 边、坐标、Prompt、revision 与 hash。
8. Stage A 退出门结论：可信图基座、自由画布、属性编辑、CAS 保存、保存后 GET 重读和重启恢复已闭环。dry-run、运行历史、发布与自动化不属于 Stage A，禁止扩大完成口径。

## 13. Stage B 实施记录（已完成，2026-08-01）

1. 可信 dry-run、10 kind fail-closed executor、不可变运行历史、逐节点状态/错误定位、Inputs 显式应用和 Inspector 必需配置已完成；详细契约和证据见 `228-AIP-Logic可信DryRun与运行历史实施方案.md` v1.1。
2. Logic 后端专项 `85 passed`、API 全量 `8155 passed / 3 skipped / 2 subtests passed`、Web 专项 `76 passed`、Web 全量 `110 files / 1759 passed`，typecheck/build、OpenAPI、Router manifest、Alembic、Ruff、36 页 interaction-honesty 均通过。
3. 浏览器已完成真实拖动→dirty→保存回读→成功试跑，以及 LLM adapter 缺失失败关闭；API 重启后成功/失败历史均持久存在。
4. 浏览器异常 drop 事件暴露的超大坐标已增加有限数与 5000px 可操作范围防御，专项 14 项和 Web 全量复跑通过；异常验收数据已恢复为 revision 3 合理坐标。
5. Stage B 所有退出门已关闭；Stage C 发布、Evals gate、Draft/Ontology 生产写回与生产自动化仍属于后续独立方案，当前继续禁用。

## 14. 画布端口拖线与方向箭头收口（已完成，2026-08-02）

1. 按 `228-AIP-Logic端口拖线与方向箭头实施方案.md` 完成输出端口拖入目标输入端口、实时预览、无效落点取消、SVG 方向箭头与画布级 Pointer 释放兜底；原点击连接路径继续保留。
2. 新连接仍统一经过 `tryAddLogicEdge`，重复边、自环、环路、端口与 Branch path 校验未旁路；未成功落点不修改 graph、不标 dirty。
3. 浏览器实测连接数从 3 增至 4、预览正常清理、全部正式边存在方向 marker；专项 16、Web 全量 1761、TypeScript、Vite build 与 36 页 interaction-honesty 均通过，合入 m1 `186ddd9`。
4. 本次是 Stage A 画布交互收口，不扩展 Stage C；发布、生产自动化和 Ontology 真实写回仍保持禁用。
