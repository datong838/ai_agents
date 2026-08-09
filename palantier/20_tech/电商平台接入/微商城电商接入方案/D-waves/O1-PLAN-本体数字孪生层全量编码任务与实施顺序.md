# O1-PLAN：本体数字孪生层全量编码任务与实施顺序

> **版本**：v1.0 · 2026-08-09
> **状态**：**Wave 1～10 全部 GREEN；本体数字孪生层与 D4/D5 已独立封板**
> **目标租户**：`org-org` · `dev-project`（默认工作区）
> **代码基线**：`aos-platform/m1@24938e4`
> **上位方案**：`O1-本体数字孪生层改造方案.md`、`O1-UX-本体数字孪生九菜单与知识图谱补强方案.md`、`O1-UA0-上层应用反向约束与本体能力前置对账清单.md`
> **状态边界**：O1-UA0 `PLAN_APPROVED`；O1-UX1、O1-UA1、O1-D、O1-UA2、O1-UX2～UX6、D4-SPEC-SYNC、G17、G18、G19 全部 GREEN

## 0. 使用的 Rules

| Rule | 计划约束 |
|---|---|
| 先方案后编码 | 用户批准本计划前，不修改 AOS 功能代码 |
| 完整计划公开 | 本体数字孪生层全部任务均登记在本文件，不保留隐性编码计划 |
| 真实范围 | 真实数据与页面验收只认 `org-org/dev-project`；`dev-org` 只可用于明确隔离 canary |
| 单一权威真源 | PostgreSQL、电商 Object/Link、Installation-aware compose、Receipt/CAS 保持唯一权威链 |
| 最小演进 | 复用 O1-UX0 已冻结合同，不另建 ObjectRef、图数据、权限或状态真源 |
| 先测试 | 每项功能先建立失败测试，再完成最小实现和回归 |
| 交互诚实 | 未完成能力不显示假成功按钮，不以 Mock、localStorage、静态图或 toast 代替真实结果 |
| 分支收口 | 适合并行时才创建 w1～w4；每波结束最终同步到同一 m1 起跑线 |
| 波次闭环 | 每波更新 D-waves、AOS 项目上下文、证据和记忆，并检查 Prime Agent |

## 1. 计划目标与非目标

### 1.1 目标

把当前“九页面权威读链基础闭环”推进为可真实使用、可持久化、可审计的本体数字孪生产品层：

```text
O1-UX1 只读对象探索产品化
  → O1-UA1 共同合同冻结
  → O1-D 稳定对象身份
  → O1-UA2 Wiki/Action/Task/Evidence 权威骨架
  → O1-UX2 探索资产持久化
  → O1-UX3 权威图查询
  → O1-UX4 统一知识图谱画布
  → O1-UX5 其余八页任务流
  → O1-UX6 九页证据封板
  → D4/D5 独立规格与证据收口
```

### 1.2 非目标

- 本计划不一次实现六数字同事的全部候选领域对象。
- 不复制 Foundry 产品、示例数据或品牌信息架构。
- 不建立第二套图数据库、前端权限状态机或客户端哈希真相。
- 不用 `Customer` 替代当前 `CustomerLite`，不把 Creator 继承为 Customer。
- 不把计划通过、测试通过或页面可打开误报为 `CONTRACT_GATE_GREEN` 或 D5 总门 GREEN。

## 2. 总体依赖门

