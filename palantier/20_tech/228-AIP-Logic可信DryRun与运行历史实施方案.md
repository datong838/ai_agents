# 228 · AIP Logic 可信 Dry-Run 与运行历史实施方案

> 版本：v1.2（2026-08-01，Stage B 最终关闭）
> 状态：**Stage B 已完成：实现、专项/全量门、浏览器成功/失败、坐标异常防御和 API 重启持久化全部通过；Stage C 发布/生产自动化仍禁用**
> 目标页面：`/aip/logic`、`/aip/logic/:flowId`
> 前置方案：`228-AIP-Logic核心自由画布与可信执行方案.md`
> 开工基线：m1 `9d2f145`；最终代码：m1 `1fb0fa2`

## 1. 使用 Rules

1. 先方案后编码；本文件冻结 API、执行语义、文件归属、风险和验收门，变更语义必须先改本文。
2. Stage A 全量回归、浏览器保存/刷新/API 重启恢复均通过后才进入 Stage B；Stage B 全量回归通过后才讨论 Stage C。
3. 只执行服务端已保存的 canonical revision；不接受客户端自带图执行，不执行 dirty 草稿。
4. 默认 fail-closed：未知 kind、缺能力、版本错配、无安全适配器、表达式错误、输出超限均明确失败，禁止 silent fallback 或 mock 成功。
5. `dry_run` 永远 `production_written=false`；`apply_action` 只生成 proposed edits，`execute` 只生成目标预览，Handoff 只生成移交意图，均不得产生外部写入。
6. 不返回或持久化模型私有 CoT；只允许结构化步骤摘要、真实工具调用元数据、真实 usage 和真实单调时钟耗时。
7. 最小改动并隔离旧系统：新 canonical executor 不直接复用会暴露 CoT、伪造 token/耗时或允许生产写的旧 `aip_logic_engine.py` / `logic_engine.py` 执行入口。
8. 四 Worker 文件互斥；共享 manifest、OpenAPI、迁移 head、页面集成与最终回归由 Planner 单点维护。

## 2. Stage A 前置出口证据

1. 前端专项 6 files / 48 tests、Web 全量 107 files / 1711 tests、typecheck、Vite build、36 页 interaction-honesty 均通过。
2. 后端专项 29 passed、相关累计 169 passed、API 全量 8098 passed / 4 skipped / 2 subtests passed；Alembic 为单 head `228logicgraph`。
3. 浏览器完成 Branch 拖入、LLM 节点横向约 170px/纵向约 120px 自由拖动、连边删除重建、Prompt 编辑与保存。
4. 服务端创建 `logic-msaibpn1-2`，保存到 revision 2；浏览器强刷和 API 重启后恢复相同节点、边、坐标、Prompt、revision 与 hash。
5. 因此 Stage A 已满足可信图基座退出门；Stage B 不再改写自由画布基础交互。

## 3. 现状审计与禁止复用边界

### 3.1 旧执行器问题

1. `aip_logic_engine.py` 默认走进程内 mock，仅识别 `task/branch/handoff/llm/tool`，会合成 token、耗时和 CoT；与 canonical 10 kind 不一致。
2. `logic_engine.py` 接受客户端图，采用单游标沿一条边执行，不具备完整 DAG 多入边/Handoff 语义；结果含 CoT。
3. 旧 `logic_engine.py` 的非 debug `apply_action` 把结果标成 `applied=true`，不满足本阶段绝不写生产的保证。
4. 旧 `use_llm` 默认调用真实网关，旧 `use_tool` 默认调用全局工具注册表；两者没有 canonical dry-run capability allowlist，不能直接接入。
5. `/v1/logic/run-graph`、`/v1/aip/logic/execute` 等旧入口接受客户端图或旧 kind，不能作为新页面真源。

### 3.2 可有限复用的纯能力

1. `function_engine` 的受限表达式 `parse/evaluate` 可通过新适配层复用，但必须增加输入/输出大小和异常映射测试。
2. Prompt 的变量替换思路可复用，但实现放入 canonical executor，并限制模板、变量与输出大小；不得复用旧 CoT 生成。
3. 工具注册表和 LLM 网关只能通过显式 dry-run adapter 注入；运行时没有已批准 adapter 时返回 `CAPABILITY_UNAVAILABLE`，测试使用确定性 fake。
4. proposed edits 的去重思路可复用，但所有字段必须校验，结果始终 `applied=false`。
5. adapter 调用必须经过有界并发的响应时限隔离；即使 adapter 阻塞或忘记 cooperative checkpoint，API 也须按节点预算返回 `ADAPTER_TIMEOUT`。底层 adapter 仍必须声明 read-only/dry-run-safe 并自行设置网络超时，默认生产注册表为空。

