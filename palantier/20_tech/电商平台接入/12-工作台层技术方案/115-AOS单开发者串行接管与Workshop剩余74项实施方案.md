# AOS 单开发者串行接管与 Workshop 剩余 74 项实施方案

> 日期：2026-08-24
> 开工基线：`AOS-000156 / aos-platform/m1@54031a8`
> 用户授权：当前执行者成为整个 AOS 唯一开发者，在 `m1` 串行维护 Data、Ontology/Domain、AIP、Workshop 与运行交付层
> 当前事实：96 个主 Task 已完成 22 个，剩余 74 个；下一主 Task 为 W2-01
> 执行状态：`APPROVED_FOR_SERIAL_IMPLEMENTATION / S1_IN_PROGRESS / AOS-000158`

## 1. 目标与不变量

本方案把原跨 Owner 等待改成单开发者串行修复：Workshop 遇到 Data、Ontology、AIP 或运行层缺口时，由同一执行者在方案与 Lease 约束下直接维护对应层，直到 Workshop 可继续。任何内部 Owner 名称不再构成停工理由。

以下硬门不因角色变化而解除：

- 正向只认 `org-org/dev-project`，`dev-org/dev-project` 只作负向 canary；
- authority/01/06/Prime 只走 `m1` 串行 CAS、确定性 sync 与 exact readback；
- Secret/PII/provider payload 不进入命令、日志、Receipt 或记忆；
- migration 必须独立 Lease、single head、RLS/FORCE RLS、upgrade/downgrade 与回滚；
- 外部调用、真实业务数据写入、Pipeline replay 与发布不能由代码测试或用户“连续开发”授权替代；
- unknown 外部结果进入 reconcile，禁止盲重试或扩大 timeout 伪造成功。

## 2. 剩余总波次

| 波次 | 主 Task 数 | 范围 | 主要产物 |
|---|---:|---|---|
| S0 | 0 | 接管、清单、ADR、authority 路由 | 82/100 解环、总清单、Task/Delivery Receipt、CAS |
| S1 | 2 | W2-01 + W3-12 | D0、统一运营只读模型、OperationCase authority、命令与浏览器闭环 |
| S2 | 9 | W2-02～W2-10 | 其余七领域只读模型、shared ref/timeline/navigation、八页矩阵 |
| S3 | 13 | W3 除 W3-12 | 公共生产合同消费、Task/Handoff、内容与经营 authority、累计门 |
| S4 | 8 | W4-01～W4-08 | Evidence/Eval/Wiki/Query/SavedExploration |
| S5 | 9 | W5-01～W5-09 | 受控 Action、Adapter、幂等、unknown/reconcile |
| S6 | 10 | W6-01～W6-10 | 职责解析与达人/价格/客户批次 |
| S7 | 23 | W7 + W8 | 多媒体、六场景、运营就绪与发布决定 |
| **合计** | **74** |  |  |

## 3. S1 固定无环顺序

```text
D0 Data exact authority
  → W2-01A public read primitives and blocked-aware slices
  → W3-12A OperationCase authority
  → W2-01B seven-slice unified view
  → W3-12B commands, UI and browser acceptance
```

### 3.1 D0

冻结 ProductSku/Inventory 语义 revision、售后 Event/Object authority、exact ref/hash、正负租户证据；不复制业务 payload。若 P01 或其他 SourceReadiness 运行失败，先诊断并修复系统代码/配置，在无真实运行授权时不得重放 Pipeline，而由 W2-01A 对应 slice 诚实 blocked。

#### 3.1.1 D0-A 文件级实施清单（2026-08-24）

本子波不新增数据库对象，不执行 Pipeline，不读取真实业务 payload，只闭合可由代码权威证明的语义合同：

- `ecom_core_models.py`：把 `stock`、`stockAlarm` 冻结为 ProductSku 可选规范属性，库存数量继续属于 ProductSku original，不创建第二 Inventory 真源；
- `ec_normalizer.py`：把源 `stock` / `goods_stock_alarm` 映射到 ProductSku properties，现有 `stock_health` 派生逻辑保持不变；
- 新增 `ecommerce_data_authority_contracts.py` 与 `ecommerce_data_authority.py`：定义 tenant-bound exact authority descriptor、semantic revision、canonical content hash，以及 Inventory/AfterSalesEvent 两份只读合同；AfterSalesEvent 此时只冻结事件引用字段，不落库、不复制退款 payload；
- 新增对应 contract/service tests，并扩充 `test_ec_normalizer.py`、`test_ecom_core_models.py`；正向 tenant 为 `org-org/dev-project`，负向 canary 为 `dev-org/dev-project`，二者 descriptor 必须 tenant-bound 且 hash 相同、ref 不可跨租户复用；
- 最后把 D0 descriptor 注入 `ecommerce_workshop_operations.py`：exact semantic revision/hash/Receipt 匹配后关闭“authority 不存在”缺口，但在真实 reader 与 SourceReadiness 未闭合前，Inventory 与 aftersaleEvents 切片继续以 `*_READER_NOT_WIRED` 结构化 `blocked`；不得仅凭合同存在就提升业务切片为 `ready`。

当前事实：W2-01A backend strict DTO/GET 壳已在 `m1@5b0e715` GREEN；D0-A semantic authority 已在 `m1@5282b7b` GREEN，累计 Data/Workshop `139 passed`。W2-01 主 Task 尚未完成，后续顺序为 D0 real readers → W3-12A → W2-01B → W3-12B。

测试顺序固定为：失败合同测试 → D0 专项 → ProductSku normalizer/core model 邻接回归 → W2-01A operations 回归 → Workshop 累计回归。禁止项仍为 migration、真实数据读写、Provider、Pipeline replay 和发布。

#### 3.1.2 D0-B tenant-safe Inventory reader（下一子波）

新增 `ecommerce_inventory_reader_contracts.py`、`ecommerce_inventory_reader.py` 与 `test_ecommerce_inventory_reader.py`。Reader 仅从 `ecom_object` 的同租户 `ProductSku` originals 读取 `stock`、`stockAlarm`、`stock_health`、`source_updated_at`、`payload_hash`，固定 `REPEATABLE READ READ ONLY`、`aos_runtime` 与 transaction-local tenant GUC；不读取 raw source 表，不调用 Pipeline，不把临时 raw 行或通用 Ontology API 当 authority。

首批只交付内部 bounded reader 与 exact row ref，不新增外部 API、不把数据嵌入 W2 壳。测试必须覆盖：正向/负向租户参数、只读 SQL、截止时间、确定性排序、边界上限、缺失库存语义失败关闭、naive cutoff 拒绝、无写语句。AfterSalesEvent 因当前仅 contract-only，不得仿照 Inventory 读取或制造事件；继续结构化 blocked，随后直接进入 W3-12A code authority。

### 3.2 W2-01A 首批文件级清单

新增：

- `services/aos-api/aos_api/ecommerce_workshop_operations_contracts.py`
- `services/aos-api/aos_api/ecommerce_workshop_operations.py`
- `services/aos-api/tests/test_ecommerce_workshop_operations_contracts.py`
- `services/aos-api/tests/test_ecommerce_workshop_operations_api.py`

最小修改：

- `services/aos-api/aos_api/routers/ecommerce_workshop.py`
- `apps/web/src/api/ecommerceWorkshop/contracts.ts`
- `apps/web/src/api/ecommerceWorkshop/parser.ts`
- `apps/web/src/api/ecommerceWorkshop/client.ts`
- `apps/web/src/api/ecommerceWorkshop/index.ts`
- 对应 parser/client tests

首批只实现 strict DTO、GET-only router、Principal 租户、稳定 cursor、slice readiness、count/join ledger 和 exact ref 校验；不新增 migration，不写真实业务数据。页面在后端与 SDK 同版 GREEN 后进入下一子提交，并使用内置浏览器验收。

### 3.3 W3-12A/B

W3-12A 独立登记 migration Lease，实现 append-only Case/Decision/Policy authority、RLS/FORCE RLS、expectedVersion、幂等和可逆聚合；W3-12B 最后接命令、Approval/ExecutionLease/Receipt、strict SDK/UI、三视口和双租户浏览器验收。

#### 3.3.1 W3-12A1 authority contract 与 migration schema

以 `AOS-000160`、`aip13_001` 单一 Alembic head 和 100 号 ADR 为输入，先闭合代码控制面，不运行真实 migration：

- 新增 `ecommerce_operation_case_contracts.py`，冻结 tenant-bound exact original ref、OperationCase/CaseEvent、ClassificationDecision、AggregationPolicy、MembershipDecision、SLA Policy/Clock、AutomationKill Decision 与幂等 Receipt 的严格模型；所有 hash 为 64 位小写 SHA-256，时间必须带时区，禁止订单、支付、地址、客户或 Provider payload；
- 新增 `w3_012_operation_case_authority.py`，唯一 `down_revision=aip13_001`。head 仅保存 current revision/version；事件、分类、策略、成员、SLA、kill 与 Receipt 全部 append-only，并为每张 tenant 表启用 RLS/FORCE RLS；运行角色不得 UPDATE/DELETE/TRUNCATE append-only 表；
- downgrade 在任一 authority 表非空时失败关闭，只允许空表回滚；不得以 drop canonical history 的方式伪造可逆；
- 新增 contract 与 migration 静态/捕获 SQL 测试，覆盖 aware time、exact ref、成员多重集合守恒、拆并 predecessor/successor、SLA pause/resume、kill 三检查点语义、跨租户 hash 绑定、single head、RLS/FORCE RLS、append-only 与非空 downgrade guard；
- 本子波不新增 API、Store、SDK、页面，不执行 migration、不写真实数据。A1 GREEN 后进入 A2 Store：expectedVersion、同 key 同 payload replay、同 key 异 payload冲突、乱序/重复 original 去重与 projection rebuild；A1/A2 合并验证后才形成 `W3_12A_OPERATION_CASE_AUTHORITY_GREEN` Receipt。

