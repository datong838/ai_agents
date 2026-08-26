# 生意探究平台观察、数据需求与语义水合 Adapter 契约

> 版本：v1.3 开工门整改稿  
> 性质：L2 AdapterPack 与 Data/Adapter 接缝目标方案；补齐 ObservationLease 严格只读边界，但不构成接入、采集或运行授权  
> 评审状态：`BI_W0_PLAN_REMEDIATED / INTERNAL_REREVIEW_GREEN / USER_IMPLEMENTATION_AUTHORIZATION_PENDING`；详见[118 号评审记录](118-经营参谋生意探究技术方案评审优化与封板结论.md)与[119 号开发总控计划](119-BI-W0经营参谋生意探究全量开发清单与波次实施计划.md)  
> 上位总方案：[经营参谋·生意探究跨四层技术总方案](115-经营参谋生意探究跨四层技术总方案.md)  
> 相邻分册：[AIP 分册](../AIP通用能力实施方案/160-AIP生意探究分析编排证据评估与方案决策实施方案.md)｜[工作台分册](116-经营参谋生意探究工作区技术方案.md)

## 1. 目标

本契约把“浏览器看遍前后台 + 数据库/API/文件全域探索”从个人摸索经验，转化为平台可治理、可复用、可审计的观察与数据履行能力。它解决两类问题：

1. **知道平台有什么、数据在哪里、怎样安全定位**；
2. **为一次具体生意探究，按最小必要原则取得、治理和水合所需事实**。

平台熟悉技能与经营探究技能都属于 AdapterPack 能力，但前者不自动推出后者成功。菜单存在不等于数据可用，数据可见不等于允许采集，采集完成不等于经营结论成立。

## 2. 四层位置

```text
L0 Data/AIP/Workshop generic contracts
         ↑ capability interface
L1 ecommerce InvestigationProfile / RequiredFactProfile
         ↑ platform contribution
L2 PlatformAdapterPack
  ├─ private-mall / Niushop
  ├─ wechat-store
  ├─ douyin-store
  └─ future taobao/pdd/amazon/...
         ↑ installation lock + config refs
L3 InstanceOverlay
  ├─ 栖月汇私域商城
  ├─ 栖月汇微信小店
  ├─ 裕威参行微信小店
  └─ 裕威参行抖店
```

L2 定义方法、能力、页面语义、数据映射和降级策略；L3 只绑定经营实体、账号引用、计划、策略、授权范围、SecretRef 和实例差异。

## 3. Adapter 能力模型

```yaml
apiVersion: aos.platform-observation/v1
kind: PlatformObservationCapability
metadata:
  platformType: wechat-store
  capabilityId: store.operation.read
spec:
  revision: 1
  modes: [browser, export, api]
  riskClass: R0_READ_ONLY
  supportedFacts: []
  supportedEntities: []
  requiredHumanAssistance: [pre_authenticated_session]
  allowedOperations: []
  forbiddenOperations: []
  outputSchemas: []
  receiptSchemaRef: "..."
  contractSuiteRef: "..."
```

能力状态必须分开：`declared / installed / configured / session_ready / contract_tested / runtime_verified / blocked`。目录可见或 skill 存在不表示 runtime verified。

## 4. DataRequirement 权威合同

### 4.1 请求者与所有者

- AIP/领域 Case 是 requester，描述经营语义和目的；
- Data/Adapter 是 canonical owner，决定安全履行路径；
- Workshop 只显示状态和结果引用；
- 平台 Adapter 只执行已接受的 fulfillment plan。

### 4.2 请求字段

| 字段 | 说明 |
|---|---|
| tenantScope | 服务端绑定 org/project |
| requestId/revision/hash | 不可变需求身份 |
| case/taskRun/checkpoint refs | 请求来源和恢复点 |
| purposeCode | 经营问题与使用目的 |
| channel/entity refs | 渠道和具体经营实体 |
| requiredFacts | 对象、关系、指标、事件 |
| timeWindow/grain/cutoff | 时间与粒度 |
| freshness/quality | 新鲜度和质量门 |
| marking/pii/minPopulation | 数据治理边界 |
| acceptableDegradation | 可接受的降级或缩小范围 |
| requestedOutputs | Dataset/DataProduct/Ontology/Evidence |
| budget/expiry | 成本和有效期 |
| idempotencyKey | 服务端防重 |

