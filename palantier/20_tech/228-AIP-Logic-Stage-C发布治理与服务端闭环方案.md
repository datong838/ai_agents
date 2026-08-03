# 228 AIP Logic Stage C 发布治理与服务端闭环方案

> 版本：v1.1（2026-08-02，C1 交付复核）
> 编码基线：`aos-platform` m1 `b78a3bf`；交付版本：m1 `bc9711a`
> 状态：Stage C C1 已完成；C0.2 未关闭前禁止生产写回；具体电商平台、外部写回执行器和真实商家凭据后置
> 上游：[`07-AIP引擎k-LLM与AgentStudio产品方案.md`](../07-AIP引擎k-LLM与AgentStudio产品方案.md)、[`228-AIP-Logic核心自由画布与可信执行方案.md`](./228-AIP-Logic核心自由画布与可信执行方案.md)、[`228-AIP-Logic可信DryRun与运行历史实施方案.md`](./228-AIP-Logic可信DryRun与运行历史实施方案.md)

---

## 1. 目标与阶段边界

Stage C 将已完成的 canonical Graph 和不可变 Dry-Run 证据提升为可信发布能力：

1. 发布只引用服务端已保存、无脏数据的精确 `revision + graph_hash`。
2. 发布必须绑定同一 Logic revision 的真实 Evals 证据；未通过、证据缺失、目标不一致或证据过期均 fail-closed。
3. 发布产物不可变；后续编辑仍形成新草稿 revision，不得原地修改已发布快照。
4. 页面发布成功后必须 GET 回读发布记录，再显示“已发布”。
5. 自动化只能绑定已发布产物；第一波只建设受治理的绑定契约和禁用原因，不启用生产调度执行。
6. Dry-Run 的 proposed edits 仍不写生产；外部执行器、Ontology Action 写回或 Draft 自动创建缺少完整契约时继续禁用，禁止用旧内存引擎模拟。

本方案不包含具体电商平台连接器、商家授权、平台字段映射、Webhook 或生产任务调度。

## 2. 现状与禁止复用边界

| 能力 | 可复用 | 禁止直接复用 |
|---|---|---|
| Graph | `aip_logic_graph` 当前快照、`aip_logic_graph_revision` 不可变修订、CAS revision/hash | 旧 `aip_logic_version.py` 进程内版本管理 |
| 执行证据 | canonical `aip_logic_graph_runs` 及逐节点历史 | 接受客户端图、可产生伪写回的旧 Logic 执行器 |
| Evals | `/v1/evals` 页面交互和 run→report→gate 一致性检查可作产品入口 | 当前进程内 suite/report 无认证、无租户、可回显 expected 自证通过，不能直接作为发布证据 |
| Draft | `runtime_write.apply_draft_approval()` 的对象写入、状态更新、lineage 同事务思路可复用 | 当前 Draft/对象/lineage 仍有租户键、权限、幂等、并发和重复路由缺口；C0 前不得用于 Stage C 写回 |
| Automation | 产品规则、L4 熔断和只读展示可复用 | `phase3_aip_logic` 内存 automation 不得绑定生产发布版本 |

### 2.1 C0 治理止血门（安全复核新增）

编码前复核确认，下列问题属于生产写回 P0，不得被 C1 发布 UI 掩盖：

1. Evals 路由缺少 Principal/租户，suite/report 仅在进程内存；空 `target_expr` 会返回 expected，存在自证绿灯。
2. Draft 同一路径存在 PostgreSQL 与 Phase3 内存实现的重复注册；审批缺少强制角色、职责分离、持久幂等和行级并发控制。
3. `obj_instance`、部分 branch/lineage/wiki 主键或查询没有完整 org/project 维度，尚不能证明跨租户生产隔离。
4. 旧 Automate `fire()` 不执行 canonical Logic 即返回 completed/随机 proposal ID，属于模拟完成。
5. 旧 Logic/Evals/Draft/Automation 单例引擎均不得成为 Stage C 生产真源。

C0 分两层退出：

- **C0.1 发布证据层**：先完成租户隔离的 Evals suite/report 持久化，取消 expected 回显，生成绑定 graph/revision/hash 的不可变 `report_id`；完成后方可实施 C1 发布。
- **C0.2 生产写回层**：在开启 Draft/Automation/Ontology 生产链前，必须另波完成对象与 lineage 租户化、Draft 路由唯一性、审批授权/职责分离、持久幂等、CAS/行锁和 branch merge 受控化。C0.2 未关闭不阻止创建只读 publication，但必须阻止自动化和外部写回。

## 3. 第一波：可信发布最小闭环

### 3.1 数据模型

新增迁移顺序固定为 `228logiceval` → `228logicpublish`；并行开发允许 worker 临时都基于 `228logicrun`，合并时由 Planner 串成唯一 Alembic head：