文件范围固定为：

- `services/aos-api/aos_api/ecommerce_operation_case_contracts.py`
- `services/aos-api/alembic/versions/w3_012_operation_case_authority.py`
- `services/aos-api/tests/test_ecommerce_operation_case_contracts.py`
- `services/aos-api/tests/test_w3_012_operation_case_migration.py`

迁移 Lease 仅覆盖上述 migration 文件与测试，不授权执行 upgrade、写入真实租户或发布。

#### 3.3.2 W3-12A2 authority Store

A2 新增 `ecommerce_operation_case_store.py` 与 `test_ecommerce_operation_case_store.py`，首个安全闭环只开放内部 Python Store，不注册 router。Store 固定使用服务端 `TenantScope`，所有 publish/create/append 请求先计算 canonical request hash，再按 `(org_id, project_id, operation, idempotency_key)` 查 Receipt：同 key 同 payload 返回 exact result ref，同 key 异 payload失败关闭。

第一提交实现 AggregationPolicy publish/get 与 OperationCase create/get：head 行 `FOR UPDATE`，`expectedVersion=0` 仅允许首次创建，后续 revision 必须严格递增；Case 成员只接收同租户 exact originals，去重后校验 `attached + unmatched + conflicted = original total`，不保存 original payload。第二提交追加 classification、CaseEvent、membership、SLA 与 kill Decision；任何旧/乱序/重复 original 不得重复成员或 CaseEvent sequence，拆并必须通过合同层的 predecessor/successor 和多重集合守恒。

测试使用 fake tenant connection，不连接真实数据库，覆盖：正向 `org-org/dev-project`、负向 `dev-org/dev-project` 参数独立；expectedVersion 冲突；同 key replay；同 key 异 payload冲突；跨租户 original 拒绝；重复 member 拒绝；Receipt 不含 PII、Secret、支付、地址或 Provider payload。文件范围固定为：

- `services/aos-api/aos_api/ecommerce_operation_case_store.py`
- `services/aos-api/tests/test_ecommerce_operation_case_store.py`

A2 不执行 migration、不新增 API/页面、不写真实业务数据；Store 与 A1 累计 GREEN 后才允许签发 W3-12A exact authority Receipt。

#### 3.3.3 W2-01B1 OperationCase slice 消费

W3-12A exact code/control Receipt 到位后，W2-01B 首提交只关闭 OperationCase authority 缺口：

- 在 `ecommerce_operation_case_store.py` 增加 tenant-bound、`REPEATABLE READ READ ONLY`、bounded current-head reader，返回 strict `OperationCaseRevision` exact refs；不执行 migration、不创建 Case；
- `ecommerce_workshop_operations.py` 通过依赖注入消费该 reader；有 canonical Case 时 OperationCase slice 为 `ready`，无 Case 时仍是合法空 `ready`，但 reader/表不可用、hash 漂移或 scope 错误必须结构化 `blocked`；
- `ecommerce_workshop_operations_contracts.py` 放宽 W2-01A 的全零 shell 限制，使 page/count 由七切片 count ledger 推导，禁止客户端 synthetic cursor；其余 orders/orderLines/inventory/shipments/payments/aftersaleEvents 在各自 reader 接入前继续诚实 blocked；
- 测试覆盖正向 tenant、负向 canary、空 authority、Case exact ref/count、reader failure、scope 注入拒绝和七切片顺序。页面数据仍未接入，因此本提交不做浏览器正向完成声明。

文件范围：`ecommerce_operation_case_store.py`、`ecommerce_workshop_operations.py`、`ecommerce_workshop_operations_contracts.py` 及三者现有测试。完成 B1 后继续 B2 订单/订单行/库存/履约/支付只读 reader 组合；售后原始事件在 canonical source 缺失时保持 blocked，不制造事件。

#### 3.3.4 W2-01B2 transaction 与 Inventory slices

新增 `ecommerce_operations_object_reader.py` 和测试，从同租户 `ecom_object` 只读取 Order、OrderLine、Shipment、Payment 的 `external_id/object_type/source_updated_at/payload_hash`，固定 `REPEATABLE READ READ ONLY`、cutoff、确定性排序和每类上限；绝不读取或返回 properties、地址、支付、客户、Provider payload。Inventory 复用已 GREEN 的 `EcommerceInventoryReader`，不得另建库存真源。

`ecommerce_workshop_operations.py` 通过构造器注入两个 reader，将 orders/orderLines/inventory/shipments/payments 转换为 exact authority refs 与 count ledger；reader 成功且为空是合法 `ready`，reader 错误是结构化 `blocked`。OrderLine join 守恒在后续组合 reader 中显式记录 unmatched/conflicted，当前 exact-ref 子波不得用 `0` 假装已校验 join。afterSalesEvents 继续 blocked，OperationCases 保持 B1 行为。

文件范围：新 reader 与测试、`ecommerce_workshop_operations.py`、`ecommerce_workshop_operations_contracts.py` 及其测试。只做 fake-connection 与 API contract 验证，不探测真实业务库、不新增 mutation、页面或外部副作用。

#### 3.3.5 W3-12B1 command readiness 与视觉动作抽屉

W2-01B 七切片 strict Web 已 GREEN 后，W3-12B 先交付一个不产生业务写入的 command-readiness 子波，避免把视觉稿中的“批准退款”“一键采纳”等示例按钮直接变成无门槛副作用：

- `ecommerce_operation_command_contracts.py`：新增 strict command descriptor、风险级别、可用状态与 blocker 模型；固定 `classify`、`createCase`、`changeMembership`、`manageSla`、`automationKill`、`refund` 六项 canonical command。未具备 exact Proposal/Approval/ExecutionLease/Receipt 链的命令必须 `blocked`，不得用前端角色或按钮状态推断授权；
- `ecommerce_operation_commands.py`：只读解析 Principal tenant、模块安装、W3-12A authority code/control 与命令依赖，返回确定性 command-readiness；本子波不得调用 Store mutation、不得创建 Policy/Case/Decision、不得调用 Adapter 或 Provider；
- `routers/ecommerce_workshop.py`：新增 GET-only `/v1/ecommerce-workshop/commands/operations/readiness`，拒绝 query/body scope 注入并保持安装可见性门；
- `apps/web/src/api/ecommerceWorkshop/{contracts,parser,client,index}.ts`：加入唯一 strict SDK，拒绝 extra/missing、错误 command 顺序、未知 blocker、租户漂移和 false-ready；
- `apps/web/src/components/workshop/OperationsPage.tsx` 与现有样式/测试：对照正式视觉稿右栏增加“AI/动作建议”抽屉，但只显示服务端 readiness、exact blocker 与后续门，所有命令默认禁用；不得复制视觉稿中的客户姓名、订单号、金额、退款建议、GMV 或“客服自动处理已开启”等示例事实；
- 浏览器至少覆盖 1280/1440/1920、七切片选择、右栏抽屉、键盘 focus、0 可执行副作用控件、0 水平溢出、0 console error。fixture 仅证明视觉/交互，真实 API 不可用时继续标记 operational unavailable。

本子波退出后进入 W3-12B2：在独立命令方案中接入内部 authority mutation 与 canonical Proposal→Approval→ExecutionLease→Receipt；先写失败测试，再按 classify/create Case、membership/SLA、kill、外部 Action 分段实现。任何真实调用、真实数据库写入、migration apply、退款/改址/催发货/通知仍须独立运行门，不能由 B1 的 readiness/UI GREEN 代替。

W3-12B1 已由 `m1@a4b3479` 完成：后端专项与累计 `27 passed`，Web 累计 `205 files / 2012 tests`，TypeScript、production build、diff check GREEN；内置浏览器在 1280/1440/1920 三档验证七切片、六命令全部失败关闭、键盘可达与零水平溢出。该浏览器证据来自受控只读 fixture，只证明页面视觉/交互，不证明真实运行时或任何副作用可执行。Delivery Receipt 已推进至 `AOS-000168` 并同步三份 Prime 强一致投影；96 项主 Task 计数仍保持 `22/96`。

#### 3.3.6 W3-12B2a 内部 classify/createCase 命令执行门

B2 先拆出不依赖外部 Provider 的 `classify` 与 `createCase` 两项内部 authority 命令。即使当前为唯一开发者，也不得把“内部写入”降级为无治理写入；本子波固定采用服务端 Principal tenant、exact Proposal/Approval/ExecutionLease、`Idempotency-Key`、expected authority revision 与 Operation authority Receipt 的双重校验。

文件级施工范围：