## 4. Canonical Dry-Run API

### 4.1 创建运行

`POST /v1/aip/logic/graphs/{graph_id}/dry-run`

请求：

```json
{
  "expected_revision": 2,
  "dry_run": true,
  "expected_graph_hash": "64-char-server-hash",
  "inputs": {"workOrder": {"status": "open"}},
  "idempotency_key": "optional-client-key"
}
```

约束：DTO `extra=forbid`；`expected_revision >= 1`；`expected_graph_hash` 必须为 64 位 hash；`dry_run` 必须显式且严格为 `true`，缺失、写成 `dryRun`、false 或非布尔值均 422；`inputs` 必填，必须为 JSON 对象且序列化后不超过 256 KiB；键、深度、字符串与集合长度受限；`idempotency_key` 最长 160。服务端按 Principal 绑定 org/project，精确读取已保存 revision 并复算 checksum，再校验 current revision/hash 与请求期望一致，绝不使用请求携带图。

响应：

```text
LogicDryRun
  run_id, graph_id, mode="dry_run"
  status="succeeded|failed"
  evaluated_revision, graph_hash
  production_written=false
  started_at, finished_at, elapsed_ms
  total_tokens|null
  node_results[]
  proposed_edits[]
  error|null
```

`total_tokens` 只有 adapter 返回可信 usage 时才为整数，否则 `null`，禁止估算。`elapsed_ms` 使用服务端单调时钟实测。执行失败也以不可变 run 记录保存并返回结构化结果；资源/租户/版本前置校验失败不创建假 run。

### 4.2 历史与详情

- `GET /v1/aip/logic/graphs/{graph_id}/runs?limit=20&before=<cursor>`：倒序分页，最大 100；返回轻量摘要和 next cursor。
- `GET /v1/aip/logic/graphs/{graph_id}/runs/{run_id}`：返回该次不可变完整结果。
- 两接口均 tenant scoped；graph/run 不存在统一 404，不提供 demo fallback。
- 历史保存执行时的 `evaluated_revision` 和 `graph_hash`，因此后续图更新不改变旧运行证据。
- POST 返回后，前端必须用 run detail 回读 `run_id/revision/hash/status`；回读缺失或不一致时提示“响应已收到，但历史持久化核验失败”，不得在本地伪造已持久化历史。

### 4.3 错误语义

| 场景 | HTTP/状态 | 结果 |
|---|---|---|
| graph 不存在/跨租户 | 404 | 不创建 run |
| expected revision/hash 不匹配 | 409 | 不执行、不创建 run |
| 请求格式/限制不合法 | 422 | 不创建 run |
| graph canonical 校验失败 | 422 | 不执行、不创建 run |
| 节点执行失败/能力不可用 | 200 + `status=failed` | 保存失败 run，后继节点 skipped |
| 历史保存失败 | 503 | 不返回“成功”；日志不含敏感输入 |

## 5. DAG 执行语义

### 5.1 调度

1. 执行前一次性严格校验非空图及全部 10 kind 配置，任何配置错误均 422 且不创建 run；entry 必须结构入度为 0。随后从 `entry_node_ids` 建立激活集合，服务端重新做 DAG 与端口校验并生成稳定拓扑序，同层按节点原顺序/ID 稳定排序。
2. 普通节点执行成功后激活全部 `out` 边；Branch 只激活唯一选中 path 的边，未选路径及只依赖未激活路径的节点标记 `skipped`。
3. 非 Handoff 多入边节点在至少一条已激活入边到达，且所有可能上游已确定 executed/skipped/failed 后执行一次。
4. Handoff 只等待“被激活的上游”；所有激活上游成功后执行一次。任一激活上游失败则 Handoff 与其后继 skipped。
5. 任一执行节点失败后立即停止新的调度；已激活但未开始的节点标记 `canceled/fail_fast`，确定未激活的节点仍为 `skipped`。最终 run 为 failed，禁止吞异常后走 default 或继续伪成功。
6. 设置节点数、边数、输出字节、总上下文字节、单节点耗时和总耗时预算；超限替换为失败证据后必须重新校验最终响应仍在预算内，绝不截断或返回超限内容后假装成功。
7. 执行器意外异常或 API 重启中断时，历史仍必须包含与 graph revision 完整对应的节点终态：稳定选择首个入口/拓扑节点记录 `failed`，其余记录 `canceled` 或 `skipped`，顶层 error.node_id 与失败节点一致；禁止只写顶层 failed 而丢失全部节点证据。
8. 后端响应模型和数据库回读边界执行与前端同构的交叉自洽校验：status/error、时间顺序、token 汇总、节点全集/kind、error 与 edit 来源均须一致；矛盾审计数据 fail-closed，不向页面返回不可解释的 200。