| 门 | 解锁范围 | 必须满足 |
|---|---|---|
| G-PLAN | 开始 UX1-0 | 用户明确批准本计划 |
| G-UX1 | 开始 UA1 | 全宽只读探索在真实租户通过浏览器与回归验证 |
| G-UA1 | 开始 O1-D/UA2 合同实现 | ADR、注册表、DTO/OpenAPI、安全和兼容测试通过 |
| G-O1D | UX2 真实保存、UX3 权威图切换 | alias manifest、copy/hash、冲突隔离、残留扫描和回滚证据 GREEN |
| G-UA2 | Wiki/Action/Task/Evidence 生产读取 | PG/RLS、Store/Service、CAS/Receipt、Overlay compose 与负向门通过 |
| G-UX2 | UX3/UX4 上层资产联动 | Exploration/ObjectSet/Share/Annotation 保存回读和跨租户门通过 |
| G-UX3 | UX4 图画布读取 | GraphSnapshot 与详情邻居、Graph Health 对账一致 |
| G-UX4/5 | UX6 封板 | 九页面主任务可用、无假按钮、性能和可访问性达标 |
| G-UX6 | D4/D5 最终对账 | 九页、RLS、canary、manifest 与文档状态同步 |
| G-D5 | 宣告本地数据孪生层证据闭环 | D4-SPEC、D5-E1、23 资源 canary、G17/G18/G19 全部 PASS |

## 3. 全量编码任务

### Wave 1：O1-UX1 对象探索全宽只读产品化

> **执行结论（2026-08-09）**：GREEN。专用全宽容器、按需详情抽屉、专注模式、窄屏 Sheet、Schema 优先宽表和安全 deep-link 已落地；154 files / 2017 tests、TypeScript、production build 和五类视口浏览器验证通过。当前页面可见 15 个 OT，其中 D4 微商城域仍为 12 OT，另有 `OrderItem/Site/WorkOrder` 三个既有平台 OT；该差异进入 UA1 注册表和 D4-SPEC-SYNC 对账，不混写口径。

#### 任务 1：UX1-0 失败测试与页面基线

**目标**：先把当前挤压布局、抽屉、滚动和深链问题变成可复现测试。

**预计代码目录**：

- `aos-platform/apps/web/src/pages/s2/`
- `aos-platform/apps/web/src/components/ontology/`
- `aos-platform/apps/web/src/api/`

**实施项**：

- 为主画布全宽、详情抽屉、专注模式、宽表滚动建立失败测试。
- 覆盖 `ObjectRef {objectType, objectId}`、URL 刷新、返回上下文和跨类型邻居。
- 记录 1280×720、1440×900、1920、768、390 五类基线。

**退出门**：新增测试在实现前稳定 RED；当前真实读链和 O1-UX0 交互诚实性测试保持 GREEN。

#### 任务 2：UX1-1 专用全宽容器

**实施项**：

- 从 `workshop.tsx` 抽离对象探索专用页面容器，不全局修改 `BpSplit`。
- 主结果画布默认全宽；详情为可关闭、可调整宽度抽屉。
- 增加专注模式；窄屏详情使用底部 Sheet。
- 页面内容使用纵向滚动，不把复杂内容压进固定高度。

**退出门**：五类视口无挤压；关闭抽屉后主画布恢复全宽；不改变后端读链。

#### 任务 3：UX1-2 Schema 驱动宽表

**实施项**：

- 从 composed schema 生成列、单位、枚举、PII 和空值语义。
- 不再从第一条对象数据猜测列。
- 支持横向滚动、稳定表头、单对象详情选择与多行选择分离。
- 保持服务端脱敏、分页、排序和过滤权威。

**退出门**：真实 12 OT 可浏览；跨类型下钻、刷新和返回上下文一致；前端全量测试和 TypeScript 通过。

**并行建议**：该波改动集中、共享 `workshop.tsx` 状态，建议在 `m1` 串行完成，不强行建立四 worker。

### Wave 2：O1-UA1 公共合同与安全门

#### 任务 4：UA1-0 合同 ADR 与领域注册表

**产出**：

- Domain Graph / Operational Lineage Graph ADR。
- 当前 12 OT、候选类型、owner、canonical identity、authority 注册表。
- `conflictResolution=resolved|blocked|pending`；所有阻断冲突必须 resolved。
- 平台模板、Installation、组织 Overlay 和 Knowledge Pack 责任矩阵。

