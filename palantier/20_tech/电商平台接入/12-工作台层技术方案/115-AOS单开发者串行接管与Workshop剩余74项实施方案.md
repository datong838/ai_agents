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