### 5.2 NodeResult

```text
node_id, kind, status(executed|skipped|failed|canceled)
started_at|null, finished_at|null, elapsed_ms|null
summary, output|null, usage|null, tool_call|null
selected_branch_path|null, proposed_edits[]
error|null
```

`summary` 是固定模板生成的短说明，不包含隐式推理；输出按安全规则裁剪/脱敏并记录是否 truncated。skipped 必须带机器可读 reason，例如 `branch_not_selected`、`upstream_failed`、`not_reachable`。

### 5.3 十种 Block 的 Stage B 行为

| kind | dry-run 行为 | 失败条件/边界 |
|---|---|---|
| `input` | 校验请求 inputs 与 `config.schema`，写入上下文 | schema 非对象或输入不匹配 |
| `create_variable` | 用 `config.name` + `config.expression` 计算变量 | 名称/表达式缺失或解析失败 |
| `get_property` | 从明确的 source/property 获取字段；若仅有 property，则从唯一上游输出读取 | 源不存在、字段不存在或来源不唯一 |
| `transform` | 用 `config.expression` 生成受限 JSON 值 | 表达式失败/输出超限 |
| `branch` | 按 `config.paths` 顺序求值非 default condition；首个 true 胜出，否则唯一 default | 多命中仍首个稳定胜出；无命中且无 default 则失败 |
| `handoff` | 生成 `{decision,handoff_to,context_summary,submitted:false}` | 目标不在 allowlist；绝不发 webhook/创建 Draft |
| `apply_action` | 根据 `config.action` 与 edits 模板生成并校验 proposed edits | 未配置 edits/字段非法；始终 `applied=false` |
| `execute` | 生成 `{target,request,executed:false}` 目标预览 | 未注册 sandbox adapter 时 fail-closed，不调用子流程/外部系统 |
| `use_llm` | 经显式 dry-run LLM adapter 调用；记录输出与真实 usage | adapter/模型未批准、超时、usage 非法；不输出 CoT |
| `use_tool` | 仅调用注册为 `read_only + dry_run_safe` 的 adapter | 未注册、可写工具、超时或返回超限均失败 |

前端现有字段 `name/expression/property/prompt/model/tool/action/target/decision/handoff_to/paths/schema` 是本阶段 canonical 配置名。后端拒绝把旧 `expr/tool_id/action_ref/query` 静默当成新字段；旧 API 的映射另立兼容适配，不污染 canonical snapshot。

## 6. 持久化与数据保护

新增迁移 `228logicrun`，`down_revision=228logicgraph`：

1. `aip_logic_graph_runs`：联合租户键、graph_id、run_id、revision/hash、status、时间、真实 elapsed/token、production_written 固定 false、inputs/output 摘要、proposed edits、error、actor、idempotency key；运行开始前先插入 running，完成后只允许一次 terminal finalize。
2. `aip_logic_graph_run_nodes`：联合租户/run/node 键、topo index、kind/status、selected path、安全输入/输出摘要、proposed edits、真实 usage/elapsed 与结构化 error；逐节点只写 terminal 记录。
3. 索引 `(org_id, project_id, graph_id, started_at DESC, run_id DESC)`；run 关联不可变 graph revision 的联合租户键；scope 内 idempotency 唯一；删除 current graph 不级联历史。
4. 原始 inputs 默认只保存经过限制和敏感键脱敏的 snapshot；密码、token、secret、authorization、cookie 等键值替换为固定标记。
5. 结果与日志不落 Prompt/LLM 原始回答、模型私有推理、工具原始参数、Authorization、连接器凭据或完整敏感对象；API 响应与持久化使用同一 sanitizer，LLM 只保存模型、真实 usage、长度/hash 和脱敏摘要。
6. 每一步的 terminal 写入和最终 finalize 具备事务边界；finalize 失败不能返回“成功”。API 重启时只按目标 graph、逐 run 隔离恢复超时 running；坏 snapshot 保留审计但不得放大为同租户其他 graph 的 503。迁移必须 upgrade/downgrade、单 head、生成检查和临时 schema 验证通过。

## 7. 前端产品行为