**退出门**：命名、图域、authority、CustomerLite/Creator/Content 边界无 P0/P1。

#### 任务 5：UA1-1 引用 DTO 与 OpenAPI

> `depends-on: UA1-0`

**预计代码目录**：

- `aos-platform/services/aos-api/aos_api/`
- `aos-platform/services/aos-api/tests/`
- `aos-platform/apps/web/src/api/`

**实施项**：

- 复用 `ObjectRefDTO/ObjectRef {objectType, objectId}`。
- 新增 `LinkRefDTO`、`KnowledgeSubjectRefDTO`、`TaskRefDTO`、`EvidenceRefDTO`。
- GraphSnapshot 以兼容 expand 方式增加 `graphDomain`、`edgeAuthority`、revision、validity 和 evidence reference。
- Python/TypeScript/OpenAPI 字段和错误码冻结。

**退出门**：未知字段拒绝；旧 O1-UX0 合同不破坏；OpenAPI diff 只有批准的兼容扩展。

#### 任务 6：UA1-2 安全、深链和回退门

**实施项**：

- capability、Action 风险、审批、防客户端提权。
- PII、Prompt injection、数据外传指令、恶意工具参数负向测试。
- `returnTo` 只允许站内白名单路径，拒绝协议、主机、`//`、穿越和未知路由。
- schemaEtag/watermark 只由服务端产生，客户端写 DTO 不接受。
- 固化强制回退触发条件、feature flag 和 evidence manifest。

**退出门**：缺 scope、未知 scope、跨租户、伪造风险等级和未知 authority 全部失败关闭。

**并行建议**：UA1-0 串行完成后，DTO、前端类型、安全负向测试可拆分，但最终由 m1 做合同统一复审。

### Wave 3：O1-D Canonical Alias Migration

#### 任务 7：O1-D-0～D-n 稳定身份迁移

**预计代码目录**：

- `aos-platform/services/aos-api/alembic/`
- `aos-platform/services/aos-api/aos_api/`
- `aos-platform/services/aos-api/scripts/`
- `aos-platform/services/aos-api/tests/`

**实施项**：

- 建立版本化 alias manifest：旧主键、目标 canonical ID、Object Type、hash、来源、冲突类别和处置状态。
- 执行只读盘点、冲突隔离、copy/hash 对账、受控切换、残留扫描和回滚演练。
- 迁移裸 ID/非规范别名，不改写 `ecom_object` 权威主键。
- 验证跨类型同 ID、同业务 ID 跨租户共存和未知别名失败关闭。

**退出门**：无第二对象、无未分类冲突、无裸 ID 残留、跨租户零可见；完整 manifest 和回滚证据存在。

**并行建议**：高风险迁移和切换必须在 `m1` 串行；只读盘点、测试矩阵和证据格式可独立准备，但不能并行执行真实切换。

### Wave 4：O1-UA2 上层公共权威骨架

> **执行结论（2026-08-09）**：GREEN。10 类 operational record 已建立双租户 head/revision 权威表，append/archive/cleanup Receipt、CAS、不可变历史、RetentionPolicy、未安装不可见与 Action 防降权通过；migration head=`o1ua2_002`，23/23 表 RLS+FORCE RLS，定向 9 passed，真实目标 scope 零新增记录。`CONTRACT_GATE_GREEN` 已达成。

#### 任务 8：UA2-0 PostgreSQL 模型与迁移

**预计代码目录**：

- `aos-platform/services/aos-api/alembic/`
- `aos-platform/services/aos-api/aos_api/`
- `aos-platform/services/aos-api/tests/`

**实施项**：

- Wiki/Knowledge、Action Type/Instance、Task/Plan/Checkpoint/Artifact、Eval/Evidence 权威表。
- 双租户复合键、FK、CHECK、RLS + FORCE RLS。
- 不可变 revision、归档、supersedes/revokes、RetentionPolicy reference。
- upgrade/downgrade、历史兼容和同业务 ID 跨 scope 测试。