1. `aip_logic_publication`：租户键、`publication_id`、`graph_id`、`graph_revision`、`graph_hash`、不可变 graph snapshot、`eval_suite_id`、`eval_report_id`、门控摘要、actor、created_at。
2. 同一租户与 graph revision 只允许一个发布产物；幂等重试返回同一 publication。
3. `aip_logic_graph.published_version` 记录最后发布的 graph revision，但 graph 当前编辑状态保持 draft；不得把当前 payload 改成可变的 published payload。
4. 外键同时包含 org/project/graph/revision，发布后删除或编辑 current graph 不得改变 publication snapshot。

### 3.2 发布接口

`POST /v1/aip/logic/graphs/{graph_id}/publish`

请求字段：

- `expected_revision`
- `expected_graph_hash`
- `eval_suite_id`
- `eval_report_id`
- `idempotency_key`

严格规则：

1. Graph 不存在/跨租户统一 404；revision/hash 冲突 409。
2. Graph 必须通过 canonical 校验且至少存在一条与当前 revision/hash 一致的成功 dry-run。
3. Evals report 必须来自 C0.1 持久层、门控通过、target 为该 graph 的精确 revision/hash；不能只凭 suite 最新绿灯。
4. 任一依赖异常不得新增 publication 或更新 `published_version`。
5. 成功响应后前端调用 `GET .../publications/{publication_id}` 回读；不一致不得显示成功。

读取接口：

- `GET /v1/aip/logic/graphs/{graph_id}/publications`
- `GET /v1/aip/logic/graphs/{graph_id}/publications/{publication_id}`

### 3.3 Evals 发布证据

第一波将发布所需的 suite/report 元数据迁入租户隔离持久层，并增加 Logic revision 目标：

1. 每次报告拥有不可变 `report_id`。
2. 报告保存 `target_type=logic_graph`、`target_id`、`target_revision`、`target_hash`。
3. 发布只读取指定 report，不重新运行、不复用其他 revision 报告。
4. 旧无目标报告可以继续在 Evals 页面查看，但不能作为 Logic 发布证据。
5. `logic_graph` 评测必须由 canonical `LogicDryRunExecutor` 执行指定 revision/hash 的不可变快照；禁止接收独立 `target_expr` 或回显用例 expected 作为目标输出。
6. 每个用例的 actual 取自实际执行路径上最后一个已执行终端节点；图校验、适配器、节点执行或终端输出不唯一时，本次评测整体 fail-closed 且不产生可发布报告。

## 4. 第二波：页面发布治理

`/aip/logic/:flowId` 增加发布面板：

1. 仅 persisted、无 dirty、revision/hash 合法、非运行中时允许选择 Evals suite/report。
2. 明示展示 Graph revision/hash、report ID、通过率、阈值和运行时间。
3. 未运行 Evals、报告未通过、报告目标不一致、网络错误均展示具体禁用原因。
4. 发布中禁止重复提交；409 不覆盖本地草稿。
5. POST 后 GET 回读一致才展示 publication ID 和“已发布 revision N”。
6. 发布历史只读；选择旧 publication 不改变当前画布。
7. “自动化”页签展示“仅可绑定 publication”的契约；生产调度未闭环前保持禁用。

## 5. 第三波：Draft / Automation 安全扩展

第三波必须在新的独立退出门下实施：

1. 从指定成功 run 的 proposed edits 创建 PostgreSQL Draft，并记录 graph/publication/run 三重来源。
2. Draft 评论、历史、退回修改及完整状态流需新增 PG 表和审计事件，不能落内存。
3. Automation 绑定表只接受 `publication_id`；变更绑定创建新版本，不能原地替换审计证据。
4. 生产执行必须注册明确 executor，受 Principal、Action Submission Criteria、幂等、熔断和审计约束。
5. 没有 executor 或不满足权限时 fail-closed；第一波/第二波完成不代表外部写回已启用。

## 6. 文件所有权与并行策略

| 角色 | 独占范围 | 禁止同时修改 |
|---|---|---|
| W1 | 新发布 DTO/store/迁移及后端专项测试 | Evals、前端页面、共享 Router manifest |
| W2 | C0.1 Evals 持久化证据、租户隔离、Logic target 契约及专项测试 | Graph store、前端页面 |
| W3 | 前端 publication contracts/API/纯展示组件及测试 | 后端、`LogicCanvasPage.tsx` |
| Planner | 两份上游文档、canonical Router、manifest/OpenAPI、页面最终集成、合并与回归 | Worker 独占实现文件 |

若共享文件冲突，由 Planner 串行处理；任何 worker 不得自行改全局 CSS、路由聚合或 OpenAPI 快照。

## 7. 测试与退出门