### 4.3 FulfillmentPlan

Data/Adapter 编译计划：

```text
required facts
→ inventory available governed sources
→ select least-privilege mode
→ capability/readiness/license check
→ observation/query/export steps
→ mapping/profiling/quality
→ dataset/data product
→ ontology hydration
→ evidence/receipt
```

优先级不是固定 API 优先，而是：已治理数据产品 > 已授权稳定 API > 受控导出 > 人工预登录只读浏览器观察 > 只读数据库发现。选择依据包括完整性、合法性、新鲜度、稳定性、成本和最小暴露。

## 5. 浏览器观察合同

### 5.1 SessionLease

人工可提前完成登录。AOS 只接收短期 `SessionLeaseRef`：

- tenant/entity/platform 绑定；
- browser/profile/port 只作运行引用；
- issuedAt/expiresAt；
- allowed domains/routes/read-actions；仅允许 navigate、wait、scroll、filter、open-detail、read 和经独立导出授权的只读 export；
- operator/human-assisted 标记；
- 固定 `scope: read-only-observation`；Observation SessionLease 不承载任何业务写、配置写或 Action scope；
- revocation 状态。

不得把 Cookie、密码、验证码、Token、浏览器本地存储或会话 payload 写入数据库、日志、Receipt、文档、命令行或 Memory。

### 5.2 ObservationPlanRevision

```text
Plan
├─ goal and required facts
├─ page inventory and route patterns
├─ steps: navigate / wait / scroll / filter / open-detail / read / export
├─ expected semantic fields
├─ pagination and virtual-list policy
├─ network/timeout/backoff policy
├─ screenshot/DOM/export evidence policy
├─ prohibited controls
├─ stop conditions
└─ human takeover points
```

只读计划禁止：保存、提交、删除、上下架、发布、发货、改价、触达、签约、结算、批量操作和权限配置。即使用户另行授权写操作，也必须进入 AIP `ActionProposal → Approval → ExecutionLease → Attempt → Receipt → Reconcile/Effect`；Action 使用不同的 lease type、purpose、capability、idempotency 与 expiry，绝不升级、复用或扩张 Observation SessionLease。

### 5.3 ObservationReceipt

每步回执至少包含：

- plan/step/capability/session exact refs；
- URL pattern 或 semantic route，不保存敏感 query；
- started/finished/cutoff；
- observed field set 与 row/page coverage；
- screenshot/DOM/export artifact refs + hashes；
- permission/empty/loading/partial/error 状态；
- page version/fingerprint；
- operator/human intervention；
- nonClaims 与下一步。

截图是观察证据，不是结构化业务 authority。关键数字需要来源、口径、时间窗、分页覆盖和与其他数据的对账。

## 6. 数据库/API/文件探索合同

### 6.1 数据库发现

适用于有明确授权的私域系统，例如经 SSH 隧道只读连接 MySQL。要求：

- Connector/credential 由 Data/Adapter 管理，Workshop/AIP 不取值；
- read-only 用户、allowlisted schema、query budget、statement timeout；
- 先做 schema inventory、PK/FK、row count/profile，再提出最小查询；
- 禁止源库 DDL/DML、锁表、全表无界导出；
- SQL dump 是带 cutoff 的快照，不等于当前实时库；
- 即使经营停摆使快照高度接近当前，也必须保留新鲜度声明。

### 6.2 API 与导出

- OAuth/SecretRef、scope、rate limit、license/terms、webhook signature 都由 Adapter 管理；
- API 返回与 UI 口径可能不同，必须记录 definition 和 cutoff；
- 导出文件按 checksum、schema、生成时间、过滤范围和操作者登记；
- 失败、截断、限流和分页未完不得标记完整。

## 7. Schema Reasoning 与 Adaptive Profiling

平台接入面对异构表、页面和 API，不应预先硬编码全部字段。受治理的 FDE/Adapter 工作流为：