#### 任务 9：UA2-1 Store/Service

- Principal 推导 scope，不接受客户端覆盖。
- Idempotency-Key、CAS/If-Match、Receipt、不可变历史。
- 同 key 同 payload 原样重放；异 payload 冲突；旧 ETag 412。
- Evidence 清理按 RetentionPolicy，保留不可逆 hash 和清理 Receipt。

#### 任务 10：UA2-2 Compose/Overlay

- 公共 Knowledge Pack 随平台模板和 Installation 分发。
- 组织私有 Wiki、反馈和 Episodic Memory 严格隔离。
- Action 默认定义来自模板；组织 Overlay 只能提高限制或禁用，不能降低硬门。
- 所有页面和 Agent 使用同一 composed schema/policy。

**退出门**：迁移、RLS、Store、CAS、Receipt、compose、未安装不可见、组织只收紧策略全部通过，才可标记 `CONTRACT_GATE_GREEN`。

**并行建议**：合同冻结后可拆成 PG/RLS、Store/Service、Compose/Overlay、安全测试四个 worker；合并前先统一 migration 顺序和公共 DTO。

### Wave 5：O1-UX2 探索资产持久化

#### 任务 11：UX2-0～UX2-2 Exploration/ObjectSet/Share/Annotation

**预计代码目录**：

- `aos-platform/services/aos-api/alembic/`
- `aos-platform/services/aos-api/aos_api/`
- `aos-platform/services/aos-api/tests/`
- `aos-platform/apps/web/src/api/`
- `aos-platform/apps/web/src/pages/s2/`
- `aos-platform/apps/web/src/components/ontology/`

**实施项**：

- PostgreSQL Exploration、ObjectSet、ObjectSetItem。
- 保存探索、列配置、图布局、private/workspace 分享。
- Wiki/Draft 注释、归档与恢复；不提供生产物理删除。
- 停用生产可达的进程内 ExplorationEngine。

**退出门**：保存后服务端回读一致；幂等/CAS/归档恢复通过；跨租户零可见；无假成功按钮。

### Wave 6：O1-UX3 权威图查询

#### 任务 12：UX3-0～UX3-2 GraphSnapshot Service

**实施项**：

- Domain/Operational Lineage 分层查询。
- owned/non-owned、authoritative/inferred/compat_projection 明确标识。
- 1～5 跳、多种子、最短路径、过滤、cursor、watermark、截断和预算。
- 关闭生产可达的进程内/dev 写边入口。

**退出门**：详情邻居与图谱边一致；Graph Health 对象/边/孤立/悬空计数可对账；未知 authority 不被展示为事实。

### Wave 7：O1-UX4 统一知识图谱画布

> **执行结论（2026-08-10）**：GREEN。原生 SVG 确定性布局在 100/300/500 节点为 0.213/0.895/0.554ms，新增图依赖 0；统一画布已覆盖对象探索和 Graph Health，支持真实 pan/zoom/fit、双布局、移动列表、全屏、1～5 hops、关系/对象类型过滤、可见路径、Domain/Operational 分层与失败关闭。157 files / 2032 tests、TypeScript、production build、内置浏览器与设计 QA 通过；证据 `O1-UX4_20260809T175244Z.json` GREEN。

#### 任务 13：UX4-0 图形库基准

- 评审许可证、包体、主题适配、布局、可访问性。
- 对 100/300/500 节点做性能基准。
- 基准评审通过后才确定依赖，不预先锁死图形库。

#### 任务 14：UX4-1～UX4-3 图谱画布

**预计代码目录**：

- `aos-platform/apps/web/src/components/ontology/graph/`
- `aos-platform/apps/web/src/pages/s2/`
- `aos-platform/apps/web/src/api/`

**实施项**：