1. 仅在 `graph.persisted=true`、无 dirty、revision/hash 有效且当前没有运行中的请求时启用“安全试跑”；否则按钮 disabled 并显示具体原因。
2. 点击试跑前发送当前 `revision`，执行期间锁定再次触发；409 保留本地草稿并提示重新加载，不自动覆盖。
3. 页面提供独立的 Dry-Run Inputs JSON 编辑区；只接受 JSON 对象并显式应用，不把 inputs 写入 graph revision，不以隐藏默认值替代用户输入。
4. 结果面板先对响应做白名单校验：mode、graph/revision/hash、run_id、节点归属/唯一性、状态及 `production_written` 必须严格一致；递归出现 `cot/reasoning/chain_of_thought` 字段即拒绝渲染。通过后才显示总体状态、真实耗时/token（null 显示“未提供”）、逐节点 executed/skipped/failed 和错误定位。
5. 画布节点同步高亮本次状态；切换历史记录只读回放，不修改图，不把历史结果写入画布模型。
6. 历史 Tab 从服务端分页读取；GET 失败显示真实错误和重试，不回落本地假记录。
7. `自动化`、生产执行、发布仍禁用；Stage B 不新增“看起来可用”的开关。
8. 为让 10 kind 可配置，第二小波以受控 JSON 编辑器补齐 `get_property.source`、`use_tool.arguments`、`apply_action.edits`、`execute.request`；字段必须显式应用并在客户端先做结构校验，后端仍是最终真源。不得用隐藏默认值制造成功。

## 8. 文件分工与并行策略

### 第一小波

| 角色 | 独占文件 | 任务 |
|---|---|---|
| W2 | 新增 `aip_logic_dry_run_models.py`、`aip_logic_dry_run_executor.py`、`aip_logic_run_store.py`、迁移和专属 tests | canonical 调度、10 kind、安全适配器接口、运行历史持久化；不改 Router/manifest/Web |
| W1 | 新增 `logicRunContracts.ts`、`logicRunApi.ts` 与专属 tests | 严格 DTO、响应白名单/CoT 拒绝、dry-run、历史列表/详情和 POST 后回读；不改页面 |
| W3 | 新增 `LogicRunPanel.tsx`、专属 tests/CSS | 纯受控逐节点结果、历史列表/下钻和错误定位展示；不自行请求、不含 demo |
| Planner | 文档、契约复核、合并和专项门 | 审查三路实现是否符合本文，先合独占文件并跑累计回归 |

### 第二小波

1. 三路合入 m1 并回归后，W3 独占修改 `LogicCanvasPage.tsx` 与页面测试，接入试跑、历史和状态高亮。
2. 页面集成稳定后，W1 独占扩展 `LogicGraphInspector.tsx` 与测试，补齐 Stage B 必需的 source/arguments/edits/request 受控配置；其他 Worker 不同时修改 Inspector。
3. W3 以独立 B2.1 小波给 `LogicGraphCanvas` 增加只读节点运行态徽标；不得改变 DnD、选中、端口和连线模型。
4. Planner 独占修改 canonical Router 注册、domain manifest、OpenAPI/inventory、迁移基线与 interaction-honesty 描述；处理共享冲突。
5. W1/W2 只做各自文件的审查修复，不同时触碰页面/Router。

## 9. 测试与阶段退出门

### 9.1 后端专项

1. 10 kind 成功/失败矩阵；未知 kind/未知 config 字段、表达式异常、超时、大小/深度限制。
2. 多入口、多分支、default、无命中、合流、Handoff 等待、未激活路径、上游失败、稳定拓扑序。
3. use_llm/use_tool 无 adapter fail-closed；fake adapter 返回真实 usage；可写工具拒绝；绝无 CoT 字段。
4. apply_action/handoff/execute 均证明 `production_written=false` 且无外部副作用。
5. revision 409、跨租户 404、历史不可变、倒序分页、API/进程重启恢复、失败 run 保存、事务失败不伪成功。
6. sanitizer 对 secret/token/cookie/authorization 与嵌套集合生效；输出/上下文预算。

### 9.2 前端专项

1. 未保存、dirty、运行中、无 revision 四种 disabled 原因。
2. 成功/部分 skipped/failed/409/网络错误/历史空态与重试。
3. token null 不显示 0，elapsed 只显示服务端值，明确展示“不写生产”。
4. 历史切换不修改 graph/dirty；旧请求晚到不能覆盖新 flowId。
5. 节点状态高亮与 run detail 一致，关闭/切换后恢复编辑态。

### 9.3 累计与浏览器门

1. Worker 专项 → Logic 相关累计 → API/Web 全量 → typecheck/build → migration/OpenAPI/router/generator → interaction-honesty。
2. 浏览器在已保存 revision 运行 Input→Get Property→Use LLM/安全失败→Branch→Apply Action，逐节点结果与图高亮一致。
3. 验证成功 run、失败 run、历史重载、浏览器强刷和 API 重启后 run detail 一致。
4. 网络断开、版本冲突、adapter 缺失均清晰 fail-closed；生产写入口仍禁用。
5. 全部退出门通过后才把 Stage B 标记完成；任何一门失败都不进入 Stage C。