- 新增 `services/aos-api/aos_api/ecommerce_operation_command_execution_contracts.py`：定义 strict 命令请求、治理链引用、classify/createCase payload、成功 Receipt envelope 与稳定错误；请求模型禁止 `orgId/projectId/actorId`，仅接受 exact resource/version/hash/ref；
- 新增 `services/aos-api/aos_api/ecommerce_operation_command_service.py`：先调用只读 canonical governance verifier，核对同租户 Proposal 已 approved、审批 quorum 有效、Lease active/未过期且 owner 为当前 Principal、proposal hash/action type/object ref 与请求完全一致；校验通过后才调用现有 `OperationAuthorityStore.append_classification` 或 `create_case`，返回 exact `OperationAuthorityReceipt`；
- 修改 `services/aos-api/aos_api/routers/ecommerce_workshop.py`：增加两条显式 POST command endpoint，强制 `Idempotency-Key`，tenant 只取 Principal，并将版本/幂等/治理链/依赖错误映射为稳定 HTTP 错误；GET readiness 继续诚实反映“handler 已绑定但每次执行仍需 exact chain”，不得把存在 endpoint 表述为任意请求 ready；
- 修改 `scripts/export_openapi.py` 与 `services/aos-api/tests/test_openapi_contract.py` 的受控 route/path/schema 总数，并确定性重生 `packages/contracts/openapi/v1.generated.json` 与 `v1.inventory.json`；补齐此前尚未进入冻结产物的 Operations view/readiness 两条 GET 与本子波两条显式 POST，共四条可解释差量，重复路由集合不得变化；
- 修改 `services/aos-api/aos_api/ecommerce_operation_commands.py` 与 contracts：只把 handler 绑定事实从 blocker 中移除，命令执行资格仍按请求级 Proposal/Approval/Lease 动态裁决；页面在没有 exact chain 前保持禁用；
- 新增 `services/aos-api/tests/test_ecommerce_operation_command_service.py`，扩展 `test_ecommerce_workshop_operations_api.py` 与 readiness 测试：覆盖正向 fake authority、跨租户、body scope 注入、maker/owner 漂移、过期或已消费 Lease、proposal/action/payload/hash 漂移、expectedVersion 冲突、幂等重放与幂等冲突；
- 本子波不改 Web 为可执行态，不执行真实数据库写入，不创建真实 Proposal/Approval/Lease，不应用 migration，不调用外部 Action。页面浏览器回归仍需证明六按钮失败关闭、视觉稿信息层级未回退、零示例业务事实与零 console error。

B2a 完成后自动进入 B2b membership/SLA；复用同一治理 verifier 与 command envelope，不另造 Proposal、Approval、Lease 或 Receipt authority。B3 再处理 automation kill 的 Proposal/Lease/executor checkpoint 专项预检；refund 等外部动作延后到 W5 canonical Action/Adapter 波次，当前保持 blocked。

W3-12B2a 已由 `m1@45f938f` 完成代码控制闭环：`classify/createCase` 两条内部命令统一经过 Principal tenant、strict request、exact Proposal/Approval/ExecutionLease、`Idempotency-Key`、expectedVersion、canonical AIP Action Receipt 与 Operation authority Receipt，幂等重放返回原 Receipt、漂移请求失败关闭。累计后端 `56 passed`、OpenAPI deterministic check、Web `205 files / 2012 tests`、production build 与 diff check GREEN；内置浏览器在 1280/1440/1920 三档确认七切片、六命令仍全部禁用且零水平溢出。浏览器 fixture 只证明视觉与失败关闭，未执行真实命令、数据库写入或外部副作用。96 项主 Task 计数仍为 `22/96`。

#### 3.3.7 W3-12B2b membership/SLA 内部命令执行门

B2b 复用 B2a 唯一的 canonical governance verifier 与 Action execution/Receipt 链，只增加 `changeMembership` 与 `manageSla` 的 typed payload 和内部 Operation authority adapter；不得复制一套 Proposal、Approval、Lease、幂等或 Receipt authority。

文件级施工范围：

- 扩展 `services/aos-api/aos_api/ecommerce_operation_command_execution_contracts.py`：加入 strict membership revision 与 SLA clock decision 请求；禁止 body scope，要求 resource 当前版本精确递增，新建 SLA clock 仅接受 expectedVersion=0，并把 action payload 规范化为稳定 canonical JSON；
- 扩展 `services/aos-api/aos_api/ecommerce_operation_command_service.py`：在现有 `_InternalOperationAdapter` 内接入 `OperationAuthorityStore.append_membership` 与 `append_sla_clock`，继续将 exact Operation authority Receipt 嵌入 canonical AIP Action Receipt；任何 unknown、timeout 或 Receipt 不一致均失败关闭且不自动重试；
- 扩展 `services/aos-api/aos_api/routers/ecommerce_workshop.py`：增加两条显式 POST endpoint，复用 Principal tenant、安装门、`Idempotency-Key` 与稳定 409/503 映射；不提供通用任意 action endpoint；
- 更新 `services/aos-api/aos_api/ecommerce_operation_commands.py`：四项内部 handler 均已绑定，但 readiness 仍返回 `EXACT_ACTION_CHAIN_REQUIRED`，`automationKill/refund` 继续保持各自未绑定或外部动作 blocker；
- 扩展专项 API/service/store/OpenAPI 测试，覆盖 membership/SLA 正向 fake authority、跨租户、版本漂移、action/payload/hash 漂移、过期/已消费 Lease、同键重放与异键冲突；确定性重生 OpenAPI 与 inventory，重复路由集合不得变化；
- Web 本波仍不接收 Proposal/Lease 输入，不切换按钮为可执行；浏览器三档回归继续对照正式视觉稿验证七切片、证据抽屉、六命令失败关闭、零示例业务事实与零水平溢出。

B2b 退出后自动进入 B3 automation kill 专项预检与执行门。真实 automation kill、外部 refund、真实数据库写入、migration apply 或 Provider 调用均不属于本波。

W3-12B2b 已由 `m1@b6cdf25` 完成代码控制闭环：`changeMembership/manageSla` 复用 B2a 的唯一 canonical verifier、Principal tenant、exact Proposal/Approval/ExecutionLease、expectedVersion、`Idempotency-Key` 与 Action/Operation 双 Receipt，canonical adapter fake path 已验证 membership/SLA authority Store 路由。累计后端 `65 passed`，Web `205 files / 2012 tests` 与 production build、OpenAPI deterministic、compile/diff check GREEN；内置浏览器 1280/1440/1920 均保持七切片、六命令禁用、零水平溢出和零示例业务事实。fixture 的 aos-api unavailable warning 是受控降级证据，不是运行时可执行证明。96 项主 Task 计数仍为 `22/96`。

#### 3.3.8 W3-12B3 automation kill 高风险命令门

B3 只处理内部 `automationKill` authority decision，不处理退款或 Provider 动作。该命令风险高于 B2a/B2b，除复用 canonical Proposal/Approval/ExecutionLease/Receipt 外，还必须保持既有 `AutomationKillDecisionRevision` 的 proposal、lease、executor 三 checkpoint 齐全且唯一，并将 exact `scopeHash` 固化在 Proposal payload、Lease proposalHash、Action Receipt 与 Operation authority Receipt 的证据链中。

文件级施工范围：

- 扩展 `ecommerce_operation_command_execution_contracts.py`：新增 strict `KillOperationAutomationCommandRequest`，要求 revision 精确推进 expectedVersion 一次；依赖既有 contract 验证三个 checkpoint 齐全、唯一，禁止 body scope/actor 注入；
- 扩展 `ecommerce_operation_command_service.py`：在唯一 `_InternalOperationAdapter` 增加 `append_kill` 路由，使用独立 Action Type `ecommerce.operation.automation-kill`；tenant/actor、proposal payload/hash/version、审批 refs、Lease owner/status/expiry/hash、幂等键和双 Receipt 任一漂移均失败关闭；unknown 不自动重试；
- 扩展 `routers/ecommerce_workshop.py`：只增加显式 `/commands/operations/automation-kill` POST，不增加任意 command dispatch；继续复用安装门、Principal、`Idempotency-Key` 和稳定 409/503；
- 更新 readiness：仅把 automationKill 的静态 handler blocker 改为请求级 exact chain blocker，状态仍是 `blocked`；refund 保持 `EXTERNAL_ACTION_GATE_NOT_BOUND`；
- 扩展 service/API/readiness/OpenAPI 测试，覆盖缺 checkpoint、重复 checkpoint、版本漂移、tenant/actor/payload/hash/approval/Lease 漂移、同键重放与异键冲突、canonical adapter/Operation Receipt；确定性重生 OpenAPI；
- Web 不接收高风险治理凭据、不放开 automationKill 按钮；内置浏览器三档继续对照正式视觉稿验证动作抽屉信息层级、六命令全禁用、零示例业务事实、零水平溢出。真实 kill、数据库写入、migration apply、退款与 Provider 调用全部禁止。

B3 退出后自动进入 W3-12B4 command observability/unknown reconcile 读模型与前端证据呈现；外部 refund 继续留在 W5 canonical Action/Adapter 波次。

W3-12B3 已由 `m1@b71fb65` 完成代码控制闭环：automationKill 使用独立 typed request、三个 checkpoint 强校验、exact scopeHash、Principal tenant/actor、canonical Proposal/Approval/ExecutionLease、expectedVersion、幂等键和 Action/Operation 双 Receipt；canonical fake adapter 已验证 `append_kill` 路由。累计后端 `71 passed`，Web `205 files / 2012 tests`、production build、OpenAPI deterministic、diff check GREEN；内置浏览器三档保持七切片、六命令全禁用、零水平溢出和零示例事实。未执行真实 kill、数据库写入或外部动作，refund 仍失败关闭。96 项主 Task 计数保持 `22/96`。

#### 3.3.9 W3-12B4 command observability 与 unknown 只读对账

B4 不新增副作用命令，先把既有 canonical Action Receipt 与 Operation authority Receipt 的只读状态组合为请求级证据视图：明确 `applied/failed/unknown`、proposal/lease/receipt refs、幂等键 hash 和下一步；unknown 只能读后对账，不自动重放。