- 自动布局、缩放、平移、框选、拖动、适配画布。
- 节点展开、多跳、路径、图例、过滤和截断提示。
- 详情抽屉、Wiki、Action、任务与证据图层联动。
- 对象探索与图谱健康度复用同一画布。
- 键盘完成聚焦、打开、邻居移动和关闭。

**退出门**：100/300/500 节点性能门、标签可读性、键盘和主题验收通过。

### Wave 8：O1-UX5 其余八页任务流

#### 任务 15：UX5-0～UX5-4 九菜单完整闭环

**预计代码目录**：

- `aos-platform/apps/web/src/pages/s2/ontology.tsx`
- `aos-platform/apps/web/src/pages/s2/remainder.tsx`
- `aos-platform/apps/web/src/pages/s2/WikiIndexPage.tsx`
- `aos-platform/apps/web/src/components/ontology/`
- 对应后端 Router/Service/Test 目录

**实施项**：

- 本体管理：Object/Link/Action 类型和组织定制入口。
- Funnel：阶段、失败证据和受控重跑。
- OKF Funnel/概览：电商默认、覆盖率、阻断字段、mapping revision 和影响分析。
- 活知识 Wiki/Wiki 索引：主体选择、来源、版本、Draft 和覆盖缺口。
- 分支与 Overlay：diff、当前/历史、组织定制和 reset-to-inherit。

**退出门**：九页主任务逐页闭环；所有可见主按钮有真实结果或明确不可用原因。

### Wave 9：O1-UX6 总验收与证据封板

#### 任务 16：UX6-0～UX6-2

**验证范围**：

- 前后端针对性测试、累计回归、TypeScript、构建。
- 九页面浏览器全量验收和五类视口回归。
- RLS、跨租户 canary、PII、Prompt 注入、Action 防提权。
- 图查询性能、可访问性和浏览器错误/网络失败检查。
- evidence manifest：git SHA、migration head、scope、feature flags、schemaEtag、watermark、文件 hash 和总体结论。

**退出门**：P0/P1=0；证据完整；O1 主方案、O1-R、O1-UA0、O1-UX、D-waves 和项目上下文统一对账。

### Wave 10：D4/D5 独立规格与证据收口

> **执行结论（2026-08-10）**：GREEN。Shipment 权威支付时间批读与独立派生 CAS 已落地；8 项指标、投影所有权、30 条 DLQ、23 类资源 canary、鉴权矩阵、真实 scope 守恒全部通过。代码 `a3d4619`，证据 `24938e4`；最终证据 `D5-E2_FINAL_<最新UTC>.json` 的 `overall_pass=true`。

#### 任务 17：D4-SPEC-SYNC → D5-E1 → D5-E2

**实施项**：

- 同步 12 OT、14 Link、8 项派生指标、Canonical ID 和运行级临时 scope 口径。
- D5-E1 三类真实失败路径、30 条临时 scope DLQ、脱敏、持久化、幂等和 retry Receipt。
- 五组矩阵、23 类资源跨租户 canary；真实 `org-org/dev-project` 只读，前后 hash 和测试标识零写。
- D5-E2 全门回归 G17/G18/G19。

**退出门**：任何 `RED/INCONCLUSIVE/NO_DATA/EXTERNAL_WRITE` 均保持封板失败；所有清理成功并有持久化证据后才能总体 GREEN。

## 4. 分支与并行策略

| 波次 | 默认策略 | 原因 |
|---|---|---|
| UX1 | m1 串行 | 页面状态和 `workshop.tsx` 高耦合 |
| UA1 | UA1-0 串行；之后有限并行 | 名称/ADR 必须先冻结，DTO 与安全测试才可分工 |
| O1-D | m1 串行真实切换 | 高风险身份迁移，不允许多写者并发 |
| UA2 | 适合四 worker | PG/RLS、Store、Compose、安全测试边界相对独立 |
| UX2 | 后端/前端/隔离测试可并行 | 公共 DTO 和 migration 先由 m1 冻结 |
| UX3/UX4 | 先 UX3 后 UX4；内部有限并行 | 查询 DTO 是画布前置依赖 |
| UX5 | 可按页面族拆分 | 共用 SDK/组件先冻结，防止复制权限和租户状态 |
| UX6/D5 | 总控串行 | 证据、真实 scope 和最终状态必须唯一判定 |