```text
source capability discovery
→ schema/page semantic discovery
→ candidate object/field/relationship mapping
→ profile cardinality/null/duplicate/range/distribution
→ compare with ontology requirements
→ mapping proposal + confidence + conflicts
→ human review where needed
→ immutable mapping revision
→ data product + ontology hydration
```

LLM 可以提出 mapping 和 profile 建议，但不能直接发布 authority。高风险字段、身份合并、客户归属、佣金关系、医疗健康含义必须人工复核。

## 8. 语义水合合同

### 8.1 通用经营语义

首批对象/关系建议：

- `BusinessEntity / ChannelAccount / Store`
- `Product / ProductVariant / Offer / InventoryPosition`
- `Customer / Member / Promoter / Creator / Organization`
- `Order / OrderLine / Payment / Refund / Fulfillment`
- `Coupon / ExperienceCode / Campaign / ContentAsset`
- `ReferralRelation / CustomerOwnership / CommissionRule / CommissionEvent`
- `TrafficObservation / ConversionObservation / ServiceIssue`

平台字段只映射到这些稳定语义；平台独有能力以 extension/marking 保留，不污染通用对象。

### 8.2 HydrationReceipt

水合完成返回：

- source snapshot/cutoff；
- mapping revision/hash；
- object/link type refs；
- created/updated/quarantined counts；
- identity resolution method；
- quality/constraint violations；
- watermark/outbox/lineage；
- masked/PII handling；
- unmet semantic facts；
- rollback/rebuild refs。

“对象数为 0”与“未观测/未授权/查询失败”必须区分。

## 9. 首批平台方法

### 9.1 私域商城 / Niushop

可用模式：后台浏览器观察、MySQL SSH 只读发现、代码/SQL dump 辅助语义理解。  
重点事实：商品/SKU/库存、订单/支付/退款、会员/分销/客户归属、优惠券、体验码、佣金、内容/装修、后台能力。  
关键风险：源表复杂、历史/测试数据混杂、客户关系和佣金口径、SQL dump 新鲜度、线上代码与文档漂移。  
实例差异放入栖月汇 Overlay，通用方法不保存本地源码绝对路径。

### 9.2 微信小店

可用模式：人工预登录的官方后台只读观察、受控导出、未来合规 API。  
重点事实：店铺资料/诊断、商品草稿/售卖/审核、订单履约、售后、推荐运营、营销、用户运营、优选联盟、资金结算、店铺数据。  
关键风险：页面异步加载、数字脱敏、权限不足、商品列表与店铺累计口径差异、多菜单滚动/虚拟列表、平台规则变化。

### 9.3 抖店

可用模式：人工预登录的抖店后台只读观察、平台导出、未来开放平台 API。  
重点事实：商品/渠道品/库存/质量分、订单/售后、搜索/短视频/直播/图文/商城流量、营销活动、千川/联盟、达人、罗盘、服务与资金。  
关键风险：菜单和权限高度动态、内容/广告/自然流量口径、多店/多账号关系、平台算法不可观察、页面推荐不是店铺事实。

### 9.4 平台方法的共同输出

每个平台必须发布：

- capability inventory；
- page/API/schema semantic map；
- navigation locator；
- required human assistance；
- fact coverage matrix；
- data quality known issues；
- observation recipes；
- mapping revision；
- contract tests；
- runtime receipt 与 nonClaims。

## 10. InstanceOverlay

具体店铺实例只配置：

- entity/channel/account exact refs；
- platform adapter installation lock；
- SecretRef/Session policy refs；
- allowed domains/routes；
- schedule、cutoff、budget、retention；
- store-specific mapping/identity exceptions；
- approval thresholds；
- feature flags/kill switch；
- DataRequirement fulfillment policy。

不得把账号密码、Cookie、数据库明文 DSN、客户 PII、平台页面快照正文写入 Overlay。

## 11. 降级与失败语义