## 10. 明确非目标

1. 本阶段不发布、不生产执行、不启用 Automate、不创建真实 Draft、不写 Ontology、不发 webhook。
2. 不完成某一具体电商平台的连接器或能力注册；只做通用平台 executor 与 adapter 边界。
3. 不删除旧 Logic API；只停止新页面混用。旧 API 收敛/废弃另立兼容方案。
4. 不把测试 fake、demo 数据或 mock adapter 注册到生产运行时。

## 11. 最终收口补充（2026-08-01）

1. interaction-honesty 清单必须同步更新为 Stage B 的真实能力边界：仅已保存、无 dirty 且 revision/hash 一致的图可执行安全试跑；试跑结果必须 POST 后 GET 详情回读，历史来自服务端；生产自动化继续禁用。
2. 清单测试索引必须覆盖页面试跑/历史集成、运行契约严格校验、运行 API 回读、画布节点状态和 Inspector 的 10 kind 配置，不得继续只引用 Stage A 的保存与拖拽测试。
3. 最终 OpenAPI 以 `inputs` 必传和严格响应交叉校验后的模型为准；实现提交后必须重新生成并执行 deterministic check，禁止保留旧快照。
4. 最终验收顺序固定为：专项测试 → Logic 累计回归 → Web/API 全量 → typecheck/build → OpenAPI/router/migration → interaction-honesty → API 重启与浏览器成功/失败/历史持久化实测。

## 12. Stage B 实施记录（已完成）

1. canonical dry-run 已完成：只接受服务端已保存 revision/hash 和显式 `inputs`；10 kind 严格 preflight，未知配置、版本冲突、未批准 adapter、表达式/预算/超时异常均 fail-closed。
2. 运行历史已完成：`228logicrun` 两张租户隔离表保存不可变 run/逐节点证据；running 恢复按 graph 隔离，坏记录隔离后不放大为同租户其他 graph 的 503；数据库与代码均为唯一 `228logicrun (head)`。
3. 安全边界已完成：默认生产 adapter registry 为空；adapter 必须同时声明 read-only 与 dry-run-safe，并经过有界并发/响应时限隔离；`apply_action` 只生成 `applied=false` 提议，全部响应固定 `production_written=false`，不返回 CoT 或伪造 usage。
4. 页面已完成：独立 Inputs JSON 显式应用、严格试跑门禁、POST 后 GET 详情核验、服务端历史分页/下钻/重试、逐节点运行态、错误定位，以及 10 kind Inspector 的 source/arguments/edits/request 编辑。
5. 自动门证据：Logic 后端专项 `85 passed`；API 全量 `8155 passed / 3 skipped / 2 subtests passed`；Web 专项 `6 files / 76 passed`；Web 全量 `110 files / 1759 passed`；TypeScript、Vite production build、OpenAPI deterministic check、Router manifest、36 页 interaction-honesty、Ruff 和迁移 current/head 均通过。
6. 浏览器成功证据：`logic-stageb-success` 的 Input→Create Variable→Transform→Apply Action 图中，Input 节点真实拖动后进入 dirty，保存并回读到 revision 2；试跑 4/4 executed，产生 1 条未应用提议，历史 run 为 `succeeded` 且 `production_written=false`。
7. 浏览器失败证据：`logic-stageb-failclosed` 的未注册 LLM 返回 `LLM_ADAPTER_UNAVAILABLE`，输入 executed、LLM failed、下游 skipped，完整逐节点证据进入历史且 Token 显示“未提供”；未出现模拟成功。
8. API 再次重启后，上述成功与失败 run 的原 `run_id`、revision/hash、错误码和节点计数仍能从服务端读取；强刷页面仍显示同一历史，证明不是内存或前端假状态。
9. API 全量回归最终为 `8155 passed / 3 skipped / 2 subtests passed`，Stage B 所有退出门关闭。Stage C 发布/生产自动化仍保持禁用。
10. 最终浏览器自动化暴露的异常坐标缺口已关闭：自由画布对 `NaN/Infinity`、异常超大 delta 和 palette drop 做有限数防御并钳制到 5000px 可操作范围；正常缩放拖动、负坐标回弹和 drop 语义保持不变。新增边界/交互 14 项通过，随后 Web 全量 1759 项再次通过；验收图恢复为合理坐标、保存到 revision 3，并由重启后的 API 回读确认。