如创建 w1～w4：从最新干净 m1 建立；worker 完成后合入 m1；最终四 worker 再同步最终 m1。任一波不适合并行时只在 m1 实施，不为形式强拆。

## 5. 每波统一工程过程

1. 核对最新 m1、工作树、上位方案、D-waves 清单和真实服务状态。
2. 生成或更新该波改动清单，冻结文件、DTO、错误码、测试、风险和回滚。
3. 先写失败测试，再做最小实现。
4. 运行针对性测试、累计回归、类型检查/构建。
5. 使用内置浏览器验证 `org-org/dev-project` 真实页面、交互、刷新、失败态和控制台。
6. 执行租户、PII、Action、幂等、CAS 和回滚负向验证。
7. 代码与方案逐条对账；审查无假成功、无第二真源、无用户改动被覆盖。
8. 提交并按需要同步 worker；记录 commit、测试和证据。
9. 更新 AOS 项目上下文、D-waves、总计划/228 路线和双层记忆。
10. 检查 Prime Agent 状态和是否需要其支持下一波；汇报本波结果与下波建议。

## 6. 统一回滚原则

- 布局波只回退新容器，不恢复 O1-UX0 已移除的假功能按钮。
- 合同采用 expand-compatible；失败时关闭新消费者，不撤销旧安全校验。
- O1-D 任何 copy/hash、冲突或清理异常立即停止切换，保留 manifest 和隔离区。
- 数据迁移先 expand，验证后切读/写，最后 contract；不得一波执行不可恢复缩表。
- 跨租户、真实 scope 测试污染、RLS 失败、Action 提权或敏感数据泄漏属于立即 RED，不能事后删除掩盖。
- 图画布可回退渲染层，但 GraphSnapshot authority 和服务端预算不能回退到前端临时拼图。

## 7. 当前暂存结论

- 用户已于 2026-08-09 明确批准按本计划从 Wave 1 循环执行至 Wave 10；Wave 1～10 已依次通过，不跳波。
- O1-UX2 已在 `m1@b8a7f95` 完成 PostgreSQL 真源、Canonical API、页面保存/对象集/注释/分享与刷新恢复；真实 scope 活跃验收资产清零，审计历史可逆保留。
- O1-UX3 已在 `m1@4eb6360` 完成 Domain/Operational Lineage 分层 GraphSnapshot、1～5 跳、多种子、过滤、cursor、path、预算、真实租户写边关闭及详情/页面/Graph Health 统一对账。
- 既有未跟踪 `services/aos-api/uv.lock` 与三份 D5-E0 历史证据不在本波范围，持续保留不触碰。
- O1-UX4 已在 `m1@2ba4fa0` 完成统一知识图谱画布、Graph Health 分层检查器、真实过滤/路径/全屏/响应式与设计 QA；未新增图依赖。
- O1-UX5 已在 `m1@209f13d` 完成九菜单主任务闭环：电商 OKF 切换到真实 `Order` 并增加 CAS/影响分析，Funnel 增加 receipt 回读，Wiki 索引区分真实覆盖与知识缺口，Overlay 展示 current/history/diff/reset-to-inherit；证据 `O1-UX5_20260809T182730Z.json` 为 GREEN。
- O1-UX6 已在 `m1@41dd989` 完成累计回归、安全负向、跨租户 canary、九页面浏览器和最终 manifest；证据 `O1-UX6_20260809T183937Z.json` 为 GREEN。
- Wave 10 已完成：D4/D5 独立封板 GREEN。下一入口不再属于本计划，应单独评审“上层应用消费本体能力”的新计划，禁止继续扩写 O1 范围。