| 场景 | 正确状态 | 禁止 |
|---|---|---|
| 无权限 | `BLOCKED_PERMISSION` | 等待后写成空数据 |
| 页面加载慢 | `PARTIAL/LOADING_TIMEOUT` | 把首屏当全量 |
| 虚拟列表未到底 | `PARTIAL_PAGINATION` | 宣称菜单/商品全覆盖 |
| API 限流 | `BLOCKED_RATE_LIMIT` | 本地放宽/无限重试 |
| 数据快照旧 | `STALE` | 当当前实时事实 |
| 字段无法映射 | `QUARANTINED/UNKNOWN_SEMANTIC` | 模型猜字段含义 |
| 外部结果未知 | `UNKNOWN_RECONCILE` | 自动重放写操作 |
| SourceReadiness 缺项 | `WAITING_DATA/BLOCKED` | Workshop 直查源头 |

## 12. 安全军规

- 最小权限、只读优先、域名/路由 allowlist；
- SessionLease 短期、可撤销、与实体/目的绑定；
- browser/API/DB 运行与任务租户一致；
- Secret payload 永不进入文档、日志、Receipt、Memory、命令参数和截图；
- PII/健康/佣金按 marking、purpose、minimum population 和 retention 管理；
- 导出/截图可撤销、加密存储、到期清理；
- 真实平台写动作使用独立 Action Lease 和 kill switch；
- `org-org/dev-project` 正向，`dev-org/dev-project` 仅负向隔离。

## 13. Contract Suite

每个 Adapter 至少验证：

1. manifest/schema/签名/安装 lock；
2. capability 与 risk class；
3. tenant/entity/session scope；
4. allowlist 与 forbidden controls；
5. pagination/scroll/virtual list coverage；
6. permission/loading/empty/partial 区分；
7. receipt hash、cutoff、artifact refs；
8. schema/mapping/profile repeatability；
9. PII/Secret/日志扫描；
10. DataRequirement 幂等与 fulfillment 状态机；
11. Hydration identity、RLS、quarantine、lineage；
12. restart/revoke/expiry/kill；
13. `org-org` 正向与 `dev-org` 负向；
14. 外部 unknown 不自动成功或重试。

## 14. API 目标面

以下为 Data/Adapter 目标合同，实际路由和 owner 在 BI-W0 评审冻结：

```text
POST /v1/data/requirements
GET  /v1/data/requirements/{id}
POST /v1/data/requirements/{id}:accept
POST /v1/data/requirements/{id}:plan
POST /v1/data/requirements/{id}:fulfill
POST /v1/data/requirements/{id}:reconcile
GET  /v1/data/requirements/{id}/receipts

POST /v1/platform-observations
GET  /v1/platform-observations/{id}
POST /v1/platform-observations/{id}:start
POST /v1/platform-observations/{id}:pause
POST /v1/platform-observations/{id}:resume
POST /v1/platform-observations/{id}:reconcile
GET  /v1/platform-observations/{id}/receipts
```

Workshop 不调用这些底层 API；AIP/Data 服务通过受控 SDK 和 exact refs 组合。

## 15. 实施波次

| 波次 | 范围 | 退出条件 |
|---|---|---|
| AD-BI-0 | owner ADR、schema、风险矩阵、能力目录 | 无重复 authority |
| AD-BI-1 | DataRequirement/Fulfillment 合同 | 幂等/CAS/RLS/Receipt |
| AD-BI-2 | ObservationPlan/SessionLease/Receipt | 只读、Secret 扫描、故障态 |
| AD-BI-3 | Mapping/Profile/Hydration 合同 | identity/quality/lineage/quarantine |
| AD-BI-4 | Niushop AdapterPack | 浏览器+DB 方法合同验证 |
| AD-BI-5 | 微信小店 AdapterPack | 菜单/页面/导出方法合同验证 |
| AD-BI-6 | 抖店 AdapterPack | 商品/流量/达人/罗盘方法合同验证 |
| AD-BI-7 | 真实实例受限验证 | `org-org`、无写操作、current cutoff |

## 16. 非主张

- 不主张当前已存在统一 DataRequirement authority；
- 不主张平台菜单摸索等于全量数据采集；
- 不主张 SQL dump 等于当前实时数据库；
- 不主张截图、后台推荐或页面统计等于完整经营真值；
- 不主张微信小店、抖店或微商城已获得无人值守访问权；
- 不主张任一 Adapter 可执行真实发布、改价、上下架、触达或结算；
- 不主张本契约授权创建连接器、迁移或真实运行。