文件级范围：新增 strict command execution observation contract/store/service 与 GET endpoint；只按 Principal tenant 和 exact proposal/lease ref 查询，拒绝 scope 注入；Web 动作抽屉只展示服务端证据摘要、归因路径、关键假设和不确定性，不展示或收集 secret/PII，不提供 replay 按钮；补齐 service/API/parser/component 测试、OpenAPI、三档视觉与键盘验收。B4 完成后再评估 W3-12 主项闭合条件，refund 仍进入 W5。

2026-08-24 闭合检查点：后端只读 observation 已在 `m1@7d0d63f`，Web strict SDK 与证据抽屉已在 `m1@2b9a8a8` 形成安全提交。Web 累计 `205 files / 2016 tests`、production build `319 modules`；后端本波精确组合 `35 passed`，OpenAPI deterministic export GREEN。内置浏览器已完成 1280/1440/1920 三档复核：七个权威切片完整、六个动作全部禁用、请求级 Proposal/Lease 表单可交互、失败返回 `INVALID_ERROR_RESPONSE` 并明确不重放或补偿、三档均无水平溢出，且未出现客户、批准退款或自动处理等示例事实。浏览器 fixture 只证明视觉与失败关闭；`applied/failed/unknown` 的语义由 strict parser/component/API 测试证明，不提升为真实执行事实。B4 可进入 Receipt/CAS/Prime 闭环，refund 仍留在 W5。

### 3.4 S2 / W2-02A exact Stage compilation 只读切片

W3-12B4 闭合后独立审查正式 96 项清单：W3-12 仍依赖 W3-10、W2-01 主项与真实 runtime/recovery 轴，W2-01 仍缺 aftersale event originals 与 timeline，因此两项均不提前勾选，主进度保持 `22/96`。下一实际代码波进入 W2-02 的第一个缺口，不等待其他开发者，也不复制第二套 Stage authority。

本子波复用 canonical `aip_task_run.plan_revision_id → aip_plan_revision.risk.productionContract`，新增 run-scoped `production-context` GET 只读投影：

- `ecommerce_workshop_task_cockpit_contracts.py`：新增 exact ref、Stage compilation item 与 production context envelope；只接受 `StageTemplateRevision`、`ResponsibilityPlanRevision`、`PlanRevision` 三类 exact ref，hash 为 64 位小写 SHA-256，stage id 唯一，`applicable/not_applicable` 显式分离；
- `ecommerce_workshop_task_cockpit.py`：在 `REPEATABLE READ READ ONLY` 与 transaction-local tenant scope 中按 exact run/plan 读取 `steps/risk`，核对 Plan ref、StageTemplate ref、ResponsibilityPlan ref、compiler version 和 stage/step 数量守恒；缺失、旧格式、hash/type/step 漂移均结构化失败关闭，不回退为静态阶段；
- `routers/ecommerce_workshop.py` 与 OpenAPI：新增唯一 GET `/views/task-cockpit/runs/{run_id}/production-context`，拒绝 body/query scope 注入并复用安装可见性门；
- Web strict SDK/parser 与 `TaskCockpitPage.tsx`：展开 Run 时与 Step/Checkpoint 并行读取 Stage compilation，只显示 exact template/plan、适用性与阶段映射；保留正式视觉稿的“执行组—当日任务流—策划组—复盘”层级，不复制视觉稿中的任务数、六角色在线状态或经营样例；
- 测试覆盖正向 exact mapping、跨租户、run/plan 不存在、risk 缺失、hash/type/compiler/stage-step 漂移、extra/missing Web 字段、明细任一失败整块失败关闭、三档视口、键盘展开、零水平溢出与 console；不新增 migration、不写真实数据、不启动 TaskRun、不执行 Action。

W2-02A 只关闭 exact Stage compilation 缺口；Responsibility/Handoff/Approval/ReviewIssue/Action reconcile 仍按后续子波逐项消费 canonical owner，不以本波页面 GREEN 代替 W2-02 主项完成。

2026-08-24 闭合检查点：代码已以 `m1@f47fb71` 安全提交；后端专项 `15 passed`、累计组合 `28 passed`，Web 累计 `205 files / 2016 tests`、production build `319 modules`，OpenAPI 确定性导出与检查通过。内置浏览器 1280/1440/1920 三档均显示 exact Plan/StageTemplate/ResponsibilityPlan ref、Stage 适用性、依赖与槽位，无水平溢出或禁止命令，console error 为 0。Delivery Receipt 为 `w2-02a-exact-stage-compilation-read-model-20260824`，authority/Prime 已经 `AOS-000174` 精确回读。`ruff` 可执行文件在环境中不可用，未虚构 lint GREEN；语法与行为由上述专项及累计测试覆盖。

### 3.5 S2 / W2-02B Responsibility/Handoff 精确只读切片

本子波消费 W2-02A 已校验的 `ResponsibilityPlanRevision` exact ref，并按同一 TaskRun 读取 canonical Handoff envelope/decision；不新建第二套职责、交接或 owner authority：

- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit_contracts.py`：新增职责槽位、结构 assignee、Handoff envelope 摘要、decision timeline 和 run-scoped envelope；将 ResponsibilityPlan contract readiness 与 assignee operational readiness 分开，未有 `AssigneeResolutionReceipt` 时固定为 `unverified`；
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`：在单一 `REPEATABLE READ READ ONLY` 事务内重新校验 run→Plan→Responsibility exact 链，再用 tenant + run id 读取 Handoff envelope 及按 revision 排序的 decision；仅返回最小摘要，不泄露 bearer/token/context payload/object/artifact/evidence 内容；
- `services/aos-api/aos_api/routers/ecommerce_workshop.py` 与 OpenAPI：新增唯一 GET `/views/task-cockpit/runs/{run_id}/responsibility-handoffs`，复用安装可见性与 principal tenant，不接受 body/query 注入；
- `apps/web/src/api/ecommerceWorkshop/*`：增加 strict contract/parser/client，extra/missing/type/hash/timeline 漂移全部失败关闭；
- `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与 `apps/web/src/styles/45-ecommerce-workshop.css`：在正式视觉稿的“执行组/策划组”边界内展示职责槽位、结构 assignee 与交接决定链；明示“运行就绪未验证”，不复制六个在线数字同事或经营样例，不新增消费/决策命令；
- 测试覆盖 exact hash/lifecycle/tenant/run 归属、slot 唯一与 required-slot 覆盖、Handoff/decision 数量守恒与顺序、最小披露、空 Handoff、跨租户/404/409/503、Web 整块失败关闭、键盘与 1280/1440/1920 零溢出。

本子波不把 ResponsibilityPlan 的 `ready` 冒充为 selected assignee operational readiness，也不把 Handoff `consumed` 冒充为业务 `accepted`或 owner 已变更。Approval/ReviewIssue/Action reconcile 仍属 W2-02 后续子波。

2026-08-24 闭合检查点：代码已以 `m1@f1f38db` 安全提交；后端专项 `18 passed`、累计与 OpenAPI `31 passed`，Web 累计 `205 files / 2016 tests`、production build `319 modules`，OpenAPI 确定性导出与检查通过。内置浏览器在 1280/1440/1920 三档确认 exact ResponsibilityPlan、职责槽位、结构 assignee、Handoff 与 decision timeline，无横向溢出或命令入口；刷新前后 error log 均为 4 条历史热更新错误，本次新增为 0。正式视觉稿已逐区对照“指标—指令区—执行组—任务流—策划组—复盘”层次，经营样例、在线角色与“下达”按钮未复制。Delivery Receipt 为 `w2-02b-responsibility-handoff-read-model-20260824`；下一子波为 `W2-02C Approval/ReviewIssue exact read model`，主清单仍不提前勾选 W2-02。

### 3.6 S2 / W2-02C Approval／ReviewIssue 精确只读切片

本子波只组合既有 Plan、ActionProposal/ApprovalEvent、Artifact、ReviewIssue/Event 与 ReturnDecision authority，不新建审批、问题、返工或导航 authority。Run 已存在时，其 Plan 审批只作历史事实回读；Action 审批导航只返回服务端固定 route identity、exact target、目的页重新鉴权要求与 return-focus token，打开目的页不等于批准，批准也不等于 Action applied。

文件级施工范围：

- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit_contracts.py`：新增 Plan approval、Action approval timeline、ApprovalNavigationTarget、ReviewIssue timeline/lineage 与 run-scoped envelope；数量、事件顺序、proposal hash/version、artifact hash、return stage 与 attempt 关联必须守恒；
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`：在单一 `REPEATABLE READ READ ONLY` tenant 事务内读取 Run→Task→Plan、同 Run ActionProposal→ApprovalEvent、同 Run Artifact→ReviewIssue/Event→ReturnDecision；ReviewIssue 仅允许通过 `artifact.run_id` 精确归属，ReturnDecision 必须再次匹配同 Run、Stage 与 StepRun attempt。没有 ReturnDecision 的 open issue 明示 `attempt_unresolved`，不得按标题、时间或“最新”猜 attempt；
- `services/aos-api/aos_api/routers/ecommerce_workshop.py` 与 OpenAPI：新增唯一 GET `/views/task-cockpit/runs/{run_id}/approval-review-issues`，只取 Principal tenant、拒绝 query/body scope 注入、复用模块安装门；
- `apps/web/src/api/ecommerceWorkshop/*`：增加 strict contract/parser/client，extra/missing、未知枚举、非连续事件、hash/version/数量漂移均失败关闭；
- `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与既有样式：在 Run 明细中展示 Plan 审批事实、Action 审批决定链、导航 readiness 与 ReviewIssue 证据/返工 lineage；本波不提供 approve/resolve/return/apply 按钮，不使用示例审批、问题或人员数据；
- 后端、API、Web 测试覆盖 exact 正向、空集合、open issue attempt 未解析、returned issue exact attempt、跨 Run/tenant、hash/version/event/step drift、404/409/503、明细整块失败关闭；页面继续做 1280/1440/1920、键盘展开、零横向溢出、零新增 console error，并逐区对照正式视觉稿层级。

禁止项：不新增 migration，不修改真实业务数据，不执行 Plan/Action Approval，不 resolve/return ReviewIssue，不创建新 attempt，不应用 Action，不把 Plan approved 表述为 ProductionStart，也不把 Action approved 表述为 applied。W2-02C 完成后自动进入 W2-02D Task-scoped Action receipt/unknown/reconcile 只读聚合；W2-02 主项在剩余轴闭合前不提前计数。

2026-08-24 闭合检查点：代码已以 `m1@68ccb10` 安全提交；后端专项 `21 passed`、累计与 OpenAPI `39 passed`，Web 专项 `37 passed`、累计 `205 files / 2016 tests`、typecheck 与 production build `319 modules`，OpenAPI 确定性导出与检查通过。内置浏览器在 1280/1440/1920 三档确认 exact Plan approval、Action approval timeline/navigation readiness、ReviewIssue 证据与返工 lineage，无横向溢出；审批区按钮和链接均为 0，旧的 Approval/ReviewIssue blocker 已消失，新的 assignee operational-readiness blocker 正确保留，且本次没有新增 console error。正式视觉稿已逐区对照“顶部指标—三路任务流—右侧复核—底部共享能力”层次，没有复制经营样例、在线角色或命令入口。Delivery Receipt 为 `w2-02c-approval-review-issue-read-model-20260824`；authority 与 Prime 已推进到 `AOS-000176` 且强一致投影 CURRENT。下一子波为 `W2-02D Task-scoped Action receipt/unknown/reconcile read model`，主清单仍保持 `22/96`，不提前勾选 W2-02。

### 3.7 S2 / W2-02D Action Receipt／unknown／reconcile 精确只读切片

本子波只组合既有 `aip_action_proposal`、`aip_action_execution_lease` 与 append-only `aip_action_receipt` authority，不执行 Action，不调用 Provider，不发起 reconcile 或 compensation。Cockpit 以当前 Run 的 exact `task_id + run_id` 双引用筛选 Proposal；存在同 Run、不同 Task 的 Proposal 时视为 authority drift 并失败关闭，不按时间、ActionType 或“最新”猜归属。

文件级施工范围：

- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit_contracts.py`：新增安全的 Proposal/Lease/Receipt chain 与 run envelope；保留 `accepted/applied/failed/unknown/reconciled`，区分 initial 与 reconcile Receipt，并对 Proposal、Lease、attempt、supersedes、request fingerprint、数量和 unresolved unknown 守恒；
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`：在单一 `REPEATABLE READ READ ONLY` tenant 事务内读取 Run→Task、同 Task+Run Proposal、同 Proposal Lease 与 Receipt；`unknown` 只有在没有 exact superseding reconcile Receipt 时才是 `reconcile_required`，reconcile Receipt 必须指向同 Proposal、同 Lease、同 fingerprint 的 initial unknown；
- `services/aos-api/aos_api/routers/ecommerce_workshop.py` 与 OpenAPI：新增唯一 GET `/views/task-cockpit/runs/{run_id}/action-receipts`，只取 Principal tenant、拒绝 query/body scope 注入、复用 Module 安装门；
- `apps/web/src/api/ecommerceWorkshop/*`：增加 strict contract/parser/client；extra/missing、未知枚举、Task/Run/Proposal/Lease/Receipt 错链、错误 supersedes、数量漂移均失败关闭；
- `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与既有样式：在 Run 明细中展示 Proposal 状态、attempt、最小 Receipt timeline、unknown 待对账与已对账结果；provider request id 仅投影为 `present/missing`，不返回真实 ID、payload 或证据正文；本波没有 execute/reconcile/retry/compensate 按钮；
- 后端、API、Web 测试覆盖无 Action、无 Lease/Receipt、accepted/applied/failed、unresolved unknown、resolved unknown、跨 Task/Run/tenant、supersedes/fingerprint/attempt drift、404/409/503、整块失败关闭，并执行累计回归、OpenAPI 确定性检查、build 与 1280/1440/1920 浏览器验收。

禁止项：不新增 migration，不修改真实业务数据，不读取或展示 Action payload、provider request id、PII/Secret，不把 accepted/approved/Task succeeded 当成 applied，不把 unknown 当 failed，不自动重试外部副作用，不发起 reconcile 或 compensation。对账只由新的 immutable Receipt 证明；补偿仍是新的受控 Proposal。W2-02D 闭合后再依据 W2-02 主项的剩余 assignee/business-context 边界更新清单，不能为追求计数提前去除真实 blocker。

2026-08-24 闭合检查点：代码已以 `m1@c2cd471` 安全提交；后端累计 `42 passed`，Web 专项 parser/client/page `34 passed`、Host `3 passed`、累计 `205 files / 2016 tests`，typecheck、production build `319 modules`、OpenAPI 确定性导出与检查、diff check 均通过；锁定环境未提供 Ruff，因此未虚构 Ruff 结论。内置浏览器在 1280/1440/1920 三档确认 Action Proposal/Lease/Receipt 精确链、unknown 待对账语义与 provider ref 封存态，无 execute/reconcile/retry/compensate 命令、无横向溢出；正式视觉稿已逐区对照任务流主层与证据辅层，没有复制经营样例、在线角色或命令入口。Delivery Receipt 为 `w2-02d-action-receipt-unknown-reconcile-read-model-20260824`；authority 与 Prime 已推进到 `AOS-000177` 且强一致投影 CURRENT。96 项主计数仍为 `22/96`，W2-02D 是真实子波进度但不提前勾选 W2-02；下一子波立即进入 `W2-02E Assignee operational-readiness read model`。

### 3.8 S2 / W2-02E Assignee Resolution 观测就绪只读切片

本子波消费 W-L20 已有 append-only `AssigneeResolutionReceipt`，不重新执行 resolver、不创建 Receipt、不推断租户全局 Binding。为避免同一 assignee 在别的任务或职责槽上的 Receipt 误点亮当前 Run，唯一 subject identity 冻结为 `responsibility-plan:{planId}@{revision}/slot:{slotId}`；读取时还必须同时匹配 tenant、kind、resourceId 与 version。缺 Receipt、subject 不匹配、assignee 漂移或同一观测时刻出现冲突状态均失败关闭。

当前 W-L20 Receipt 只有 `createdAt`，没有目标 ADR 要求的 `observedAt/expiry/policy/health/capacity` 全快照，因此页面只能诚实展示 `resolved_at_observation / blocked_at_observation / unverified`，不得将历史 `resolved` 表述为“当前可执行”或 `ready`。本波关闭的是 exact reader 与可审计呈现，不修改 migration，也不扩大运行授权。

文件级施工范围：

- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit_contracts.py`：为结构 assignee 增加只读观测状态与最小 Receipt summary；Receipt 仅返回 receipt/subject/status/blocker/contentHash/createdAt，不返回 actor、resolvedRef、Binding/Provider 内部标识或 payload；
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`：在既有 Responsibility/Handoff 的单一 `REPEATABLE READ READ ONLY` tenant 事务中，按所有 exact slot subject 一次读取 append-only Receipt；校验 subject、kind/resource/version、状态与 blocker 守恒，按 `createdAt + receiptId` 返回确定性时间线；同一最大 createdAt 的冲突状态报 409，不按任意行选“最新”；
- `apps/web/src/api/ecommerceWorkshop/{contracts,parser}.ts`：严格解析三种观测状态与 Receipt timeline，拒绝 extra/missing、subject/assignee 错链、状态映射、时间线/数量漂移；
- `apps/web/src/components/workshop/TaskCockpitPage.tsx` 与既有样式：职责槽展示“观测时已解析／观测时阻断／未验证”、Receipt 时间与 reasonCodes，并固定提示“无 expiry，不代表当前 ready”；无 resolve/reassign/takeover/refresh-authority 命令；
- 后端、API、Web 测试覆盖无 Receipt、resolved/blocked、历史状态演进、同刻冲突、跨 subject/kind/resource/version/tenant、actor/resolvedRef 不泄露、403/404/409/503 与整块失败关闭；完成累计回归、OpenAPI deterministic、build、正式视觉稿逐区复审和 1280/1440/1920 浏览器验收。

禁止项：不新增或执行 migration，不修改真实业务数据，不调用 POST resolver，不把 Responsibility coverage、Handoff consumed 或历史 resolved Receipt 冒充当前 runnable，不显示 actor/resolvedRef/Binding/Provider 私有信息，不启用改派或接管。W2-02E 闭合后自动进入 W2-02F business-context enrichment；若真实 SourceReadiness 仍不足，则先实现诚实 SourceReadiness/unknown 读模型所需的系统缺口，不等待其他开发者。

2026-08-24 闭合检查点：代码已以 `m1@221b429` 安全提交；后端累计 `40 passed`，Web 专项 `38 passed`、累计 `205 files / 2017 tests`，production build `319 modules`、OpenAPI 确定性导出/检查与 diff check 均通过。实现只消费既有 append-only `AssigneeResolutionReceipt`，按 tenant + exact subject + kind/resource/version 约束槽位，冲突观测与漂移失败关闭；响应不返回 actor/resolvedRef，也没有 resolver POST、改派、接管、执行或发布命令。内置浏览器在 1280/1440/1920 三档确认“观测时已解析／观测时阻断／无 expiry 不代表当前 ready”与 blocker reason，三档零横向溢出、当前重载后 console error 为 0；正式视觉稿已复审任务流主轴、职责和复盘分区，没有复制 GMV、在线人数或样例任务。Delivery Receipt 为 `w2-02e-assignee-operational-readiness-read-model-20260824`；authority 与 Prime 已推进到 `AOS-000178`，强一致投影 CURRENT，memory validate/gate GREEN。96 项主计数仍为 `22/96`；下一子波立即进入 `W2-02F SourceReadiness business-context read model`。

### 3.9 S2 / W2-02F SourceReadiness 业务上下文共享快照

复核 `28` 号 W2 readiness 方案、`83/105` 号 W2-02 ADR、`114` 号 blocked-state UI ADR 与当前代码后确认：canonical `SourceReadinessEnvelope` owner、Principal-scoped Workshop facade、strict Web parser/client 和 Shell 面板均已存在。本子波不新增第二 API、不复制 P01～P12 计算，也不把 SourceReadiness 嵌入 Task 数据库事务；Task cutoff 与 SourceReadiness cutoff 是两个独立快照，必须分别展示。当前 envelope 若为 blocked 或 `receiptRef=null`，只能作为失败关闭的业务上下文，不能升级为 operational GREEN。

文件级施工范围：

- `apps/web/src/components/workshop/SourceReadinessContext.tsx`：新增 Shell 内共享的易失只读 Provider，唯一发起 canonical `getSourceReadiness()`，绑定当前 tenant，保留 loading/forbidden/failed/ready 与显式 reload；不缓存到 localStorage，不持久第二 authority；
- `apps/web/src/components/workshop/SourceReadinessPanel.tsx`、`EcommerceWorkshopShell.tsx` 与 `index.ts`：把现有面板改为消费共享快照，并由 Shell 包裹 Module 主内容，确保面板与 Task Cockpit 使用同一次响应；保留现有 `client` 测试注入兼容层；
- `apps/web/src/components/workshop/TaskCockpitPage.tsx`：新增“业务上下文 · 独立 SourceReadiness 快照”只读摘要，展示 envelope status、checkedAt、cutoffAt、P01～P12 状态计数、唯一 blocker 集、Receipt 是否存在；明确 source cutoff 不与 Task cutoff 混算、blocked/unknown 不当作 empty、无 Receipt 不声明 EvidencePack；
- `services/aos-api/aos_api/ecommerce_workshop_task_cockpit.py`：把旧的 `TASK_COCKPIT_BUSINESS_CONTEXT_BLOCKED` 静态 reader 缺口改为 `TASK_COCKPIT_BUSINESS_CONTEXT_INDEPENDENT_SNAPSHOT` warning，说明业务上下文由 Shell 单一 canonical snapshot 消费；不读取第二份数据、不重算状态；
- `SourceReadinessPanel.test.tsx`、`EcommerceWorkshopHost.test.tsx`、`TaskCockpitPage.test.tsx` 与后端 cockpit 测试：覆盖单次 GET、同响应双消费、tenant drift、blocked/ready/failed、Receipt 缺失、independent cutoff、旧 blocker 消失、无数据伪零和零命令；
- `apps/web/src/styles/45-ecommerce-workshop.css`：只补共享快照摘要的最小响应式样式；完成专项/累计、build、正式视觉稿逐区复审和 1280/1440/1920 内置浏览器验收。

禁止项：不修改 canonical SourceReadiness status precedence，不直连 Pipeline/niushop，不读取 P08/P10 原始属性，不执行 Pipeline/retry，不生成 Receipt，不把 Shell 的重复视图变成第二 authority，不把 SourceReadiness checkedAt 当 Task evaluatedAt，也不因 12 个 item 都存在而宣称 12/12 READY。W2-02F 只关闭 W2-02 的业务上下文消费轴；W2-02 主项是否可勾选仍须按 §5.2 对全部已交付子轴、真实非空详情和完整 EvidencePack 做累计复审。

2026-08-24 闭合检查点：代码已以 `m1@62c9090` 安全提交。Shell 现在只读取一次 tenant-bound canonical `SourceReadinessEnvelope`，数据源面板和 Task Cockpit 消费同一易失响应；Task evaluatedAt/taskCutoff 与 Source checkedAt/cutoffAt 分别展示，blocked、0/12 与 `receiptRef=null` 均保持失败关闭。后端 Workshop 累计 `79 passed`，Web 累计 `205 files / 2017 tests`，production build `320 modules`，OpenAPI deterministic 与合同 `13 passed`；内置浏览器 1280/1440/1920 三档零横向溢出、唯一 H1、旧 blocker 消失、新 independent-snapshot warning/无 exact EvidencePack Receipt 可见、零禁止任务命令，本次页面加载后 console error 为 0。正式视觉稿复审确认新增摘要位于权威指标与只读命令边界之间，没有复制经营数字、在线角色或示例数据。Delivery Receipt 为 `w2-02f-source-readiness-business-context-read-model-20260824`。W2-02 的代码轴已累计闭合，但真实非空 Step/Checkpoint 与目标态完整 EvidencePack 尚无授权证据，因此 96 项主计数诚实保持 `22/96`；不阻塞串行开发，下一子波立即进入 `W2-03`。

### 3.10 S2 / W2-03A 内容活动只读合同与失败关闭 API 壳

复核 `11` 号内容与活动技术方案、`84` 号 W2-03 预检 ADR、`99` 号 W3-11 authority 预检 ADR 和 `07` 号领域读模型合同后，冻结唯一 GET-only 表面 `GET /v1/ecommerce-workshop/views/content-campaign`。响应必须在同一 tenant/evaluatedAt/dataCutoff 下显式分离 `plan/calendar/content` 三个切片；CampaignRevision、CalendarEntry、MasterContentIntent 是三个独立 canonical authority，ContentVariant 只能是 Artifact revision 的读投影，不得自建 body 真源。

本子波先闭合可验证的严格合同/API 壳：

- 新增 `services/aos-api/aos_api/ecommerce_workshop_content_campaign_contracts.py`，定义 strict camelCase envelope、三切片固定顺序、aware timestamp、exact authority ref、blocker、eligible/attached/unmatched/conflicted 守恒与稳定无假 cursor 分页；
- 新增 `services/aos-api/aos_api/ecommerce_workshop_content_campaign.py`，仅组合 Principal tenant 下的失败关闭壳。当 canonical reader/Receipt 未实现时，三切片均返回结构化 `blocked`、明确 `CANONICAL_*_AUTHORITY_NOT_AVAILABLE`、`eligible=0/items=[]`；这只表示没有可评估的 authority，不能将空数据表述为业务结果为零或 readiness GREEN；
- 扩展 `services/aos-api/aos_api/routers/ecommerce_workshop.py`，使用 `ecommerce.content-campaign` 安装门、Principal 租户、拒绝任何 query scope 注入，且 OpenAPI 仅暴露 operationId `ecommerceWorkshopContentCampaignViewGet` 的 GET；
- 新增 `services/aos-api/tests/test_ecommerce_workshop_content_campaign.py`，并扩展 `test_ecommerce_workshop_operations_api.py`，覆盖 strict extra/missing、三切片顺序、守恒、false-ready、naive time、tenant 绑定、安装失败、scope 注入和非 GET 拒绝；
- 确定性重生 `packages/contracts/openapi/v1.generated.json` 与 `v1.inventory.json`，仅接受这一条 GET 的可解释差量。

禁止项：本子波不新增/执行 migration，不写真实业务数据，不返回 prompt/body/token/PII/Provider id，不创建或修订 Campaign/Calendar/Intent/Artifact，不排期、审批、启动、发布或回滚。A 壳 GREEN 后自动进入 W2-03B canonical authority foundation；由当前唯一开发者补齐必需跨层代码，但 migration apply、真实数据写入与发布仍必须保持独立门。

2026-08-24 闭合检查点：代码已以 `m1@b35f410` 安全提交。唯一 GET-only 表面已按 Principal tenant 与 `ecommerce.content-campaign` 安装门关闭 scope 注入；plan/calendar/content 三切片在 authority reader/Receipt 未实现时均返回结构化 blocked、空 items 与 `eligible=0`，未把无可评估 authority 冒充业务零值或 GREEN。专项合同/API `17 passed`，Workshop 后端累计 `75 passed`，OpenAPI `4325` operations 确定性导出/检查与 diff check GREEN；内置浏览器累计回归在 1280/1440/1920 三档均零横向溢出、唯一 H1、零可执行禁止类副作用按钮，本次重载新增 console error 为 0。本子波不新增/执行 migration，没有任何 Campaign/Calendar/Intent/Artifact 写入、排期、发布或 Provider 调用。Delivery Receipt 为 `w2-03a-content-campaign-readonly-contract-shell-20260824`；W2-03 主项继续未勾选，96 项主计数保持 `22/96`，下一子波立即进入 W2-03B canonical authority foundation。

### 3.11 S2 / W2-03B Campaign/Calendar/Intent authority 代码控制基座

为不再把缺少跨层 authority 作为等待他人的阻塞，本子波由唯一开发者补齐 W3-11 中 W2-03 必需的代码控制面，但严格分离“迁移文件 GREEN”与“已对真实库执行”。本波只建立三类 append-only authority 合同、head/revision schema 与幂等 Receipt schema，不注册写 API、不执行 Alembic upgrade。

文件级范围：

- 新增 `services/aos-api/aos_api/ecommerce_content_campaign_authority_contracts.py`：定义 `CampaignRevision`、`CalendarEntryRevision`、`CalendarDecisionRevision`、`MasterContentIntentRevision`、exact authority ref 和 `ContentCampaignAuthorityReceipt`。所有 revision/hash/time 严格校验；修订要求 prior exact ref；Calendar 必须保存 IANA timezone、aware resolved instants、DST resolution、exact Campaign/Artifact refs；排期不表示发布；Intent 不保存 prompt/body/token，master/channel 产物只引用 canonical Artifact revision；
- 新增 `services/aos-api/alembic/versions/w3_011_content_campaign_authority.py`，唯一 `down_revision=d0_after_001`。Campaign/Calendar/Intent 各有 tenant-bound mutable head 与 append-only revision，Calendar Decision 和 Receipt 也是 append-only；全表 RLS/FORCE RLS，runtime 对 history 只有 SELECT/INSERT，禁止 UPDATE/DELETE/TRUNCATE；非空 canonical history 时 downgrade 失败关闭；
- 新增 `services/aos-api/tests/test_ecommerce_content_campaign_authority_contracts.py` 和 `test_w3_011_content_campaign_authority_migration.py`，覆盖 strict extra、aware time、revision/prior、exact type/hash、时间窗口、DST、渠道唯一、排期/发布分离、Intent 最小披露、single head、RLS/FORCE RLS、append-only grant/trigger 与非空 downgrade guard。

禁止项：不执行 migration，不写 `org-org/dev-project` 或任何真实库，不新建 ContentVariant body/head/table，不复制 TaskBrief/Artifact/ArtifactRelation/Action/Approval/Lease/Receipt authority，不提供 create/revise/reschedule/cancel/publish HTTP，不调用 Provider。B 合同/迁移代码 GREEN 后自动进入 W2-03C tenant-bound Store/reader，先用 fake connection 验证 CAS/幂等/跨租户/读事务，再接入 W2 GET 视图。

2026-08-24 闭合检查点：代码已以 `m1@fb2ffdf` 安全提交。三类 canonical revision、Calendar successor decision、exact ref 与 authority Receipt 合同均严格校验 tenant/time/hash/revision/prior/type，Calendar 保存 IANA timezone 与 resolved window，Intent 只引用 Brief/Artifact exact revision 且 strict extra 拒绝 raw body/prompt。`w3_011` 唯一继承 `d0_after_001`，Alembic 实测仍为单 head；8 张表全部 RLS/FORCE RLS，5 张 history/decision/Receipt 表仅 SELECT/INSERT 并有 UPDATE/DELETE/TRUNCATE guard，非空 downgrade 失败关闭。专项 `7 passed`，Workshop+内容活动累计 `82 passed`，OpenAPI deterministic 保持 `4325` operations；内置浏览器累计回归 1280/1440/1920 零横向溢出、唯一 H1、零可执行禁止类副作用按钮、新增 console error 0。本波没有执行 migration、没有真实数据写入、写 API 或发布副作用。Delivery Receipt 为 `w2-03b-content-campaign-authority-foundation-20260824`；W2-03 主项仍未勾选，下一子波立即进入 W2-03C tenant-bound Store/reader。

### 3.12 S2 / W2-03C tenant-bound Store 与 bounded reader

本子波在 B 合同/schema 上新增单一内部 Store，不注册公开写 router。写路径仅供后续治理命令复用，必须先校验 `TenantScope == item.tenant`、actor、expectedVersion、revision 单步递增与 Idempotency-Key；同 key 同 request hash 返回原 exact result ref，同 key 异 hash 冲突。任何失败均不自动重试。

文件级范围：

- 新增 `services/aos-api/aos_api/ecommerce_content_campaign_authority_store.py`，实现 campaign/calendar/intent head `FOR UPDATE` + append revision + immutable Receipt 原子提交，Calendar decision 只 append；所有 SQL 用参数传租户，不把 tenant/actor 信任交给 body；
- 同一 Store 提供 `list_campaigns/list_calendar_entries/list_intents`，每次开启 `REPEATABLE READ READ ONLY`，固定 tenant/cutoff/确定性排序/limit<=100，仅返回当前 exact revision 严格合同；连接、payload、scope 或 contract drift 均统一失败关闭；
- 新增 `services/aos-api/tests/test_ecommerce_content_campaign_authority_store.py`，仅用 fake connection 覆盖首次创建、修订 CAS、同键 replay/异 payload 冲突、跨租户与 actor 拒绝、Calendar decision append-only、三类 bounded read-only 回读、row tenant drift 失败关闭。

禁止项：不连接真实库，不执行 `w3_011` migration，不注册 create/revise/schedule/cancel/publish API，不创建 Artifact/Action/Approval/Lease，不保存正文、prompt、token、PII 或 Provider 数据。C GREEN 后自动进入 W2-03D，将只读 reader 依赖注入 GET view，reader 不可用仍结构化 blocked，空但可用的 canonical authority 才能是 ready empty。

2026-08-24 闭合检查点：代码已以 `m1@47976bf` 安全提交。三类 publish 内部 Store 均在连接前校验 item tenant/actor，连接内先查 immutable Receipt、再 `FOR UPDATE` head 并校验 expectedVersion/单步 revision，成功时同一事务 append revision + Receipt + commit；同 key 同 hash 返回原 exact ref，异 hash 冲突。Calendar decision 只 append。三类 reader 均使用 `REPEATABLE READ READ ONLY`、tenant/cutoff/稳定排序/limit<=100，row 或 payload tenant drift 失败关闭。专项累计 `16 passed`，Workshop+内容活动累计 `91 passed`，diff check GREEN；内置浏览器累计回归 1280/1440/1920 零横向溢出、唯一 H1、零可执行禁止类副作用按钮、页面新增 console error 0。测试只用 fake connection，未执行 migration、未连接真实数据库、未注册写 API。Delivery Receipt 为 `w2-03c-content-campaign-store-readers-20260824`；W2-03 主项仍未勾选，下一子波立即进入 W2-03D GET view reader composition。

### 3.13 S2 / W2-03D revision Receipt 联结与 GET view composition

C 后的方案一致性复审发现：若 revision row 不持久化创建它的 immutable Receipt ID，W2 只读视图就无法对每个 item 返回真实 exact Receipt，并会诱发用代码 Delivery Receipt 冒充业务 revision Receipt 的错误。因此 D 先在尚未 apply 的 `w3_011` schema 中增加 `receipt_id NOT NULL`，与 Store 同事务生成/写入的 authority Receipt 一对一联结，然后才组合 GET view。

文件级范围：

- 修改 `w3_011_content_campaign_authority.py`，revision/decision 表加 `receipt_id TEXT NOT NULL`，同 tenant 组合唯一；迁移仍未执行，因此不做线上 ALTER；
- 修改 `ecommerce_content_campaign_authority_store.py`，在 append revision 前生成 receipt ID，revision row 与 Receipt row 同事务写入同一 ID；reader 返回 typed `ContentCampaignAuthorityObservation(revision, receiptId)`，禁止缺 Receipt 或错 tenant row；
- 修改 `ecommerce_workshop_content_campaign.py/contracts.py`，依赖注入 Store 并分别读 plan/calendar/content；reader 成功且空时可返回 ready empty，非空时每项必须带 exact revision/hash/authority Receipt，单切片 reader 失败只阻塞该切片、不伪造全局空值；
- 扩展 migration/Store/view/API 测试，覆盖 receipt 联结、空 ready、非空 exact refs、单切片失败、tenant drift、count ledger 与 GET-only 不回退。

禁止项：不将 Delivery Receipt 当业务 Receipt，不执行 migration，不连接/写入真实库，不开放写 API，不伪造 ContentVariant，不排期或发布。D GREEN 后自动进入 W2-03E ArtifactRelation-based ContentVariant projection，只读 canonical Artifact/Relation，不建第二正文 authority。

2026-08-24 闭合检查点：代码已以 `m1@2b7f3dc` 安全提交。四类 revision/decision row 与同事务 authority Receipt 使用同一 `receipt_id` 并在 tenant 内唯一；reader 只返回 typed revision + exact Receipt observation。GET view 对 plan/calendar/content 三切片独立读取：可信空 authority 为 `ready + eligible=0`，非空数据逐项返回 exact resource/revision/hash/Receipt，单 reader 失败只阻塞对应切片。专项 `17 passed`，Workshop 累计 `92 passed`，OpenAPI deterministic 与 diff check GREEN；内置浏览器累计回归 1280/1440/1920 零横向溢出、唯一 H1、本页零可执行禁止类副作用按钮。迁移未执行、真实数据库未连接、未注册写 API，也未创建 ContentVariant 或触发任何排期/发布/Provider 副作用。Delivery Receipt 为 `w2-03d-content-campaign-view-composition-20260824`；下一子波自动进入 W2-03E ArtifactRelation-based ContentVariant projection。

### 3.14 S2 / W2-03E ArtifactRelation-based ContentVariant projection

上位方案已冻结 ContentVariant 为可重建读模型而非正文 authority，关系方向固定为 Variant → Master。E 复用 canonical `aip_artifact`、`aip_artifact_relation` 与 `aip_production_contract_receipt`：只读查询 `variant_of` relation，在同 tenant/cutoff 下校验 relation 两端 exact hash 与当前 Artifact authority 一致，并要求精确的 `artifact_relation.create` Receipt；再与同 cutoff MasterContentIntent 的 `masterArtifactRef` 精确匹配。任何 missing Receipt、孤儿、hash drift、重复 relation/Receipt 或跨租户事实均失败关闭，不通过 createdAt 猜测 current。

文件级范围：

- 扩展 `ecommerce_workshop_content_campaign_contracts.py`，新增 strict `ContentVariantProjection`，明确 intent exact ref、master/variant Artifact exact ref、relation ID/Receipt 与唯一 canonical 名称；不承载正文、prompt、provider ID 或客户数据；
- 扩展 `ecommerce_content_campaign_authority_store.py`，新增 bounded `list_content_variants` reader，使用 `REPEATABLE READ READ ONLY`、tenant/cutoff、稳定排序和 limit，联结 canonical relation、Artifact 与 production Receipt 并验证 hash/唯一性；
- 扩展 `ecommerce_workshop_content_campaign.py`，content slice 在 Intent authority 成功后组合 Variant projection；无 relation 是可信空 Variant 集，relation/Receipt/Artifact drift 则只阻塞 content slice；
- 扩展 Store/view/API 测试，覆盖 Variant → Master、exact hash/Receipt、intent 联结、orphan/drift/duplicate/tenant failure、数量守恒与 GET-only。

禁止项：不新增 ContentVariant head/revision/body/table/Store/API namespace，不创建 Artifact/Relation/Receipt，不修改 canonical Artifact 数据，不执行 migration，不连接真实库，不排期、生产或发布。E GREEN 后自动进入 W2-03F strict Web SDK 与正式视觉稿页面实现/三视口验收。

2026-08-24 闭合检查点：代码已以 `m1@d18d21c` 安全提交。新增的 bounded reader 只读 `variant_of` relation，并联结两端 canonical Artifact 当前 hash 与精确 `artifact_relation.create` Receipt；跨租户、孤儿、Receipt 缺失/重复、relation 类型或 hash drift 均失败关闭。content slice 仅在 exact MasterContentIntent 的 `masterArtifactRef` 与 relation Master 完全一致且唯一时投影 `ContentVariant`，同时返回 Intent revision Receipt、Master/Variant exact hash 和 relation Receipt。专项 `29 passed`、Workshop 累计 `101 passed`、compileall、OpenAPI deterministic 与 diff check GREEN；内置浏览器 1280/1440/1920 零横向溢出、唯一 H1、本页零可执行生产/排期/发布等副作用按钮。没有新增 ContentVariant 真源、迁移或写 API，也未连接真实数据库。Delivery Receipt 为 `w2-03e-content-variant-artifact-projection-20260824`；下一子波自动进入 W2-03F strict Web SDK 与正式页面。

### 3.15 S2 / W2-03F strict Web 与正式视觉验收

本子波复习 `84`、`99` ADR、3.10～3.14 与正式视觉稿 `foundry/html/workshop-content-campaign.html`。页面继承三栏信息层级、主视图分区和数量概览，但不继承示例业务事实、保存、批准、发布、自动拆任务或排期写入。

文件级范围：

- `apps/web/src/api/ecommerceWorkshop/contracts.ts`：增加 plan/calendar/content 三切片、exact authority、ContentVariant lineage、blocker、ledger 与 page 类型；
- `apps/web/src/api/ecommerceWorkshop/parser.ts`、`client.ts`：增加 exact-key、canonical-order、同 cutoff、tenant、hash、Receipt、variant lineage、数量守恒及 blocked/ready 语义的失败关闭解析；只暴露 GET `/v1/ecommerce-workshop/views/content-campaign`；
- 新增 `ContentCampaignPage.tsx/.test.tsx` 并修改 `EcommerceWorkshopHost.tsx/.test.tsx`：挂载正式只读页面，覆盖 blocked、可信 empty、非空 exact authority/ContentVariant、tenant drift 与错误状态；
- `apps/web/src/styles/45-ecommerce-workshop.css`：按正式稿实现自适应三栏，1280/1440/1920 不横向溢出，保留单一 H1、键盘焦点与长 hash 换行。

验收包含 strict parser/client/component/host 专项、Workshop Web 累计回归、TypeScript build、内置浏览器三宽度与 blocked/empty/nonempty 状态矩阵、方案/代码一致性复审、Delivery Receipt、authority CAS 与 Prime 强一致回读。禁止 apply migration、写真实数据库、调用 Provider/排期/发布副作用或增加任何可用写控件。

2026-08-24 闭合检查点：代码已以 `m1@2a72391` 安全提交。strict Web SDK 对三切片 canonical order、同 cutoff、租户、exact hash/Receipt、ContentVariant `variant_of` lineage、identity 唯一性、数量守恒和 blocked/ready 语义失败关闭；正式页面保留视觉稿三栏层级、主视图、数量概览和证据边界，但没有保存、审批、排期、发布或自动拆任务入口。专项 parser/client/page/host GREEN，Web 累计 `207 files / 2024 tests`、TypeScript noEmit 与 diff check GREEN；内置浏览器 blocked/empty/nonempty 及 1280/1440/1920 状态矩阵零横向溢出、唯一 H1、ContentVariant 归因可见且越权按钮为零。SourceReadiness 仍诚实显示 visual-fixture blocked，未推断运营 GREEN；未 apply migration、未写真实数据库、未调用 Provider/邀约/排期/发布副作用。Delivery Receipt 为 `w2-03f-content-campaign-strict-web-visual-20260824`；下一子波自动进入 W2-04A。

### 3.16 S2 / W2-04 达人增长只读模型施工拆分

本波复习 `85` ADR、产品 `07`、逐区域规格 `228` 与正式视觉稿 `workshop-creator-outreach.html`。保持 `workflowPhase=discovery/evidence/matching/batch_prepare/start` 与 `businessStage=candidate/outreach/contract/delivery/relationship` 两条正交轴；Observation 不等于 Decision，平台接受不等于合同签署，PRELIMINARY 不晋升关系，PII 仅返回受控 ref，不复制联系方式、合同正文、账号 secret 或寄样地址。

串行子波：

- `W2-04A`：冻结 `creator-growth-view/v1`、五个 business slice、双阶段轴、exact ref、blocker、数量守恒、GET-only 路由和 OpenAPI；所有 slice 初始失败关闭，不新增领域真源；
- `W2-04B`：新增候选/身份/Match Observation/Decision canonical authority 与 append-only Store，不做 discovery、合并、排除或批次准备；
- `W2-04C`：新增 OutreachBatch/Item prepare authority、input 与 start ledger；prepare/freeze 零副作用，accepted/applied/failed/unknown/skipped 分离；
- `W2-04D`：新增 Contract/TermDiff、Delivery、Relationship exact authority 与同合作 lineage；SIGNED、履约结果和关系成熟度互不反推；
- `W2-04E`：组合五 slice bounded reader，统一 cutoff、唯一 identity、分页与双租户失败关闭；
- `W2-04F`：strict Web SDK、正式五 Tab 只读页面、blocked/empty/nonempty 与 1280/1440/1920 浏览器矩阵；移除视觉稿中的导入、新建批次、写邀约、批准、发送、签署、寄样、佣金和关系 mutation 控件。

`W2-04A` 文件级范围：新增 `ecommerce_workshop_creator_growth_contracts.py` 与 `ecommerce_workshop_creator_growth.py`，挂载只读路由；更新 OpenAPI/operation inventory；新增契约、GET-only、租户、双轴、五 slice、同 cutoff、blocker/ledger 和 cursor 失败关闭测试。禁止 migration、真实数据库写入、Provider 调用及任何达人发现/邀约/合同/履约/关系副作用。

2026-08-24 闭合检查点：W2-04A 已以 `m1@a8627e8` 安全提交。`creator-growth-view/v1` 固定五个业务阶段切片与五个工作流阶段正交表达，exact authority ref、唯一性、同 cutoff、数量守恒、分页和 blocked/ready 语义全部失败关闭；GET-only 路由受安装态与双租户约束，五切片在 canonical authority 不存在时只返回独立 blocker，不制造达人事实或写入口。专项 creator-growth/API `26 passed`、Workshop 累计（排除受保护未跟踪 `plugins/ops/` 资产范围）`78 passed`，OpenAPI 契约与确定性导出、compileall、diff check GREEN。未 apply migration、未写真实数据库、未触发发现/邀约/合同/履约/关系副作用。Delivery Receipt 为 `w2-04a-creator-growth-contract-shell-20260824`；下一子波自动进入 W2-04B。

2026-08-24 W2-04B 闭合检查点：代码已以 `m1@3fa8b4c` 安全提交。候选身份、Profile Evidence、Match Observation 与 Match Decision 使用独立 immutable authority；Observation 只表达可复核评分证据，Decision 只引用 exact Observation，`accepted` 不产生合同状态。PII 只保留唯一 opaque ref；Store 以双租户、exact Receipt、append-only INSERT、repeatable-read bounded reader 和 tenant drift fail-closed 固定边界。专项/邻接 `30 passed`、compileall 与 diff check GREEN；未创建或 apply migration，未发现、邀约或修改真实达人数据。下一子波自动进入 W2-04C。

## 4. 每个 Loop

每个子波固定执行：

1. 复读 authority、01/06、上位方案、当前 ADR、Git 与全部 Lease；
2. 冻结当前文件、前后 SHA-256、接口、测试、回滚与禁止项；
3. 先写失败测试，再做最小实现；
4. 跑专项、邻接、累计、类型/构建，页面用内置浏览器；
5. 复审方案—代码一致性、租户、安全、PII/Secret、迁移和副作用；
6. Delivery Receipt、安全提交、authority CAS、memory sync/validate/gate、Prime exact readback；
7. 自动进入下一个依赖已满足的子波。

## 5. S0 退出与 S1 入口

S0 退出条件：82/100 ADR 和总清单已同步无环顺序，Task Receipt/Lease 有效，记忆门 GREEN，目标文件无争用，`m1` 未跟踪用户范围未被纳入。

S1 第一个实现提交是 W2-01A strict contract/API shell；D0 与缺失 Case slice 在对应 exact authority 到位前保持结构化 blocked。该策略保证不因外部事实停工，也不伪造 operational GREEN。