### 7.1 后端专项

1. 成功发布、幂等重放、重复 revision、并发发布。
2. 404/409/422、hash 篡改、无成功 dry-run、Evals 未通过、report 目标不一致或过期。
3. publication snapshot 不可变；current graph 后续 revision 不改变旧发布记录。
4. 跨租户隔离、API 重启恢复、事务失败不伪成功。
5. 迁移 upgrade/downgrade、单 head、Router manifest/OpenAPI 确定性。
6. Evals 无 Principal、空 target、expected 回显、跨租户读取、API 重启丢失等旧问题必须有负向测试并关闭。
7. Evals 必须证明用例 actual 来自指定 Logic revision/hash 的 canonical 执行；伪造 `target_expr`、历史 revision/hash 错配、无终端输出均不得生成绿灯。

### 7.2 前端专项

1. dirty/未保存/运行中/报告缺失/报告失败/目标不一致的禁用原因。
2. POST 后 GET 回读成功、回读不一致、409、网络错误和重复点击。
3. 发布历史切换不修改 graph、dirty、节点或 dry-run 历史。
4. 页面不得把旧 Evals 绿灯、localStorage 或 mock 当发布证据。

### 7.3 累计与浏览器门

1. Worker 专项 → Logic/Evals 累计 → API/Web 全量 → typecheck/build。
2. OpenAPI、Router manifest、migration single-head、interaction-honesty 全部通过。
3. 浏览器完成：保存 revision → 对同一 revision 运行 Evals → 发布 → GET 回读 → 强刷 → API 重启后重读 publication。
4. 修改图形成下一 revision 后，旧报告不得发布新 revision；旧 publication 内容保持不变。
5. 每个波次全部退出门通过后才能进入下一波；失败即停止合并，不以补文案代替修复。

## 8. 后续通用平台波次

Stage C 第一、二波关闭后，按独立 `228-` 子方案依次处理：

1. C0.2 对象/Draft/lineage 租户与审批安全闭环，然后再做 Draft/Studio 服务端闭环。
2. Wiki/Property/Function 真落库。
3. Observability/Capacity/Model Catalog/Action Type 治理契约。
4. Analyst、Widget、Wiki HTML、L4/COP 和低频 Canvas 菜单。
5. 旧 Model Router/Logic API 调用归零与进程内状态迁移。

完成上述通用平台能力并通过全量回归后，再进入具体电商平台接入专项。

## 9. 实施结果（2026-08-02）

### 9.1 交付状态

| 工作流 | 结果 | 合入记录 |
|---|---|---|
| W1 不可变 publication store / 迁移 | 已完成 | `82b59bb` → m1 `239ebbc` |
| W2 租户隔离 Evals 证据 | 已完成 | `3c49393` → m1 `46b9bda` |
| W3 publication 前端契约/面板 | 已完成 | `8fe6389` → m1 `73ec007` |
| Planner Router/页面集成/OpenAPI/canonical Evals | 已完成 | m1 `bc9711a` |

### 9.2 真实性与安全边界

1. Evals suite/report 已持久化并按 org/project 隔离，report 绑定精确 Logic revision/hash。
2. `target_expr` 已从 Logic Evals 公开契约移除；actual 仅来自 canonical `LogicDryRunExecutor` 对指定不可变快照的实际执行。
3. publication 需同 revision/hash 的成功 dry-run 与指定通过 report，交易内锁定并写入不可变快照；POST 后必须 detail GET 与 Graph GET 双重回读。
4. Automation、Draft 生产写回和外部电商动作仍禁用；C0.2 未关闭前不得开启。

### 9.3 退出门结果

- Web 专项：5 文件 / 36 项通过。
- Web 全量：113 文件 / 1781 项通过；TypeScript 与生产构建通过。
- API 受影响累计：59 通过、1 条外部条件跳过、2 个子测试通过。
- API 第二次完整全量：8180 通过、3 条外部条件跳过、2 个子测试通过。
- OpenAPI 双进程确定性、Router manifest、36 页 interaction-honesty 与 Alembic 唯一 `228logicpublish` head 全部通过。
- 浏览器主流程：先用既有终点为 Action proposal 的图验证 Eval 0/1 且发布阻断；再用 `logic-stagec-browser` 完成 Eval 1/1、成功 Dry-Run、不可变 publication `logic-pub-b16d658495f64d05ba73251421a1f1fa` 详情回读。普通刷新及 API 进程重启后，run/report/publication 均可重新读取，`production_written=false`。

### 9.4 下一步

Stage C C1 已关闭。电商专项前仍建议优先关闭 C0.2（对象/Draft/lineage 租户与审批安全）；如电商专项首期仅做读取、映射和手工发布，可在明确不开启生产写回的前提下并行准备产品/技术方案。
